from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(image_path, output_path, first_name, last_name, course_name, font_path="text.ttf", font_size=250,
                      position1=(4000, 4250), position2=(4000, 4850), fill_color='black'):
    # Открываем изображение
    image = Image.open(image_path)

    # Загружаем шрифт
    font = ImageFont.truetype(font_path, font_size)
    drawer = ImageDraw.Draw(image)

    # Добавляем текст
    full_name = f"{first_name} {last_name}"
    drawer.text(position1, full_name, font=font, fill=fill_color)
    drawer.text(position2, course_name, font=font, fill=fill_color)

    # Сохраняем и отображаем изображение
    image.save(output_path)
    image.show()


# Пример использования функции
add_text_to_image("72.jpg", "new_img.jpg", "Имя", "Фамилия", "Наименование курса")
