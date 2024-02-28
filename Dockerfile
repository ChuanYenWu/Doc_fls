#FROM python:3.8.3-alpine3.12
#FROM ufoym/deepo:pytorch-py38-cpu
FROM cnstark/pytorch:2.0.1-py3.10.11-ubuntu22.04

ADD . /app
WORKDIR /app

EXPOSE 5000
#RUN pip install -r requirement.txt
RUN pip install flask
RUN pip install opencv-python-headless
#RUN pip install pytorch

CMD python main.py