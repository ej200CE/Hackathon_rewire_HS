FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1


WORKDIR /ETL

COPY data_processing/ETL/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY data_processing/ETL/ .

COPY shared/ shared/

CMD ["python", "Jumbo/html_parser.py"]





