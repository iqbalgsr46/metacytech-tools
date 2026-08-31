import sys
import qrcode
from PIL import Image

def generate_poster(url, output_path="dana_kaget_ready.jpg"):
    base = Image.open('templates/danakaget/poster_base.jpg').convert('RGB')
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    qr_img = qr_img.resize((452, 452), Image.Resampling.NEAREST)
    
    logo = Image.open('templates/danakaget/center_logo.png')
    qr_w, qr_h = qr_img.size
    logo_w, logo_h = logo.size
    logo_pos = ((qr_w - logo_w) // 2, (qr_h - logo_h) // 2)
    
    qr_img.paste(logo, logo_pos, logo)
    base.paste(qr_img, (153, 310))
    base.save(output_path, quality=95)
    print(f"Poster generated: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_poster(sys.argv[1])
    else:
        print("Please provide a URL")
