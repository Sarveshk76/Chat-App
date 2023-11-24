FROM python:3.11-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update --fix-missing

RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/
COPY requirements.txt /usr/src/app/
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /usr/src/app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]