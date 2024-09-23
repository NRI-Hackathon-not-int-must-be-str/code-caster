# CodeCaster

## System Overview

CodeCaster is a service that automatically generates README files from code using Google's Gemini Pro model. It provides a user-friendly way to create informative and well-structured READMEs, saving developers time and effort. 

## Main Features

* **README Generation:**  Upload a zip file containing your code, and CodeCaster will analyze it and generate a comprehensive README file.
* **Gemini Pro Integration:** Leverages the power of Gemini Pro, a large language model, for accurate and context-aware README generation.
* **Dockerized Backend:** The backend service is containerized using Docker, ensuring portability and ease of deployment.
* **FastAPI Framework:** Uses FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
* **API Key Authentication:** Securely access the API endpoints using API key authentication.

## Architecture Explanation

The system consists of a backend service responsible for processing user requests and generating READMEs.

**Technologies Used:**

* **Backend:**
    * Python 3.12
    * FastAPI
    * Vertex AI
    * Gemini Pro
    * Gunicorn
    * Docker

* **Dev Environment:**
    * VS Code Development Container
    * Python Extension
    * Ruff (Linting)
    * MyPy (Type Checking)

* **Deployment:**
    * GitHub Actions
    * Google Artifact Registry
    * Google Cloud Run

## Build Instructions

**Prerequisites:**

* Docker
* Google Cloud Project with Artifact Registry and Cloud Run enabled
* API Key for the CodeCaster service

**Steps:**

1. Clone the CodeCaster repository.
2. Navigate to the `backend` directory.
3. Build the Docker image using the provided `Dockerfile`:
   ```bash
   docker build -t [your-image-name] .
   ```
4. Push the Docker image to Google Artifact Registry:
   ```bash
   docker push asia-northeast1-docker.pkg.dev/[your-project-id]/[your-repository]/[your-image-name]:[your-tag]
   ```

## Run Instructions

**Starting the Service:**

1. Deploy the Docker image to Google Cloud Run:
    ```bash
    gcloud run deploy code-caster-backend --image asia-northeast1-docker.pkg.dev/[your-project-id]/[your-repository]/[your-image-name]:[your-tag] --region asia-northeast1
    ```

**Using the API:**

1. **Generate README:**
    * Send a `POST` request to the `/gen/readme/` endpoint with the zip file of your code as the request body. Include your API key in the `Authorization` header.
    * The response will contain a `token` that identifies the generated README content.
2. **Retrieve README:**
    * Send a `GET` request to the `/gen/readme/{token}` endpoint, replacing `{token}` with the token received from the previous step. Include your API key in the `Authorization` header. 
    * The response will be the generated README file.