# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 17:14:14 2024

@author: Bernardo
"""

import fitz 

def obtener_dimensiones_pdf(ruta_pdf):
    # Abre el documento PDF
    documento = fitz.open(ruta_pdf)
    
    # Itera sobre las páginas del documento y obtiene las dimensiones
    dimensiones_paginas = []
    for pagina_num in range(len(documento)):
        pagina = documento.load_page(pagina_num)
        dimensiones = pagina.rect  # Obtiene el rectángulo que define la página
        dimensiones_paginas.append((dimensiones.width, dimensiones.height))
    
    return dimensiones_paginas

# Ejemplo de uso
ruta_pdf = "ID-CJV-T1M-P-2-CRE-PD-1001_06_REV_0.pdf"
dimensiones = obtener_dimensiones_pdf(ruta_pdf)
for idx, (ancho, alto) in enumerate(dimensiones):
    print(f"Página {idx + 1}: {ancho} x {alto} puntos")
    
    

