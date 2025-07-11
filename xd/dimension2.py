import os
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def insertar_dos_imagenes_en_pdf(pdf_path, imagen1_path, imagen2_path, output_path, coords1, escala1, coords2, escala2):
    # Abrir el PDF original
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Dimensiones de la primera página
    page = reader.pages[0]
    width = float(page.mediabox.upper_right[0])
    height = float(page.mediabox.upper_right[1])

    # Crear un PDF temporal con ambas imágenes
    temp_pdf_path = "temp.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=(width, height))

    imagen1 = ImageReader(imagen1_path)
    img1 = Image.open(imagen1_path)
    ancho1, alto1 = img1.size
    x1, y1 = coords1
    nuevo_ancho1 = ancho1 * escala1
    nuevo_alto1 = alto1 * escala1

    # Rotar la imagen 1
    c.saveState()
    c.translate(x1, y1)
    c.rotate(90)
    c.drawImage(imagen1, 0, 0, width=nuevo_ancho1, height=nuevo_alto1, mask='auto')
    c.restoreState()

    # === Imagen 2 ===
    img2 = Image.open(imagen2_path)
    img2_width, img2_height = img2.size
    x2, y2 = coords2
    new_w2 = img2_width * escala2
    new_h2 = img2_height * escala2
    c.drawImage(ImageReader(imagen2_path), x2, y2, width=new_w2, height=new_h2, mask='auto')

    # Guardar
    c.showPage()
    c.save()

    # Fusionar con PDF original
    with open(temp_pdf_path, "rb") as temp_pdf:
        temp_reader = PdfReader(temp_pdf)
        first_page = reader.pages[0]
        first_page.merge_page(temp_reader.pages[0])
        writer.add_page(first_page)

        # Añadir el resto de páginas
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])

    # Guardar PDF final
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)

    # Borrar temporal
    os.remove(temp_pdf_path)

    print(f"Imágenes insertadas en {output_path}")

# === Ejemplo de uso ===
ruta_pdf = "ID-CJV-T1M-P-2-CRE-PD-1001_06_REV_0.pdf"
imagen1 = "vinci.jpg"         # Primera imagen PNG
imagen2 = "sello_ajuste.png"   # Segunda imagen PNG

output_path = "nuevo_documento_con_dos_imagenes.pdf"

# Configura coordenadas y escalas de cada imagen
coords1 = (2065, 3035)
escala1 = 0.11

coords2 = (1637, 2859)
escala2 = 0.45

# Ejecutar
insertar_dos_imagenes_en_pdf(
    ruta_pdf,
    imagen1,
    imagen2,
    output_path,
    coords1,
    escala1,
    coords2,
    escala2
)
