# CodeCaster

## CodeCaster Backend Summary

This code defines a Python backend service using FastAPI for generating README files from code using Google's Gemini Pro model. It utilizes Docker for containerization and has configurations for VS Code development.

**Key Components:**

1.  **Dev Container Configuration (`devcontainer.json`)**:
    *   Sets up a development container with Python 3.12.
    *   Uses a pre-built Docker image from Microsoft.
    *   Installs VS Code extensions for Python development (Python, Ruff, MyPy).
    *   Configures VS Code settings for Python formatting, linting, and type checking.

2.  **GitHub Action Workflow (`.github/workflows/main.yml`)**:
    *   Triggers on every push to the repository.
    *   Runs on Ubuntu.
    *   Checks out the code.
    *   Uses a custom GitHub Action (presumably for deploying to Cloud Run).
    *   Builds and pushes a Docker image to Google Artifact Registry.
    *   Deploys the image to Cloud Run.

3.  **`.gitignore`**:
    *   Defines files and directories to be excluded from version control (common Python project files).

4.  **`compose.yaml`**:
    *   Not provided in the code snippet. Likely defines Docker Compose services for the application.

5.  **`poetry.lock`**:
    *   Contains locked versions of Python dependencies managed by Poetry.

6.  **`Dockerfile` (backend)**:
    *   Defines the steps to build the Docker image for the backend service.
    *   Uses a multi-stage build process (builder and runner).
    *   Installs Poetry and project dependencies.
    *   Configures a Gunicorn user.
    *   Copies the application code.
    *   Sets the working directory and exposes port 8000.
    *   Defines the default command to start the Gunicorn server.

7.  **Gunicorn Configuration (`gunicorn_conf.py`)**:
    *   Defines Gunicorn server settings (workers, timeouts, logging, etc.).
    *   Uses environment variables for configuration with a nested delimiter (`__`).

8.  **Backend Server (app)**:
    *   Uses FastAPI framework.
    *   Requires API key authentication for all endpoints.
    *   Defines an endpoint (`/gen/readme/`) for generating README files:
        *   Accepts a zip file containing code as input.
        *   Extracts the zip file.
        *   Uses Vertex AI and Gemini Pro to generate a README based on the code.
        *   Saves the generated README to a file.
    *   Defines an endpoint (`/gen/readme/{token}`) to retrieve the generated README file.

**Schemas:**

*   `CreateGenReadmeResponse`: Defines the response structure for both generating and retrieving README files. Contains a `token` field to identify the generated content.

**Overall:**

This code represents a well-structured backend for a service that leverages a large language model (Gemini Pro) to generate README files from code. It employs best practices for containerization, configuration, dependency management, and API design.