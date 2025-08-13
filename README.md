
---

## 🚀 Pipeline Overview

The pipeline (`deploy.yaml`) runs on:

- **Pushes to `feature/**`** → Deploy to **Dev**
- **Pushes to `stage`** → Deploy to **Staging**
- **Pushes to `main`** → Deploy to **Production** (manual approval required)

You can also trigger it manually with **workflow_dispatch**.

---

## 🔄 Workflow Stages

### 1️⃣ Build and Push Image
- **Checkout code**
- **Set up QEMU + Buildx** for multi-platform builds
- **Login to GHCR** (GitHub Container Registry)
- **Check if image already exists** in GHCR by SHA (skip rebuild if present)
- **Build & push Docker image** with:
    - `dev-<branch>-<sha>` tag
    - `<sha>` tag (used for staging and prod)
- **Scan image** using [Trivy](https://github.com/aquasecurity/trivy)  
  Blocks pipeline on **HIGH/CRITICAL** vulnerabilities.

---

### 2️⃣ Deploy to Dev
- Triggered on pushes to `feature/**`
- Creates namespace `dev-<branch>` dynamically
- Deploys with `values-dev.yaml`
- Used for short-lived feature testing  
  *(namespace can be deleted after testing via `kubectl delete ns dev-<branch>`)*

---

### 3️⃣ Deploy to Staging
- Triggered on pushes to `stage`
- Uses SHA-only tag (no rebuild)
- Deploys with `values-stage.yaml` to fixed `staging` namespace

---

### 4️⃣ Deploy to Production
- Triggered on pushes to `main`
- **Manual approval step** before deployment
- Uses `values-prod.yaml` and fixed `production` namespace
- Prevents concurrent prod deployments via `concurrency: production`

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