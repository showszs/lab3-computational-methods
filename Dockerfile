# Модель: Стрільба по рухомій цілі 
# Автор: Пасат Іван, група АІ-232

FROM python:3.10-slim

WORKDIR /app

COPY main.py .

RUN pip install numpy matplotlib

CMD ["python", "main.py"]