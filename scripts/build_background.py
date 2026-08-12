from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SOURCE = ASSETS / "profile-background-source.gif"
MASTER = ASSETS / "profile-background.png"
SLICES = ASSETS / "background"
PROOF = ROOT / "tmp" / "background-motion-proof.webp"

MASTER_WIDTH = 1280
MASTER_HEIGHT = 1348
DARKEN_ALPHA = 58
TARGET_FRAME_DURATION_MS = 200
WEBP_QUALITY = 58

SLICE_BOXES = {
    "header": (0, 0, 1280, 250),
    "about": (0, 250, 640, 610),
    "tugep": (640, 250, 1280, 610),
    "imece": (0, 610, 640, 970),
    "toolkit": (640, 610, 1280, 970),
    "languages": (0, 970, 640, 1230),
    "activity": (640, 970, 1280, 1230),
    "song": (0, 1230, 640, 1348),
    "quote": (640, 1230, 1280, 1348),
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


def darken(frame: Image.Image) -> Image.Image:
    shade = Image.new("RGBA", frame.size, (0, 0, 0, DARKEN_ALPHA))
    return Image.alpha_composite(frame.convert("RGBA"), shade).convert("RGB")


def source_frames() -> tuple[list[Image.Image], int]:
    source = Image.open(SOURCE)
    source_count = getattr(source, "n_frames", 1)
    if source_count < 2:
        raise RuntimeError(
            f"{SOURCE.name} contains only one frame; upload the original GIF inside a ZIP"
        )

    durations: list[int] = []
    decoded: list[Image.Image] = []
    for index in range(source_count):
        source.seek(index)
        durations.append(max(20, int(source.info.get("duration", 70))))
        decoded.append(source.convert("RGBA").copy())

    total_duration = sum(durations)
    target_count = max(2, round(total_duration / TARGET_FRAME_DURATION_MS))
    cumulative: list[int] = []
    elapsed = 0
    for duration in durations:
        elapsed += duration
        cumulative.append(elapsed)

    sampled: list[Image.Image] = []
    source_index = 0
    for target_index in range(target_count):
        target_time = target_index * total_duration / target_count
        while source_index < source_count - 1 and cumulative[source_index] <= target_time:
            source_index += 1
        sampled.append(decoded[source_index])
    return sampled, round(total_duration / target_count)


def master_frames() -> tuple[list[Image.Image], int]:
    frames, duration = source_frames()
    return [darken(cover(frame, MASTER_WIDTH, MASTER_HEIGHT)) for frame in frames], duration


def save_webp(frames: list[Image.Image], path: Path, duration_ms: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        quality=WEBP_QUALITY,
        method=6,
        minimize_size=True,
    )


def main() -> None:
    frames, duration_ms = master_frames()
    MASTER.parent.mkdir(parents=True, exist_ok=True)
    SLICES.mkdir(parents=True, exist_ok=True)
    frames[0].save(MASTER, format="PNG", optimize=True)

    for name, box in SLICE_BOXES.items():
        sliced_frames = [frame.crop(box) for frame in frames]
        sliced_frames[0].save(SLICES / f"{name}.png", format="PNG", optimize=True)
        save_webp(sliced_frames, SLICES / f"{name}.webp", duration_ms)

    proof_frames = [
        frame.resize((640, 674), Image.Resampling.LANCZOS) for frame in frames
    ]
    save_webp(proof_frames, PROOF, duration_ms)

    print(f"Loaded {SOURCE.name}: {len(frames)} sampled animated frames")
    print(f"Saved {MASTER_WIDTH}x{MASTER_HEIGHT} first frame to {MASTER}")
    print(f"Saved {len(SLICE_BOXES)} synchronized animated WebP slices to {SLICES}")
    print(f"Saved original light-animation proof to {PROOF}")


if __name__ == "__main__":
    main()
