
# Jetbrain DevOps Task – CI/CD Pipeline

## ⚙️ How the Workflow Works

- **Development Branches (`feature/*`, `dev/*`)**  
  Every push builds a Docker image with a unique tag (`dev-branchname-sha`) and deploys it to a temporary namespace (`dev-<branch>`).

- **Staging (`stage` branch)**  
  When code is merged into staging, the pipeline reuses the built image, scans it for vulnerabilities (Trivy), and deploys it to the staging namespace.  
  The staging image is always tagged as `staging-latest`.

- **Production (`main` branch)**  
  Production never builds a new image.  
  Instead, it reuses the **staging-latest** tag that was already tested in staging, ensuring consistency between environments.  
  Deployment requires manual approval through GitHub Issues.

- **Cleanup Workflow**  
  Temporary dev namespaces can be deleted manually by running the **cleanup-stage** workflow.  
  ⚠️ Use with caution: it permanently deletes all resources in that namespace.
---

## 📦 Image Tag Format

| Environment | Example Tag                                         |
|-------------|------------------------------------------------------|
| Dev         | `dev-feature-loginfix-a1b2c3d4`                      |
| Staging     | `a1b2c3d4e5f6g7h8i9j0`, `staging-latest`             |
| Production  | `staging-latest` (reuses staging image)              |

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
- **Trivy Scanning** → Detects critical/high vulnerabilities before staging deploy.
- **Helm `--atomic`** → Automatic rollback on deployment failure.
- **Manual Approval for Prod** → Human gate before production release.

---

## 🛠 Managing Test Namespaces

Temporary namespaces are created for feature branches during **Dev deployments** (e.g., `dev-feature-loginfix`).  
To keep the cluster clean, these namespaces should be deleted after testing.

A dedicated workflow **`cleanup-stage.yml`** is provided:

- **Input:** Requires the branch name to clean.
- **Action:** Deletes the matching `dev-<branch>` namespace if it exists.
- **Safety:** Skips deletion on `main` and `stage` branches to prevent accidents.

⚠️ **Caution:**  
This action is **destructive**. Running the cleanup workflow with the wrong branch name will permanently delete the corresponding namespace.  
Always double-check the branch name before running.

---
## 🖥 Manual Production Deployment

1. Go to the **Actions** tab in GitHub.
2. Select **jetbrain devops task** workflow.
3. Click **Run workflow** on the `main` branch.
4. The workflow will:
- Verify that the `staging-latest` image exists.
- Create a GitHub Issue for manual approval.
- Wait for approval before deploying.
- Deploy the verified image to **Production** using Helm.

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