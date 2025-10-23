from PIL import Image

# 讀取圖片
img = Image.open("images.jpg")

# 調整大小
resized_img = img.resize((128, 160), Image.LANCZOS)

# 儲存新圖片
resized_img.save("mita.jpg")
