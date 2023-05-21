FROM python:3.8

ENV DockerHOME=/usr/mysql

RUN mkdir -p ${DockerHOME}

WORKDIR ${DockerHOME}

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt ${DockerHOME}

RUN pip install -r requirements.txt

ENV PATH=$PATH:/usr/mysql
ENV PYTHONPATH /usr/mysql
COPY . ${DockerHOME}

EXPOSE 8000
CMD ["python","manage.py", "runserver", "0.0.0.0:8000"]
