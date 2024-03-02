FROM jupyterhub/k8s-hub:3.1.0

LABEL authors="Alex Egorov"
LABEL telegram="https://t.me/ialex_ops"

LABEL description="JupyterHub for Kubernetes with custom spawner"

USER root

COPY . .
RUN pip install .

USER 1000