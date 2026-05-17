# FastAPI OAuth — Clean & Hexagonal Architecture Showcase

> A ready **FastAPI** boilerplate that demonstrates **Clean / Hexagonal Architecture**, app-based project organisation,
> a custom **Beanie ODM extension**, and a full OAuth 2.0 password-flow implementation.

---

## ✨ Key Ideas

| Goal                               | How it is achieved                                                                                                                                                                             |
|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Clean Architecture**             | Every app is split into `api` (transport) → `services` (use-cases) → `repository` (data access) layers; nothing in the inner layers depends on the outer ones.                                 |
| **Hexagonal Architecture**         | Core business logic lives in `app/core/` and `app/libs/`; adapters (FastAPI routers, Beanie documents, email sender) plug in from the outside.                                                 |
| **App-based project organisation** | Each feature (`login`, `oauth`, `registration`, `user`) is an isolated Django-style _app_ with its own router, models, services and tests. A bootstrap pipeline auto-discovers and loads them. |
| **Beanie ODM extension**           | `libs/beanie_odm_ext` adds a generic `BaseRepository` with `create`, `get`, `find_one_or_error`, `get_or_create` helpers on top of Beanie/Motor.                                               |
| **OAuth 2.0**                      | Password grant-type flow via a pluggable `BaseOauthFlowManager` in `libs/oauth_flow`.                                                                                                          |

---

## 🗂 Project Structure

```
app/
├── app_bootstrap.py          # Bootstraps the app-loader pipeline
├── fast_api_app.py           # FastAPI application factory
├── apps/
│   ├── login/                # Login feature app
│   ├── oauth/                # OAuth 2.0 token endpoints
│   ├── registration/         # User registration feature app
│   └── user/                 # User management feature app
├── core/
│   ├── auth/                 # Password hashing & verification tokens
│   ├── dependency/           # FastAPI security dependencies
│   ├── email/                # Email configuration & sending
│   ├── exception_handler/    # Global exception handlers
│   ├── exceptions/           # Base & validation exception classes
│   ├── middlewares/          # CORS and other ASGI middlewares
│   ├── pydantic/             # Pydantic helpers / custom fields
│   ├── schemas/              # Shared Pydantic schemas & constants
│   └── security/             # JWT utilities
└── libs/
    ├── app_loader/           # Auto-discovery bootstrap pipeline
    ├── beanie_odm_ext/       # Beanie repository extension
    ├── click_cli/            # Async Click CLI bootstrap
    ├── jwt_auth/             # JWT auth manager & token helpers
    ├── managment/            # Settings management
    ├── oauth_flow/           # Pluggable OAuth grant-type manager
    ├── system_app/           # System-level helpers
    ├── token_generator/      # Secure token generation
    └── utils/                # Shared utilities
```

### Inside every feature app

```text
apps/<feature>/
├── app.py          # App metadata (name, version)
├── models.py       # Beanie Document models
├── repository.py   # Data-access layer (extends BaseRepository)
├── router.py       # Mounts api/ and view/ routers
├── api/            # JSON API endpoints
├── services/       # Business-logic / use-cases
├── templates/      # Jinja2 HTML templates (where applicable)
├── view/           # Server-side rendered view endpoints
├── commands/       # App CLI commands (auto-discovered)
└── tests/
```

---

## 🔑 Core Libraries

### `libs/beanie_odm_ext` — Repository Pattern for Beanie

```python
from app.libs.beanie_odm_ext.repository import BaseRepository
from myapp.models import UserDocument


class UserRepository(BaseRepository):
    __model__ = UserDocument


repo = UserRepository()
user = await repo.create(email="alice@example.com", hashed_password="...")
user = await repo.find_one_or_error(UserDocument.email == "alice@example.com")
user = await repo.get_or_create(UserDocument.email == "alice@example.com",
                                defaults={"hashed_password": "..."})
```

### `libs/oauth_flow` — Extensible Grant-Type Manager

```python
from app.libs.oauth_flow.manager import BaseOauthFlowManager


class MyOauthManager(BaseOauthFlowManager):
    supported_grant_types = ["password", "refresh_token"]

    async def password(self, username, password, **kwargs):
        ...

    async def refresh_token(self, refresh_token, **kwargs):
        ...


manager = MyOauthManager()
token = await manager.process_flow(grant_type="password",
                                   username="alice",
                                   password="secret")
```

### `libs/app_loader` — Auto-Discovery Bootstrap

`ApplicationBootStrap` runs a configurable middleware pipeline at startup:

1. **`AutoImportAppLoader`** — scans `APPS_DIR` and imports every app package.
2. **`BeanieModelLoader`** — collects all `Document` subclasses for Beanie initialisation.
3. **`ClickCommandLoader`** — registers CLI commands from each app's `commands/` directory.

---

## 🚀 Getting Started

### Prerequisites

* Python **3.11+**
* [Pipenv](https://pipenv.pypa.io/)
* Docker & Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/fast-api-oauth.git
cd fast-api-oauth
```

### 2. Install dependencies

```bash
pipenv install --dev
```

### 3. Configure environment

Copy the example env file and fill in the values:

```bash
cp .env.example .env
```

Key variables:

| Variable                        | Description                         |
|---------------------------------|-------------------------------------|
| `MONGO_HOST`                    | MongoDB host (default: `localhost`) |
| `MONGO_PORT`                    | MongoDB port (default: `27017`)     |
| `MONGO_DB_NAME`                 | Database name                       |
| `MONGO_USER` / `MONGO_PASSWORD` | MongoDB credentials                 |
| `SECRET_KEY`                    | JWT signing secret                  |
| `PROJECT_NAME`                  | Displayed in OpenAPI docs           |
| `DEBUG`                         | Enable debug mode                   |
| `MAIL_*`                        | SMTP / MailHog configuration        |

### 4. Start infrastructure (MongoDB + MailHog)

```bash
docker compose up mongo mailhog -d
```

> MongoDB is configured as a **single-node replica set** (`rs0`) to support Beanie transactions.

### 5. Run the development server

```bash
pipenv run uvicorn app.fast_api_app:app --reload --host 0.0.0.0 --port 8080
```

Or via Docker (full stack):

```bash
docker compose up --build
```

The API will be available at:

* **API** → http://localhost:8080
* **Swagger UI** → http://localhost:8080/docs
* **ReDoc** → http://localhost:8080/redoc
* **MailHog UI** → http://localhost:8025

---

## 🧪 Testing

```bash
# Run all tests
pipenv run pytest

# Run with coverage report
pipenv run coverage run -m pytest
pipenv run coverage report -m
```

Tests are co-located with each app under `apps/<feature>/tests/` and share fixtures from `app/conftest.py`.

---

## 🛠 CLI

The project ships an async [Click](https://click.palletsprojects.com/) CLI powered by `asyncclick`:

```bash
pipenv run python manage.py --help
```

Commands are auto-discovered from each app's `commands/` directory.

### Command example inside app structure

Create command modules inside `apps/<feature>/commands/`.

```python
import asyncclick as click
from bson import ObjectId

from app.libs.beanie_odm_ext import transaction
from app.libs.beanie_odm_ext.session import auto_session
from app.libs.beanie_odm_ext.tests.fixtures.click_async import fast_api_cli_test
from app.libs.beanie_odm_ext.tests.fixtures.models import Category, Product


@fast_api_cli_test.command()
@auto_session
@transaction.atomic
async def create_products():
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_cli", category=category, price=10)
    await product.save()
    click.echo(f"{product.name}")


@fast_api_cli_test.command()
@auto_session
@transaction.atomic
async def create_products_with_error():
    click.echo("Creating products...")
    category = Category(name="Test category", description="test description")
    await category.save()
    product = Product(name="product_with_cli_error", category=category, price=10)
    await product.save()
    click.echo(f"{product.name}")
    raise Exception("Product creation failed")


@fast_api_cli_test.command()
@click.argument("product_id")
@auto_session
async def get_product(product_id: str):
    product = await Product.find_one(Product.id == ObjectId(product_id))
    click.echo(f"{str(product.id)}")
```

Command patterns shown above:

- `@auto_session` injects DB session handling.
- `@transaction.atomic` wraps write operations in a transaction.
- `@click.argument(...)` maps CLI args to async handlers.

---

## 📦 Tech Stack

| Layer         | Technology                                                                   |
|---------------|------------------------------------------------------------------------------|
| Web framework | [FastAPI](https://fastapi.tiangolo.com/)                                     |
| ODM           | [Beanie](https://beanie-odm.dev/) (MongoDB async ODM)                        |
| Database      | MongoDB 7 (replica set via Docker)                                           |
| Auth          | JWT via [python-jose](https://python-jose.readthedocs.io/), bcrypt passwords |
| Email         | [fastapi-mail](https://sabuhish.github.io/fastapi-mail/) + MailHog (dev)     |
| OTP           | [pyotp](https://pyauth.github.io/pyotp/)                                     |
| CLI           | [asyncclick](https://github.com/python-trio/asyncclick)                      |
| Validation    | [Pydantic v2](https://docs.pydantic.dev/) + pydantic-settings                |
| Testing       | pytest + pytest-asyncio + polyfactory                                        |
| Linting       | flake8 · isort · black · mypy                                                |

---

## 🏛 Architecture Deep Dive

```
┌─────────────────────────────────────────────┐
│              Transport Layer                │
│  FastAPI Routers  (apps/*/api, apps/*/view) │
└───────────────────┬─────────────────────────┘
                    │  calls
┌───────────────────▼─────────────────────────┐
│             Application Layer               │
│         Services  (apps/*/services)         │
└───────────────────┬─────────────────────────┘
                    │  calls
┌───────────────────▼─────────────────────────┐
│             Domain / Core Layer             │
│  core/auth  core/security  libs/oauth_flow  │
└───────────────────┬─────────────────────────┘
                    │  calls
┌───────────────────▼─────────────────────────┐
│           Infrastructure Layer              │
│  Repositories  (apps/*/repository)          │
│  libs/beanie_odm_ext  →  MongoDB            │
└─────────────────────────────────────────────┘
```

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
