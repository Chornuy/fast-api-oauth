# define an alias for the specfic python version used in this file.
FROM python:3.11.6-slim-bullseye as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

ENV PIPENV_CUSTOM_VENV_NAME=env

ENV PIPENV_CUSTOM_VENV_NAME=env

ARG USER_UID=1000
ARG GROUP_GID=1000
ARG USER_NAME=app

ARG GROUP_NAME=app
ARG HOME_DIR=/home/${USER_NAME}

ARG USER

ARG APP_FOLDER=/app
ARG APP_PATH=/var${APP_FOLDER}

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}


RUN pip install --upgrade pip setuptools wheel pipenv

RUN set -eux; \
	groupadd -r ${GROUP_NAME} --gid=${GROUP_GID}; \
	useradd -r ${USER_NAME} -g ${GROUP_NAME} --home-dir=${HOME_DIR} --uid=${USER_UID}; \
    mkdir -p ${HOME_DIR} ; \
	chown -R ${USER_NAME}:${GROUP_NAME} ${HOME_DIR}


# Python build stage
FROM base as python-build-stage

RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc


# Install python dependencies in /.venv
USER $USER_NAME
WORKDIR /opt/app

COPY --chown=$USER:$USER \
    Pipfile Pipfile.lock ./

RUN pipenv sync --dev

# Python 'run' stage
FROM base as python-run-stage

#COPY --from=python-build-stage /.venv /.venv
#ENV PATH="/.venv/bin:$PATH"


WORKDIR ${APP_PATH}

# explicitly set user/group IDs
#RUN set -eux; \
#	groupadd -r ${GROUP_NAME} --gid=${GROUP_GID}; \
#	useradd -r ${USER_NAME} -g ${GROUP_NAME} --home-dir=${HOME_DIR} --uid=${USER_UID}; \
#    mkdir -p ${HOME_DIR} ; \
#	chown -R ${USER_NAME}:${GROUP_NAME} ${HOME_DIR}

# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Gpg keys \
  gnupg \
  # helper for requests
  curl \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/* \
  && pip install pipenv


# grab gosu for easy step-down from root
# https://github.com/tianon/gosu/releases
ENV GOSU_VERSION 1.16

RUN set -eux; \
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends ca-certificates wget; \
	rm -rf /var/lib/apt/lists/*; \
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	gpgconf --kill all; \
	rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark > /dev/null; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false; \
	chmod +x /usr/local/bin/gosu; \
	gosu --version; \
	gosu nobody true


# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
#COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
#RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
#	&& rm -rf /wheels/


COPY --chmod=755 .provisions/docker/fast-api/dev/docker-entrypoint.sh /usr/local/bin/
RUN mkdir /docker-startup-script

USER ${USER_NAME}

COPY --from=python-build-stage --chmod=755 --chown=$USER_NAME:$USER_NAME \
    /home/$USER_NAME/.local/share/virtualenvs/$PIPENV_CUSTOM_VENV_NAME \
    /home/$USER_NAME/.local/share/virtualenvs/$PIPENV_CUSTOM_VENV_NAME

ENV  PATH="/home/$USER_NAME/.local/share/virtualenvs/$PIPENV_CUSTOM_VENV_NAME/bin:$PATH"


ENTRYPOINT ["docker-entrypoint.sh"]

# copy application code to WORKDIR
COPY . ${APP_PATH}

CMD [ "uvicorn", "app.fast_api_app:app", "--host", "0.0.0.0", "--port", "8080", "--reload" ]
