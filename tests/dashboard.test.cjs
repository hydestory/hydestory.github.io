const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const vm = require('node:vm');

function integrations(fetch = async () => { throw new Error('offline'); }) {
  class FixedDate extends Date { static now() { return Date.parse('2026-09-08T02:00:00Z'); } }
  const context = vm.createContext({ document: { addEventListener() {} }, console: { error() {} }, fetch, AbortController, setTimeout, clearTimeout, Date: FixedDate });
  vm.runInContext(readFileSync('static/js/weather-integration.js', 'utf8') + '\nthis.usage = new AppUsageIntegration(); this.weather = new WeatherIntegration();', context);
  return context;
}

test('usage totals seconds and selects the most-used app, regardless of entry order', () => {
  const result = integrations().usage.parseUsageData({ Editor: 7200, Browser: 1800, Terminal: 3600 });
  assert.equal(result.totalHours, 3.5);
  assert.equal(result.topApp, 'Editor');
});

test('empty and invalid usage records are unavailable, not invented usage', () => {
  for (const data of [{}, null, [], { Editor: -2 }, { Editor: '3600' }]) {
    assert.equal(integrations().usage.parseUsageData(data), null);
  }
});

test('failed usage requests do not return simulated hours', async () => {
  assert.equal(await integrations().usage.fetchUsageData(), null);
});

test('failed weather requests do not return made-up temperatures', async () => {
  assert.equal(await integrations().weather.fetchWeatherData(), null);
});

test('incomplete or expired forecasts are unavailable', () => {
  assert.equal(integrations().weather.parseWeatherData({ records: { location: [] } }), null);
  assert.equal(integrations().weather.parseWeatherData(forecast('2026-09-07 06:00:00', '2026-09-07 18:00:00')), null);
});

function forecast(startTime, endTime) {
  return { records: { location: [{ weatherElement: Object.entries({ MinT: '0', MaxT: '12', Wx: '多雲', PoP: '0', CI: '稍有寒意' }).map(([elementName, parameterName]) => ({ elementName, time: [{ startTime, endTime, parameter: { parameterName } }] })) }] } };
}

test('current Taiwan forecast accepts zero temperature and zero precipitation', () => {
  const data = integrations().weather.parseWeatherData(forecast('2026-09-08 06:00:00', '2026-09-08 18:00:00'));
  assert.equal(data.min_temp, 0);
  assert.equal(data.rain_prob, '0');
});

test('the earliest upcoming forecast is usable when no current forecast exists', () => {
  const data = integrations().weather.parseWeatherData(forecast('2026-09-08 18:00:00', '2026-09-09 06:00:00'));
  assert.ok(data);
  assert.equal(data.period, '09-08 18:00–09-09 06:00');
});
