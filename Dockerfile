FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY server.py server.py
CMD ["python", "-u", "server.py"]