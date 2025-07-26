# 📄 Change Log

All notable changes to this project will be documented in this file 🙌🏽

## [1.0.0]
### Initial
- Initialized Django project inside `devops/` directory
- Created Django application called `demo` inside the `devops/demo/` folder.
- Added `requirements.txt` via `pip freeze`
- Built a `Dockerfile` using `python:3.13-slim`
  - Installed dependencies inside container
  - Set working directory to `/app`
  - Exposed port `8000`
  - Ran Django development server using `CMD`
- Handled `ALLOWED_HOSTS` settings to include EC2 public IP
- Added `.dockerignore` (e.g., `__pycache__/`, `.DS_Store`, `db.sqlite3`, etc.)
- Verified app is accessible via: `curl http://<EC2-PUBLIC-IP>:8000/`
