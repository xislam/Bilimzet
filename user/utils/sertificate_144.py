from PIL import Image, ImageDraw, ImageFont

image = Image.open("144.jpg")

font = ImageFont.truetype("text.ttf", 250)
drawer = ImageDraw.Draw(image)
drawer.text((4000, 4250), "Hello World!", font=font, fill='black')
drawer.text((4000, 4850), "Наименование курса", font=font, fill='black')
image.save('new_img.jpg')
image.show()