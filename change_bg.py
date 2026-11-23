"""
Gegeen Terelj menu — дэвсгэр зураг солих скрипт.

Ашиглах:
  python change_bg.py index.html shine_zurag.jpg screen   # номын ард байгаа дэлгэцийн дэвсгэр
  python change_bg.py index.html shine_zurag.jpg page     # цэсний хуудасны (цаасны) дэвсгэр

Шаардлага:  pip install pillow
"""
import base64
import io
import re
import sys

from PIL import Image, ImageOps


def to_data_uri(path, target):
    img = Image.open(path).convert("RGB")
    if target == "page":
        # A4 харьцаа (1:1.414) руу голоос нь тайрч тааруулна
        img = ImageOps.fit(img, (1060, 1499), Image.LANCZOS)
    else:
        # дэлгэцийн дэвсгэр — хэт том бол багасгана
        img.thumbnail((1920, 1920), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def main():
    if len(sys.argv) != 4 or sys.argv[3] not in ("screen", "page"):
        print(__doc__)
        sys.exit(1)
    html_path, img_path, target = sys.argv[1:]
    html = open(html_path, encoding="utf-8").read()

    # screen = body{...} доторх зураг, page = .pg{...} доторх зураг
    selector = r"body\{" if target == "screen" else r"\.pg\{"
    pattern = re.compile(r"(" + selector + r"[^}]*?url\()data:image/[a-z]+;base64,[A-Za-z0-9+/=]+(\))")
    new_html, n = pattern.subn(lambda m: m.group(1) + to_data_uri(img_path, target) + m.group(2), html, count=1)
    if n == 0:
        print("Дэвсгэр зураг олдсонгүй — файл өөр бүтэцтэй байж магадгүй.")
        sys.exit(1)

    open(html_path, "w", encoding="utf-8").write(new_html)
    print(f"Бэлэн: {target} дэвсгэрийг {img_path} зургаар солилоо → {html_path}")


if __name__ == "__main__":
    main()
