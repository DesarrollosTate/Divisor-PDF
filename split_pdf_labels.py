import os
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas

def split_pdf_into_labels(input_pdf_path, output_pdf_path, poppler_path=None):
    # Convertir las páginas del PDF a imágenes
    pages_as_images = convert_from_path(input_pdf_path, dpi=300, poppler_path=poppler_path)

    # Definir las dimensiones de la etiqueta (10x15 cm en puntos)
    label_width = 283.5  # 10 cm
    label_height = 425.25  # 15 cm

    # Crear un nuevo PDF para las etiquetas
    c = canvas.Canvas(output_pdf_path, pagesize=(label_width, label_height))

    # Recorrer todas las imágenes de las páginas del PDF original
    for page_image in pages_as_images:
        # Dimensiones de la página (imagen)
        page_width, page_height = page_image.size

        # Número de etiquetas por fila y columna (2x2 en este caso)
        cols, rows = 2, 2
        label_width_image = page_width // cols
        label_height_image = page_height // rows

        # Generar recortes dinámicos para cada etiqueta
        for row in range(rows):
            for col in range(cols):
                # Coordenadas del recorte (origen en la esquina superior izquierda)
                left = col * label_width_image
                upper = row * label_height_image
                right = left + label_width_image
                lower = upper + label_height_image

                # Recortar la etiqueta
                cropped_label = page_image.crop((left, upper, right, lower))

                # Guardar la etiqueta temporalmente como archivo en memoria
                temp_image_path = f"temp_label_{row}_{col}.png"
                cropped_label.save(temp_image_path, format="PNG")

                # Dibujar la etiqueta en la página del PDF (ajustada a 10x15 cm)
                c.drawImage(temp_image_path, 0, 0, width=label_width, height=label_height, mask="auto")

                # Eliminar la imagen temporal
                os.remove(temp_image_path)

                # Añadir nueva página para el siguiente recorte
                c.showPage()

    # Guardar el PDF final
    c.save()

    print(f"Se generó el archivo con etiquetas en: {output_pdf_path}")

# Parámetros de entrada y salida
input_pdf_path = "andreani_labels.pdf"  # Ruta del PDF original
output_pdf_path = "output_labels.pdf"  # Ruta del nuevo PDF
poppler_path = r"C:\Users\usuario\Desktop\Divisor-PDF-main\poppler-24.08.0\Library\bin"  # Ruta al binario de Poppler

# Ejecutar la función
split_pdf_into_labels(input_pdf_path, output_pdf_path, poppler_path)

