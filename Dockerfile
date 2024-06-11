FROM python:3.12-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc g++ curl procps net-tools tini

ENV VIRTUAL_ENV=/usr/local
ADD --chmod=755 https://astral.sh/uv/install.sh /install.sh
RUN /install.sh && rm /install.sh

# Set up the Python environment
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

COPY . /app/

RUN  /root/.cargo/bin/uv pip install --no-cache -r /app/requirements.lock

# Expose the application port
EXPOSE 8000
EXPOSE 5678