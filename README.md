# Mock Service

A simple HTTP mock service for testing and development in Kubernetes.

## Features

- Returns 200 OK for all requests
- Echoes back request data
- Customizable status codes
- Delayed response simulation
- Health check endpoint

## API Endpoints

- `GET /` - Root endpoint that returns request info
- `GET /health` - Health check endpoint
- `POST /echo` - Echo back request body
- `GET /status/<code>` - Return custom HTTP status code
- `GET /delay/<seconds>` - Simulate delayed response

## Local Development

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the service locally:

```bash
python app.py
```

The service listens on port `8080` by default.

## Running with Docker

Build and run the container:

```bash
docker build -t mock-service .
docker run -p 8080:8080 mock-service
```

The image runs as a non-root user and includes a built-in health check
against `GET /health` every 30 seconds.

## CI/CD Pipeline

This project ships with a GitHub Actions pipeline (`.github/workflows/ci.yml`)
that mirrors the kind of security-conscious, multi-stage deployment process
used in production environments — built here with free, open-source tooling
so anyone can run it.

**What it does, stage by stage:**

1. **Lint & Test** — runs `flake8` and `pytest` against the codebase before
   anything else happens.
2. **SAST Scan (Semgrep)** — scans the source code itself for common
   security issues (injection risks, unsafe patterns, etc.) before an image
   is even built.
3. **Build Image** — builds the Docker image using Buildx, with layer
   caching to keep runs fast.
4. **Image Scan & Severity Gate (Trivy)** — scans the built image for
   known vulnerabilities in the base image and dependencies. This is the
   core design decision in the pipeline: **CRITICAL/HIGH severity findings
   fail the build**, while LOW/MEDIUM findings are reported but don't block
   deployment. This avoids the two common failure modes teams run into —
   shipping known-dangerous vulnerabilities, or drowning developers in
   alert fatigue over low-risk findings.
5. **Push to GHCR** — once the image passes the security gate, it's pushed
   to GitHub Container Registry, tagged with the short commit SHA.
6. **Deploy to Staging** — deploys the scanned, approved image to a staging
   environment.
7. **Manual Approval Gate** — the pipeline pauses and waits for a human to
   explicitly approve production promotion (configured via GitHub
   Environments), rather than deploying straight to production automatically.
8. **Deploy to Production** — deploys the same image that was tested and
   scanned, ensuring what's running in production is exactly what passed
   every prior stage.

**Why this matters for a real business:** every image that reaches
production has been linted, scanned for code-level and dependency-level
vulnerabilities, and explicitly approved by a human — with none of that
slowing down day-to-day development, since only serious findings actually
block a build.

## Notes

Staging and production deploy steps in the pipeline are placeholders —
swap them out for your actual deploy target (a VM, a cloud platform, or a
Kubernetes cluster via `kubectl`/Helm/ArgoCD).
