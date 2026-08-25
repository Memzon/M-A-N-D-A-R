import io
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def _load_font(size: int, bold: bool = False):
    """Sistemde bulunan bir TrueType fontu yüklemeyi dener, yoksa varsayılana düşer."""
    candidates = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "Arial Bold.ttf" if bold else "Arial.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _vip_gradient(width, height, top_color, bottom_color):
    base = Image.new("RGB", (width, height), top_color)
    draw = ImageDraw.Draw(base)
    for y in range(height):
        ratio = y / height
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    return base


def _centered_text(draw, cx, y, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, y), text, font=font, fill=fill)


def _draw_chest(draw: ImageDraw.ImageDraw, x, y, w, h, number, glow_color):
    body_color = (120, 78, 30)
    lid_color = (150, 100, 40)
    metal = (230, 190, 90)

    # Glow / çerçeve efekti
    draw.rounded_rectangle(
        [x - 6, y - 6, x + w + 6, y + h + 6], radius=18, outline=glow_color, width=4
    )

    # Sandık gövdesi
    draw.rounded_rectangle([x, y + h * 0.42, x + w, y + h], radius=10, fill=body_color)
    # Sandık kapağı
    draw.rounded_rectangle([x, y, x + w, y + h * 0.5], radius=14, fill=lid_color)
    # Orta metal bant
    draw.rectangle([x + w / 2 - 6, y, x + w / 2 + 6, y + h], fill=metal)
    # Kilit
    lock_r = w * 0.14
    cx, cy = x + w / 2, y + h * 0.5
    draw.ellipse(
        [cx - lock_r, cy - lock_r, cx + lock_r, cy + lock_r],
        fill=metal,
        outline=(90, 60, 15),
        width=2,
    )

    # Numara etiketi
    font = _load_font(int(h * 0.22), bold=True)
    _centered_text(draw, x + w / 2, y + h + 10, str(number), font, (255, 255, 255))


def generate_chest_image(count: int = 5) -> io.BytesIO:
    width, height = 900, 420
    img = _vip_gradient(width, height, (25, 10, 45), (55, 15, 80))
    draw = ImageDraw.Draw(img)

    title_font = _load_font(46, bold=True)
    _centered_text(draw, width / 2, 24, "VIP SANDIK ETKİNLİĞİ", title_font, (255, 215, 90))

    sub_font = _load_font(22)
    _centered_text(draw, width / 2, 82, "Bir sandık seç, ödülünü kap!", sub_font, (230, 230, 230))

    chest_w, chest_h = 120, 130
    gap = 30
    total_w = count * chest_w + (count - 1) * gap
    start_x = (width - total_w) / 2
    y = 180

    glow_colors = [
        (255, 215, 0),
        (255, 120, 200),
        (120, 200, 255),
        (150, 255, 150),
        (255, 150, 100),
    ]
    for i in range(count):
        x = start_x + i * (chest_w + gap)
        _draw_chest(draw, x, y, chest_w, chest_h, i + 1, glow_colors[i % len(glow_colors)])

    img = img.filter(ImageFilter.SMOOTH_MORE)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


def generate_speed_image(code: str) -> io.BytesIO:
    width, height = 900, 320
    img = _vip_gradient(width, height, (10, 30, 45), (10, 60, 70))
    draw = ImageDraw.Draw(img)

    title_font = _load_font(40, bold=True)
    _centered_text(draw, width / 2, 26, "EL ALIŞTIRMASI", title_font, (120, 230, 255))

    sub_font = _load_font(20)
    _centered_text(
        draw, width / 2, 80, "Aşağıdaki kodu ilk yazan ödülü kapar!", sub_font, (220, 220, 220)
    )

    code_font = _load_font(70, bold=True)
    char_colors = [
        (255, 215, 90),
        (255, 120, 200),
        (120, 255, 200),
        (255, 150, 100),
        (150, 200, 255),
    ]

    widths = []
    for ch in code:
        bbox = draw.textbbox((0, 0), ch, font=code_font)
        widths.append(bbox[2] - bbox[0] + 14)
    total_w = sum(widths)
    x = width / 2 - total_w / 2
    y_base = 170

    for i, ch in enumerate(code):
        char_img = Image.new("RGBA", (100, 110), (0, 0, 0, 0))
        cd = ImageDraw.Draw(char_img)
        cd.text((10, 10), ch, font=code_font, fill=random.choice(char_colors))
        angle = random.randint(-12, 12)
        char_img = char_img.rotate(angle, expand=True)
        img.paste(char_img, (int(x), int(y_base - 20)), char_img)
        x += widths[i]

    # Hafif dekoratif gürültü (VIP/şık görünüm için)
    for _ in range(60):
        px = random.randint(0, width - 1)
        py = random.randint(0, height - 1)
        r = random.randint(0, 1)
        draw.ellipse([px, py, px + r, py + r], fill=(255, 255, 255))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf
