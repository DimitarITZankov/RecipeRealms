FROM python:3.11-slim
LABEL maintainer="DimitarITZankov"

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

# Install build-time dependencies for Pillow and PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY ./requirements.txt /tmp/requirements.txt

# Create virtual environment and install Python packages
ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf /tmp

# Optional: remove build dependencies to reduce image size
RUN apt-get purge -y gcc || true && \
    apt-get autoremove -y || true && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY ./application /application
WORKDIR /application

# Create user and media/static folders
RUN adduser --disabled-password --no-create-home django-user && \
    mkdir -p /vol/web/media /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chown -R django-user /application

EXPOSE 4000

USER django-user

# Default command
CMD ["/py/bin/python", "manage.py", "runserver", "0.0.0.0:4000"]
