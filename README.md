# Crowd Flow

This is a small project which is being built by a group of unemployed friends, so that we can revise some key concepts and have a good time :)

It's an application whose purpose is to inform the user which places have more people in a certain moment in a certain area.
This can be helpful since we can prevent people from waiting long queues or encourage to visit another room of the museum, just to name a couple of use cases. 

# Quickstart Guide

A step-by-step guide to deploying and running the microservices infrastructure (PostgreSQL, Apache Kafka, ZooKeeper, Node.js Backend, Python Vision Service, and React Frontend) in development or production.

---

## 1. Prerequisites

Ensure you have the following components installed on your system before proceeding:

* **Docker Engine** (v20.10+) and **Docker Compose** (v2.0+)
* **Git**
* **Bash** terminal environment (Linux, WSL2 on Windows, or macOS)

---

## 2. Initial Setup

### Step 2.1: Clone the repository
Open your terminal and navigate to your preferred working directory:

```bash
git clone https://github.com/your-org/crowd-flow.git
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

Spins up PostgreSQL, ZooKeeper, Kafka, the Python vision service, Node.js API, and the React (Vite) frontend with hot-reloading enabled:

```Bash
./start.sh
```

**Note:** By default, the script reads NODE_ENV=development from your .env file and executes the development profile.

### Production Mode (prod)
Builds the static React frontend assets and serves them via an Apache Web Server:

```Bash
NODE_ENV=production ./start.sh
```
## 4. Initializing the Database

Once all containers are running and PostgreSQL reaches a healthy state, execute the SQL migration script to apply database schemas and tables:

```Bash
./sql.sh
```

## 5. Service Port Mapping

| Service | Container Name | Host Access URL / Port |
|---|---|---|
| Frontend (Development) | `frontend_dev` | `http://localhost:5173` |
| Frontend (Production) | `apache_frontend` | `http://localhost:80` |
| Backend API | `node_backend` | `http://localhost:5000` |
| PostgreSQL DB | `postgres_db` | `localhost:5432` |
| Kafka Broker | `kafka_broker` | `localhost:9092` |## 5. Service Port Mapping
ServiceContainer NameHost Access URL / PortFrontend (Development)frontend_devhttp://localhost:5173Frontend (Production)apache_frontendhttp://localhost:80Backend APInode_backendhttp://localhost:5000PostgreSQL DBpostgres_dblocalhost:5432Kafka Brokerkafka_brokerlocalhost:9092

## 6. Useful Maintenance Commands
Stream live logs across all services:
```Bash
docker compose --profile dev logs -f
```
Inspect logs for a specific container (e.g., Vision Service):
```Bash
docker logs -f vision_app
```
Stop all active containers:
```Bash
docker compose --profile dev down
```
Stop containers and remove persistent database volumes:
```Bash
docker compose --profile dev down -v
```