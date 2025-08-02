from PIL import Image

def convert_to_rgb565(image_path, output_path):
    image = Image.open(image_path)
    image = image.convert('RGB')
    pixels = image.load()
    width, height = image.size

    with open(output_path, 'wb') as f:
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                f.write(rgb565.to_bytes(2, byteorder='big'))

convert_to_rgb565('mita.jpg', 'mita.bin')