echo "FROM python:3.10-slim" > Dockerfile
echo "WORKDIR /app" >> Dockerfile
echo "COPY requirements.txt ." >> Dockerfile
echo "RUN pip install --no-cache-dir -r requirements.txt" >> Dockerfile
echo "COPY . ." >> Dockerfile
echo "EXPOSE 8000" >> Dockerfile
echo 'CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]' >> Dockerfile