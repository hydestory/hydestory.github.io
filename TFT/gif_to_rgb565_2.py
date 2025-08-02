import os
from PIL import Image
import struct

def rgb_to_rgb565(r, g, b):
    """將 RGB 顏色轉換為 RGB565 格式"""
    return (r >> 3) << 11 | (g >> 2) << 5 | (b >> 3)

def gif_to_rgb565_frames(gif_file, output_folder):
    """將 GIF 檔案的每一幀轉換為 RGB565 並儲存為 bin 檔案"""
    # 開啟 GIF 檔案
    img = Image.open(gif_file)

    # 確保圖片是 RGBA 格式（有透明度的圖片）
    img = img.convert('RGBA')

    # 檢查並創建輸出資料夾
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍歷每一幀
    frame_number = 0
    while True:
        # 取得當前幀
        frame = img.copy()

        # 取得圖片的寬高
        width, height = frame.size

        # 輸出檔案名稱
        output_file = os.path.join(output_folder, f"frame_{frame_number}.bin")

        # 開啟 bin 檔案來寫入 RGB565 數據
        with open(output_file, 'wb') as f:
            for y in range(height):
                for x in range(width):
                    # 取得當前像素的 RGBA 顏色
                    r, g, b, a = frame.getpixel((x, y))
                    
                    # 若透明度為 0，則設為背景色（這裡設為黑色）
                    if a == 0:
                        r, g, b = 0, 0, 0
                    
                    # 轉換為 RGB565
                    rgb565 = rgb_to_rgb565(r, g, b)
                    
                    # 寫入 bin 檔案
                    f.write(struct.pack('<H', rgb565))

        print(f"第 {frame_number} 幀已儲存為 {output_file}")
        
        # 移動到下一幀
        frame_number += 1
        
        # 嘗試加載下一幀，若無更多幀則退出
        try:
            img.seek(frame_number)
        except EOFError:
            break

# 執行轉換
gif_to_rgb565_frames("src/ame.gif", "src/gif_frame/ame")
