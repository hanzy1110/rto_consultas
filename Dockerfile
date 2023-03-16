# using ubuntu LTS version
FROM python:3.10 AS builder-image

# avoid stuck build due to user prompt
# ARG DEBIAN_FRONTEND=noninteractive

# RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3.10-dev python3.10-venv python3-pip python3-wheel build-essential && \
RUN apt-get install -y default-libmysqlclient-dev libpq-dev && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python -m venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM python:3.10 AS runner-image
# RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3-venv && \
ARG CACHEBUST=1

RUN apt-get install -y default-libmysqlclient-dev libpq-dev mysql-client && \
	apt-get clean && rm -rf /var/lib/apt/lists/* 

# RUN apt-get -y update && apt-get install -y libmysqlclient-dev libpq-dev 

COPY --from=builder-image /home/venv /home/venv

# copy project files
RUN mkdir /home/code
RUN mkdir /home/tmp
WORKDIR /home/code
# RUN mkdir ./rto_consultas
# COPY /home/ubuntu/git/rto_consultas/manage.py .
# COPY /home/ubuntu/git/rto_consultas/entrypoint.sh .
# COPY /home/ubuntu/git/rto_consultas/rto_consultas/* ./rto_consultas

COPY . .
RUN echo "OK VERSION?"
RUN ls ./rto_consultas/settings.py

RUN chmod +x entrypoint.sh

# Expose port
EXPOSE 8000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/venv
ENV PATH="/home/venv/bin:$PATH"
# CMD ["python manage.py runserver", "-D", "FOREGROUND"]
