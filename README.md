
---

# Jetbrain DevOps Task – CI/CD Pipeline

This repository contains a **GitHub Actions** pipeline for building, scanning, and deploying a Dockerized application to **Dev**, **Staging**, and **Production** Kubernetes environments using **Helm**.

---

## 📋 Pipeline Overview

The workflow (`.github/workflows/pipeline.yml`) automates:

- **Docker Image Build & Push** → Builds multi-platform images and pushes to **GitHub Container Registry (GHCR)**.
- **Environment Deployments**:
  - **Dev** → Auto-deploys feature/dev branches to dynamic namespaces.
  - **Staging** → Deploys `stage` branch image with Trivy vulnerability scanning.
  - **Production** → Manually approved deployment reusing the staging image.
- **Security & Safety**:
  - Vulnerability scan before staging deploy.
  - Manual approval required for production.
  - Concurrency control to prevent simultaneous prod deployments.

---

## 🚀 Trigger Rules

| Event Type              | Branch Pattern             | Action Taken                  |
|-------------------------|----------------------------|--------------------------------|
| **Push**                | `feature/**`, `dev/**`     | Build & deploy to **Dev**     |
| **Push**                | `stage`                    | Build, scan, deploy to **Staging** |
| **Pull Request Closed** | Target = `stage`            | Build, scan, deploy to **Staging** |
| **Manual Dispatch**     | _n/a_                       | Deploy to **Production** (with approval) |

---

## 🛠 Job Descriptions

### **1. build**
- Runs on push/PR (except prod deploy).
- Builds & pushes Docker images.
- Tags:
  - Dev: `dev-{safe-branch}-{commit-sha}`
  - Staging: `{commit-sha}`

### **2. deploy-dev**
- Deploys dev images to **`dev-{safe-branch}`** namespace.
- Uses Helm values from `charts/values-dev.yaml`.

### **3. deploy-staging**
- Deploys staging image to `staging` namespace.
- Runs **Trivy** scan (CRITICAL & HIGH).
- Publishes scan results to GitHub job summary.
- Uses Helm values from `charts/values-stage.yaml`.

### **4. deploy-production**
- Triggered manually with `workflow_dispatch`.
- Inputs:
  - `approve` → must be `"YES"`
  - `image_tag` → SHA tag from staging build.
- Manual approval step before deployment.
- Verifies image exists in GHCR before deploy.
- Uses Helm `--atomic` to rollback on failure.
- Publishes Helm status to GitHub job summary.

---

## 🖥 Manual Production Deployment

1. Go to **Actions** tab in GitHub.
2. Select **jetbrain devops task** workflow.
3. Click **Run workflow** → choose branch.
4. Fill in:
  - **approve** → `YES`
  - **image_tag** → SHA from staging deployment.
5. Approve deployment via the GitHub Issue created by the workflow.

---

## 📦 Image Tag Format

| Environment | Example Tag                                         |
|-------------|------------------------------------------------------|
| Dev         | `dev-feature-loginfix-a1b2c3d4`                      |
| Staging     | `a1b2c3d4e5f6g7h8i9j0`                               |
| Production  | Uses the staging tag provided in manual input        |

---

## 🔒 Required Secrets

| Secret Name               | Purpose                                   |
|---------------------------|-------------------------------------------|
| `GITHUB_TOKEN`            | GHCR authentication & GitHub API actions |
| `KUBECONFIG_CONTENT`      | Base64 kubeconfig for target clusters     |

---

## ⚠ Safeguards

- **Concurrency Lock** → Only one production deploy at a time.
- **Image Existence Check** → Prevents deploying missing images.
- **Trivy Scanning** → Detects critical/high vulnerabilities.
- **Helm `--atomic`** → Automatic rollback on deployment failure.
---

## 🛠 Managing Test Namespaces

To remove a Dev namespace after testing:

```bash
kubectl delete namespace dev-<branch>
```
---

## overview

```
Project/
├── .github/
│   └── workflows/
│       └── deploy.yaml
├── app/
├── charts/
│   ├── templates/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── values-stage.yaml
├── Dockerfile
└── README.md
```