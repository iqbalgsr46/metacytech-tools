import sys
from PIL import Image

def process():
    img_path = r"C:/Users/tbiqb/.gemini/antigravity/brain/d2e14882-e0ce-4c79-b5ac-87228d558c81/.user_uploaded/media_1787799645426.png"
    img = Image.open(img_path)
    img = img.convert("RGBA")
    
    # We look for pixels that are not the dark gray background color.
    # The background in the image is probably around (40, 40, 40) or (50, 50, 50).
    # Let's get the color of a pixel on the right side to determine the background color.
    bg_color = img.getpixel((img.width - 5, img.height // 2))
    print(f"Detected background color: {bg_color}")
    
    # Find bounding box of anything that differs significantly from bg_color
    min_x, min_y = img.width, img.height
    max_x, max_y = 0, 0
    
    for x in range(img.width):
        for y in range(img.height):
            p = img.getpixel((x, y))
            # Check color distance
            dist = sum((p[i] - bg_color[i]) ** 2 for i in range(3))
            if dist > 500: # Threshold
                # Also ignore the black edges on the far left
                if x > 10 and x < 50:
                    if x < min_x: min_x = x
                    if x > max_x: max_x = x
                    if y < min_y: min_y = y
                    if y > max_y: max_y = y

    print(f"Icon bounding box: ({min_x}, {min_y}, {max_x}, {max_y})")
    
    if min_x <= max_x and min_y <= max_y:
        icon = img.crop((min_x, min_y, max_x+1, max_y+1))
        icon = icon.resize((32, 32), Image.Resampling.LANCZOS)
        # Save as favicon.ico inside the bibd template
        dest_path = r"d:/HACKING/transaksi-transfer-bank/templates/bibd/public/favicon.ico"
        icon.save(dest_path, format="ICO")
        print(f"Saved to {dest_path}")
    else:
        print("Could not find icon")

if __name__ == "__main__":
    process()
