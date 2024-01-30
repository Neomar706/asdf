from PIL import Image


def avg_image_color(path):
    img = Image.open(path)
    img = img.convert('RGB')

    width, height = img.size

    r_total = 0
    g_total = 0
    b_total = 0
    count   = 0

    for x in range(width):
        for y in range(height):
            r, g, b = img.getpixel((x, y))

            r_total += r
            g_total += g
            b_total += b
            count   += 1

    return hex(int(r_total/count)).split('x')[-1] + \
           hex(int(g_total/count)).split('x')[-1] + \
           hex(int(b_total/count)).split('x')[-1]