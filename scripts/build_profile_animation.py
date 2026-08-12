from __future__ import annotations

import io
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageEnhance, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BACKGROUND = ASSETS / "profile-background-source.gif"
OUTPUT = ASSETS / "profile-console.webp"
POSTER = ASSETS / "profile-console-poster.png"

WIDTH = 1280
HEIGHT = 1348
BACKGROUND_DARKEN_ALPHA = 58
FRAME_COUNT = 60
FRAME_DURATION_MS = 200
WEBP_QUALITY = 44

PANELS = (
    ("profile-header.svg", (0, 0), (1280, 250)),
    ("about-card.svg", (0, 250), (640, 360)),
    ("toolkit-card.svg", (640, 610), (640, 360)),
    ("languages-card.svg", (0, 970), (640, 260)),
    ("activity-card.svg", (640, 970), (640, 260)),
    ("song-1.svg", (0, 1230), (640, 118)),
    ("quote-card.svg", (640, 1230), (640, 118)),
)

SPACECRAFT = (
    ("spacecraft-01.gif", (640, 250)),
    ("spacecraft-02.gif", (0, 610)),
)

BACKGROUND_IMAGE_RE = re.compile(
    r'\s*<image href="data:image/(?:png|gif|webp);base64,[^"]+"[^>]*(?:/\>|>[\s\S]*?</image>)',
    re.IGNORECASE,
)


def cover(image: Image.Image, width: int, height: int) -> Image.Image:
    source_width, source_height = image.size
    scale = max(width / source_width, height / source_height)
    resized_width = round(source_width * scale)
    resized_height = round(source_height * scale)
    resized = image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
    left = (resized_width - width) // 2
    top = (resized_height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def darken(frame: Image.Image) -> Image.Image:
    shade = Image.new("RGBA", frame.size, (0, 0, 0, BACKGROUND_DARKEN_ALPHA))
    return Image.alpha_composite(frame.convert("RGBA"), shade).convert("RGBA")


def sample_indices(source_count: int) -> list[int]:
    return [round(index * (source_count - 1) / (FRAME_COUNT - 1)) for index in range(FRAME_COUNT)]


def background_frames() -> list[Image.Image]:
    with Image.open(BACKGROUND) as source:
        if getattr(source, "n_frames", 1) < 2:
            raise RuntimeError(f"{BACKGROUND.name} must be animated")
        frames = []
        for source_index in sample_indices(source.n_frames):
            source.seek(source_index)
            frames.append(darken(cover(source.convert("RGBA"), WIDTH, HEIGHT)))
        return frames


def render_panel_overlay(svg_name: str, size: tuple[int, int]) -> Image.Image:
    try:
        import cairosvg
    except ImportError as error:
        raise RuntimeError("CairoSVG is required to build the profile animation") from error

    svg_path = ASSETS / svg_name
    source = svg_path.read_text(encoding="utf-8")
    source, count = BACKGROUND_IMAGE_RE.subn("", source, count=1)
    if count != 1:
        raise RuntimeError(f"Embedded background was not found in {svg_name}")
    rendered = cairosvg.svg2png(
        bytestring=source.encode("utf-8"),
        output_width=size[0],
        output_height=size[1],
    )
    return Image.open(io.BytesIO(rendered)).convert("RGBA")


def panel_overlays() -> list[tuple[Image.Image, tuple[int, int]]]:
    return [
        (render_panel_overlay(name, size), position)
        for name, position, size in PANELS
    ]


def extract_spacecraft_layers(
    frames: list[Image.Image],
) -> list[tuple[list[Image.Image], tuple[int, int]]]:
    layers: list[tuple[list[Image.Image], tuple[int, int]]] = []
    for gif_name, position in SPACECRAFT:
        with Image.open(ASSETS / gif_name) as source:
            indices = sample_indices(source.n_frames)
            extracted: list[Image.Image] = []
            for output_index, source_index in enumerate(indices):
                source.seek(source_index)
                spacecraft_frame = source.convert("RGB")
                background_crop = frames[output_index].crop(
                    (
                        position[0],
                        position[1],
                        position[0] + spacecraft_frame.width,
                        position[1] + spacecraft_frame.height,
                    )
                ).convert("RGB")
                difference = ImageChops.difference(spacecraft_frame, background_crop)
                mask = difference.convert("L").point(
                    lambda value: 0 if value < 9 else min(255, (value - 9) * 18)
                )
                mask = ImageEnhance.Contrast(mask).enhance(1.35)
                mask = mask.filter(ImageFilter.GaussianBlur(0.55))
                layer = spacecraft_frame.convert("RGBA")
                layer.putalpha(mask)
                extracted.append(layer)
            layers.append((extracted, position))
    return layers


def main() -> None:
    frames = background_frames()
    overlays = panel_overlays()
    spacecraft_layers = extract_spacecraft_layers(frames)

    composed: list[Image.Image] = []
    for frame_index, background in enumerate(frames):
        canvas = background.copy()
        for overlay, position in overlays:
            canvas.alpha_composite(overlay, position)
        for layers, position in spacecraft_layers:
            canvas.alpha_composite(layers[frame_index], position)
        composed.append(canvas.convert("RGB"))

    composed[0].save(POSTER, format="PNG", optimize=True)
    composed[0].save(
        OUTPUT,
        save_all=True,
        append_images=composed[1:],
        duration=FRAME_DURATION_MS,
        loop=0,
        quality=WEBP_QUALITY,
        method=4,
        minimize_size=True,
    )
    print(
        f"Saved {len(composed)}-frame seamless profile animation to {OUTPUT} "
        f"({WIDTH}x{HEIGHT}, {FRAME_DURATION_MS} ms/frame)"
    )


if __name__ == "__main__":
    main()
