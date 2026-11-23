import qrcode
import qrcode.image.svg

URL = "https://menu.gegeen-terelj.workers.dev/"

# PNG — хэвлэхэд
qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% гэмтсэн ч уншигдана
    box_size=30,   # нэг дөрвөлжингийн хэмжээ (px) — том байх тусам зураг томорно
    border=4,      # эргэн тойрны цагаан зай (заавал 4 байх нь зөв)
)
qr.add_data(URL)
qr.make(fit=True)
qr.make_image(fill_color="#2e2014", back_color="white").save("menu-qr.png")

# SVG — ямар ч хэмжээгээр томруулахад
qrcode.make(
    URL,
    image_factory=qrcode.image.svg.SvgPathImage,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    border=4,
).save("menu-qr.svg")

print("Бэлэн: menu-qr.png, menu-qr.svg")