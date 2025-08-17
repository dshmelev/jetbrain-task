
# 🚀 JetBrains DevOps Task – CI/CD Pipeline

This project demonstrates a **GitHub Actions–based CI/CD pipeline** with automated builds, Kubernetes deployments, and security scanning.  
The workflow supports **Dev, Staging, and Production** environments.

---

## ⚙️ Workflow Overview

- **Development (`feature/*`, `dev/*`, `dev-*`)**
  - On every push, a Docker image is built and tagged as:  
    `dev-<branch>-<sha>`
  - Deployed into a **dynamic namespace**: `dev-<branch>`.
  - Each branch gets its own isolated environment.

- **Staging (`stage` branch)**
  - Builds a Docker image tagged with the **commit SHA**.
  - Runs **Trivy vulnerability scanning** before deployment.
  - Deploys into the **staging namespace** (`staging`).
  - Ensures staging always reflects the tested commit.

- **Production (`main` branch, manual trigger)**
  - **Does not rebuild images.**
  - Reuses an image from staging by providing its **SHA tag** manually.
  - Requires **manual approval** via GitHub Issue before deployment.
  - Deploys into the **production namespace** (`production`).
  - Ensures production always uses a previously tested staging image.

- **Cleanup Workflow**
  - Developers can trigger a cleanup workflow (`cleanup-stage.yml`) to delete dev environments.
  - This prevents unused namespaces from cluttering the cluster.

---

## 📦 Image Tag Format

| Environment | Example Tag                          |
|-------------|--------------------------------------|
| Dev         | `dev-feature-loginfix-a1b2c3d4`      |
| Staging     | `ffc82d62b35419bfde99696fc5c8627c8e7f6e48` |
| Production  | Manually entered staging SHA tag     |

---

## 🔒 Required Secrets

| Secret Name          | Purpose                                    |
|----------------------|--------------------------------------------|
| `GITHUB_TOKEN`       | Auth for GHCR & GitHub API actions         |
| `KUBECONFIG_CONTENT` | Base64 kubeconfig for target cluster       |

---

## ⚠ Safeguards

- **Manual Approval for Production** – human gate before release.
- **Concurrency Lock** – prevents multiple prod deployments at once.
- **Image Existence Check** – ensures production reuses a valid staging image.
- **Trivy Scan** – blocks staging deployments if vulnerabilities are found.
- **Helm `--atomic`** – ensures rollback on failed deployments.

---

## 🖥 Manual Production Deployment

1. Go to **Actions → jetbrain devops task**.
2. Select the `main` branch and click **Run workflow**.
3. Provide the **SHA image tag** of the staging build (from last staging deploy).
4. A GitHub Issue will be created requesting approval.
5. Once approved, the workflow deploys that image to production.

---

## 🛠 Managing Test Namespaces

- Every `feature/*`, `dev/*`, or `dev-*` branch gets a **dedicated namespace** (e.g., `dev-feature-loginfix`).
- To delete old namespaces, run the **cleanup-stage.yml** workflow manually.

⚠️ **Caution:**  
This action is **destructive**. Running the cleanup workflow with the wrong branch name will permanently delete the corresponding namespace.  
Always double-check the branch name before running.

---
### Overview
```
Project/
├── .github/
│   └── workflows/
│       ├── deploy.yaml
│       └── cleanup-stage.yml 
├── app/
├── charts/
│   ├── templates/
│   ├── Chart.yaml
│   ├── values-dev.yaml
│   ├── values-prod.yaml
│   └── values-stage.yaml
├── Dockerfile
└── README.md
```