FROM python:3.10.8-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONPATH="/opt/app:$PYTHONPATH"

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

WORKDIR /opt/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./docker/entrypoint.sh ./docker/wait_for_services.py /opt/
RUN chmod +x /opt/entrypoint.sh

RUN playwright install --with-deps chromium

WORKDIR /opt/app
COPY ./app .

ENTRYPOINT ["/opt/entrypoint.sh"]
CMD ["python", "main.py"]