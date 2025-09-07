FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /scraping

COPY data_processing/scraping/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/

COPY data_processing/scraping/ .

CMD ["python", "Jumbo/run_all.py"]
