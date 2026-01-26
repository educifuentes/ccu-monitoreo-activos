# Deployment & Update Guide

Your application is now successfully deployed to Google Cloud Run!

## 🚀 How to deploy new updates
Whenever you make changes to your code or secrets and want to push them to the live server, simply run:

```bash
./scripts/deploy.sh
```

### What this command does:
1.  **Syncs Secrets**: Updates GCP Secret Manager with any changes in your local `.streamlit/secrets.toml`.
2.  **Builds & Pushes**: Uploads your latest code and builds a new Docker image in the cloud.
3.  **Deploys**: Updates the Cloud Run service to use the new image.

## 🔗 Useful Links

- **Live Application**: [Open App](https://ccu-monitoreo-activos-219154903837.southamerica-west1.run.app)
- **Monitoring & Logs**: [Cloud Run Console](https://console.cloud.google.com/run/detail/southamerica-west1/ccu-monitoreo-activos/logs?project=clear-data-485013)
- **Billing & Cost**: [GCP Billing Dashboard](https://console.cloud.google.com/billing?project=clear-data-485013)
- **Container Registry**: [Artifact Registry Images](https://console.cloud.google.com/artifacts/docker/clear-data-485013/southamerica-west1/cloud-run-source-deploy?project=clear-data-485013)

---

## 🛠️ Infrastructure Overview

- **Service URL**: [https://ccu-monitoreo-activos-219154903837.southamerica-west1.run.app](https://ccu-monitoreo-activos-219154903837.southamerica-west1.run.app)
- **Region**: `southamerica-west1` (Santiago)
- **Secrets**: Managed via **GCP Secret Manager** (`ccu_streamlit_secrets`).
- **Builds**: Handled by **Google Cloud Build**.

## 📝 Configuration Files
- `Dockerfile`: Defines the container environment.
- `.gcloudignore`: Prevents local files (like `.venv`) from being uploaded to the cloud.
- `scripts/deploy.sh`: The master script for one-command deployment.
- `scripts/upload_secrets.sh`: Helper script specifically for secret management.

