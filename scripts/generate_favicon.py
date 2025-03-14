from PIL import Image, ImageDraw

def create_favicon():
    # 32x32 boyutunda yeni bir resim oluştur
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Mavi arka plan dairesi çiz
    draw.ellipse([0, 0, 31, 31], fill='#0D6EFD')
    
    # Sol ok
    draw.polygon([
        (8, 12),   # Sol üst
        (12, 8),   # Üst orta
        (12, 11),  # Üst sağ
        (16, 11),  # Sağ üst
        (16, 13),  # Sağ alt
        (12, 13),  # Alt sağ
        (12, 16),  # Alt orta
        (8, 12)    # Sol alt
    ], fill='white')
    
    # Sağ ok
    draw.polygon([
        (16, 16),  # Sağ alt
        (20, 12),  # Alt orta
        (20, 15),  # Alt sol
        (24, 15),  # Sol alt
        (24, 17),  # Sol üst
        (20, 17),  # Üst sol
        (20, 20),  # Üst orta
        (16, 16)   # Sağ üst
    ], fill='white')
    
    # PNG olarak kaydet
    png_path = 'app/static/img/favicon.png'
    img.save(png_path, 'PNG')
    
    # ICO olarak dönüştür
    ico_path = 'app/static/img/favicon.ico'
    img.save(ico_path, 'ICO', sizes=[(16, 16), (32, 32)])
    
    print(f'Favicon oluşturuldu: {ico_path}')

if __name__ == '__main__':
    create_favicon() 