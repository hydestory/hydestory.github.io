from PIL import Image
import os

# 讀取 GIF
gif_path = "src/mita2_resized.gif"
output_dir = "src/gif_frame/mita2_compressed"
os.makedirs(output_dir, exist_ok=True)
gif = Image.open(gif_path)

# 設定 TFT 螢幕的尺寸
tft_width = 128
tft_height = 160


# 將每一幀轉換為 RGB565 格式並儲存為 bin 檔案
def convert_to_rgb565(image):
    rgb565_data = bytearray()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b = image.getpixel((x, y))
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            rgb565_data.append((rgb565 >> 8) & 0xFF)
            rgb565_data.append(rgb565 & 0xFF)
    return rgb565_data

# 逐幀處理，這裡每隔1幀取一幀
frame_interval = 2

for frame in range(0, gif.n_frames, frame_interval):
    gif.seek(frame)
    frame_image = gif.copy().convert("RGB").resize((tft_width, tft_height), Image.LANCZOS)
    frame_image = frame_image.quantize(colors=256).convert("RGB")

    # 轉換為 RGB565
    rgb565_data = convert_to_rgb565(frame_image)
    
    # 儲存為 bin 檔案
    frame_filename = os.path.join(output_dir, f"frame_{frame//frame_interval:03d}.bin")
    with open(frame_filename, "wb") as f:
        f.write(rgb565_data)

print("GIF 已轉換並儲存為多個逐幀 bin 檔案")