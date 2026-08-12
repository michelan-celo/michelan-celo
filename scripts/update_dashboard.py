from __future__ import annotations

import base64
import datetime as dt
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
MUSIC_DATA = ROOT / "data" / "music.json"
QUOTES_DATA = ROOT / "data" / "quotes.json"
README = ROOT / "README.md"
LOGIN = os.environ.get("GITHUB_LOGIN", "michelan-celo")

BACKGROUND = "#0d1117"
PANEL = "#0b111b"
BORDER = "#2387b8"
TEXT = "#e6edf3"
MUTED = "#8b949e"
BLUE = "#58a6ff"
CYAN = "#4fdaf5"
GREEN = "#3fb950"

BACKGROUND_FILES = {
    "profile-header": "header.png",
    "about-card": "about.png",
    "toolkit-card": "toolkit.png",
    "languages-card": "languages.png",
    "activity-card": "activity.png",
    "song-1": "song.png",
    "quote-card": "quote.png",
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def background_data_uri(identifier: str) -> str:
    path = BACKGROUND_SLICES / BACKGROUND_FILES[identifier]
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def svg_document(width: int, height: int, body: str, identifier: str) -> str:
    background = background_data_uri(identifier)
    shade_opacity = "0.34" if identifier == "profile-header" else "0.48"
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
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="20" fill="#02060b" fill-opacity="{shade_opacity}" stroke="{BORDER}" stroke-opacity="0.24"/>
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
  <rect x="38" y="35" width="682" height="180" rx="18" fill="#02060b" fill-opacity="0.46" stroke="#4fdaf5" stroke-opacity="0.18"/>
  <text x="64" y="82" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="15" font-weight="700" letter-spacing="3">ORBITAL RESEARCH CONSOLE</text>
  <text x="62" y="145" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="48" font-weight="750" letter-spacing="1.2">CELAL GÜNDÜZ</text>
  <text x="64" y="186" fill="{CYAN}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="18" font-weight="650" letter-spacing="2.4">SPACE ENGINEER · RESEARCHER</text>
  <path d="M790 189 H1190" stroke="{CYAN}" stroke-opacity="0.32" stroke-dasharray="5 8"/>
  <text x="1190" y="178" text-anchor="end" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="10" letter-spacing="1.4">EARTH ORBIT / SYSTEMS NOMINAL</text>
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
  <rect x="{x}" y="{y}" width="{width}" height="34" rx="17" fill="#07111d" fill-opacity="0.82" stroke="{color}" stroke-opacity="0.5"/>
  <circle cx="{x + 17}" cy="{y + 17}" r="4" fill="{color}"/>
  <text x="{x + 30}" y="{y + 22}" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="{font_size}" font-weight="600">{esc(label)}</text>
'''


def write_about() -> None:
    body = f'''
  <text x="34" y="48" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="15" font-weight="700" letter-spacing="1.8">ABOUT / CURRENT ORBIT</text>
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
  <path d="M34 319 H606" stroke="#2387b8" stroke-opacity="0.25"/>
  <text x="34" y="341" fill="{CYAN}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="11" font-weight="650" letter-spacing="1">OPEN TO CONNECT · EXCHANGE IDEAS · COLLABORATE ↗</text>
'''
    (ASSETS / "about-card.svg").write_text(
        svg_document(640, 360, body, "about-card"), encoding="utf-8"
    )


def toolkit_chip(x: int, y: int, width: int, label: str, index: str) -> str:
    return f'''
  <rect x="{x}" y="{y}" width="{width}" height="58" rx="12" fill="#07111b" fill-opacity="0.86" stroke="#526171" stroke-opacity="0.68"/>
  <rect x="{x}" y="{y}" width="4" height="58" rx="2" fill="{CYAN}" opacity="0.8"/>
  <text x="{x + 18}" y="{y + 22}" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9">SYS.{index}</text>
  <text x="{x + 18}" y="{y + 43}" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="14" font-weight="650">{esc(label)}</text>
'''


def write_toolkit() -> None:
    cards = (
        (34, 82, 174, "STK", "01"),
        (220, 82, 174, "GMAT", "02"),
        (406, 82, 200, "FreeFlyer", "03"),
        (34, 154, 174, "Orekit", "04"),
        (220, 154, 174, "SPENVIS", "05"),
        (406, 154, 200, "SolidWorks", "06"),
        (34, 226, 174, "CATIA", "07"),
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
  <rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="22" rx="11" fill="#161b22"/>
  <clipPath id="language-bar"><rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="22" rx="11"/></clipPath>
  <g clip-path="url(#language-bar)">{''.join(segments)}</g>
  {''.join(legend)}
'''
    (ASSETS / "languages-card.svg").write_text(
        svg_document(640, 260, body, "languages-card"), encoding="utf-8"
    )


def fetch_contributions() -> dict | None:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
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
    with urllib.request.urlopen(request, timeout=30) as response:
        result = json.load(response)
    if result.get("errors"):
        raise RuntimeError(result["errors"])
    return result["data"]["user"]["contributionsCollection"]["contributionCalendar"]


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


def cube(x: float, y: float, level: int) -> str:
    height = (0, 4, 8, 13, 19)[level]
    colors = (
        ("#161b22", "#0d1117", "#10151d"),
        ("#123f37", "#0b2d31", "#0d3432"),
        ("#1b6c4b", "#11513f", "#155d44"),
        ("#28a05f", "#197948", "#218b54"),
        ("#52d273", "#279e58", "#36b965"),
    )
    top, left, right = colors[level]
    top_y = y - height
    outline = "#30363d" if level == 0 else "#66e28a"
    return f'''
  <polygon points="{x},{top_y} {x + 8},{top_y - 4} {x + 16},{top_y} {x + 8},{top_y + 4}" fill="{top}" stroke="{outline}" stroke-opacity="0.48" stroke-width="0.7"/>
  <polygon points="{x},{top_y} {x + 8},{top_y + 4} {x + 8},{y + 4} {x},{y}" fill="{left}"/>
  <polygon points="{x + 8},{top_y + 4} {x + 16},{top_y} {x + 16},{y} {x + 8},{y + 4}" fill="{right}"/>
'''


def write_activity(calendar: dict | None) -> None:
    levels = {
        "NONE": 0,
        "FIRST_QUARTILE": 1,
        "SECOND_QUARTILE": 2,
        "THIRD_QUARTILE": 3,
        "FOURTH_QUARTILE": 4,
    }
    cells = []
    if calendar:
        weeks = calendar["weeks"][-26:]
        for week_index, week in enumerate(weeks):
            for day_index, day in enumerate(week["contributionDays"]):
                x = 31 + week_index * 20 + day_index * 7
                y = 205 - week_index * 4 + day_index * 7
                cells.append((y, cube(x, y, levels[day["contributionLevel"]])))
        total = calendar["totalContributions"]
        streak = contribution_streak(calendar)
        status = "PUBLIC ACTIVITY · LAST 26 WEEKS"
        total_text = str(total)
        streak_text = f"{streak}D"
    else:
        for week_index in range(26):
            for day_index in range(7):
                x = 31 + week_index * 20 + day_index * 7
                y = 205 - week_index * 4 + day_index * 7
                cells.append((y, cube(x, y, 0)))
        status = "SYNC PENDING · RUN WORKFLOW ONCE"
        total_text = "—"
        streak_text = "—"
    cells.sort(key=lambda item: item[0])
    body = f'''
  <text x="34" y="42" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="15" font-weight="700" letter-spacing="1.8">CONTRIBUTION TELEMETRY</text>
  <text x="34" y="64" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9" letter-spacing="0.8">{esc(status)}</text>
  <text x="474" y="38" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="8">TOTAL</text>
  <text x="474" y="59" fill="{TEXT}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="17" font-weight="700">{total_text}</text>
  <text x="555" y="38" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="8">STREAK</text>
  <text x="555" y="59" fill="{GREEN}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="17" font-weight="700">{streak_text}</text>
  <g>{''.join(cell for _, cell in cells)}</g>
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
  <circle cx="46" cy="59" r="24" fill="#101f2c" stroke="{CYAN}" stroke-opacity="0.52"/>
  <polygon points="41,48 41,70 59,59" fill="{CYAN}"/>
  <text x="84" y="35" fill="{MUTED}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="9" letter-spacing="1">RANDOM TRANSMISSION / 0{index}</text>
  <text x="84" y="61" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="16" font-weight="700">{esc(track['title'])}</text>
  <text x="84" y="84" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="11">{esc(track['artist'])}</text>
  {waveform(track['url'])}
'''
    return svg_document(640, 118, body, f"song-{index}")


def wrap_quote(value: str, max_characters: int = 66) -> list[str]:
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
    font_size = 14 if len(item["quote"]) <= 76 else 12
    line_height = 21 if font_size == 14 else 17
    start_y = {1: 62, 2: 48, 3: 34, 4: 25}.get(len(lines), 25)
    text_lines = "".join(
        f'<text x="76" y="{start_y + index * line_height}" fill="{TEXT}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="{font_size}" font-weight="600">{esc(line)}</text>'
        for index, line in enumerate(lines)
    )
    body = f'''
  <text x="34" y="45" fill="{CYAN}" font-family="Georgia,serif" font-size="46" opacity="0.86">“</text>
  {text_lines}
  <text x="606" y="103" text-anchor="end" fill="{BLUE}" font-family="Segoe UI,Ubuntu,sans-serif" font-size="10" font-weight="650" letter-spacing="1">— {esc(item['author'])}</text>
'''
    return svg_document(640, 118, body, "quote-card")


def daily_randomizer(namespace: str) -> random.Random:
    date_value = os.environ.get("MUSIC_DATE") or dt.datetime.now(dt.timezone.utc).date().isoformat()
    refresh_value = os.environ.get("REFRESH_NONCE", "scheduled")
    seed = int.from_bytes(
        hashlib.sha256(
            f"{LOGIN}:{date_value}:{refresh_value}:{namespace}".encode()
        ).digest()[:8]
    )
    return random.Random(seed)


def choose_music() -> dict:
    tracks = json.loads(MUSIC_DATA.read_text(encoding="utf-8"))
    return daily_randomizer("music").choice(tracks)


def choose_quote() -> dict:
    quotes = json.loads(QUOTES_DATA.read_text(encoding="utf-8"))
    return daily_randomizer("quote").choice(quotes)


def write_music_and_readme() -> None:
    track = choose_music()
    quote = choose_quote()
    (ASSETS / "song-1.svg").write_text(music_card(track, 1), encoding="utf-8")
    (ASSETS / "quote-card.svg").write_text(quote_card(quote), encoding="utf-8")
    replacement = f'''<!-- MUSIC_LINKS:START -->
<p align="center"><a href="{track['url']}"><img src="assets/song-1.svg" width="50%" alt="{esc(track['title'])} by {esc(track['artist'])}"></a><img src="assets/quote-card.svg" width="50%" alt="{esc(quote['quote'])} — {esc(quote['author'])}"></p>
<!-- MUSIC_LINKS:END -->'''
    readme = README.read_text(encoding="utf-8")
    pattern = re.compile(
        r"<!-- MUSIC_LINKS:START -->.*?<!-- MUSIC_LINKS:END -->", re.DOTALL
    )
    updated, count = pattern.subn(replacement, readme)
    if count != 1:
        raise RuntimeError("README music marker block is missing or duplicated")
    README.write_text(updated, encoding="utf-8")


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    write_header()
    write_about()
    write_toolkit()
    write_languages()
    try:
        calendar = fetch_contributions()
    except Exception as error:
        print(f"Contribution telemetry refresh skipped: {error}")
        calendar = None
    if calendar is not None or not (ASSETS / "activity-card.svg").exists():
        write_activity(calendar)
    write_music_and_readme()


if __name__ == "__main__":
    main()
