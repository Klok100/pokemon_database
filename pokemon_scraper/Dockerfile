# syntax=docker/dockerfile:1
FROM python:3.12-slim

# System deps for Selenium + Firefox
RUN apt-get update && apt-get install -y --no-install-recommends \
    firefox-esr \
    geckodriver \
    ca-certificates \
    fonts-liberation \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libasound2 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxshmfence1 \
    libxi6 \
    libxtst6 \
  && rm -rf /var/lib/apt/lists/*

# Headless Firefox without changing your script
ENV MOZ_HEADLESS=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script (and anything else you need)
COPY . .

# Run the scraper
CMD ["python", "pokemon_scraper.py"]
