#Dockerfile

#Python image
FROM python:3.11-slim

#Working directory
WORKDIR /app

#Huidige directory
COPY . /app

#Installeer depedencies uit requirements
RUN pip install --no-cache-dir -r requirements.txt

#port 5000 openzetten
EXPOSE 5000

#Run applicatie
CMD ["python", "application.py"]
