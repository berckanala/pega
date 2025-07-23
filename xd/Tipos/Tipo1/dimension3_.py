import os
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def insertar_tres_imagenes_en_pdf(pdf_path, parche_path, imagen1_path, imagen2_path,
                                  output_path, coords_parche, escala_parche,
                                  coords1, escala1, coords2, escala2):
    # Abrir PDF original
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Obtener dimensiones de la primera página
    page = reader.pages[0]
    width = float(page.mediabox.upper_right[0])
    height = float(page.mediabox.upper_right[1])

    # Crear PDF temporal con las imágenes
    temp_pdf_path = "temp_overlay.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=(width, height))

    # === Imagen 1: PARCHE ===
    img_p = Image.open(parche_path)
    parche = ImageReader(parche_path)
    ancho_p, alto_p = img_p.size
    x_p, y_p = coords_parche
    nuevo_ancho_p = ancho_p * escala_parche
    nuevo_alto_p = alto_p * escala_parche
    c.drawImage(parche, x_p, y_p, width=nuevo_ancho_p, height=nuevo_alto_p, mask='auto')

    # === Imagen 2: VINCI (ROTADA 90°) ===
    img1 = Image.open(imagen1_path)
    ancho1, alto1 = img1.size
    nuevo_ancho1 = ancho1 * escala1
    nuevo_alto1 = alto1 * escala1
    x1, y1 = coords1

    c.saveState()
    c.translate(x1, y1)
    c.rotate(0)
    c.drawImage(ImageReader(imagen1_path), 0, 0, width=nuevo_ancho1, height=nuevo_alto1, mask='auto')
    c.restoreState()

    # === Imagen 3: SELLO (normal) ===
    img2 = Image.open(imagen2_path)
    ancho2, alto2 = img2.size
    nuevo_ancho2 = ancho2 * escala2
    nuevo_alto2 = alto2 * escala2
    x2, y2 = coords2

    c.drawImage(ImageReader(imagen2_path), x2, y2, width=nuevo_ancho2, height=nuevo_alto2, mask='auto')

    # Guardar PDF temporal con las imágenes
    c.save()

    # Combinar la página editada con el PDF original
    with open(temp_pdf_path, "rb") as temp_pdf:
        temp_reader = PdfReader(temp_pdf)
        first_page = reader.pages[0]
        first_page.merge_page(temp_reader.pages[0])
        writer.add_page(first_page)

        # Copiar el resto de las páginas
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])

    # Guardar el nuevo PDF
    with open(output_path, "wb") as f_out:
        writer.write(f_out)

    # Eliminar PDF temporal
    os.remove(temp_pdf_path)
    print(f"✅ Parche, Vinci y Sello insertados en {output_path}")

# === Uso ===
ruta_pdf = "ID-CJV-T1M-C-X-ALC-IN-DG00-00_Rev_A.pdf"
parche = "parche.png"
imagen1 = "vinci.jpg"
imagen2 = "VCGP.png"
output_path = "nuevo_documento.pdf"

coords_parche = (320, 264)
escala_parche = 0.4

coords1 = (395, 410)
escala1 = 0.075

coords2 = (87, 57)
escala2 = 0.25

insertar_tres_imagenes_en_pdf(
    ruta_pdf,
    parche,
    imagen1,
    imagen2,
    output_path,
    coords_parche,
    escala_parche,
    coords1,
    escala1,
    coords2,
    escala2
)
