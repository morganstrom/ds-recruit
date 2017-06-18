FROM hypriot/rpi-python
MAINTAINER Morgan Strom "morgan.e.strom@gmail.com"
COPY requirements.txt /code/requirements.txt
WORKDIR /code
RUN pip install -r requirements.txt
COPY . /code
WORKDIR /code
ENTRYPOINT ["python"]
CMD ["app.py"]
