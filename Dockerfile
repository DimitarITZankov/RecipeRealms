FROM python:3.11-slim
LABEL maintainer="DimitarITZankov"

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"

RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt

RUN python -m venv /py && \
	/py/bin/pip install --upgrade pip && \
	/py/bin/pip install -r /tmp/requirements.txt && \
	rm -rf /tmp

COPY ./application /application
WORKDIR /application

RUN adduser --disabled-password --no-create-home django-user && \
	chown -R django-user /application

EXPOSE 4000

USER django-user

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:4000"]