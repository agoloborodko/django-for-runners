FROM python:3.10

WORKDIR /usr/src/app

ADD . /usr/src/app

# Creates .venv and configures environment
RUN ./manage.py --help

EXPOSE 8000/tcp

CMD ["python", "manage.py", "run_dev_server", "0.0.0.0:8000"]
