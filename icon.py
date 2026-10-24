"""Generate the RunCoach app icon: a 300x300 PNG for the Garmin app form.

Drawn at 4x and downsampled so the curves and the route line stay smooth at
300 px. No external assets: the mark is a route with a start dot and a finish
ring, which is what the app actually does with Garmin (it sends the race
course to the watch).
"""

from PIL import Image, ImageDraw

SIZE = 1200          # working canvas, downsampled to 300
BG = (15, 23, 42)    # slate 900
ACCENT = (249, 115, 22)   # orange 500
ACCENT_2 = (251, 146, 60)  # orange 400
RING = (248, 250, 252)     # slate 50


def rounded_mask(size: int, radius: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1], radius, fill=255)
    return mask


def build() -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), BG + (0,))
    draw = ImageDraw.Draw(img)

    # Subtle vertical gradient so the tile does not look flat.
    for y in range(SIZE):
        t = y / SIZE
        r = int(BG[0] + (30 - BG[0]) * t)
        g = int(BG[1] + (41 - BG[1]) * t)
        b = int(BG[2] + (59 - BG[2]) * t)
        draw.line([(0, y), (SIZE, y)], fill=(r, g, b, 255))

    # The route: bottom-left to top-right with two bends, like a course profile.
    pts = [
        (250, 900),
        (430, 760),
        (560, 820),
        (720, 560),
        (860, 610),
        (960, 320),
    ]
    draw.line(pts, fill=ACCENT + (255,), width=54, joint="curve")

    # Start dot (solid) and finish ring, the two anchors of a course.
    draw.ellipse([250 - 46, 900 - 46, 250 + 46, 900 + 46], fill=ACCENT_2 + (255,))
    draw.ellipse([960 - 74, 320 - 74, 960 + 74, 320 + 74], outline=RING + (255,), width=26)
    draw.ellipse([960 - 30, 320 - 30, 960 + 30, 320 + 30], fill=RING + (255,))

    img.putalpha(rounded_mask(SIZE, 230))
    return img


def main() -> None:
    icon = build()
    icon.resize((300, 300), Image.LANCZOS).save("assets/icon-300.png")
    icon.resize((512, 512), Image.LANCZOS).save("assets/icon-512.png")
    print("wrote assets/icon-300.png and assets/icon-512.png")


if __name__ == "__main__":
    main()
