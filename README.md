# 🧩 TICKETING

Servicio desarrollado con **FastAPI** para gestionar eventos y tickets.  

---

## 🚀 Tecnologías principales

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Python 3.11+](https://www.python.org/)
- [Docker](https://www.docker.com/)
- [Docker-Compose](https://docs.docker.com/compose/)
- [strawberry-graphql[fastapi]](https://strawberry.rocks/)
- [logging](https://docs.python.org/3/library/logging.html)
- [pytest](https://docs.pytest.org/en/stable/)

---

## 💾 Esquema SQL

Se adjunta un archivo **schema.sql** que permite visualizar la estructura SQL de MySQL

---

## ⚙️ Variables de entorno

Las variables de entorno se cargan mediante el archivo `env.sh` **(Mac)**.  
Ejemplo de contenido:

```bash
export NAMESPACE=ticket-management
export RESOURCE=tracking
export MYSQL_USER=root
export MYSQL_PASSWORD=password
export MYSQL_HOST=localhost
export MYSQL_DATABASE=ticketing
export STRAWBERRY_DISABLE_RICH_ERRORS=1
```

Para cargarlas en tu entorno local **(Mac)**:

```bash
source env.sh
```

## ⚙️ Variables de entorno del contenedor levantado con docker-compose

Las variables de entorno que se utilizarán para el contenedor deben estar en un archivo `.env`.  
Ejemplo de contenido:

```bash
NAMESPACE=ticket-management
RESOURCE=tracking
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_HOST=ticketing-db
MYSQL_DATABASE=ticketing
STRAWBERRY_DISABLE_RICH_ERRORS=1
```

---

## 🐳 Ejecución con Docker y/o Podman

### 1️⃣ Construir la imagen

```bash
docker build -t ticketing-image:1.0.0 .
podman build -t ticketing-image:1.0.0 .
```

### 2️⃣ Ejecutar el contenedor

```bash
docker run -d -p 8000:8000 --name ticketing-container --env-file ./.env ticketing-image:1.0.0
podman run -d -p 8000:8000 --name ticketing-container --env-file ./.env ticketing-image:1.0.0
```

> ⚠️ Nota: asegúrate de que el archivo `.env` esté en el mismo directorio donde ejecutas el comando `docker run`.

> ⚠️ Nota: asegúrate de tener MySQL en el mismo entorno donde se ejecuto el **ticketing-container**, sino habrá problemas de comunicación, y el schema SQL debe estar cargado dentro de MySQL container o MySQL localhost (se puede evitar este paso usando docker-compose).

> ⚠️ Nota: si ejecutas MySQL en un contenedor separado, asegurate de que la variable de entorno **MYSQL_HOST** tenga el valor de la IP del contenedor MySQL.

> **⚠️ Nota: se recomienda utilizar docker-compose**


### 3️⃣ Ejecución del docker-compose [All In One]

```bash
docker compose up -d --build [Levantar procesos]
podman compose up -d --build [Levantar procesos]

docker compose down -v [Kill procesos]
podman compose down -v [Kill procesos]
```

---

## ▶️ Ejecución local **(Mac)**

Crea un entorno virtual y activa las variables:

```bash
python -m venv .venv
source .venv/bin/activate
source env.sh
pip install -r requirements.txt
```

Ejecuta el servidor:

```bash
python src/main.py
```

---

## 📂 Estructura general del proyecto

```bash
ticketing/
├── src/
│   ├── application/
│   │   ├── services/
│   │   ├── usecases/
│   ├── domain/
│   │   ├── exceptions/
│   │   ├── interfaces/
│   │   ├── schemas/
│   │   ├── settings.py
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── repositories/
│   │   ├── routes/
│   ├── log/
│   ├── container.py
│   ├── main.py
├── tests/
├── .env
├── env.sh
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── schema.sql
└── README.md
```

---

## 🧠 Endpoints REST

| Método | Ruta | Descripción |
|--------|------|--------------|
| `GET`  | `/ticket-management/api/v1/tracking/liveness` | Verifica si el servicio esta funcionando |
| `POST` | `/ticket-management/api/v1/tracking/events` | Crea un nuevo evento |
| `GET`  | `/ticket-management/api/v1/tracking/events/{id}` | Obtiene los detalles de un evento |
| `PATCH`  | `/ticket-management/api/v1/tracking/events/{id}` | Actualiza parcialmente un evento |
| `DELETE`  | `/ticket-management/api/v1/tracking/events/{id}` | Elimina un evento por id |
| `POST`  | `/ticket-management/api/v1/tracking/tickets` | Realiza la operación de crear un nuevo ticket |
| `PATCH`  | `/ticket-management/api/v1/tracking/tickets/{code}` | Realiza la operación de canje de un ticket vendido |

---

## 📜 Swagger del servicio

### Docs Endpoints REST URL 

```bash
http://localhost:8000/ticket-management/api/v1/tracking/rest
```

### Docs Schema GraphQL URL 

```bash
http://localhost:8000/ticket-management/api/v1/tracking/graphql
```

---

## 🧾 Logging

El proyecto usa un logger JSON personalizado que incluye detalles de un proceso en ejecución.  
Ejemplo de salida:

```json
{
  "timestamp": "2025-11-14T14:03:32.529368+00:00",
  "level": "INFO",
  "logger": "ticketing",
  "path": "/ticketing/ticketing/src/application/usecases/create_event.py",
  "message": "event created with success",
  "details": "extra info ..."
}
```

---

## 🧪 Tests

Para ejecutar las pruebas unitarias asegurate de estar en la raiz del proyecto y ejecutar el siguiente comando:

```bash
pytest tests
```

---

## ✨ Autor

**Kevin Espejel**  
📦 Proyecto interno: *TICKETING*