FROM continuumio/miniconda3 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y pkg-config default-libmysqlclient-dev libpq-dev build-essential && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# install requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

# FROM continuumio/miniconda3 AS runner-image
# RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3-venv && \
# RUN apt-get update && apt-get install -y default-libmysqlclient-dev libpq-dev && \
# 	apt-get clean && rm -rf /var/lib/apt/lists/*
# RUN apt-get -y update && apt-get install -y libmysqlclient-dev libpq-dev
# COPY --from=builder-image /home/venv /home/venv

RUN mkdir /home/code
RUN mkdir /home/tmp
WORKDIR /home/code

COPY . .
RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment

ENV VIRTUAL_ENV=/home/venv
ENV PATH="/home/venv/bin:$PATH"
# CMD ["python manage.py runserver", "-D", "FOREGROUND"]
