from __future__ import annotations

import datetime as dt
import base64
import hashlib
import html
import json
import math
import os
import random
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
BACKGROUND_SLICES = ASSETS / "background"
TOOLKIT_ICONS = ASSETS / "toolkit-icons"
MUSIC_DATA = ROOT / "data" / "music.json"
QUOTES_DATA = ROOT / "data" / "quotes.json"
SELECTION_STATE = ROOT / "data" / "current-selection.json"
README = ROOT / "README.md"
PROFILE_ANIMATION = ASSETS / "profile-console.webp"
LOGIN = os.environ.get("GITHUB_LOGIN", "michelan-celo")

BACKGROUND = "#0d1117"
TEXT = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#58a6ff"
CYAN = "#4fdaf5"
GREEN = "#3fb950"

BACKGROUND_FILES = {
    "profile-header": "header.webp",
    "about-card": "about.webp",
    "toolkit-card": "toolkit.webp",
    "languages-card": "languages.webp",
    "activity-card": "activity.webp",
    "song-1": "song.webp",
    "quote-card": "quote.webp",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def background_data_uri(identifier: str) -> str:
    encoded = base64.b64encode(
        (BACKGROUND_SLICES / BACKGROUND_FILES[identifier]).read_bytes()
    ).decode("ascii")
    return f"data:image/webp;base64,{encoded}"


def png_data_uri(path: Path) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def svg_document(width: int, height: int, body: str, identifier: str) -> str:
    background = background_data_uri(identifier)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{identifier}-title {identifier}-desc">
  <title id="{identifier}-title">{esc(identifier.replace('-', ' ').title())}</title>
  <desc id="{identifier}-desc">Space mission themed GitHub profile panel</desc>
  <defs>
    <filter id="glow-{identifier}" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <image href="{background}" x="0" y="0" width="{width}" height="{height}" preserveAspectRatio="none"/>
  {body}
</svg>
'''


def star_field(width: int, height: int, seed: int, count: int) -> str:
    randomizer = random.Random(seed)
    stars = []
    for _ in range(count):
        x = randomizer.randrange(16, width - 16)
        y = randomizer.randrange(12, height - 12)
        radius = randomizer.choice((0.7, 0.8, 1.0, 1.2, 1.6))
        opacity = randomizer.uniform(0.18, 0.72)
        stars.append(
            f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#d8efff" opacity="{opacity:.2f}"/>'
        )
    return "".join(stars)


def write_header() -> None:
    width, height = 1280, 250
    body = f'''
  <text x="62" y="116" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="48" font-weight="750" letter-spacing="1.2">CELAL GÜNDÜZ</text>
  <text x="64" y="160" fill="{CYAN}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="18" font-weight="650" letter-spacing="2.4">SPACE ENGINEER · RESEARCHER</text>
  <text x="1190" y="160" text-anchor="end" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="10" letter-spacing="1.4">EARTH ORBIT / SYSTEMS NOMINAL</text>
'''
    (ASSETS / "profile-header.svg").write_text(
        svg_document(width, height, body, "profile-header"), encoding="utf-8"
    )


def chip(
    x: int,
    y: int,
    width: int,
    label: str,
    color: str = CYAN,
    font_size: int = 12,
) -> str:
    return f'''
  <circle cx="{x + 17}" cy="{y + 17}" r="4" fill="{color}"/>
  <text x="{x + 30}" y="{y + 22}" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="{font_size}" font-weight="600">{esc(label)}</text>
'''


def write_about() -> None:
    body = f'''
  <text x="34" y="48" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="15" font-weight="700" letter-spacing="1.8">ABOUT</text>
  <circle cx="36" cy="80" r="4" fill="{GREEN}" filter="url(#glow-about-card)"/>
  <text x="50" y="85" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="16" font-weight="650">Researcher at TÜBİTAK UZAY</text>
  <text x="34" y="122" fill="{MUTED}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14">An enthusiastic orbitalist with a background in</text>
  <text x="34" y="145" fill="{MUTED}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14">Astronautical Engineering and graduate studies in</text>
  <text x="34" y="168" fill="{MUTED}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14">Aerospace Engineering.</text>
  <text x="34" y="207" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="11" font-weight="700" letter-spacing="1.4">INTERESTS</text>
  {chip(34, 220, 132, 'ORBIT DESIGN', font_size=10)}
  {chip(176, 220, 164, 'MANEUVER PLANNING', font_size=10)}
  {chip(350, 220, 178, 'THREE-BODY DYNAMICS', font_size=9)}
  {chip(34, 264, 138, 'OPTIMIZATION', font_size=10)}
  {chip(182, 264, 178, 'CONSTELLATION ANALYSIS', font_size=9)}
  {chip(370, 264, 218, 'PROPAGATOR INFRASTRUCTURE', font_size=9)}
  <text x="34" y="341" fill="{CYAN}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="11" font-weight="650" letter-spacing="1">OPEN TO CONNECT · EXCHANGE IDEAS · COLLABORATE ↗</text>
'''
    (ASSETS / "about-card.svg").write_text(
        svg_document(640, 360, body, "about-card"), encoding="utf-8"
    )


def toolkit_chip(
    x: int,
    y: int,
    width: int,
    label: str,
    index: str,
    icon_name: str,
) -> str:
    icon = png_data_uri(TOOLKIT_ICONS / f"{icon_name}.png")
    return f'''
  <image href="{icon}" x="{x}" y="{y + 15}" width="34" height="34" preserveAspectRatio="xMidYMid meet"/>
  <text x="{x + 44}" y="{y + 22}" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9">SYS.{index}</text>
  <text x="{x + 44}" y="{y + 43}" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14" font-weight="650">{esc(label)}</text>
'''


def write_toolkit() -> None:
    cards = (
        (34, 82, 174, "STK", "01", "stk"),
        (220, 82, 174, "GMAT", "02", "gmat"),
        (406, 82, 200, "FreeFlyer", "03", "freeflyer"),
        (34, 154, 174, "Orekit", "04", "orekit"),
        (220, 154, 174, "SPENVIS", "05", "spenvis"),
        (406, 154, 200, "SolidWorks", "06", "solidworks"),
        (34, 226, 174, "CATIA", "07", "catia"),
    )
    body = f'''
  <text x="34" y="48" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="15" font-weight="700" letter-spacing="1.8">ENGINEERING TOOLKIT</text>
  <text x="606" y="48" text-anchor="end" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="10">MISSION STACK / 07</text>
  {''.join(toolkit_chip(*card) for card in cards)}
  <text x="34" y="327" fill="{MUTED}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="11" letter-spacing="1">MISSION DESIGN · SIMULATION · SPACE ENVIRONMENT · CAD</text>
'''
    (ASSETS / "toolkit-card.svg").write_text(
        svg_document(640, 360, body, "toolkit-card"), encoding="utf-8"
    )


def write_languages() -> None:
    bar_x, bar_y, bar_width = 38, 102, 564
    languages = (
        ("JAVA", 80, "#f0a34a"),
        ("MATLAB", 15, "#e66b35"),
        ("FORTRAN", 3, "#a371f7"),
        ("C", 2, "#58a6ff"),
    )
    segments = []
    cursor = bar_x
    for name, percentage, color in languages:
        width = bar_width * percentage / 100
        segments.append(
            f'<rect x="{cursor:.2f}" y="{bar_y}" width="{width:.2f}" height="22" fill="{color}"/>'
        )
        cursor += width
    legend = []
    positions = ((38, 164), (182, 164), (338, 164), (492, 164))
    for (name, percentage, color), (x, y) in zip(languages, positions):
        legend.append(f'''
  <circle cx="{x}" cy="{y}" r="5" fill="{color}"/>
  <text x="{x + 14}" y="{y + 5}" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="13" font-weight="650">{name}</text>
  <text x="{x + 14}" y="{y + 25}" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="11">{percentage}%</text>
''')
    body = f'''
  <text x="34" y="48" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="15" font-weight="700" letter-spacing="1.8">MOST-USED LANGUAGES</text>
  <text x="606" y="48" text-anchor="end" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="10">DECLARED DISTRIBUTION / 100%</text>
  <clipPath id="language-bar"><rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="22" rx="11"/></clipPath>
  <g clip-path="url(#language-bar)">{''.join(segments)}</g>
  {''.join(legend)}
'''
    (ASSETS / "languages-card.svg").write_text(
        svg_document(640, 260, body, "languages-card"), encoding="utf-8"
    )


def fetch_contributions() -> dict:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is required for contribution telemetry")
    query = '''
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            date
            contributionCount
            contributionLevel
          }
        }
      }
    }
  }
}
'''
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": LOGIN}}).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{LOGIN}-profile-dashboard",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except Exception as error:
        raise RuntimeError(f"GitHub contribution request failed: {error}") from error
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    user = result.get("data", {}).get("user")
    if not user:
        raise RuntimeError(f"GitHub user not found: {LOGIN}")
    calendar = user["contributionsCollection"]["contributionCalendar"]
    if not calendar.get("weeks"):
        raise RuntimeError("GitHub returned an empty contribution calendar")
    return calendar


def contribution_streak(calendar: dict) -> int:
    counts = {}
    for week in calendar["weeks"]:
        for day in week["contributionDays"]:
            counts[dt.date.fromisoformat(day["date"])] = day["contributionCount"]
    cursor = dt.datetime.now(dt.timezone.utc).date()
    if counts.get(cursor, 0) == 0:
        cursor -= dt.timedelta(days=1)
    streak = 0
    while counts.get(cursor, 0) > 0:
        streak += 1
        cursor -= dt.timedelta(days=1)
    return streak


def contribution_cell(
    x: float,
    y: float,
    level: int,
    count: int,
) -> str:
    # GitHub's familiar contribution palette, split into top/front/right faces
    # so each day reads as a small isometric block.  Empty days stay bright,
    # while activity rises from the board according to the real daily count.
    top_colors = ("#eef2f5", "#9be9a8", "#40c463", "#30a14e", "#216e39")
    front_colors = ("#b8c2cc", "#62b971", "#269342", "#1b7938", "#11562a")
    right_colors = ("#d1d9e0", "#7dce8a", "#31a64e", "#228b40", "#176532")
    outline_colors = ("#c8d0d8", "#76c982", "#2ba148", "#20833d", "#155f30")
    floor_height = 1.4
    tower_height = min(42.0, 6.0 + math.log2(max(count, 1) + 1) * 6.0)

    # Both vectors are shared by every cell.  The seven-day direction rises
    # up-right and the 53-week direction falls down-right, producing one
    # coherent isometric board like the reference contribution cityscape.
    week_face = (8.1, 2.0)
    day_face = (4.5, -3.6)
    base = (
        (x, y),
        (x + week_face[0], y + week_face[1]),
        (x + week_face[0] + day_face[0], y + week_face[1] + day_face[1]),
        (x + day_face[0], y + day_face[1]),
    )
    floor_top = tuple(
        (point_x, point_y - floor_height) for point_x, point_y in base
    )

    def points(values: tuple[tuple[float, float], ...]) -> str:
        return " ".join(f"{point_x:.2f},{point_y:.2f}" for point_x, point_y in values)

    tooltip = f"{count} contribution" + ("" if count == 1 else "s")
    floor = f'''
    <polygon points="{points((base[0], base[1], floor_top[1], floor_top[0]))}" fill="{front_colors[level]}"/>
    <polygon points="{points((base[1], base[2], floor_top[2], floor_top[1]))}" fill="{right_colors[level]}"/>
    <polygon points="{points(floor_top)}" fill="{top_colors[level]}" stroke="{outline_colors[level]}" stroke-width="0.55" stroke-linejoin="round"/>'''
    if not level:
        return f'''<g>
    <title>{tooltip}</title>
    {floor}
  </g>'''

    center_x = sum(point[0] for point in floor_top) / 4
    center_y = sum(point[1] for point in floor_top) / 4
    tower_base = tuple(
        (
            center_x + (point_x - center_x) * 0.72,
            center_y + (point_y - center_y) * 0.72,
        )
        for point_x, point_y in floor_top
    )
    tower_top = tuple(
        (point_x, point_y - tower_height) for point_x, point_y in tower_base
    )
    return f'''<g>
    <title>{tooltip}</title>
    {floor}
    <polygon points="{points((tower_base[0], tower_base[1], tower_top[1], tower_top[0]))}" fill="{front_colors[level]}"/>
    <polygon points="{points((tower_base[1], tower_base[2], tower_top[2], tower_top[1]))}" fill="{right_colors[level]}"/>
    <polygon points="{points(tower_top)}" fill="{top_colors[level]}" stroke="{outline_colors[level]}" stroke-width="0.55" stroke-linejoin="round"/>
  </g>'''


def write_activity(calendar: dict | None, preview_reason: str | None = None) -> None:
    levels = {
        "NONE": 0,
        "FIRST_QUARTILE": 1,
        "SECOND_QUARTILE": 2,
        "THIRD_QUARTILE": 3,
        "FOURTH_QUARTILE": 4,
    }
    cell_specs: list[tuple[float, float, int, int]] = []
    grid_x = 39.0
    grid_y = 112.0
    week_step = (9.45, 2.35)
    day_step = (5.1, -4.15)
    if calendar:
        weeks = calendar["weeks"]
        week_count = len(weeks)
        for week_index, week in enumerate(weeks):
            for day_index, day in enumerate(week["contributionDays"]):
                x = grid_x + week_index * week_step[0] + day_index * day_step[0]
                y = grid_y + week_index * week_step[1] + day_index * day_step[1]
                cell_specs.append(
                    (
                        x,
                        y,
                        levels[day["contributionLevel"]],
                        day["contributionCount"],
                    )
                )
        cell_total = sum(
            day["contributionCount"]
            for week in weeks
            for day in week["contributionDays"]
        )
        api_total = calendar["totalContributions"]
        if cell_total != api_total:
            raise RuntimeError(
                "GitHub contribution total does not match the rendered calendar "
                f"({api_total} != {cell_total})"
            )
        total = cell_total
        streak = contribution_streak(calendar)
        status = "LIVE GITHUB DATA · FULL CONTRIBUTION YEAR"
        total_text = str(total)
        streak_text = f"{streak}D"
    else:
        week_count = 53
        for week_index in range(week_count):
            for day_index in range(7):
                x = grid_x + week_index * week_step[0] + day_index * day_step[0]
                y = grid_y + week_index * week_step[1] + day_index * day_step[1]
                cell_specs.append((x, y, 0, 0))
        status = preview_reason or "PREVIEW ONLY · RUN WORKFLOW FOR LIVE DATA"
        total_text = "—"
        streak_text = "—"
    cells = [
        contribution_cell(x, y, level, count)
        for x, y, level, count in sorted(cell_specs, key=lambda item: (item[1], item[0]))
    ]
    body = f'''
  <text x="34" y="42" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="15" font-weight="700" letter-spacing="1.8">CONTRIBUTION TELEMETRY</text>
  <text x="34" y="64" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9" letter-spacing="0.8">{esc(status)}</text>
  <text x="474" y="38" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="8">TOTAL</text>
  <text x="474" y="59" fill="{TEXT}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="17" font-weight="700">{total_text}</text>
  <text x="555" y="38" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="8">STREAK</text>
  <text x="555" y="59" fill="{GREEN}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="17" font-weight="700">{streak_text}</text>
  <text x="34" y="128" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="8" letter-spacing="1">−52W</text>
  <text x="594" y="225" text-anchor="end" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="8" letter-spacing="1">NOW</text>
  <g>{''.join(cells)}</g>
'''
    (ASSETS / "activity-card.svg").write_text(
        svg_document(640, 260, body, "activity-card"), encoding="utf-8"
    )


def waveform(seed: str) -> str:
    digest = hashlib.sha256(seed.encode()).digest()
    bars = []
    for index in range(31):
        value = digest[index % len(digest)]
        height = 7 + value % 24
        x = 375 + index * 6
        y = 58 - height / 2
        bars.append(
            f'<rect x="{x}" y="{y:.1f}" width="2" height="{height}" rx="1" fill="{CYAN}" opacity="{0.34 + (value % 50) / 100:.2f}"/>'
        )
    return "".join(bars)


def music_card(track: dict, index: int) -> str:
    body = f'''
  <circle cx="46" cy="59" r="24" fill="#101f2c"/>
  <polygon points="41,48 41,70 59,59" fill="{CYAN}"/>
  <text x="84" y="35" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9" letter-spacing="1">RANDOM TRANSMISSION / 0{index}</text>
  <text x="84" y="61" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="16" font-weight="700">{esc(track['title'])}</text>
  <text x="84" y="84" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="11">{esc(track['artist'])}</text>
  {waveform(track['url'])}
'''
    return svg_document(640, 118, body, f"song-{index}")


def wrap_quote(value: str, max_characters: int = 62) -> list[str]:
    words = value.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        candidate = " ".join((*current, word))
        if current and len(candidate) > max_characters:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines[:4]


def quote_card(item: dict) -> str:
    lines = wrap_quote(item["quote"])
    font_size = 17 if len(lines) == 1 else 14 if len(lines) == 2 else 12
    line_height = 21 if len(lines) <= 2 else 17
    start_y = {1: 72, 2: 58, 3: 49, 4: 42}.get(len(lines), 42)
    text_lines = "".join(
        f'<text x="34" y="{start_y + index * line_height}" fill="{TEXT}" font-family="Georgia,Times New Roman,serif" font-size="{font_size}" font-style="italic" font-weight="500">{esc(line)}</text>'
        for index, line in enumerate(lines)
    )
    body = f'''
  <circle cx="37" cy="22" r="3" fill="{CYAN}"/>
  <text x="48" y="26" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9" letter-spacing="1.4">FIELD NOTE / RANDOM SIGNAL</text>
  <text x="606" y="26" text-anchor="end" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="10" font-weight="650" letter-spacing="1">{esc(item['author'].upper())}</text>
  {text_lines}
'''
    return svg_document(640, 118, body, "quote-card")


def refresh_randomizer(namespace: str) -> random.Random:
    refresh_value = os.environ.get("REFRESH_NONCE", "scheduled")
    seed = int.from_bytes(
        hashlib.sha256(
            f"{LOGIN}:{refresh_value}:{namespace}".encode()
        ).digest()[:8]
    )
    return random.Random(seed)


def load_selection_state() -> dict:
    if not SELECTION_STATE.exists():
        return {}
    try:
        value = json.loads(SELECTION_STATE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return value if isinstance(value, dict) else {}


def choose_music(exclude_url: str | None = None) -> dict:
    tracks = json.loads(MUSIC_DATA.read_text(encoding="utf-8"))
    candidates = [track for track in tracks if track["url"] != exclude_url]
    return refresh_randomizer("music").choice(candidates or tracks)


def quote_key(item: dict) -> str:
    return hashlib.sha256(
        f"{item['author']}\n{item['quote']}".encode("utf-8")
    ).hexdigest()


def choose_quote(exclude_key: str | None = None) -> dict:
    quotes = json.loads(QUOTES_DATA.read_text(encoding="utf-8"))
    candidates = [item for item in quotes if quote_key(item) != exclude_key]
    return refresh_randomizer("quote").choice(candidates or quotes)


def write_music_and_quote() -> None:
    state = load_selection_state()
    track = choose_music(state.get("music_url"))
    quote = choose_quote(state.get("quote_key"))
    (ASSETS / "song-1.svg").write_text(music_card(track, 1), encoding="utf-8")
    (ASSETS / "quote-card.svg").write_text(quote_card(quote), encoding="utf-8")
    SELECTION_STATE.write_text(
        json.dumps(
            {"music_url": track["url"], "quote_key": quote_key(quote)},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def build_profile_animation() -> None:
    from build_profile_animation import main as build_animation

    build_animation()
    if not PROFILE_ANIMATION.exists() or PROFILE_ANIMATION.stat().st_size == 0:
        raise RuntimeError("Profile animation was not generated")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    write_header()
    write_about()
    write_toolkit()
    write_languages()
    if os.environ.get("ALLOW_PREVIEW_DATA") == "1":
        try:
            calendar = fetch_contributions()
        except Exception as error:
            print(f"Preview mode: contribution telemetry unavailable: {error}")
            calendar = None
            preview_reason = "PREVIEW ONLY · TOKEN IS PROVIDED BY GITHUB ACTIONS"
        else:
            preview_reason = None
    else:
        calendar = fetch_contributions()
        preview_reason = None
    write_activity(calendar, preview_reason)
    write_music_and_quote()
    build_profile_animation()


if __name__ == "__main__":
    main()
