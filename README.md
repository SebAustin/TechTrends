# TechTrends (Udacity ND064 project)

Flask app in [`techtrends/`](techtrends/), packaged with Docker, built via [`.github/workflows/techtrends-dockerhub.yml`](.github/workflows/techtrends-dockerhub.yml), and deployed with raw manifests in [`kubernetes/`](kubernetes/), Helm in [`helm/`](helm/), and Argo CD Applications in [`argocd/`](argocd/).

**Quick start (local):** see [`techtrends/README.md`](techtrends/README.md).

**Docker Hub CI:** create GitHub secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.

**Argo CD:** replace `YOUR_GITHUB_USERNAME` in [`argocd/helm-techtrends-staging.yaml`](argocd/helm-techtrends-staging.yaml) and [`argocd/helm-techtrends-prod.yaml`](argocd/helm-techtrends-prod.yaml) with your GitHub user or org.

**Helm:** update [`helm/Chart.yaml`](helm/Chart.yaml) maintainer and, if needed, [`helm/values.yaml`](helm/values.yaml) `image.repository` to match your Docker Hub image (for example `youruser/techtrends`).
