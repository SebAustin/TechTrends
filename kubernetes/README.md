# Kubernetes manifests (sandbox)

Apply the declarative manifests after your k3s cluster is running and `kubectl` is configured (often as root on the Vagrant box):

```bash
kubectl apply -f kubernetes/namespace.yaml
kubectl apply -f kubernetes/deploy.yaml
kubectl apply -f kubernetes/service.yaml
```

The deployment uses image `techtrends:latest`. Load that image on the node (for example `docker build` / `docker save` + import into k3s) or change the image reference to your Docker Hub repository (for example `yourdockerhubuser/techtrends:latest`) and set `imagePullPolicy: Always` if the cluster should pull from the registry.

Verify:

```bash
kubectl get all -n sandbox
```
