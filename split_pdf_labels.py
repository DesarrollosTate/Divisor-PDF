import os
from pdf2image import convert_from_path
from PIL import Image
from reportlab.pdfgen import canvas

def split_pdf_into_labels(input_pdf_path, output_pdf_path, poppler_path=None):
    # Convertir las páginas del PDF a imágenes
    pages_as_images = convert_from_path(input_pdf_path, dpi=300, poppler_path=poppler_path)

    # Definir las dimensiones de la página (10x15 cm en puntos)
    label_width = 283.5  # 10 cm
    label_height = 425.25  # 15 cm

    # Crear un nuevo PDF para las etiquetas
    c = canvas.Canvas(output_pdf_path, pagesize=(label_width, label_height))

    for page_image in pages_as_images:
        # Dimensiones de la página (imagen)
        width, height = page_image.size

        # Dimensiones de cada etiqueta
        label_width_image = width // 2
        label_height_image = height // 2

        # Coordenadas de las 4 etiquetas
        label_coords = [
            (0, height // 2, label_width_image, height),  # Arriba izquierda
            (label_width_image, height // 2, width, height),  # Arriba derecha
            (0, 0, label_width_image, height // 2),  # Abajo izquierda
            (label_width_image, 0, width, height // 2),  # Abajo derecha
        ]

        for coords in label_coords:
            # Recortar la etiqueta correspondiente
            cropped_label = page_image.crop(coords)

            # Guardar la etiqueta temporalmente como archivo
            temp_image_path = "temp_label.png"
            cropped_label.save(temp_image_path, format="PNG")

            # Dibujar la etiqueta en el PDF
            c.drawImage(temp_image_path, 0, 0, width=label_width, height=label_height, mask='auto')
            c.showPage()

            # Eliminar la imagen temporal
            os.remove(temp_image_path)

    # Guardar el PDF final
    c.save()

    print(f"Se generó el archivo con etiquetas en: {output_pdf_path}")

# Parámetros de entrada y salida
input_pdf_path = "andreani_labels.pdf"  # Ruta del PDF original
output_pdf_path = "output_labels.pdf"  # Ruta del nuevo PDF
poppler_path = r"C:\Users\usuario\Desktop\Trabajos\Python\poppler-24.08.0\Library\bin"  # Ruta al binario de Poppler

# Ejecutar la función
split_pdf_into_labels(input_pdf_path, output_pdf_path, poppler_path)
