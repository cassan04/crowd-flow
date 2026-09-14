# Crowd Flow

This is a small project which is being built by a group of unemployed friends, so that we can revise some key concepts and have a good time :)

It's an application whose purpose is to inform the user which places have more people in a certain moment in a certain area.
This can be helpful since we can prevent people from waiting long queues or encourage to visit another room of a museum, just to name a couple of use cases. 

# Quickstart Guide

A step-by-step guide to deploying and running the microservices infrastructure (PostgreSQL, Apache Kafka, Node.js Backend, Python Vision Service, and React Frontend) in **development mode only**, for now.

### Project structure

Each service owns its `Dockerfile` and `.dockerignore`. `docker-compose.yml` builds each image using the service folder as build context:

```
backend/          Node.js API           
frontend/         React (Vite) frontend
vision-service/   Python vision service
```

We use Kafka as MOM.

---

## 1. Prerequisites

Ensure you have the following components installed on your computer before proceeding:

* **Docker Engine**  and **Docker Compose**
* **Git**
* **Bash** terminal environment (Linux, WSL2 on Windows, or macOS)

---

## 2. Initial Setup

### Step 2.1: Clone the repository
Open your terminal and navigate to your preferred working directory:

```bash
git clone https://github.com/cassan04/crowd-flow.git
cd crowd-flow
```
### Step 2.2: Create the environment variables file

Copy the `.env.example` template to generate your local `.env` configuration file:

```bash
cp .env.example .env
```
### 2.3: Grant execution permission to main scripts

Make sure Bash scripts have execution permission. You can give them this permission with this command:

```Bash
chmod +x start.sh sql.sh
```

---

## 3. Deploying Containers

Spins up PostgreSQL, Kafka, the Python vision service, the Node.js API, and the React (Vite) frontend with hot-reloading enabled:

```Bash
./start.sh
```

> **Warning:** `backend/sql/init.sql` starts with `DROP TABLE IF EXISTS occupancy_metrics`, so every run of `sql.sh` (including the one done by `start.sh`) deletes all stored data.

---

## 4. Service Port Mapping

| Service | Container Name | Host Access URL / Port |
|---|---|---|
| Frontend (Development) | `frontend_dev` | `http://localhost:5173` |
| Backend API | `node_backend` | `http://localhost:5000` |
| PostgreSQL DB | `postgres_db` | `localhost:5432` |
| Kafka Broker | `kafka_broker` | `localhost:29092` |

**Kafka addresses:** containers on the Docker network connect to `kafka:9092`, while clients running on your host machine (e.g. kcat, Offset Explorer, local scripts) connect to `localhost:29092`. If you run a service outside Docker, point it to `localhost:29092` (the backend reads it from the `KAFKA_BROKER` variable).

## 6. Useful Maintenance Commands
Stream live logs across all services:
```Bash
docker compose logs -f
```
Inspect logs for a specific container (e.g., Vision Service):
```Bash
docker logs -f vision_app
```
Stop all active containers:
```Bash
docker compose down
```
Stop containers and remove persistent database volumes:
```Bash
docker compose down -v
```

**Note:** The `frontend` service belongs to the `dev` profile, so `docker compose up` on its own does not start it. `start.sh` adds `--profile dev` in development mode; add the same flag if you run Compose by hand. `docker compose down` stops every container regardless of profile.

**Frontend development:** the browser runs on your host, so the API is reachable at `http://localhost:5000`, never at `http://backend:5000`. Compose passes that URL to the dev server as `VITE_API_URL`, so use `import.meta.env.VITE_API_URL` in the React code instead of hardcoding it. The backend already allows this origin through `CORS_ORIGIN`.