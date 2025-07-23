from PIL import Image, ImageDraw

def crear_parche_png(output_path):
    # Crear imagen transparente de 800x800 píxeles
    img_size = (800, 800)
    img = Image.new("RGBA", img_size, (255, 255, 255, 0))

    # Crear objeto de dibujo
    draw = ImageDraw.Draw(img)

    # Definir coordenadas del rectángulo
    rect_width = 400
    rect_height = 100
    x0 = (img_size[0] - rect_width) / 2
    y0 = (img_size[1] - rect_height) / 2
    x1 = x0 + rect_width
    y1 = y0 + rect_height

    # Dibujar rectángulo blanco opaco
    draw.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 255))

    # Guardar como PNG
    img.save(output_path, "PNG")

# Ejecutar la función
crear_parche_png("parche.png")
