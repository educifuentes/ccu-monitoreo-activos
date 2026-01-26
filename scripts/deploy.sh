#!/bin/bash

# Configuration
SERVICE_NAME="ccu-monitoreo-activos"
REGION="south-america-west1"
SECRET_NAME="ccu_streamlit_secrets"
PROJECT_ID=$(gcloud config get-value project)

echo "🚀 Starting Deployment Process..."

# 1. Upload Secrets
echo "--- Step 1: Uploading Secrets to Secret Manager ---"
./scripts/upload_secrets.sh

# 2. Deploy to Cloud Run
# This command will build the image using Google Cloud Build and deploy it.
echo "--- Step 2: Deploying to Cloud Run ---"
gcloud run deploy $SERVICE_NAME \
    --source . \
    --region $REGION \
    --allow-unauthenticated \
    --set-secrets="/app/.streamlit/secrets.toml=${SECRET_NAME}:latest" \
    --port 8080

echo "✅ Deployment complete!"
