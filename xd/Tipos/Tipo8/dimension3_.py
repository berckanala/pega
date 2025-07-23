import os
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def insertar_tres_imagenes_en_pdf(pdf_path, parche_path, imagen1_path, imagen2_path, imagen3_path,
                                  output_path, coords_parche, escala_parche,
                                  coords1, escala1, coords2, escala2, coords3, escala3):
    # Abrir el PDF original
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Dimensiones de la primera página
    page = reader.pages[0]
    width = float(page.mediabox.upper_right[0])
    height = float(page.mediabox.upper_right[1])

    # Crear PDF temporal
    temp_pdf_path = "temp.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=(width, height))

    # === Imagen PARCHE (1a) ===
    parche = ImageReader(parche_path)
    img_p = Image.open(parche_path)
    ancho_p, alto_p = img_p.size
    x_p, y_p = coords_parche
    nuevo_ancho_p = ancho_p * escala_parche
    nuevo_alto_p = alto_p * escala_parche
    # Rotar imagen 1
    c.saveState()
    c.translate(x_p, y_p)
    c.rotate(0)
    c.drawImage(ImageReader(parche_path), 0, 0, width=nuevo_ancho_p, height=nuevo_alto_p, mask='auto')
    c.restoreState()

    # === Imagen 1 (Vinci) ===
    img1 = Image.open(imagen1_path)
    ancho1, alto1 = img1.size
    x1, y1 = coords1
    nuevo_ancho1 = ancho1 * escala1
    nuevo_alto1 = alto1 * escala1

    # Rotar imagen 1
    c.saveState()
    c.translate(x1, y1)
    c.rotate(0)
    c.drawImage(ImageReader(imagen1_path), 0, 0, width=nuevo_ancho1, height=nuevo_alto1, mask='auto')
    c.restoreState()

    # === Imagen 2 (Sello) ===
    img2 = Image.open(imagen2_path)
    ancho2, alto2 = img2.size
    x2, y2 = coords2
    nuevo_ancho2 = ancho2 * escala2
    nuevo_alto2 = alto2 * escala2
        # Rotar imagen 2
    c.saveState()
    c.translate(x2, y2)
    c.rotate(0)
    c.drawImage(ImageReader(imagen2_path), 0, 0, width=nuevo_ancho2, height=nuevo_alto2, mask='auto')
    c.restoreState()

    # === Imagen 3 (Sello Ajuste) ===
    img3 = Image.open(imagen3_path)
    ancho3, alto3 = img3.size
    x3, y3 = coords3
    nuevo_ancho3 = ancho3 * escala3
    nuevo_alto3 = alto3 * escala3

    # Rotar imagen 3
    c.saveState()
    c.translate(x3, y3)
    c.rotate(270)
    c.drawImage(ImageReader(imagen3_path), 0, 0, width=nuevo_ancho3, height=nuevo_alto3, mask='auto')
    c.restoreState()

    # Guardar página
    c.showPage()
    c.save()

    # Fusionar con el PDF original
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

    print(f"Parche + Vinci + Sello insertados en {output_path}")


# === Ejemplo de uso ===
ruta_pdf = "ID-CJV-T1M-X-X-ELX-PL-0251_03_REV_0.pdf"
parche = "parche.png"          # El parche blanco
imagen1 = "vinci.jpg"          # Vinci
imagen2 = "VCGP.png"         # Sello VCGP
imagen3 = "sello_ajuste.png"   # Sello ajuste

output_path = "nuevo_.pdf"

# Configurar coordenadas y escalas
coords_parche = (4120, 191)
escala_parche = 0.38

coords1 = (4210, 325) #x, -y
escala1 = 0.1

coords2 = (4218, 63)
escala2 = 0.2

coords3 = (4030, 750)
escala3 = 0.45

# Ejecutar
insertar_tres_imagenes_en_pdf(
    ruta_pdf,
    parche,
    imagen1,
    imagen2,
    imagen3,
    output_path,
    coords_parche,
    escala_parche,
    coords1,
    escala1,
    coords2,
    escala2,
    coords3,
    escala3
)
