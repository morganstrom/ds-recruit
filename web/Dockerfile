FROM python:3.6
MAINTAINER Morgan Strom "morgan.e.strom@gmail.com"
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["python"]
CMD ["app.py"]
