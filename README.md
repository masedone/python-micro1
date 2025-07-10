# Microservicio de Referencia con FastAPI

## Requisitos
- Python 3.11+
- RabbitMQ
- Redis

## Instalación local (venv)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Docker

```bash
docker build -t python-reference-micro .
docker run -p 8000:8000 --env-file .env python-reference-micro
```

## Kubernetes

Aplica los manifiestos en el cluster:

```bash
kubectl apply -f k8s/
``` 