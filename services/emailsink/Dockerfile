FROM zogg/nanomsg

WORKDIR /myproject

COPY requirements.txt /myproject/requirements.txt
RUN pip install -r requirements.txt

COPY libs /myproject
COPY local-libs.txt /myproject/local-libs.txt
RUN pip install -r local-libs.txt

COPY ./src /myproject

ENTRYPOINT ["python", "-u", "run.py"]
