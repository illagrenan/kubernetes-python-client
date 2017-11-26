# =====================================================================
# Kubernetes Python Client Docker Image
# -------------------------------------
#
# Build Image:
# ------------
#
#     >>> docker build -t illagrenan/kubernetes-python-client .
#
#
# Run Image:
# ----------
#
#     >>> docker run --rm -it -p 5555:5555 illagrenan/kubernetes-python-client
#
# =====================================================================
FROM python:3.6
LABEL authors="Vašek Dohnal <vaclav.dohnal@gmail.com>"

# ---------------------------------------------------------------------
# 1. System Settings
# ---------------------------------------------------------------------
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV HOME /root
ENV DEBIAN_FRONTEND noninteractive

# ---------------------------------------------------------------------
# 2. Requirements
# ---------------------------------------------------------------------
RUN pip install --isolated --no-input --compile --exists-action=a --disable-pip-version-check --use-wheel --no-cache-dir 'kubernetes~=4.0.0'
RUN pip install --isolated --no-input --compile --exists-action=a --disable-pip-version-check --use-wheel --no-cache-dir 'click~=6.7.0'

# ---------------------------------------------------------------------
# 3. App sources
# ---------------------------------------------------------------------
RUN mkdir -p /app
WORKDIR /app
COPY ./app /app/
