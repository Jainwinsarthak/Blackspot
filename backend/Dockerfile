FROM python:3.11-slim

WORKDIR /app

# Render builds from the repository root. Copy the API and the offline ML
# pipeline together so the API can load its generated data and local models.
COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY backend /app/backend
COPY ml /app/ml

# Create reproducible demo assets inside the image; generated CSVs and joblib
# files therefore do not need to be committed to Git.
RUN cd /app/ml && python generate_demo_data.py && python train_model.py

WORKDIR /app/backend
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
