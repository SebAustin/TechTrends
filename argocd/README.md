# Argo CD manifests

- `argocd-server-nodeport.yaml` — exposes the Argo CD API/UI on NodePorts **30007** (HTTP) and **30008** (HTTPS). Apply after installing Argo CD in the `argocd` namespace.
- `helm-techtrends-staging.yaml` / `helm-techtrends-prod.yaml` — Applications that install the chart under `helm/` using `values-staging.yaml` and `values-prod.yaml`.

Before applying the Application manifests, replace `YOUR_GITHUB_USERNAME` in `repoURL` with your GitHub username (or organization) and repository name where this project is hosted.

Install Argo CD (from the [official guide](https://argo-cd.readthedocs.io/en/stable/getting_started/)), then:

```bash
kubectl apply -n argocd -f argocd/argocd-server-nodeport.yaml
kubectl apply -f argocd/helm-techtrends-staging.yaml
kubectl apply -f argocd/helm-techtrends-prod.yaml
```

Ensure the cluster can pull your image (for example `YOUR_DOCKERHUB_USERNAME/techtrends:latest`); update `helm/values.yaml` (and overrides) `image.repository` / `image.tag` if needed.
