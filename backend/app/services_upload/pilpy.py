from PIL import Image, ImageDraw, ImageFont
import io

def add_star_names(image_bytes, stars):
    star_coordinates = {name: (x, y) for name, x, y in zip(stars['main_id'], stars['field_x'], stars['field_y'])}
    
    # Crear un objeto tipo archivo en memoria
    image_stream = io.BytesIO(image_bytes)

    # Abrir la imagen usando Pillow
    image = Image.open(image_stream)

    # Convertir imagen para reducir paleta de colores
    image = image.convert('RGB')
    draw = ImageDraw.Draw(image)
    
    # Elegir una fuente (puedes ajustar el tamaño si es necesario)
    try:
        font = ImageFont.truetype("arial.ttf", 20)  # Intenta con Arial si está disponible
    except IOError:
        font = ImageFont.load_default()  # Usa fuente predeterminada si no está Arial

    # Definir el radio del círculo
    radius = 10
    # Dibujar los nombres y los círculos en las coordenadas especificadas
    for star_name, (x, y) in star_coordinates.items():
        # Dibujar un círculo alrededor de las coordenadas
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), outline="greenyellow", width=2)
        
        # Dibujar el nombre de la estrella
        draw.text((x + radius + 5, y - radius), star_name, fill="greenyellow", font=font)

    # Guardar la imagen con los nombres añadidos
    #image.save('image.jpg')

    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes, image

