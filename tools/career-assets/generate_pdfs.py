"""Create the two recruiter-facing RheinShield PDFs from verified local assets."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

ROOT = Path(__file__).resolve().parents[2]
CAREER_OUT = ROOT / "artifacts" / "career"
LINKEDIN_OUT = ROOT / "artifacts" / "linkedin"
CAREER_OUT.mkdir(parents=True, exist_ok=True)
LINKEDIN_OUT.mkdir(parents=True, exist_ok=True)

NAVY = HexColor("#10283a")
INK = HexColor("#0b1723")
PAPER = HexColor("#f2f5f2")
MINT = HexColor("#1e9d78")
BLUE = HexColor("#3979bf")
AMBER = HexColor("#c57b1e")
MUTED = HexColor("#60717a")
LINE = HexColor("#ccd9d3")

DEMO_URL = "https://omarbajamel.github.io/rheinshield-azure-cloud-security/"
REPO_URL = "https://github.com/OmarBajamel/rheinshield-azure-cloud-security"


def text(canvas: Canvas, value: str, x: float, y: float, size: float, color=INK, bold=False) -> None:
    canvas.setFillColor(color)
    canvas.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    canvas.drawString(x, y, value)


def rule(canvas: Canvas, x1: float, y: float, x2: float, color=MINT, width: float = 1.5) -> None:
    canvas.setStrokeColor(color)
    canvas.setLineWidth(width)
    canvas.line(x1, y, x2, y)


def create_cv_pdf(path: Path) -> None:
    width, height = A4
    canvas = Canvas(str(path), pagesize=A4, pageCompression=1)
    canvas.setTitle("RheinShield | Azure Cloud Security Project Reference")
    canvas.setAuthor("Omar Ba Jamel")
    canvas.setSubject("Recruiter-ready reference for the RheinShield Azure security portfolio")

    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 132, width, 132, fill=1, stroke=0)

    text(canvas, "RS", 40, height - 40, 13, MINT, True)
    text(canvas, "RheinShield", 70, height - 44, 21, white, True)
    text(canvas, "Azure security evidence, made inspectable.", 40, height - 82, 25, white, True)
    text(canvas, "Omar Ba Jamel  |  Azure Cloud Security Portfolio  |  v1.0.0", 40, height - 108, 10, HexColor("#bdd0c9"))

    y = height - 168
    text(canvas, "PROJECT SNAPSHOT", 40, y, 8.5, MINT, True)
    text(canvas, "NIS2-aligned secure Azure landing zone and security operations platform", 40, y - 24, 15, INK, True)
    text(canvas, "A reproducible portfolio case study joining governance, identity, detections, incident response,", 40, y - 45, 9.5, MUTED)
    text(canvas, "risk, cost controls, and audit-ready evidence across a fictional German marketplace.", 40, y - 59, 9.5, MUTED)

    metrics_y = y - 107
    metric_data = [
        ("5", "Terraform modules", MINT),
        ("14", "Sentinel rules", BLUE),
        ("27", "scored risks", AMBER),
        ("20", "mapped controls", NAVY),
    ]
    for index, (value, label, color) in enumerate(metric_data):
        x = 40 + index * 128
        canvas.setFillColor(white)
        canvas.roundRect(x, metrics_y - 45, 116, 62, 6, fill=1, stroke=0)
        text(canvas, value, x + 12, metrics_y - 8, 21, color, True)
        text(canvas, label, x + 12, metrics_y - 28, 8.5, MUTED)

    left_x, right_x = 40, 315
    section_y = metrics_y - 79
    rule(canvas, left_x, section_y, 285)
    rule(canvas, right_x, section_y, 555, BLUE)
    text(canvas, "WHAT I BUILT", left_x, section_y - 20, 10, NAVY, True)
    text(canvas, "HOW IT WAS VERIFIED", right_x, section_y - 20, 10, NAVY, True)

    built = [
        "Enterprise landing-zone reference + isolated lab",
        "Zero Trust identity, RBAC, CA, PIM, and JML",
        "Sentinel analytics, hunts, workbooks, and SOAR",
        "INC-001 investigation and response evidence",
        "NIS2/BSIG, ISO 27001, BSI, and MCSB mapping",
    ]
    verified = [
        "Terraform fmt/init/validate + native test",
        "14/14 malicious and 14/14 benign fixtures",
        "8 bilingual routes; desktop and mobile QA",
        "0 axe A/AA violations across 3 representative scans",
        "Public privacy and secret-pattern gates",
    ]
    for index, value in enumerate(built):
        yy = section_y - 43 - index * 22
        canvas.setFillColor(MINT)
        canvas.circle(left_x + 5, yy + 3, 1.7, fill=1, stroke=0)
        text(canvas, value, left_x + 15, yy, 8.6, INK)
    for index, value in enumerate(verified):
        yy = section_y - 43 - index * 22
        canvas.setFillColor(BLUE)
        canvas.circle(right_x + 5, yy + 3, 1.7, fill=1, stroke=0)
        text(canvas, value, right_x + 15, yy, 8.6, INK)

    impact_y = section_y - 177
    rule(canvas, 40, impact_y, 555, AMBER)
    text(canvas, "EVIDENCE-LED OUTCOMES", 40, impact_y - 20, 10, NAVY, True)
    outcomes = [
        ("738", ("synthetic events", "90 days; fixed seed")),
        ("6m / 9m / 48m", ("simulated INC-001", "exercise timings")),
        ("EUR 20", ("full-run ceiling", "live apply remains gated")),
    ]
    for index, (value, labels) in enumerate(outcomes):
        x = 40 + index * 172
        text(canvas, value, x, impact_y - 53, 15, (MINT, BLUE, AMBER)[index], True)
        text(canvas, labels[0], x, impact_y - 69, 7.8, MUTED)
        text(canvas, labels[1], x, impact_y - 80, 7.8, MUTED)

    note_y = impact_y - 111
    canvas.setFillColor(HexColor("#e0f2eb"))
    canvas.roundRect(40, note_y - 43, 515, 55, 7, fill=1, stroke=0)
    text(canvas, "TRUTHFULNESS BOUNDARY", 55, note_y - 9, 8.5, MINT, True)
    text(canvas, "Synthetic portfolio data. Plan/fixture validated. No customer or tenant data.", 55, note_y - 27, 8.8, INK)

    qr_path = ROOT / "assets" / "cv" / "rheinshield-project-reference-qr.png"
    canvas.drawImage(ImageReader(str(qr_path)), 454, 39, 88, 88, preserveAspectRatio=True, mask="auto")
    text(canvas, "LIVE DEMO", 40, 106, 8, MINT, True)
    text(canvas, "omarbajamel.github.io/rheinshield-azure-cloud-security", 40, 87, 10.5, NAVY, True)
    text(canvas, "SOURCE + EVIDENCE", 40, 61, 8, BLUE, True)
    text(canvas, "github.com/OmarBajamel/rheinshield-azure-cloud-security", 40, 43, 9.5, NAVY)
    canvas.linkURL(DEMO_URL, (40, 78, 405, 102), relative=0)
    canvas.linkURL(REPO_URL, (40, 34, 400, 58), relative=0)
    text(canvas, "Scan to inspect", 460, 29, 7.8, MUTED)

    canvas.showPage()
    canvas.save()


def create_carousel_pdf(path: Path) -> None:
    page_size = (1080, 1350)
    canvas = Canvas(str(path), pagesize=page_size, pageCompression=1)
    canvas.setTitle("RheinShield | LinkedIn Carousel")
    canvas.setAuthor("Omar Ba Jamel")
    for slide in sorted((ROOT / "assets" / "linkedin" / "carousel").glob("*.png")):
        canvas.drawImage(ImageReader(str(slide)), 0, 0, width=1080, height=1350, mask="auto")
        canvas.showPage()
    canvas.save()


if __name__ == "__main__":
    create_cv_pdf(CAREER_OUT / "rheinshield-cv-one-pager.pdf")
    create_carousel_pdf(LINKEDIN_OUT / "rheinshield-linkedin-carousel.pdf")
    print("created 1-page CV PDF and 5-page LinkedIn carousel PDF")
