FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

COPY . .

#CMD ["python3", "src/main.py"]
CMD alembic upgrade head; python3 src/main.py