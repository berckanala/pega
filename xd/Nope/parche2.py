from PIL import Image, ImageDraw, ImageFont

# Parámetros
texto = "VCGP"
factor_escala = 4  # trabajar 4 veces más grande
tamaño_base = (170, 60)
tamaño_grande = (tamaño_base[0]*factor_escala, tamaño_base[1]*factor_escala)
color_fondo = "white"
color_texto = "black"
ruta_salida = "VCGP.png"

# Crear imagen grande
imagen = Image.new("RGB", tamaño_grande, color_fondo)
dibujo = ImageDraw.Draw(imagen)

# Cargar fuente delgada y escalada
try:
    fuente = ImageFont.truetype("arial.ttf", 50 * factor_escala)
except:
    fuente = ImageFont.load_default()

# Centrar texto
bbox = dibujo.textbbox((0, 0), texto, font=fuente)
w_texto = bbox[2] - bbox[0]
h_texto = bbox[3] - bbox[1]
x = (tamaño_grande[0] - w_texto) // 2
y = (tamaño_grande[1] - h_texto) // 2-20

# Dibujar texto
dibujo.text((x, y), texto, fill=color_texto, font=fuente)

# Reducir suavemente con antialiasing
imagen_final = imagen.resize(tamaño_base, Image.Resampling.LANCZOS)

# Guardar
imagen_final.save(ruta_salida)
print(f"✅ Imagen guardada como {ruta_salida} con mayor nitidez")
