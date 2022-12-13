import cv2
img = cv2.imread("machines_qr_code/392468.jpg")
detect = cv2.QRCodeDetector()
data, _, _ = detect.detectAndDecode(img)
print(data)