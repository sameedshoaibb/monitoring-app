# 🧭 Ro Monitoring App  
A **real-time monitoring dashboard** built with Flask, Docker, and Kubernetes — deployed via **Helm**.

<img width="1306" height="905" alt="Screenshot 2025-11-02 at 1 26 36 AM" src="https://github.com/user-attachments/assets/0f6e2281-ac66-4473-9ee2-1cc298a945ae" />

---

## 🚀 Overview
The **Ro Monitoring App** provides live metrics and system status through a simple Flask-based web dashboard.  
It’s containerized using Docker and deployed to a Kubernetes cluster using a Helm chart.

---

## 🧩 Prerequisites

Before deploying, ensure you have the following installed and configured:

| Tool | Minimum Version | Purpose |
|------|------------------|----------|
| Docker | 28.0.0+ | Container image build & run |
| kind | 0.25.0+ | Local Kubernetes cluster emulator |
| kubectl | 1.33.0+ | Cluster management |
| Helm | 3.18.0+ | Deployment management |
| GNU make | 3.81.0+ | Optional build automation |
| Git | 2.39.0+ | Source code versioning |

---

## ⚙️ Deployment

### 🧱 Install the Helm Release
To install the app and create the required namespace:

```bash
helm install monitoring-app-release . \
  -f values-prod.yaml \
  --namespace python-monitoring-app \
  --create-namespace
