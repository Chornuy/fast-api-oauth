# ======================================================================
# STAGE 1: Base Runtime Environment Configuration
# ======================================================================
FROM python:3.13.5-slim-bookworm AS base

# Core Python execution optimization defaults
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    UV_LINK_MODE=copy

ARG USER_UID=1000
ARG GROUP_GID=1000
ARG USER_NAME=app
ARG APP_PATH=/var/app

# Provision internal system user profile and application directories ahead of time
RUN set -eux; \
    groupadd -r ${USER_NAME} --gid=${GROUP_GID}; \
    useradd -r ${USER_NAME} -g ${USER_NAME} --home-dir=/home/${USER_NAME} --uid=${USER_UID} --create-home; \
    mkdir -p ${APP_PATH}; \
    chown -R ${USER_NAME}:${USER_NAME} ${APP_PATH}

# ======================================================================
# STAGE 2: High-Speed Dependency Isolation & Compilation
# ======================================================================
FROM base AS builder

# Pull down the high-speed standalone static binary layers for uv
COPY --from=ghcr.io/astral-sh/uv:0.7 /uv /uvx /bin/

# Install tools required to build C/Rust binary wheels (like psycopg2, cryptography)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_PATH}

# Leverage Docker layer caching by analyzing changes to dependencies independently
COPY --chown=${USER_NAME}:${USER_NAME} pyproject.toml uv.lock ./

# Compile a strict relative isolation directory using modern BuildKit caching mounts
RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv .venv && \
    uv sync --frozen --dev

# ======================================================================
# STAGE 3: Clean, Secure Execution Layer Target
# ======================================================================
FROM base AS runner

# Grab native production runtime libraries along with gosu instantly from Debian
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    gosu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR ${APP_PATH}

# Pull down the pre-compiled virtual environment layer from our builder stage
COPY --from=builder --chown=${USER_NAME}:${USER_NAME} ${APP_PATH}/.venv ${APP_PATH}/.venv

# Directly prepend our new local virtual environment binaries straight onto the runtime path execution chain
ENV PATH="${APP_PATH}/.venv/bin:$PATH"

# Set up core runtime volume directories and entrypoint vectors
COPY --chmod=755 .provisions/docker/fast-api/dev/docker-entrypoint.sh /usr/local/bin/
RUN mkdir /docker-startup-script

# CRITICAL: We explicitly reset execution state to root here.
# This gives docker-entrypoint.sh the permissions it needs to step through your
# mounted volume startup hooks. Your entrypoint then handles dropping down to your 'app' account via gosu.
USER ${USER_NAME}

ENTRYPOINT ["docker-entrypoint.sh"]

USER ${USER_NAME}
# Layer in the remainder of your application components
COPY --chown=${USER_NAME}:${USER_NAME} . ${APP_PATH}

CMD [ "uvicorn", "app.fast_api_app:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]
