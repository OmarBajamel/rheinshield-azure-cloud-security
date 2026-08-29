"""Generate deterministic RheinShield architecture diagrams as public PNG assets."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "architecture"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1600, 900
NAVY, INK, PAPER, WHITE, MINT, BLUE, AMBER, LINE, MUTED = "#10283a", "#0b1723", "#f2f5f2", "#ffffff", "#1e9d78", "#3979bf", "#c57b1e", "#cfdad5", "#60717a"


def font(size: int, bold: bool = False):
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(str(Path("C:/Windows/Fonts") / name), size)


def canvas(title: str, subtitle: str):
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, W, 96), fill=NAVY)
    draw.text((68, 24), "RS", fill=WHITE, font=font(24, True))
    draw.text((125, 18), title, fill=WHITE, font=font(34, True))
    draw.text((126, 61), subtitle, fill="#b9cbc4", font=font(16))
    draw.text((68, 852), "RheinShield · public-demo architecture · synthetic portfolio case study", fill=MUTED, font=font(15))
    draw.text((1450, 852), "v1.0.0", fill=MUTED, font=font(15))
    return image, draw


def box(draw, xy, title, lines=(), accent=MINT, fill=WHITE):
    draw.rounded_rectangle(xy, radius=12, fill=fill, outline=LINE, width=2)
    x1, y1, x2, _ = xy
    draw.rectangle((x1, y1, x1 + 7, xy[3]), fill=accent)
    draw.text((x1 + 28, y1 + 22), title, fill=INK, font=font(23, True))
    for i, line in enumerate(lines):
        draw.text((x1 + 28, y1 + 63 + i * 30), line, fill=MUTED, font=font(16))


def arrow(draw, start, end, label=""):
    draw.line((*start, *end), fill=MINT, width=4)
    x, y = end
    draw.polygon([(x, y), (x - 13, y - 8), (x - 13, y + 8)], fill=MINT)
    if label:
        cx, cy = (start[0] + end[0]) // 2, (start[1] + end[1]) // 2
        draw.text((cx - 45, cy - 25), label, fill=MUTED, font=font(14))


img, d = canvas("Enterprise landing zone", "Plan-validated target · Tenant Root Group remains untouched")
box(d, (80, 150, 1520, 245), "RheinShield reference root", ["Dedicated hierarchy below the tenant root · centralized policy and platform ownership"], NAVY)
for i, (title, lines, accent) in enumerate([
    ("Platform", ["Management", "Connectivity", "Identity"], BLUE),
    ("Landing Zones", ["Corp", "Online", "Sandbox"], MINT),
    ("Lifecycle", ["Subscription vending", "Decommissioned", "Cost management"], AMBER),
]): box(d, (80 + i*505, 300, 535 + i*505, 515), title, lines, accent)
for i, (title, lines) in enumerate([("Development", ["Delegated workload teams"]),("Test", ["Production-like controls"]),("Production", ["Approval + resilience"]) ]): box(d, (120+i*500, 590, 490+i*500, 760), title, lines, MINT)
arrow(d,(800,245),(800,292)); arrow(d,(800,515),(800,580))
img.save(OUT / "01-enterprise-landing-zone.png", optimize=True)

img, d = canvas("Deployable single-subscription lab", "Cost-gated project scope · READY_NOT_AUTHENTICATED")
box(d,(80,155,420,330),"Resource group",["rg-rheinshield-*","Mandatory expiry tags","24-hour target lifetime"],AMBER)
box(d,(535,155,900,330),"Network",["Application subnet","Private endpoints","No admin ports from Internet"],BLUE)
box(d,(1015,155,1520,330),"Workload",["Managed identity","Key Vault RBAC","Structured logs + health probes"],MINT)
box(d,(220,470,680,690),"Security controls",["14-policy baseline","Diagnostics and monitoring","Defender capability status"],BLUE)
box(d,(890,470,1380,690),"Security operations",["Log Analytics + Sentinel path","14 detections · 5 hunts","3 workbooks · 3+3 SOAR"],MINT)
arrow(d,(420,242),(525,242)); arrow(d,(900,242),(1005,242)); arrow(d,(1180,330),(1160,460)); arrow(d,(535,580),(690,580),"evidence"); arrow(d,(680,580),(880,580))
img.save(OUT / "02-deployable-lab.png", optimize=True)

img, d = canvas("Trust boundaries", "Identity, network, CI/CD, telemetry, and evidence boundaries")
box(d,(75,160,365,350),"Public user",["Untrusted requests","No tenant context"],AMBER)
box(d,(460,160,770,350),"Application",["Validated API input","Managed identity"],MINT)
box(d,(865,160,1160,350),"Azure services",["Key Vault / Storage","Private access design"],BLUE)
box(d,(1255,160,1525,350),"Data",["Confidential target","Synthetic public mode"],NAVY)
arrow(d,(365,255),(450,255)); arrow(d,(770,255),(855,255)); arrow(d,(1160,255),(1245,255))
box(d,(75,505,510,720),"GitHub CI boundary",["Untrusted PR: no Azure token","Protected environment: OIDC only","Project resource-group scope"],BLUE)
box(d,(595,505,1025,720),"Security operations",["Separate analysts and operators","Dry-run containment by default","Audit trail for decisions"],MINT)
box(d,(1110,505,1525,720),"Evidence boundary",["Raw private evidence ignored","Automated redaction + hashes","Public/Synthetic release"],AMBER)
arrow(d,(510,612),(585,612)); arrow(d,(1025,612),(1100,612))
img.save(OUT / "03-trust-boundaries.png", optimize=True)

img, d = canvas("Microsoft Sentinel data flow", "Content as code · deterministic offline validation · live path clearly separated")
for x, title, lines, accent in [
    (65,"Sources",["Entra sign-in / audit","Azure Activity","Workload diagnostics"],BLUE),
    (385,"Collection",["Diagnostic settings","Log Analytics","Schema contracts"],MINT),
    (705,"Detection",["14 analytics rules","5 hunting queries","MITRE + entities"],AMBER),
    (1025,"Response",["3 automation rules","3 disabled playbooks","Human approval"],MINT),
    (1345,"Evidence",["Fixtures + results","Incident INC-001","Public dashboard"],NAVY),
]: box(d,(x,250,x+250,600),title,lines,accent)
for x in [315,635,955,1275]: arrow(d,(x,425),(x+60,425))
d.text((110,700),"OFFLINE/PUBLIC: generator → fixtures → validation → sanitized dashboard",fill=INK,font=font(20,True))
d.text((110,745),"LIVE/OPTIONAL: minimal synthetic ingestion → KQL canary → private raw evidence → sanitizer",fill=MUTED,font=font(18))
img.save(OUT / "04-sentinel-data-flow.png", optimize=True)

img, d = canvas("Control and evidence flow", "Traceable claims from business risk to public release")
steps=[("Business context",["Services · assets · BIA"]),("Risk",["27 scored risks"]),("Controls",["20 evidence controls"]),("Implementation",["IaC · identity · KQL"]),("Validation",["Tests · scans · review"]),("Evidence",["Hash · provenance · mode"])]
for i,(title,lines) in enumerate(steps):
    x=45+i*258; box(d,(x,255,x+215,520),title,lines,[NAVY,AMBER,BLUE,MINT,BLUE,MINT][i])
    if i<5: arrow(d,(x+215,388),(x+248,388))
box(d,(285,625,1315,755),"Public claim gate",["No unsupported live status · no certification claim · no PII or secret · exact evidence path"],AMBER)
for x in [150,410,670,930,1190,1450]: d.line((x,520,x,615),fill=LINE,width=2)
img.save(OUT / "05-control-evidence-flow.png", optimize=True)

print(f"generated 5 architecture diagrams in {OUT}")
