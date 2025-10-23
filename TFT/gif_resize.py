from PIL import Image
import imageio

# 讀取 GIF
gif_path = "src/mita2.gif"
output_path = "output.gif"
gif = Image.open(gif_path)

# 調整大小，保持原始長寬比
new_width = 128
new_height = 160

frames = []
for frame in range(gif.n_frames):
    gif.seek(frame)
    frame_image = gif.copy()
    
    # 計算新的尺寸，保持長寬比
    width, height = frame_image.size
    aspect_ratio = width / height
    
    if width > height:
        new_height = int(new_width / aspect_ratio)
    else:
        new_width = int(new_height * aspect_ratio)
    
    resized_frame = frame_image.resize((new_width, new_height), Image.LANCZOS)
    frames.append(resized_frame)

# 儲存為 GIF
frames[0].save(output_path, save_all=True, append_images=frames[1:], loop=0)
print("GIF 已縮小並儲存至", output_path)