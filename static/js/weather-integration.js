// Fetch failures remain unavailable; never substitute demonstration data.
async function fetchJSON(url) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 8000);
  try {
    const response = await fetch(url, { signal: controller.signal });
    if (!response.ok) throw new Error('Data request failed');
    return await response.json();
  } finally { clearTimeout(timer); }
}
function setText(id, text) {
  const element = document.getElementById(id);
  if (element) element.textContent = text;
}
class WeatherIntegration {
    constructor() {
        this.apiKey = "CWA-EB0C41B6-0482-40E4-8153-4330E46FECA9";
        this.cityName = "臺北市";
        this.baseUrl = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001";
    }
  async fetchWeatherData() {
    try {
      const url = this.baseUrl + '?Authorization=' + this.apiKey + '&format=JSON&locationName=' + encodeURIComponent(this.cityName);
      return this.parseWeatherData(await fetchJSON(url));
    } catch { return null; }
  }
  parseWeatherData(data) {
    const elements = data?.records?.location?.[0]?.weatherElement;
    if (!Array.isArray(elements)) return null;
    const now = Date.now();
    const values = {};
    // CWA timestamps are in Taiwan time, independent of the visitor's timezone.
    const timestamp = value => Date.parse(value?.replace(' ', 'T') + '+08:00');
    const periods = elements.find(element => element.elementName === 'Wx')?.time;
    if (!Array.isArray(periods)) return null;
    const period = periods.filter(slot => timestamp(slot.endTime) > now && timestamp(slot.startTime) < timestamp(slot.endTime))
      .sort((a, b) => timestamp(a.startTime) - timestamp(b.startTime))[0];
    if (!period) return null;
    for (const element of elements) {
      const slot = element.time?.find(time => time.startTime === period.startTime && time.endTime === period.endTime);
      if (slot) values[element.elementName] = slot.parameter?.parameterName;
    }
    if (!values.Wx || !period || values.MinT == null || values.MaxT == null) return null;
    const min = Number(values.MinT), max = Number(values.MaxT);
    if (!Number.isFinite(min) || !Number.isFinite(max)) return null;
    return { min_temp: min, max_temp: max, weather: values.Wx,
      rain_prob: values.PoP, comfort_index: values.CI,
      period: period.startTime.slice(5, 16) + '–' + period.endTime.slice(5, 16) };
  }
  async updateWeatherDisplay() {
    const data = await this.fetchWeatherData();
    setText('weather-temp', data ? data.min_temp + '–' + data.max_temp + '°C' : '—');
    setText('weather-condition', data ? data.weather : '暫時無法取得預報');
    setText('weather-details', data
      ? (data.rain_prob != null ? '降雨機率 ' + data.rain_prob + '% · ' : '') + data.period + '（臺灣時間）'
      : '可前往中央氣象署查看最新天氣。');
  }
}
class AppUsageIntegration {
  constructor() { this.usageDataUrl = 'src/text/usage_log.json'; }
  async fetchUsageData() {
    try { return this.parseUsageData(await fetchJSON(this.usageDataUrl)); }
    catch { return null; }
  }
  parseUsageData(data) {
    if (!data || typeof data !== 'object' || Array.isArray(data)) return null;
    const entries = Object.entries(data);
    if (!entries.length || entries.some(([name, seconds]) =>
      !name.trim() || typeof seconds !== 'number' || !Number.isFinite(seconds) || seconds < 0)) return null;
    const totalSeconds = entries.reduce((sum, [, seconds]) => sum + seconds, 0);
    if (!Number.isFinite(totalSeconds)) return null;
    const top = entries.reduce((largest, entry) => entry[1] > largest[1] ? entry : largest);
    return { totalHours: Math.round(totalSeconds / 360) / 10,
      topApp: totalSeconds === 0 ? '尚無使用時間' : top[0], appCount: entries.length };
  }
  async updateUsageDisplay() {
    const data = await this.fetchUsageData();
    setText('app-usage', data ? data.totalHours + ' 小時' : '—');
    setText('top-app', data ? data.topApp : '暫時無法讀取紀錄');
  }
}
document.addEventListener('DOMContentLoaded', () => {
  new WeatherIntegration().updateWeatherDisplay();
  new AppUsageIntegration().updateUsageDisplay();
});
