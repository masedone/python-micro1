from fastapi import FastAPI, Request, Depends, HTTPException, Body
from fastapi.responses import HTMLResponse
from app.redis_client import RedisClient
from app.rabbitmq import RabbitMQClient
from app.auth import verify_jwt

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root(request: Request, authorization: str = None):
    results = []

    # Test Redis: escritura y lectura
    redis_test_key = "healthcheck_test"
    redis_test_value = {"test": "ok"}
    try:
        redis_client = RedisClient()
        redis_client.set_value(redis_test_key, redis_test_value)
        value = redis_client.get_value(redis_test_key)
        if value == redis_test_value:
            results.append(("Redis", True, f"Escritura y lectura OK. Valor: {value}"))
        else:
            results.append(("Redis", False, f"Valor leído no coincide: {value}"))
    except Exception as e:
        results.append(("Redis", False, str(e)))

    # Test RabbitMQ: envío de mensaje
    try:
        rabbit_client = RabbitMQClient()
        rabbit_client.send_message({"healthcheck": "ok"})
        rabbit_client.close()
        results.append(("RabbitMQ", True, "Mensaje de prueba enviado correctamente"))
    except Exception as e:
        results.append(("RabbitMQ", False, str(e)))

    # Test Keycloak (solo si hay token)
    keycloak_status = "No se proporcionó token JWT en el header Authorization"
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        try:
            payload = verify_jwt.__wrapped__(token) if hasattr(verify_jwt, "__wrapped__") else verify_jwt(token)
            results.append(("Keycloak", True, f"Token válido. Usuario: {payload.get('preferred_username', 'N/A')}"))
        except Exception as e:
            results.append(("Keycloak", False, f"Token inválido: {str(e)}"))
    else:
        results.append(("Keycloak", None, keycloak_status))

    # HTML simple
    html = """
    <html>
    <head>
        <title>Healthcheck Microservicio</title>
        <meta http-equiv='refresh' content='10'>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .ok { color: green; }
            .fail { color: red; }
            .skip { color: gray; }
        </style>
    </head>
    <body>
        <h1>Healthcheck Microservicio</h1>
        <ul>
    """
    for name, status, msg in results:
        if status is True:
            html += f"<li><b>{name}:</b> <span class='ok'>OK</span> - {msg}</li>"
        elif status is False:
            html += f"<li><b>{name}:</b> <span class='fail'>ERROR</span> - {msg}</li>"
        else:
            html += f"<li><b>{name}:</b> <span class='skip'>NO TEST</span> - {msg}</li>"
    html += """
        </ul>
        <p><small>La página se refresca cada 10 segundos.</small></p>
    </body>
    </html>
    """
    return HTMLResponse(content=html) 