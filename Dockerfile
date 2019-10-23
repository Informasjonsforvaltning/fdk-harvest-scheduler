FROM python:3

ADD hello.py /

RUN pip install pystrich

CMD [ "python", "./hello.py" ]