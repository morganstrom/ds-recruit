FROM python:3.6
MAINTAINER Morgan Strom "morgan.e.strom@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
