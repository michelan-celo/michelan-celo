from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = ASSETS / "profile-background-source.png"
MASTER = ASSETS / "profile-background.png"
SLICES = ASSETS / "background"

MASTER_WIDTH = 1280
MASTER_HEIGHT = 1348
DARKEN_ALPHA = 58

SLICE_BOXES = {
    "header.png": (0, 0, 1280, 250),
    "about.png": (0, 250, 640, 610),
    "tugep.png": (640, 250, 1280, 610),
    "imece.png": (0, 610, 640, 970),
    "toolkit.png": (640, 610, 1280, 970),
    "languages.png": (0, 970, 640, 1230),
    "activity.png": (640, 970, 1280, 1230),
    "song.png": (0, 1230, 640, 1348),
    "quote.png": (640, 1230, 1280, 1348),
}


def cover(image: Image.Image, width: int, height: int) -> Image.Image:
    source_width, source_height = image.size
    scale = max(width / source_width, height / source_height)
    resized_width = round(source_width * scale)
    resized_height = round(source_height * scale)
    resized = image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
    left = (resized_width - width) // 2
    top = (resized_height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def main() -> None:
    source = Image.open(SOURCE).convert("RGBA")
    master = cover(source, MASTER_WIDTH, MASTER_HEIGHT)
    shade = Image.new("RGBA", master.size, (0, 0, 0, DARKEN_ALPHA))
    master = Image.alpha_composite(master, shade).convert("RGB")

    MASTER.parent.mkdir(parents=True, exist_ok=True)
    SLICES.mkdir(parents=True, exist_ok=True)
    master.save(MASTER, format="PNG", optimize=True)

    for name, box in SLICE_BOXES.items():
        master.crop(box).save(SLICES / name, format="PNG", optimize=True)

    print(f"Saved {MASTER_WIDTH}x{MASTER_HEIGHT} master background to {MASTER}")
    print(f"Saved {len(SLICE_BOXES)} synchronized background slices to {SLICES}")


if __name__ == "__main__":
    main()
