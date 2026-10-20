from pathlib import Path

from PIL import Image, ImageDraw


SIZE = 256
image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(image)

draw.rounded_rectangle((8, 8, 248, 248), radius=52, fill="#3157c8")
draw.rounded_rectangle((47, 60, 209, 196), radius=16, fill="#ffffff")
draw.ellipse((83, 81, 109, 107), fill="#31a89b")
draw.polygon(((62, 174), (101, 130), (125, 156), (156, 117), (207, 178), (207, 180), (62, 180)),
             fill="#b9c9f8")
draw.polygon(((169, 130), (200, 94), (209, 105), (209, 180), (195, 180)),
             fill="#31a89b")

output = Path(__file__).with_name("app_icon.ico")
image.save(output, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
