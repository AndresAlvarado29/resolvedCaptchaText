# Captura y Resolución de Captchas con Selenium, OpenCV y OCR

Este proyecto automatiza la interacción con un sitio web utilizando Selenium para resolver captchas y extraer información relevante. La solución implementa técnicas de procesamiento de imágenes y OCR (Reconocimiento Óptico de Caracteres) para resolver captchas y realizar búsquedas automatizadas.

## Funcionalidades Principales

- **Automatización con Selenium**: Simula interacciones con el navegador para ingresar datos, capturar captchas, y realizar búsquedas en un sitio web.
- **Procesamiento de imágenes con OpenCV**: Mejora la calidad de las imágenes de captcha para facilitar su lectura.
- **Reconocimiento de texto con EasyOCR**: Convierte las imágenes procesadas en texto para resolver captchas automáticamente.
- **Tolerancia a errores**: Implementa intentos múltiples para resolver el captcha en caso de fallas.

---

## Requisitos

### Librerías Usadas

1. **Selenium**: Permite automatizar interacciones con el navegador.
   ```bash
   pip install selenium
   ```

2. **OpenCV**: Utilizada para el procesamiento de imágenes (ajustes de color, binarización, etc.).
   ```bash
   pip install opencv-python
   ```

3. **EasyOCR**: Proporciona un OCR sencillo y eficaz para leer captchas.
   ```bash
   pip install easyocr
   ```

4. **PyTesseract**: Alternativa a EasyOCR para convertir imágenes a texto.
   ```bash
   pip install pytesseract
   ```

---

## Estructura del Código

### Funciones Principales

1. **`guardarTexto`**:
   Guarda el texto extraído en un archivo de texto.
   ```python
   def guardarTexto(texto, rutaTexto="informacion.txt"):
       with open(rutaTexto, 'w', encoding="utf-8") as archivo:
           archivo.write(texto)
   ```

2. **`capturarPantalla`**:
   Captura la imagen del captcha en el sitio web.
   ```python
   def capturarPantalla(rutaImagen):
       captcha = browser.find_element(By.ID, 'formPrincipal:capimg')
       captcha.screenshot(rutaImagen)
       return rutaImagen
   ```

3. **`resolverCaptcha`**:
   Procesa la imagen del captcha y utiliza EasyOCR para extraer el texto.
   ```python
   def resolverCaptcha(rutaImagen):
       captchaImage = cv2.imread(rutaImagen)
       gray = cv2.cvtColor(captchaImage, cv2.COLOR_BGR2GRAY)
       invert = cv2.bitwise_not(gray)
       _, thresh = cv2.threshold(invert, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
       kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
       processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
       cv2.imwrite('captcha_easyOCR.png', processed)
       reader = easyocr.Reader(['en'])
       result = reader.readtext('captcha_easyOCR.png')
       return "".join([res[1] for res in result]).strip()
   ```

4. **Alternativa con PyTesseract**:
   PyTesseract fue probado para la resolución de captchas, pero los resultados fueron inferiores en comparación con EasyOCR.
   ```python
   captchaToText = pytesseract.image_to_string(dilate)
   ```

---

## Comparativa entre EasyOCR y PyTesseract

### EasyOCR:
- **Ventajas**:
  - Mayor precisión al leer caracteres distorsionados.
  - Mejor rendimiento con captchas de tipografías variadas.
- **Inconvenientes**:
  - Requiere más recursos en comparación con PyTesseract.

### PyTesseract:
- **Ventajas**:
  - Más rápido para imágenes simples y bien definidas.
  - Compatible con una amplia gama de idiomas.
- **Inconvenientes**:
  - Menor precisión con imágenes ruidosas o distorsionadas.

---
## Guía de Uso

### Paso 1: Descargar el Proyecto

1. Descarga el archivo `.zip` que se encuentra en el repositorio o puedes clonarlo

2. Extrae el contenido del archivo `.zip` en una carpeta local.

### Paso 1: Configurar el Entorno

1. Instala todas las dependencias necesarias usando `pip`:
   ```bash
   pip install selenium opencv-python easyocr pytesseract
   ```
   o

   ```bash
   pip install -r requirements.txt
   ```

2. Descarga el controlador de ChromeDriver correspondiente a la versión de tu navegador Chrome desde [ChromeDriver](https://chromedriver.chromium.org/).

3. Asegúrate de tener un archivo `cedula.txt` en el directorio raíz del proyecto que contenga la cédula de identidad a consultar.

### Paso 2: Configurar y Ejecutar el Código

1. Edita el archivo principal del código si es necesario para ajustar la ruta del archivo de entrada o salida.

2. Ejecuta el script principal:
   ```bash
   python scrapingEasyOCR.py
   ```

### Paso 3: Resultados

- El texto extraído del sitio web se guarda en el archivo `informacion.txt`.
- Los intentos de resolución del captcha se imprimen en la consola para verificar el progreso.

### Notas Importantes

- Si el captcha no se resuelve después de varios intentos, verifica que las librerías están instaladas correctamente y que el procesamiento de imágenes no tiene errores.
- Puedes ajustar los parámetros de preprocesamiento en las funciones de OpenCV para mejorar la precisión en captchas más complejos.

---

## Ejecución del Proyecto

1. **Configurar Selenium**:
   Asegúrate de tener el navegador Chrome y el driver correspondiente configurados.
   ```python
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   browser = webdriver.Chrome(options=chrome_options)
   browser.get('https://www.senescyt.gob.ec/consulta-titulos-web/faces/vista/consulta/consulta.xhtml')
   ```

2. **Procesamiento de Captchas**:
   Captura y procesa el captcha usando las funciones descritas anteriormente.

3. **Búsqueda Automatizada**:
   El código utiliza intentos múltiples para resolver captchas y extraer información de forma confiable.

---

## Conclusiones

- **EasyOCR supera a PyTesseract** para resolver captchas con distorsiones o ruido.
- La combinación de Selenium, OpenCV y EasyOCR permite una solución robusta para tareas automatizadas de extracción de información.

---

## Autor
Creado por Andres Alvarado.

