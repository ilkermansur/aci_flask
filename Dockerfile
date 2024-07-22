# Base image
FROM python:3.11.9-slim

# Create working Directory
WORKDIR /app

# Copy flask Files, requirements.txt and install modules
COPY . .

RUN pip install -r requirements.txt

# Run app
CMD ["python", "aci_project/app.py"]
