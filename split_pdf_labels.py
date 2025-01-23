import os
from pdf2image import convert_from_path
from PIL import Image, ImageChops
from reportlab.pdfgen import canvas

def is_blank_image(image, threshold=250):
    """
    Verifica si una imagen está en blanco.
    :param image: Objeto de imagen (Pillow Image).
    :param threshold: Valor para considerar píxeles como "blancos" (0-255).
    :return: True si la imagen está en blanco, False de lo contrario.
    """
    # Convertir la imagen a escala de grises
    grayscale = image.convert("L")
    # Calcular el píxel más oscuro
    extrema = grayscale.getextrema()
    # Verificar si todos los píxeles son más claros que el umbral
    return extrema[0] >= threshold

def split_pdf_into_labels(input_pdf_path, output_pdf_path, poppler_path=None):
    """
    Divide un PDF en etiquetas individuales en el orden B1, B2, A1, A2.
    Omite etiquetas que estén en blanco.
    """
    # Convertir las páginas del PDF en imágenes
    pages_as_images = convert_from_path(input_pdf_path, dpi=300, poppler_path=poppler_path)

    # Definir las dimensiones de la página de salida (10x15 cm en puntos)
    label_width = 283.5  # 10 cm
    label_height = 425.25  # 15 cm

    # Crear un nuevo PDF para las etiquetas
    c = canvas.Canvas(output_pdf_path, pagesize=(label_width, label_height))

    for page_index, page_image in enumerate(pages_as_images):
        # Dimensiones de la página original
        width, height = page_image.size

        # Dimensiones de cada etiqueta
        label_width_image = width // 2
        label_height_image = height // 2

        # Coordenadas de las etiquetas en el orden B1, B2, A1, A2
        label_coords = [
            (0, 0, label_width_image, height // 2),  # B1 (Abajo izquierda)
            (label_width_image, 0, width, height // 2),  # B2 (Abajo derecha)
            (0, height // 2, label_width_image, height),  # A1 (Arriba izquierda)
            (label_width_image, height // 2, width, height),  # A2 (Arriba derecha)
        ]

        # Procesar cada etiqueta en el orden correcto
        for coord_index, coords in enumerate(label_coords):
            # Recortar la etiqueta correspondiente
            cropped_label = page_image.crop(coords)

            # Verificar si la etiqueta está en blanco
            if is_blank_image(cropped_label):
                print(f"Etiqueta en blanco detectada: Página {page_index + 1}, Etiqueta {coord_index + 1}. Omitiendo...")
                continue

            # Guardar la etiqueta temporalmente como archivo único
            temp_image_path = f"temp_label_{page_index}_{coord_index}.png"
            cropped_label.save(temp_image_path, format="PNG")

            # Dibujar la etiqueta en el PDF
            c.drawImage(temp_image_path, 0, 0, width=label_width, height=label_height, mask='auto')
            c.showPage()

            # Eliminar el archivo temporal
            os.remove(temp_image_path)

    # Guardar el PDF final
    c.save()
    print(f"Se generó el archivo con etiquetas en: {output_pdf_path}")

# Parámetros de entrada y salida
input_pdf_path = "andreani_labels.pdf"  # Ruta del archivo PDF original
output_pdf_path = "output_labels.pdf"  # Ruta del archivo PDF generado
poppler_path = r"C:\Users\usuario\Desktop\poppler-24.08.0\Library\bin"  # Ruta al binario de Poppler

# Ejecutar la función
split_pdf_into_labels(input_pdf_path, output_pdf_path, poppler_path)

