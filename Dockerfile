FROM python:3.11-slim

WORKDIR /bff-flask-daruix

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["python"]
CMD ["app.py"]