FROM python:3.12.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 RHEINSHIELD_MODE=lab-live
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY pyproject.toml /app/pyproject.toml
RUN pip install --no-cache-dir "fastapi>=0.116,<1" "pydantic>=2.11,<3" "uvicorn>=0.35,<1"
COPY apps/secure-workload/app /app/rheinshield
USER 10001
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]
CMD ["uvicorn", "rheinshield.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
