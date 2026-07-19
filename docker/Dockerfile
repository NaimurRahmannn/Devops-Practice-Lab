FROM python:3.12-slim

WORKDIR /app

COPY apps/employee-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apps/employee-api .

EXPOSE 5000

CMD ["python","run.py"]