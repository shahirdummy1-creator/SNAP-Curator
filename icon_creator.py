from PIL import Image, ImageDraw

size = 256
img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# background
for i in range(size):
    for j in range(size):
        r = 26 + (i // 10)
        g = 74 + (j // 12)
        b = 150 + ((i + j) // 20)
        draw.point((i, j), fill=(r % 256, g % 256, b % 256, 255))

# rounded square panel
panel = (30, 30, 226, 226)
draw.rounded_rectangle(panel, radius=34, fill=(18, 55, 110, 255))

# mini image icon
img_box = (64, 64, 192, 192)
draw.rounded_rectangle(img_box, radius=16, fill=(255, 255, 255, 255))
# mountains / product shape
points = [(78, 160), (104, 120), (134, 145), (156, 102), (188, 160)]
draw.polygon(points, fill=(38, 140, 210, 255))
# small spark
for x, y in [(110, 90), (146, 88), (128, 72)]:
    draw.ellipse((x, y, x + 10, y + 10), fill=(255, 206, 84, 255))

# white border stripe
draw.rounded_rectangle((54, 54, 202, 202), radius=18, outline=(210, 230, 255, 255), width=5)

# app letter S
font_size = 88
try:
    from PIL import ImageFont
    font = ImageFont.truetype('arial.ttf', font_size)
except Exception:
    font = ImageFont.load_default()

draw.text((102, 96), 'S', font=font, fill=(255, 255, 255, 255))

img.save('snap_icon.png')
print('Created snap_icon.png')
