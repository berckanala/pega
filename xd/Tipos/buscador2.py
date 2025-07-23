import os
import fitz  # PyMuPDF
from collections import defaultdict

def buscar_pdfs(ruta_raiz):
    pdfs = []
    for dirpath, _, files in os.walk(ruta_raiz):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdfs.append(os.path.join(dirpath, file))
    return pdfs

def obtener_dimension_primera_pagina(ruta_pdf):
    try:
        with fitz.open(ruta_pdf) as doc:
            if len(doc) == 0:
                return None
            primera = doc[0]
            return (round(primera.rect.width), round(primera.rect.height))
    except Exception as e:
        print(f"⚠️ Error al leer {ruta_pdf}: {e}")
        return None

def main(ruta_raiz):
    pdfs = buscar_pdfs(ruta_raiz)
    print(f"🔍 Se encontraron {len(pdfs)} archivos PDF.\n")

    conteo_por_dimension = defaultdict(int)
    ejemplo_por_dimension = {}

    for pdf in pdfs:
        dimension = obtener_dimension_primera_pagina(pdf)
        if dimension:
            conteo_por_dimension[dimension] += 1
            if dimension not in ejemplo_por_dimension:
                ejemplo_por_dimension[dimension] = os.path.relpath(pdf, ruta_raiz)

    print("📊 Dimensiones únicas encontradas (solo primera página):")
    print("=" * 60)
    for dim in sorted(conteo_por_dimension.keys()):
        print(f"{dim}: {conteo_por_dimension[dim]:>4} archivos — Ejemplo: {ejemplo_por_dimension[dim]}")

    print(f"\n✅ Total dimensiones únicas: {len(conteo_por_dimension)}")
    print(f"✅ Total archivos analizados: {len(pdfs)}")

if __name__ == "__main__":
    ruta_directorio = "."
    main(ruta_directorio)
