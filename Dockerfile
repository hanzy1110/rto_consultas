# using ubuntu LTS version
FROM continuumio/miniconda3 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y
# RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3.10-dev python3.10-venv python3-pip python3-wheel build-essential && \
RUN apt-get install -y default-libmysqlclient-dev libpq-dev build-essential mysql-server && \
	apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages

# RUN curl https://www.python.org/ftp/python/3.9/get-pip.py -o get-pip.py
# RUN python get-pip.py
# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python
# RUN python -m venv /home/venv
# ENV PATH="/home/venv/bin:$PATH"

# install requirements

# ENV PIP_VERBOSE=1
# RUN mkdir /home/venv
# ENV PIP_TARGET=/home/venv

# COPY get-pip.py .
# RUN python ./get-pip.py

# RUN conda create -n venv python=3.10 -y && conda init bash && conda activate venv
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install wheel
RUN pip install -r requirements.txt

# FROM continuumio/miniconda3 AS runner-image
# RUN apt-get update && apt-get install --no-install-recommends -y python3.10 python3-venv && \

RUN apt-get update && apt-get install -y default-libmysqlclient-dev libpq-dev && \
	apt-get clean && rm -rf /var/lib/apt/lists/* 

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
