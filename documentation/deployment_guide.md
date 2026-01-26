# Deployment Guide: CCU Monitoreo Activos on Google Cloud Run

This guide explains how to deploy your Streamlit application to Google Cloud Run with secure secret management.

## Prerequisites
- [Google Cloud CLI (gcloud)](https://cloud.google.com/sdk/docs/install) installed and authenticated.
- Access to a Google Cloud Project with Billing enabled.
- The following APIs enabled in your project:
  - Cloud Run API
  - Cloud Build API
  - Secret Manager API

## Recommended Method: Fully Automated CLI

I have provided a script that automates the build, secret upload, and deployment.

### 1. Authenticate and Set Project
Open your terminal and run:
```bash
gcloud auth login
gcloud config set project [YOUR_PROJECT_ID]
```

### 2. Run the Deployment Script
From the root of your project:
```bash
./scripts/deploy.sh
```

**What this script does:**
1.  Uploads your local `.streamlit/secrets.toml` to **GCP Secret Manager**.
2.  Builds the Docker image using **Google Cloud Build**.
3.  Deploys to **Cloud Run** in `south-america-west1` (Santiago).
4.  Mounts the secret directly at `.streamlit/secrets.toml` in the running container.

---

## Alternative Method: Google Cloud Console (Continuous Deployment)

If you prefer using the UI with GitHub integration:

### 1. Preparation (Manual Secret Upload)
You still need to upload your secrets once. You can use the provided script:
```bash
./scripts/upload_secrets.sh
```

### 2. Create Cloud Run Service
1.  Go to [Cloud Run](https://console.cloud.google.com/run) -> **Create Service**.
2.  Select **Continuously deploy from a repository**.
3.  Set region to `south-america-west1`.
4.  Under **Container(s) -> Variables & Secrets**:
    - Click **Add a Secret Reference**.
    - Select `ccu_streamlit_secrets`.
    - Select Reference Method: **Mounted as volume**.
    - Mount Path: `.streamlit/secrets.toml`.
5.  Click **Create**.

## Troubleshooting
- **Port Error**: Ensure the port is set to `8080`.
- **Permissions Error**: Ensure the "Service Account" used by Cloud Run has the "Secret Manager Secret Accessor" role. The CLI script tries to handle deployment permissions, but the first time might require manual approval in the console.
