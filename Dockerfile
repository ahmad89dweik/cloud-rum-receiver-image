FROM public.ecr.aws/docker/library/python:3.14.7-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY app ./app

RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8080

ENTRYPOINT ["python", "-m", "app"]
