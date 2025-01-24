from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
import pytesseract
import numpy as np

browser = webdriver.Chrome()
browser.get('https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml')
#toma toda la pantalla
#browser.save_screenshot('captcha.png')
#toma un elemento en especifico
captcha = browser.find_element(By.ID, 'formPrincipal:capimg')
captcha.screenshot('captcha.png')

captchaImage = cv2.imread('captcha.png')
gray = cv2.cvtColor(captchaImage, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3, 3), 0)
invert = cv2.bitwise_not(blur)
_, thresh = cv2.threshold(invert, 150, 200, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
kernel = np.ones((1, 1), np.uint8) 
dilate = cv2.dilate(thresh, kernel, iterations=1)
cv2.imwrite('captcha_pytesseract.png', dilate)
# Convertir imagen a texto
captchaToText = pytesseract.image_to_string(dilate)
print("Texto extraído:", captchaToText)

