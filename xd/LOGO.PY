from PIL import Image, ImageDraw, ImageFont

def crear_sello_png(output_path):
    # Imagen final
    img_size = (1200, 1200)
    img = Image.new("RGBA", img_size, (255, 255, 255, 0))

    # Imagen temporal más grande para rotar sin recortes
    temp_size = (2000, 2000)
    temp = Image.new("RGBA", temp_size, (255, 255, 255, 0))
    temp_draw = ImageDraw.Draw(temp)

    # Colores
    rect_color = (0, 0, 255, 255)
    text_bg_color = (255, 255, 255, 255)
    text_color = (0, 0, 255, 255)

    # Tamaño rectángulo grande
    rect_width = 945
    rect_height = 94

    # Coordenadas rectángulo grande centrado en temp
    x0 = (temp_size[0] - rect_width) / 2
    y0 = (temp_size[1] - rect_height) / 2+11
    x1 = x0 + rect_width
    y1 = y0 + rect_height+1

    # Rectángulo solo línea
    temp_draw.rectangle(
        [x0, y0, x1, y1],
        outline=rect_color,
        width=3
    )

    # Fuente
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()

    # Texto
    text = "AJUSTE POR LEVANTAMIENTO"

    # Tamaño texto
    bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Coordenadas centradas en temp
    text_x = (temp_size[0] - text_width) / 2
    text_y = (temp_size[1] - text_height) / 2

    # Padding fondo texto
    padding = 12
    bg_x0 = text_x - padding
    bg_y0 = text_y +5
    bg_x1 = text_x + text_width + padding
    bg_y1 = text_y + text_height + padding+2

    # Fondo blanco detrás del texto
    temp_draw.rectangle([bg_x0, bg_y0, bg_x1, bg_y1], fill=text_bg_color)

    # Texto
    temp_draw.text((text_x, text_y), text, font=font, fill=text_color)

    # Rotar el bloque
    rotated = temp.rotate(135, expand=1)

    # Calcular coordenadas para pegar centrado en imagen final
    rotated_width, rotated_height = rotated.size
    paste_x = (img_size[0] - rotated_width) // 2
    paste_y = (img_size[1] - rotated_height) // 2

    # Pegar centrado
    img.paste(rotated, (paste_x, paste_y), rotated)

    # Guardar
    img.save(output_path, "PNG")

# Ejecutar
crear_sello_png("sello_ajuste.png")
