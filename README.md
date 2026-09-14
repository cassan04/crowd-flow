# Crowd Flow

This is a small project which is being built by a group of  friends, so that we can revise some key concepts and have a good time :)

It's an application whose main purpose is to inform the user which places have more people in a certain moment in a certain area.
This can be helpful since we can prevent people from waiting long queues or encourage to visit another room of a museum, just to name a couple of use cases. 

# Quickstart Guide

This is a step-by-step guide to deploying and running the microservices infrastructure (PostgreSQL, Apache Kafka, Node.js Backend, Python Vision Service, and React Frontend) in **development mode only**, for now.

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
* **Node.js 20+**
* **Git**
* **Bash** terminal environment on **Linux or WSL2 (x64)**

> The containers reuse the `node_modules` installed on your machine, so everyone **must be** on Linux or WSL2 on x64.

---

## 2. Initial setup

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
### Step 2.3: Install the Node dependencies

```bash
(cd backend && npm ci)
(cd frontend && npm ci)
```

### 2.4: Grant execution permission to main scripts

Make sure Bash scripts have execution permission. You can give them this permission with this command:

```Bash
chmod +x start.sh sql.sh
```

---

## 3. Deploying Containers

PostgreSQL, Kafka, the Python vision service, the Node.js API, and the React (Vite) frontend with hot-reloading enabled. Execute this command to start the system:

```Bash
./start.sh
```

> **Warning:** This file internally executes `backend/sql/init.sql` which starts with `DROP TABLE IF EXISTS occupancy_metrics`, so every run of `sql.sh` (including the one done by `start.sh`) deletes all stored data.

---

## 4. Service Port Mapping

| Service | Container Name | Access URL / Port |
|---|---|---|
| Frontend (Development) | `react_frontend` | `http://localhost:5173` |
| Backend API | `node_backend` | `http://localhost:5000` |
| PostgreSQL DB | `postgres_db` | `localhost:5432` |
| Kafka Broker | `kafka_broker` | `localhost:29092` |


## 5. Useful commands to use

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

## 6. Daily workflow

The rule of thumb: **npm runs on your machine, everything else runs in Docker.** Nobody installs PostgreSQL, Kafka or Python locally.

| Task | Where | Command |
|---|---|---|
| Start everything | Docker | `./start.sh` |
| See your changes | automatic | just save the file |
| Add a dependency | host | `cd frontend && npm i <package>` |
| Pull someone else's dependencies | host | `git pull`, then `npm ci` in that folder |
| Read the logs | Docker | `docker compose logs -f frontend` |
| Add a Python dependency | host | add it to `vision-service/requirements.txt`, then `docker compose up -d --build vision-service` |

Adding or pulling a dependency needs no image rebuild: the container reads the same `node_modules` you just installed. Restart the affected service (`docker compose restart frontend`) if the dev server does not pick it up.

**Hot reload** works through the bind mounts in all three services: Vite refreshes the browser, the API restarts itself because `npm run dev` runs `node --watch`, and the vision service restarts through `watchfiles`, which watches `vision-service/src`.

Python dependencies are the exception to the rule above: they are installed inside the image, not on your machine, so `requirements.txt` changes need `docker compose up -d --build vision-service`.