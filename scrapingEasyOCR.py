from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import cv2
import easyocr
import time

#funciones
def guardarTexto(texto, rutaTexto="informacion.txt"):
    with open(rutaTexto, 'w',encoding="utf-8") as archivo:
        archivo.write(texto)

def capturarPantalla(rutaImagen):
   captcha = browser.find_element(By.ID, 'formPrincipal:capimg')
   captcha.screenshot('captcha.png')
   rutaCaptcha = 'captcha.png'
   return rutaCaptcha

def extraerTexto(rutaTexto):
    with open(rutaTexto, 'r',encoding="utf-8") as archivo:
        for linea in archivo:
            texto=linea.strip();
    return texto

def resolverCaptcha(rutaImagen):
    captchaImage = cv2.imread(rutaImagen)
    gray = cv2.cvtColor(captchaImage, cv2.COLOR_BGR2GRAY)
    invert = cv2.bitwise_not(gray)
    _, thresh = cv2.threshold(invert, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite('captcha_easyOCR.png', processed)
    reader = easyocr.Reader(['en'])  # Usamos el idioma inglés para detectar letras y números
    result = reader.readtext('captcha_easyOCR.png')
    captchaToText = "".join([res[1] for res in result]).strip()
    print("Texto extraído con EasyOCR:", captchaToText)
    return captchaToText

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options)
browser.get('https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml')
#ingresar texto
text_id = browser.find_element(By.ID, 'formPrincipal:identificacion')
text_id.clear()
text_id.send_keys(extraerTexto('cedula.txt'))

#captura pantalla
rutaCaptcha = capturarPantalla('captcha.png')
captcha_input =browser.find_element(By.ID, 'formPrincipal:captchaSellerInput')
captcha_input.clear()
captcha_input.send_keys(resolverCaptcha(rutaCaptcha))

#click en boton
button = browser.find_element(By.ID, 'formPrincipal:boton-buscar')
button.click()
time.sleep(7)
try:
    error = browser.find_element(By.CLASS_NAME, 'msg-rojo').text
    if error:
        print("Error:", error)
        print("ingrese con otra cedula")
        browser.quit()
except:
    pass
try:
    info = browser.find_element(By.CLASS_NAME, 'ui-datatable-even').text
except NoSuchElementException:
    info = ""

if info.strip() != "":
    print("Información extraída:")
    print(info)
    guardarTexto(info)
    browser.quit()

MAX_REINTENTOS = 5
intento = 0
captcha_resuelto = False


while intento < MAX_REINTENTOS and not captcha_resuelto:
    print(f"Intento {intento + 1} de {MAX_REINTENTOS}")
    text_id = browser.find_element(By.ID, 'formPrincipal:identificacion')
    text_id.clear()
    text_id.send_keys(extraerTexto('cedula.txt'))
    rutaCaptcha = capturarPantalla('captcha.png')
    captcha_input = browser.find_element(By.ID, 'formPrincipal:captchaSellerInput')
    captcha_input.clear()
    captcha_input.send_keys(resolverCaptcha(rutaCaptcha))
    
    # Hacer clic en el botón
    button = browser.find_element(By.ID, 'formPrincipal:boton-buscar')
    button.click()
    time.sleep(7)
    
    # Verificar si hay un mensaje de error
    # Verificar si se obtuvo información
    try:
        info = browser.find_element(By.CLASS_NAME, 'ui-datatable-even').text
        if info.strip() != "":
            captcha_resuelto = True
            print("Información extraída:")
            print(info)
            guardarTexto(info)
            break
    except NoSuchElementException:
        pass

    intento += 1

if not captcha_resuelto:
    print("No se pudo resolver el captcha después de varios intentos.")
    browser.quit()


#esperar 5 segundos
time.sleep(5)
#toma toda la pantalla
#browser.save_screenshot('captcha.png')
#toma un elemento en especifico
    
#identificacion = browser.find_element(By.ID, 'formPrincipal:j_idt42').text
#nombres = browser.find_element(By.ID, 'formPrincipal:j_idt44').text
#genero = browser.find_element(By.ID, 'formPrincipal:j_idt46').text
#nacionalidad = browser.find_element(By.ID, 'formPrincipal:j_idt48').text
#print(identificacion)
#print("Nombres:", nombres)
#print("Género:", genero)
#print("Nacionalidad:", nacionalidad)



