# Custom JupyterHub KubeSpawner

Данный репозиторий описывает процедуру развертывания JupyterHub на Kubernetes с измененным KubeSpawner на основе групп
пользователей

## Структура репозитория

- `jupyterhub-chart/`: Chart для запуска JupyterHub с созданием Ingress Nginx (требуется заранее его установить)
- `alexspawner/`: Код с измененным KubeSpawner

## Использование

Для сборки образа hub с custom spawner необходимо выполнить команду: 

```sh
docker build -t alexspawner:v1.0.0 .
```

Запустите Helm chart:

```sh
cd jupyterhub-chart
helm upgrade --install -n jupyter -f values.yaml jupyter .
```

Перейдите в интерфейс JupyterHub и последовательно авторизуйтесь под разными пользователями:
- admin:admin
- other_user:other_user
- test:test

В зависимости от того под кем вы входите, вы можете увидеть, как изменяется интерфейс JupyterHub.

Параметры для разных групп установлены в `jupyterhub/templates/alex-configmap.yaml`

## Примечания

Данный репозиторий содержит только общие идеи изменения KubeSpawner и отражает только изменение параметров MEM, CPU.

