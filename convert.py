import sys
from PIL import Image

def process():
    img_path = r"d:/HACKING/transaksi-transfer-bank/LOGO-TAB-BROWSER-BIBD-TERBARU.png"
    img = Image.open(img_path)
    img = img.convert("RGBA")
    
    # We just resize and convert to ICO
    icon = img.resize((32, 32), Image.Resampling.LANCZOS)
    
    # Save as favicon.ico inside the bibd template
    dest_path1 = r"d:/HACKING/transaksi-transfer-bank/templates/bibd/public/favicon.ico"
    dest_path2 = r"d:/HACKING/transaksi-transfer-bank/templates/bibd/favicon.ico"
    
    icon.save(dest_path1, format="ICO")
    icon.save(dest_path2, format="ICO")
    
    print(f"Saved to {dest_path1} and {dest_path2}")

if __name__ == "__main__":
    process()
