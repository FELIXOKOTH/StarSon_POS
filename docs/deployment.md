# How to Deploy the StarSon POS AI Application

This guide provides instructions for deploying the application using Docker. Docker allows us to package the application and its dependencies into a container, which can be run consistently across different environments.

## Prerequisites

- You must have [Docker](https://www.docker.com/get-started) installed on your system.

## Deployment Steps

### 1. Build the Docker Image

First, you need to build the Docker image from the `Dockerfile` provided in the project's root directory. This command will package the application and install all the required dependencies.

Open your terminal and run the following command from the project root:

```bash
docker build -t starsos-pos-ai .
```

### 2. Run the Docker Container

Once the image has been built successfully, you can run the application as a container. This will start the Flask server on port `8080`.

```bash
docker run -p 8080:8080 -d starsos-pos-ai
```

- **`-p 8080:8080`**: This maps port `8080` on your local machine to port `8080` inside the container.
- **`-d`**: This runs the container in detached mode, so it runs in the background.

### 3. Access the Application

After running the container, the application will be accessible in your web browser at:

[http://localhost:8080](http://localhost:8080)

## Stopping the Container

To stop the running container, you will first need to find its ID.

```bash
docker ps
```

This will list all running containers. Find the `CONTAINER ID` for the `starsos-pos-ai` image and then run:

```bash
docker stop <CONTAINER_ID>
```
