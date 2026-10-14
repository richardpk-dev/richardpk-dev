"""Generate the SVG assets for the GitHub profile README, with subset Google Fonts embedded."""
import base64, re, sys, urllib.parse, urllib.request
from pathlib import Path

OUT = Path(sys.argv[1])
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36"

NAVY, NAVY2, GOLD, BLUE = "#0A1F3C", "#14375E", "#D4A84B", "#3D8BD4"
SLATE = "#6E7F94"

def font_face(family_q, family, weight, text):
    """Fetch a woff2 subset containing only `text` and return an @font-face rule with it inlined."""
    chars = "".join(sorted(set(text)))
    url = f"https://fonts.googleapis.com/css2?family={family_q}&text={urllib.parse.quote(chars)}"
    css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read().decode()
    src = re.search(r"url\((https://[^)]+)\)", css).group(1)
    data = urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": UA})).read()
    b64 = base64.b64encode(data).decode()
    return (f"@font-face{{font-family:'{family}';font-weight:{weight};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}")

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------- content ----------
NAME = "RICHARD PAUL K"
SUB = "Senior Program Manager  ·  5G RAN  ·  Transport & Datapath"
TAG = "25 YEARS IN TELECOM SOFTWARE  ·  BANGALORE, INDIA"

SECTIONS = [("01", "About"), ("02", "Focus Areas"), ("03", "Career"),
            ("04", "Toolbox"), ("05", "Credentials"), ("06", "Connect")]

# (company, role, start, end)
CAREER = [
    ("Tayana Mobility (BPL Innovision)", "Software Developer", 2000.92, 2004.0),
    ("Siemens Communication Software", "Software Developer", 2004.1, 2006.6),
    ("Alcatel-Lucent India", "Senior Technical Specialist", 2006.6, 2014.7),
    ("Nokia Networks", "Area Program Manager · Datapath SME", 2014.7, 2026.8),
]
def years(s, e):
    return f"{int(s)} – {'Present' if e > 2026 else int(e)}"

serif_text = NAME + "".join(t for _, t in SECTIONS) + "Career Timeline"
sans_text = SUB + "".join(c + r for c, r, _, _ in CAREER)
mono_text = TAG + "".join(n for n, _ in SECTIONS) + "".join(years(s, e) for *_, s, e in CAREER) + "0123456789"

FONTS = "".join([
    font_face("Source+Serif+4:opsz,wght@60,600", "SS4", 600, serif_text),
    font_face("Inter:wght@400;500", "Inter", 400, sans_text),
    font_face("Inter:wght@500", "Inter", 500, sans_text),
    font_face("IBM+Plex+Mono:wght@500", "Plex", 500, mono_text),
])
SERIF = "font-family:'SS4',Georgia,serif;font-weight:600"
SANS = "font-family:'Inter',Helvetica,Arial,sans-serif"
MONO = "font-family:'Plex',Menlo,monospace;font-weight:500"

# ---------- banner ----------
W, H = 1280, 320
arcs = "".join(
    f'<circle cx="1130" cy="160" r="{r}" fill="none" stroke="{GOLD}" stroke-opacity="{0.55 - i*0.08:.2f}" stroke-width="1.5"/>'
    for i, r in enumerate(range(40, 330, 48)))
dots = "".join(
    f'<circle cx="{x}" cy="{y}" r="1.2" fill="#FFFFFF" fill-opacity="0.07"/>'
    for x in range(20, 900, 28) for y in range(20, 320, 28))
banner = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs><style>{FONTS}</style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient>
<clipPath id="c"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>
<g clip-path="url(#c)">
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{dots}
{arcs}
<circle cx="1130" cy="160" r="7" fill="{GOLD}"/>
</g>
<text x="80" y="132" style="{MONO};font-size:15px;letter-spacing:3.5px" fill="{GOLD}">{esc(TAG)}</text>
<text x="78" y="200" style="{SERIF};font-size:68px;letter-spacing:1px" fill="#FFFFFF">{esc(NAME)}</text>
<rect x="80" y="222" width="88" height="3" fill="{GOLD}"/>
<text x="80" y="262" style="{SANS};font-weight:400;font-size:23px" fill="#C8D6E8">{esc(SUB)}</text>
</svg>'''
(OUT / "banner.svg").write_text(banner)

# ---------- section headers (transparent; colours readable on light and dark GitHub themes) ----------
for num, title in SECTIONS:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="54" viewBox="0 0 880 54">
<defs><style>{FONTS}</style></defs>
<text x="0" y="36" style="{MONO};font-size:15px;letter-spacing:2px" fill="{GOLD}">{num}</text>
<text x="38" y="37" style="{SERIF};font-size:27px" fill="{BLUE}">{esc(title)}</text>
<rect x="0" y="50" width="880" height="1.5" fill="{SLATE}" fill-opacity="0.45"/>
</svg>'''
    (OUT / f"section-{num}.svg").write_text(svg)

# ---------- career timeline (own background card so it works in both themes) ----------
TW, TH = 1000, 250
x0, x1, y0, y1 = 70, 930, 2000, 2027
X = lambda y: x0 + (y - y0) / (y1 - y0) * (x1 - x0)
BAR_Y = 118
shades = ["#2C5A8A", "#3D73A8", "#4F8CC6", GOLD]
parts = []
for yr in range(2000, 2027, 5):
    parts.append(f'<line x1="{X(yr):.1f}" y1="{BAR_Y-8}" x2="{X(yr):.1f}" y2="{BAR_Y+22}" stroke="#FFFFFF" stroke-opacity="0.12"/>')
for i, (co, role, s, e) in enumerate(CAREER):
    xa, xb = X(s), X(min(e, 2026.8))
    parts.append(f'<rect x="{xa+1.5:.1f}" y="{BAR_Y}" width="{xb-xa-3:.1f}" height="14" rx="7" fill="{shades[i]}"/>')
    cx = (xa + xb) / 2
    above = i % 2 == 1
    ty = BAR_Y - 62 if above else BAR_Y + 50
    stem_a, stem_b = (ty + 44, BAR_Y - 2) if above else (BAR_Y + 16, ty - 18)
    parts.append(f'<line x1="{cx:.1f}" y1="{stem_a}" x2="{cx:.1f}" y2="{stem_b}" stroke="{shades[i]}" stroke-width="1.5"/>')
    parts.append(f'<text x="{cx:.1f}" y="{ty}" text-anchor="middle" style="{MONO};font-size:12px;letter-spacing:1.5px" fill="{GOLD}">{years(s, e)}</text>')
    parts.append(f'<text x="{cx:.1f}" y="{ty+18}" text-anchor="middle" style="{SANS};font-weight:500;font-size:15px" fill="#FFFFFF">{esc(co)}</text>')
    parts.append(f'<text x="{cx:.1f}" y="{ty+35}" text-anchor="middle" style="{SANS};font-weight:400;font-size:13px" fill="#9FB3CC">{esc(role)}</text>')
timeline = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">
<defs><style>{FONTS}</style>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY2}"/></linearGradient></defs>
<rect width="{TW}" height="{TH}" rx="14" fill="url(#bg)"/>
<rect x="{x0}" y="{BAR_Y+5}" width="{x1-x0}" height="4" rx="2" fill="#FFFFFF" fill-opacity="0.08"/>
{"".join(parts)}
</svg>'''
(OUT / "career-timeline.svg").write_text(timeline)
print("ok", sorted(p.name for p in OUT.iterdir()))
