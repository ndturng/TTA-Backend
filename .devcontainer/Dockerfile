# 1️⃣  Base: includes non‑root “vscode” user, devcontainer utils, git, etc.
FROM mcr.microsoft.com/devcontainers/python:3.12

# 2️⃣  OS packages for Django + Postgres
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev postgresql-client \
        && rm -rf /var/lib/apt/lists/*

# 3️⃣  Python deps – adjust pins as your project matures
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣  (Optional) Extra tools you want every time
# RUN pip install ipython

CMD ["sleep", "infinity"]

# 5️⃣  Default workdir (devcontainers convention)
WORKDIR /workspaces
