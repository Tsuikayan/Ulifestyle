From python:3

COPY requirements.txt /root/

RUN cd /root && pip install -r requirements.txt

WORKDIR /root

EXPOSE 80:5000

EXPOSE 8025:8025

CMD ["python", "run.py"]
