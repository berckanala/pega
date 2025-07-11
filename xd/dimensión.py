# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 12:18:53 2024

@author: Bernardo
"""
import os
from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

def insertar_imagen_en_pdf(pdf_path, imagen_path, output_path, coordenadas, escala):
    # Abrir el PDF existente
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Verificar dimensiones de la primera página
    page = reader.pages[0]
    width = float(page.mediabox.upper_right[0])
    height = float(page.mediabox.upper_right[1])

    # Crear un nuevo PDF con la imagen en las coordenadas especificadas
    temp_pdf_path = "temp.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=(width, height))

    # Posicionar la imagen en las coordenadas especificadas
    imagen = ImageReader(imagen_path)
    img = Image.open(imagen_path)
    imagen_ancho, imagen_alto = img.size
    x, y = coordenadas

    # Calcular nuevo tamaño de la imagen basado en la escala
    nuevo_ancho = imagen_ancho * escala
    nuevo_alto = imagen_alto * escala

    c.drawImage(imagen, x, y, width=nuevo_ancho, height=nuevo_alto, mask='auto')
    c.showPage()  # Mover a la siguiente página para asegurar que se guarda
    c.save()

    # Añadir la imagen a la primera página del PDF
    with open(temp_pdf_path, "rb") as temp_pdf:
        temp_reader = PdfReader(temp_pdf)
        first_page = reader.pages[0]
        first_page.merge_page(temp_reader.pages[0])
        writer.add_page(first_page)

        # Agregar el resto de las páginas del PDF original
        for i in range(1, len(reader.pages)):
            writer.add_page(reader.pages[i])

    # Guardar el nuevo PDF
    with open(output_path, "wb") as output_pdf:
        writer.write(output_pdf)
    
    # Eliminar el PDF temporal
    os.remove(temp_pdf_path)

    print(f"Imagen insertada en {output_path}")

# Especificar los parámetros del nuevo documento
ruta_pdf = "ID-CJV-T1M-P-2-CRE-PD-1001_06_REV_0.pdf"
ruta_imagen = "sello_ajuste.png"
output_path = "nuevo_documento_con_logo.pdf"
escala = 0.45  # Escala deseada para la redimensión, ajustar según el tamaño de la imagen
coordenadas = (1637, 2859)  # Coordenadas donde colocar la imagen en el PDF, ajustar según tus necesidades

# Llamar a la función para insertar la imagen rotada y redimensionada en el PDF
insertar_imagen_en_pdf(ruta_pdf, ruta_imagen, output_path, coordenadas, escala)