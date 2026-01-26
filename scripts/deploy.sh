#!/bin/bash

# Configuration
SERVICE_NAME="ccu-monitoreo-activos"
REGION="southamerica-west1"
SECRET_NAME="ccu_streamlit_secrets"
REPO_NAME="cloud-run-source-deploy" # Standard repo name
PROJECT_ID=$(gcloud config get-value project)
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:latest"

echo "🚀 Starting Deployment Process..."

# 1. Upload Secrets
echo "--- Step 1: Uploading Secrets to Secret Manager ---"
./scripts/upload_secrets.sh

# 2. Ensure Artifact Registry Repository exists
echo "--- Step 2: Ensuring Artifact Registry Repository exists ---"
gcloud artifacts repositories describe $REPO_NAME --location=$REGION >/dev/null 2>&1 || \
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Repository for Cloud Run images"

# 3. Build the Image using Cloud Build
echo "--- Step 3: Building Image with Cloud Build ---"
gcloud builds submit --tag $IMAGE_NAME .

# 4. Deploy to Cloud Run
echo "--- Step 4: Deploying to Cloud Run ---"
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --region $REGION \
    --allow-unauthenticated \
    --set-secrets="/app/.streamlit/secrets.toml=${SECRET_NAME}:latest" \
    --port 8080

echo "✅ Deployment complete!"
