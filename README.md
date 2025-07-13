Multiplication Table Generator: Docker Learning Project
This project demonstrates a simple web application consisting of two services: a FastAPI backend and a Streamlit frontend. It's designed to help you understand and revise core Docker and Docker Compose concepts by building and orchestrating a multi-service application.

🚀 Project Overview
The application is a "Fancy Multiplication Table Generator" with the following components:

FastAPI Backend (main.py): A lightweight Python web API that receives a number and returns its multiplication table (up to 10) as JSON.

Streamlit Frontend (app.py): A user-friendly web interface that allows users to input a number, sends this number to the FastAPI backend, and displays the generated multiplication table.

This setup is ideal for learning how different services can communicate and be managed within a containerized environment.

🎯 Learning Objectives (Docker Concepts)
This project is structured to help you grasp the following fundamental Docker concepts:

1. Dockerfiles: Blueprints for Images
What it is: A text file that contains all the commands, in order, needed to build a Docker image. Each command creates a new layer in the image, promoting efficiency through caching.

Why we use two: We have two distinct services (FastAPI and Streamlit), each requiring a different set of dependencies and entrypoint commands. Therefore, we create a Dockerfile.fastapi and a Dockerfile.streamlit.

Key Directives:

FROM python:3.13-slim-bullseye: Specifies the base image. slim-bullseye is chosen for a smaller image size, containing only essential Python components.

WORKDIR /app: Sets the working directory inside the container. All subsequent commands (like COPY and RUN) will be executed relative to this directory.

COPY ./table_generator/requirements.txt /app/requirements.txt: Copies the requirements.txt file into the container. Doing this before copying the rest of the code allows Docker to cache the dependency installation layer. If only your code changes, Docker won't re-install dependencies.

RUN pip install --no-cache-dir -r requirements.txt: Executes a command during the image build process. --no-cache-dir reduces the image size by not storing pip's cache.

COPY ./table_generator/main.py /app/main.py (or app.py): Copies the actual application code into the container.

EXPOSE 8000 (or 8501): Informs Docker that the container listens on the specified network ports at runtime. This is documentation; it doesn't actually publish the port.

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]: Defines the default command that will be executed when a container is launched from this image. 0.0.0.0 makes the service accessible from outside the container's localhost.

2. Docker Images: Portable Application Packages
What it is: A lightweight, standalone, executable package that includes everything needed to run a piece of software, including the code, a runtime, libraries, environment variables, and config files.

How they are built: From a Dockerfile using docker build or docker compose build.

Tagging: Assigning a label (e.g., latest, 1.0.0) to an image for versioning and easy identification.

docker tag <local_image_name> <dockerhub_username>/<repo_name>:<tag>

Pushing to Docker Hub: Uploading your built images to a public (or private) registry like Docker Hub, making them shareable and pullable by others.

docker push <dockerhub_username>/<repo_name>:<tag>

3. Docker Containers: Running Instances of Images
What it is: A runnable instance of a Docker image. You can create, start, stop, move, or delete a container using the Docker API or CLI.

How they are run: From an image using docker run or orchestrated by docker compose up.

4. Docker Compose: Orchestrating Multi-Service Applications
What it is: A tool for defining and running multi-container Docker applications. It uses a YAML file (docker-compose.yml) to configure the application's services.

Why it's used here: To define and manage both the FastAPI backend and Streamlit frontend as a single application, handling their networking, dependencies, and port mappings.

Key Directives in docker-compose.yml:

version: '3.8': Specifies the Docker Compose file format version.

services: Defines the individual applications or components that make up your overall application.

fastapi_backend: The name of your FastAPI service. This name is used for internal DNS resolution within the Docker network.

streamlit_frontend: The name of your Streamlit service.

build: Instructs Docker Compose to build an image from a Dockerfile for this service.

context: .: Specifies the build context (the directory where Docker looks for files). . means the current directory (my_multi_app).

dockerfile: Dockerfile.fastapi: Points to the specific Dockerfile to use.

image: <dockerhub_username>/<repo_name>:<tag>: (Alternative to build) Specifies a pre-built image to pull from a registry (like Docker Hub) instead of building it locally. This is used for deployment.

ports: - "8000:8000": Maps a port on the host machine (left side) to a port inside the container (right side). This allows you to access the services from your browser.

networks: - app_network: Connects the service to a custom Docker network.

environment: FASTAPI_URL: http://fastapi_backend:8000: Sets environment variables inside the container. Crucially, fastapi_backend is used here because it's the service name within the Docker network, allowing the frontend to resolve the backend's address.

depends_on: - fastapi_backend: Ensures that the fastapi_backend service starts and is healthy before the streamlit_frontend service attempts to start.

5. Docker Networks: Enabling Inter-Container Communication
What it is: A virtual network created by Docker that allows containers to communicate with each other in an isolated environment.

Why it's used: By putting both fastapi_backend and streamlit_frontend on the same app_network, they can communicate using their service names (e.g., http://fastapi_backend:8000) instead of relying on host IP addresses.

driver: bridge: The default network driver, which creates a private internal network for containers on the same host.

📂 Project Structure
my_multi_app/
├── docker-compose.yml              # Orchestrates the multi-container application
├── Dockerfile.fastapi              # Dockerfile for the FastAPI backend
├── Dockerfile.streamlit            # Dockerfile for the Streamlit frontend
├── README.md                       # This file!
└── table_generator/
    ├── app.py                      # Streamlit frontend code
    ├── main.py                     # FastAPI backend code
    └── requirements.txt            # Combined Python dependencies for both services

🛠️ Prerequisites
Before you begin, ensure you have the following installed:

Python 3.9+ (for local development)

pip (Python package installer)

Docker Desktop (includes Docker Engine and Docker Compose)

Git (for cloning the repository)

🏃 How to Run the Application
Option 1: Run Locally (without Docker)
This option is useful for development and testing individual components.

Clone the repository:

git clone <your_repo_url>
cd my_multi_app

Create and activate a virtual environment:

python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r table_generator/requirements.txt

Open two separate terminal windows/tabs.

In Terminal 1 (for FastAPI Backend):

cd table_generator
python main.py

(FastAPI will run on http://127.0.0.1:8000)

In Terminal 2 (for Streamlit Frontend):

cd table_generator
streamlit run app.py

(Streamlit will open in your browser, typically on http://localhost:8501)

Option 2: Run with Docker Compose (Local Build)
This builds the Docker images on your machine and runs them.

Clone the repository (if you haven't already):

git clone <your_repo_url>
cd my_multi_app

Build the Docker images:
This command reads docker-compose.yml and uses Dockerfile.fastapi and Dockerfile.streamlit to create the images.

docker compose build

Run the containers:
This starts both services in detached mode (-d).

docker compose up -d

Access the application:
Open your browser and navigate to http://localhost:8501.

View Logs (for debugging):

docker compose logs -f

Stop services:

docker compose down

Option 3: Deploy with Docker Hub Images
This option assumes you have already pushed your images to Docker Hub (as described in the previous conversation). This is how someone else (or you on a new machine) would run your application without needing your source code or Dockerfiles.

Ensure your docker-compose.yml is updated to use the image: directive pointing to your Docker Hub repositories (e.g., image: <your_dockerhub_username>/multi-app-fastapi-backend:latest).

Clone the repository (if you haven't already):

git clone <your_repo_url>
cd my_multi_app

Run the containers:
Docker Compose will automatically pull the specified images from Docker Hub if they are not available locally.

docker compose up -d

Access the application:
Open your browser and navigate to http://localhost:8501.

🧹 Cleanup
To remove the Docker containers and networks created by Docker Compose:

docker compose down

To also remove the Docker images (be careful, you'll need to rebuild or pull them again):

docker compose down --rmi all
