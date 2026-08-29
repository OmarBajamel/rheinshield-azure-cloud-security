"""Generate recruiter media from verified RheinShield dashboard and diagram assets."""

from __future__ import annotations

from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "linkedin"
CAROUSEL = OUT / "carousel"
CV = ROOT / "assets" / "cv"
OUT.mkdir(parents=True, exist_ok=True)
CAROUSEL.mkdir(parents=True, exist_ok=True)
CV.mkdir(parents=True, exist_ok=True)
NAVY, INK, PAPER, WHITE, MINT, BLUE, AMBER, MUTED = (
    "#10283a",
    "#0b1723",
    "#f2f5f2",
    "#ffffff",
    "#1e9d78",
    "#3979bf",
    "#c57b1e",
    "#60717a",
)


def font(size: int, bold: bool = False):
    return ImageFont.truetype(f"C:/Windows/Fonts/{'segoeuib.ttf' if bold else 'segoeui.ttf'}", size)


def crop_cover(image: Image.Image, size: tuple[int, int], top: float = 0.0) -> Image.Image:
    ratio = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize(
        (round(image.width * ratio), round(image.height * ratio)), Image.Resampling.LANCZOS
    )
    left = (resized.width - size[0]) // 2
    upper = min(round((resized.height - size[1]) * top), resized.height - size[1])
    return resized.crop((left, upper, left + size[0], upper + size[1]))


def wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    width: int,
    size: int,
    fill: str,
    bold: bool = False,
    spacing: int = 10,
) -> int:
    words, lines, line = text.split(), [], ""
    face = font(size, bold)
    for word in words:
        proposed = f"{line} {word}".strip()
        if draw.textbbox((0, 0), proposed, font=face)[2] <= width:
            line = proposed
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    y = xy[1]
    for value in lines:
        draw.text((xy[0], y), value, font=face, fill=fill)
        y += size + spacing
    return y


dashboard = Image.open(
    ROOT / "assets/screenshots/01-executive-security-overview-desktop.png"
).convert("RGB")
soc = Image.open(ROOT / "assets/screenshots/03-soc-detection-coverage-desktop.png").convert("RGB")
incident = Image.open(ROOT / "assets/screenshots/04-incident-investigation-desktop.png").convert(
    "RGB"
)
architecture = Image.open(ROOT / "assets/architecture/01-enterprise-landing-zone.png").convert(
    "RGB"
)

# Landscape normal post: actual dashboard evidence is the dominant visual.
hero = Image.new("RGB", (1200, 627), NAVY)
hero.paste(crop_cover(dashboard, (690, 627), 0.15), (510, 0))
d = ImageDraw.Draw(hero)
d.rectangle((510, 0, 570, 627), fill=NAVY)
d.polygon([(510, 0), (660, 0), (510, 627)], fill=NAVY)
d.text((62, 50), "RS", font=font(24, True), fill=MINT)
d.text((115, 44), "RheinShield", font=font(30, True), fill=WHITE)
d.text((62, 132), "Azure security evidence,", font=font(44, True), fill=WHITE)
d.text((62, 185), "made inspectable.", font=font(44, True), fill=MINT)
d.text((62, 275), "LANDING ZONE  ·  ZERO TRUST", font=font(16, True), fill="#b7cbc4")
d.text((62, 308), "SENTINEL  ·  NIS2 / ISO / BSI", font=font(16, True), fill="#b7cbc4")
for i, (value, label) in enumerate(
    [("5", "Terraform modules"), ("14", "KQL detections"), ("27", "risks")]
):
    x = 62 + i * 145
    d.text((x, 400), value, font=font(34, True), fill=WHITE)
    wrapped(d, label, (x, 446), 125, 13, "#b7cbc4")
d.rounded_rectangle((62, 526, 454, 566), radius=20, fill="#173b42")
d.text((83, 536), "SYNTHETIC PORTFOLIO DATA", font=font(14, True), fill="#93e2c7")
d.text((62, 588), "Omar Ba Jamel · public case study", font=font(14), fill="#b7cbc4")
hero.save(OUT / "rheinshield-1200x627.png", optimize=True)

# Portrait normal post.
portrait = Image.new("RGB", (1080, 1350), PAPER)
dp = ImageDraw.Draw(portrait)
dp.rectangle((0, 0, 1080, 350), fill=NAVY)
dp.text((70, 58), "RHEINSHIELD", font=font(24, True), fill=MINT)
wrapped(dp, "Azure security evidence, made inspectable.", (70, 112), 880, 54, WHITE, True, 8)
dp.text((70, 280), "Omar Ba Jamel · Azure Cloud Security Portfolio", font=font(20), fill="#bdd0c9")
dash_crop = crop_cover(dashboard, (940, 520), 0.12)
portrait.paste(dash_crop, (70, 405))
dp.rounded_rectangle((70, 405, 1010, 925), radius=10, outline="#c8d5cf", width=3)
metrics = [
    ("5", "Terraform\nmodules"),
    ("14", "KQL\ndetections"),
    ("5", "hunting\nqueries"),
    ("27", "scored\nrisks"),
]
for i, (value, label) in enumerate(metrics):
    x = 70 + i * 235
    dp.rounded_rectangle((x, 975, x + 210, 1160), radius=14, fill=WHITE, outline="#cedbd5")
    dp.text((x + 24, 997), value, font=font(42, True), fill=MINT if i != 3 else AMBER)
    yy = 1060
    for line in label.splitlines():
        dp.text((x + 24, yy), line, font=font(18, True), fill=INK)
        yy += 26
dp.rounded_rectangle((70, 1200, 1010, 1260), radius=28, fill="#e0f2eb")
dp.text(
    (105, 1218),
    "SYNTHETIC DATA · PLAN / FIXTURE VALIDATED · NO TENANT DATA",
    font=font(17, True),
    fill="#176b53",
)
portrait.save(OUT / "rheinshield-1080x1350.png", optimize=True)


def slide_base(number: str, title: str, subtitle: str):
    image = Image.new("RGB", (1080, 1350), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1080, 180), fill=NAVY)
    draw.text((68, 46), "RS", font=font(22, True), fill=MINT)
    draw.text((122, 40), "RheinShield", font=font(28, True), fill=WHITE)
    draw.text((930, 48), number, font=font(22, True), fill="#b7cbc4")
    draw.text((68, 230), title, font=font(47, True), fill=INK)
    wrapped(draw, subtitle, (68, 300), 930, 22, MUTED)
    draw.text(
        (68, 1300), "Omar Ba Jamel · synthetic portfolio case study", font=font(16), fill=MUTED
    )
    return image, draw


s1, d1 = slide_base(
    "01 / 05",
    "Azure security, connected.",
    "From business risk to inspectable architecture, detections, response, and evidence.",
)
d1.text((68, 430), "RheinShield", font=font(82, True), fill=NAVY)
d1.text((68, 530), "LANDING ZONE", font=font(23, True), fill=BLUE)
d1.text((68, 570), "ZERO TRUST", font=font(23, True), fill=MINT)
d1.text((68, 610), "SENTINEL + KQL", font=font(23, True), fill=AMBER)
d1.text((68, 650), "NIS2 · ISO · BSI · MCSB", font=font(23, True), fill=NAVY)
s1.paste(crop_cover(dashboard, (944, 440), 0.13), (68, 775))
s1.save(CAROUSEL / "01-cover.png", optimize=True)

s2, d2 = slide_base(
    "02 / 05",
    "Two architectures. One boundary.",
    "A production-oriented reference stays separate from a disposable portfolio lab.",
)
s2.paste(crop_cover(architecture, (944, 535), 0.05), (68, 410))
for i, (value, label, color) in enumerate(
    [
        ("5", "Terraform modules", MINT),
        ("14", "policy controls", BLUE),
        ("€20", "hard cost ceiling", AMBER),
    ]
):
    x = 68 + i * 315
    d2.rounded_rectangle((x, 1000, x + 285, 1170), radius=12, fill=WHITE, outline="#ccd9d3")
    d2.text((x + 22, 1022), value, font=font(38, True), fill=color)
    d2.text((x + 22, 1085), label, font=font(18, True), fill=INK)
d2.text((68, 1215), "PLAN_VALIDATED · LIVE APPLY COST-GATED", font=font(17, True), fill=MUTED)
s2.save(CAROUSEL / "02-secure-landing-zone.png", optimize=True)

s3, d3 = slide_base(
    "03 / 05",
    "Sentinel detection as code",
    "Deterministic fixtures make logic reviewable while keeping production claims honest.",
)
s3.paste(crop_cover(soc, (944, 560), 0.22), (68, 405))
for i, (value, label) in enumerate(
    [
        ("14/14", "malicious trigger"),
        ("14/14", "benign stay quiet"),
        ("3 + 3", "automation + playbooks"),
    ]
):
    x = 68 + i * 315
    d3.text((x, 1015), value, font=font(37, True), fill=MINT if i < 2 else AMBER)
    d3.text((x, 1075), label, font=font(17, True), fill=INK)
d3.text(
    (68, 1175),
    "5 hunts · 3 workbooks · MITRE mappings · safe dry-run SOAR",
    font=font(19, True),
    fill=NAVY,
)
d3.text((68, 1220), "Fixture behavior ≠ production efficacy", font=font(17), fill=MUTED)
s3.save(CAROUSEL / "03-sentinel-detection-as-code.png", optimize=True)

s4, d4 = slide_base(
    "04 / 05",
    "Incident decisions become evidence",
    "INC-001 links detections, analyst actions, containment, recovery, risks, and controls.",
)
s4.paste(crop_cover(incident, (944, 540), 0.12), (68, 410))
for i, (value, label, color) in enumerate(
    [("6m", "MTTD", MINT), ("9m", "MTTA", BLUE), ("48m", "MTTR", AMBER), ("27", "risks", NAVY)]
):
    x = 68 + i * 235
    d4.text((x, 1005), value, font=font(39, True), fill=color)
    d4.text((x, 1062), label, font=font(16, True), fill=MUTED)
d4.text(
    (68, 1150),
    "20 evidence controls · NIS2/BSIG · ISO 27001 · BSI · MCSB",
    font=font(19, True),
    fill=INK,
)
d4.text(
    (68, 1200),
    "Exercise metrics only · no compliance or certification claim",
    font=font(17),
    fill=MUTED,
)
s4.save(CAROUSEL / "04-incident-and-compliance.png", optimize=True)

s5, d5 = slide_base(
    "05 / 05",
    "Reproduce the evidence",
    "The default public mode runs without Azure credentials and exposes no private tenant data.",
)
items = [
    ("Terraform", "format · validate · native test"),
    ("Sentinel", "28/28 fixture expectations"),
    ("Dashboard", "8 routes · EN/DE · mobile"),
    ("Accessibility", "0 axe A/AA violations · 3 representative scans"),
    ("Privacy", "pattern + screenshot review PASS"),
]
for i, (label, value) in enumerate(items):
    y = 420 + i * 118
    d5.ellipse((75, y + 5, 101, y + 31), fill=MINT)
    d5.line((82, y + 18, 87, y + 23, 95, y + 13), fill=WHITE, width=3, joint="curve")
    d5.text((130, y), label, font=font(24, True), fill=INK)
    d5.text((355, y + 3), value, font=font(20), fill=MUTED)
d5.rounded_rectangle((68, 1035, 1012, 1195), radius=16, fill=NAVY)
d5.text((100, 1068), "LIVE DEMO", font=font(15, True), fill=MINT)
d5.text(
    (100, 1100),
    "omarbajamel.github.io/rheinshield-azure-cloud-security",
    font=font(22, True),
    fill=WHITE,
)
d5.text(
    (100, 1144),
    "github.com/OmarBajamel/rheinshield-azure-cloud-security",
    font=font(18),
    fill="#c2d4ce",
)
s5.save(CAROUSEL / "05-results-and-links.png", optimize=True)

qr = qrcode.QRCode(
    version=None, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=12, border=4
)
qr.add_data("https://omarbajamel.github.io/rheinshield-azure-cloud-security/")
qr.make(fit=True)
qr.make_image(fill_color=NAVY, back_color=WHITE).convert("RGB").save(
    CV / "rheinshield-project-reference-qr.png", optimize=True
)

# Optimize the one requested image-generation asset for social metadata.
og_path = ROOT / "public" / "og.png"
if og_path.exists():
    crop_cover(Image.open(og_path).convert("RGB"), (1200, 630), 0.35).save(og_path, optimize=True)

print("generated 2 LinkedIn images, 5 carousel slides, QR code, and optimized OG image")
