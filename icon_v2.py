"""RunCoach icon: route stroke drawn as one filled polygon.

``ImageDraw.line(width=..., joint='curve')`` renders a chain of quads plus joint
discs, which leaves visible seams on a dense curve (they read as hatch marks
across the stroke). Offsetting the path and filling a single polygon gives a
uniform stroke instead; the round caps come from two end discs.
"""

import math

from PIL import Image, ImageDraw

SIZE = 1200
BG = (15, 23, 42)
ACCENT = (249, 115, 22)
ACCENT_2 = (251, 146, 60)
RING = (248, 250, 252)
STROKE = 52


def catmull_rom(points, samples=48):
    pts = [points[0]] + list(points) + [points[-1]]
    out = []
    for i in range(len(pts) - 3):
        p0, p1, p2, p3 = pts[i : i + 4]
        for s in range(samples):
            t = s / samples
            t2, t3 = t * t, t * t * t
            out.append(
                (
                    0.5
                    * (
                        2 * p1[0]
                        + (-p0[0] + p2[0]) * t
                        + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
                        + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
                    ),
                    0.5
                    * (
                        2 * p1[1]
                        + (-p0[1] + p2[1]) * t
                        + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
                        + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
                    ),
                )
            )
    out.append(points[-1])
    return out


def stroke_polygon(path, width):
    """Return the outline of a constant-width stroke along ``path``."""
    half = width / 2
    left, right = [], []
    for i, (x, y) in enumerate(path):
        x0, y0 = path[max(i - 1, 0)]
        x1, y1 = path[min(i + 1, len(path) - 1)]
        dx, dy = x1 - x0, y1 - y0
        norm = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / norm, dx / norm
        left.append((x + nx * half, y + ny * half))
        right.append((x - nx * half, y - ny * half))
    return left + right[::-1]


def build():
    img = Image.new("RGBA", (SIZE, SIZE), BG + (0,))
    draw = ImageDraw.Draw(img)
    for y in range(SIZE):
        t = y / SIZE
        draw.line(
            [(0, y), (SIZE, y)],
            fill=(
                int(BG[0] + (30 - BG[0]) * t),
                int(BG[1] + (41 - BG[1]) * t),
                int(BG[2] + (59 - BG[2]) * t),
                255,
            ),
        )

    control = [(270, 880), (450, 700), (600, 790), (740, 520), (880, 560), (930, 300)]
    path = catmull_rom(control)
    draw.polygon(stroke_polygon(path, STROKE), fill=ACCENT + (255,))

    # Round caps so the stroke does not end in a square.
    for x, y in (path[0], path[-1]):
        r = STROKE / 2
        draw.ellipse([x - r, y - r, x + r, y + r], fill=ACCENT + (255,))

    # Start dot and finish target.
    draw.ellipse([270 - 46, 880 - 46, 270 + 46, 880 + 46], fill=ACCENT_2 + (255,))
    draw.ellipse([930 - 76, 300 - 76, 930 + 76, 300 + 76], outline=RING + (255,), width=26)
    draw.ellipse([930 - 28, 300 - 28, 930 + 28, 300 + 28], fill=RING + (255,))

    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], 230, fill=255)
    img.putalpha(mask)
    return img


if __name__ == "__main__":
    icon = build()
    icon.resize((300, 300), Image.LANCZOS).save("assets/icon-300.png")
    icon.resize((512, 512), Image.LANCZOS).save("assets/icon-512.png")
    print("wrote assets/icon-300.png and assets/icon-512.png")
