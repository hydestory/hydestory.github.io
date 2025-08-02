from PIL import Image
import numpy as np

def load_rgb565_image(file_path, width, height):
    with open(file_path, 'rb') as f:
        img_data = f.read()
    
    # 每個像素佔用2個字節
    img_array = np.frombuffer(img_data, dtype=np.uint16).reshape((height, width))
    
    # 分解RGB565格式
    r = (img_array >> 8) & 0xF8
    g = (img_array >> 3) & 0xFC
    b = (img_array << 3) & 0xF8
    
    # 合併成RGB格式
    rgb_array = np.zeros((height, width, 3), dtype=np.uint8)
    rgb_array[..., 0] = r
    rgb_array[..., 1] = g
    rgb_array[..., 2] = b
    
    return rgb_array

def show_image(image_data):
    img = Image.fromarray(image_data)
    img.show()

# 設定圖片大小
width, height = 58, 56

# 讀取並顯示圖片
image_data = load_rgb565_image('output_frames/ame/frame_010.bin', width, height)
show_image(image_data)