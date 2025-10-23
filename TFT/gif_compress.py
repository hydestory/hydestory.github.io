from PIL import Image
import imageio
import os

def compress_gif(input_path, output_path, resize_factor=0.5, colors=128, quality=85):
    # 讀取 GIF
    img = Image.open(input_path)
    frames = []
    
    # 調整 GIF 的每一幀
    for frame in range(img.n_frames):
        img.seek(frame)
        frame_img = img.convert("P", palette=Image.ADAPTIVE, colors=colors)
        frame_img = frame_img.resize((
            int(img.width * resize_factor), 
            int(img.height * resize_factor)
        ), Image.Resampling.LANCZOS)
        frames.append(frame_img)
    
    # 儲存壓縮後的 GIF
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        optimize=True,
        quality=quality,
        loop=img.info.get("loop", 0),
        duration=img.info.get("duration", 100)
    )
    
    print(f"GIF 壓縮完成: {output_path}, 原始大小: {os.path.getsize(input_path)} bytes, 壓縮後大小: {os.path.getsize(output_path)} bytes")



# 測試壓縮
compress_gif("src/mita.gif", "mita_compressed.gif", resize_factor=0.7, colors=128)