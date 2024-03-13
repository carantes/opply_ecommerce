# Opply E-Commerce Workspace

## Overview

### Features

### High Level Design

### Database

## Requirements

Before run this project you need to have the following dependencies installed

- Python 3.9
- Make
- Docker
- Docker-Compose

## Quick Start

To run this project you just need to run the following shortcut. It will start all the resources, load the initial seed on the database, build and run the api.

```
make run-docker
```

Navigate to the api entrypoint

```
http://localhost:8000/api/
```

## Development Workflow

During development, you can modify the Django code, and the **changes will be automatically detected and applied**. Any new dependency needs to be added to the `requirements.txt` using `pip freeze > ./opply_project/requirements.txt`.

## Configuration

**Django Settings**: The project-specific Django settings are located in the config/settings/ directory. You can modify these files to adjust the project's configuration based on your needs.

**Database**: This project uses PostgreSQL as the database. Each module tables are organized on different schemas (identity, products, orders) and are living on two different servers (Primary/Secondary) with auto-replication.

## Resources

### Database (Postgres)

- Primary
- Secondary

### Cache (Redis)

## Admin

1. Create a super user

```
make create-superuser
```

2. Access the django admin url

```
http://localhost:8000/admin/
```

## Relevant libraries

- Django
- Django Rest Framework
- Django Environ
- Django Rest Framework Simple JWT
- Django Guid
- Pytest
- Pytest-Django

# Deployment instructions

TODO: some deployment instructions to AWS

# TODO

- Improve Tests
  - OK api contracts
  - models
  - serializers
- Configure database to high-scalability
  - Primary/Secondary
  - Different schemas?
- Audit Logs on models + Order history

## Nice to have

- Batch Inventory update endpoint
- Cache (products)
  - Cache aside strategy (read from cache and fallback to db)
  - Updates to product inventory and orders re-writes the cache
- Retry with idempotency
  - Each request id is stored in memory
  - Duplicated requests return from cache
- Product Categories and [Filters](https://django-filter.readthedocs.io/en/stable/guide/usage.html) on product list
