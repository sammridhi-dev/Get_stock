FROM python:3.13-slim

WORKDIR /app

COPY . /app

RUN python -m pip install --upgrade pip 
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7860

CMD ["python", "app.py"]