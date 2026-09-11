# Crowd Flow

This is a small project which is being built by a group of unemployed friends, so that we can revise some key concepts and have a good time :)

It's an application whose purpose is to inform the user which places have more people in a certain moment in a certain area.
This can be helpful since we can prevent people from waiting long queues or encourage to visit another room of a museum, just to name a couple of use cases. 

# Quickstart Guide

A step-by-step guide to deploying and running the microservices infrastructure (PostgreSQL, Apache Kafka, Node.js Backend, Python Vision Service, and React Frontend) in development or production.

> **Note:** The React frontend is temporarily disabled and is not started with the rest of the app. To enable it, uncomment the `frontend` and `apache` services in `docker-compose.yml` and the frontend lines in `start.sh`.

### Project structure

Each service owns its `Dockerfile` and `.dockerignore`, and `docker-compose.yml` builds each image using the service folder as build context:

```
backend/          Node.js API           
frontend/         React (Vite) frontend
vision-service/   Python vision service
sql/              Database init scripts
```

---

## 1. Prerequisites

Ensure you have the following components installed on your system before proceeding:

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
### 2.3: Grant execution permissions to management scripts

Make the provided automation Bash scripts executable:

```Bash
chmod +x start.sh sql.sh
```
## 3. Deploying Containers

### Development Mode (dev)

Spins up PostgreSQL, Kafka, the Python vision service, and the Node.js API with hot-reloading enabled:

```Bash
./start.sh
```

**Note:** By default, the script reads NODE_ENV=development from your .env file and executes the development profile.

### Production Mode (prod)
Starts the same services, using the production build of the Node.js API. Serving the static React frontend via Apache is currently disabled (see the note above):

```Bash
NODE_ENV=production ./start.sh
```
## 4. Initializing the Database

There is no need to do this manually: `start.sh` waits for PostgreSQL to be ready and then runs `sql.sh`, which applies `sql/init.sql` to the database.

If you need to re-apply the schema later (e.g. after editing `sql/init.sql`) while the containers are running, execute:

```Bash
./sql.sh
```

> **Warning:** `sql/init.sql` starts with `DROP TABLE IF EXISTS occupancy_metrics`, so every run of `sql.sh` (including the one done by `start.sh`) deletes all stored metrics.

## 5. Service Port Mapping

| Service | Container Name | Host Access URL / Port |
|---|---|---|
| Frontend (Development) — *disabled* | `frontend_dev` | `http://localhost:5173` |
| Frontend (Production) — *disabled* | `apache_frontend` | `http://localhost:80` |
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

**Note:** Only services assigned to a profile need the `--profile` flag. Currently no active service uses one; once the production frontend (`apache`, profile `prod`) is enabled, add `--profile prod` to these commands to include it.