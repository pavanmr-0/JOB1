Render Docker deployment guide

This project includes a `Dockerfile` and `entrypoint.sh` to produce a container suitable for deployment to Render (and for local testing).

Overview
- We use Docker to ensure system-level dependencies for `weasyprint`, `Pillow`, and `psycopg2` are available during build.
- `render.yaml` is configured to use Docker; Render will use the repository `Dockerfile` to build the image.

Pre-requisites
- Push your repository to GitHub (or other Git provider supported by Render).
- If you want PostgreSQL, create a managed database on Render and set `DATABASE_URL` env var accordingly.
- Set the following Render environment variables (Web Service -> Environment):
  - `SECRET_KEY`: choose a secure secret (or use the generated one Render created in `render.yaml` if you keep it)
  - `DEBUG`: `false`
  - `DATABASE_URL`: (optional) Postgres URL if using managed DB

Local Docker test (recommended, requires Docker installed locally)
1. From repo root, build the image:
```powershell
docker build -t jobportal:local .
```
2. Run container (pass minimal env):
```powershell
docker run -p 8000:8000 -e SECRET_KEY="dev-secret" -e DEBUG=true jobportal:local
```
3. Visit `http://localhost:8000` to verify the site boots.

Notes about `entrypoint.sh`
- `entrypoint.sh` runs `migrate` and `collectstatic` before starting Gunicorn.
- For production you should ensure `DATABASE_URL` points to a persistent Postgres instance and set `DEBUG=false`.

Render setup steps
1. Go to Render dashboard -> New -> Web Service.
2. Connect your GitHub repo and select the repository.
3. For "Environment", choose "Docker" (Render will detect the `Dockerfile`).
4. Set the branch to deploy.
5. In Environment, add required env vars (`SECRET_KEY`, `DEBUG=false`, `DATABASE_URL` if using DB).
6. Create and wait for the build to finish. The Dockerfile installs system packages and pip requirements, runs migrations and collectstatic, then starts Gunicorn.

Troubleshooting
- Build fails with missing system packages: the `Dockerfile` installs common dependencies required by `weasyprint` and `psycopg2`. If you see missing libs, paste the Render build logs and I'll update the Dockerfile accordingly.
- If static files 404: ensure `collectstatic` ran successfully during build or at startup; check logs for `collectstatic` output.

If you'd like, I can prepare a small `render-production.yaml` variant, create a one-click Render Deploy button, or help you configure a managed Postgres instance and set `DATABASE_URL`.
