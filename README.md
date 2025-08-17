
---

# Jetbrain DevOps Task – CI/CD Pipeline

## 🖥 Manual Production Deployment

1. Go to the **Actions** tab in GitHub.
2. Select **jetbrain devops task** workflow.
3. Click **Run workflow** on the `main` branch.
4. Fill in:
  - **approve** → `YES`
5. The workflow will:
  - Verify that the `staging-latest` image exists.
  - Create a GitHub Issue for manual approval.
  - Wait for approval before deploying.
  - Deploy the verified image to **Production** using Helm.

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

To remove a Dev namespace after testing:

```bash
Run cleanup-stage to delete test namespace
```
---

## overview

```
Project/
├── .github/
│   └── workflows/
│       └── deploy.yaml
|       └── cleanup-stage.yml 
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