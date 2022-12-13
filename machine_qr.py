import qrcode
import numpy as np
data = "392468"
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data(data)
qr.make()
img = qr.make_image(fill_color="black", back_color="white")
img.save("machines_qr_code/" + data + ".jpg")
