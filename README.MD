# Opply E-Commerce Workspace

# Overview

This is an assessment to build the backend of a mobile application to Opply customers. This app will allow users to order products using their phones.

## Requirements

### Product

- Customers may exchange their username and password for an authentication token
- Customers may see a paginated list of products. Each product in the list should have the following details: id, name, price, and quantity in stock
- Customers may order the products they need
- Number of products in stock should decrease after an order is made
- Customers may see their history of orders.

### Technical

- Django 4.x (any modules, any data structures)
- API only, no need for UI
- Production ready
- Deployment instructions to AWS

## High Level Design

![alt text](assets/high-level-design-opply.png)

## Database Schema (Logical)

![alt text](assets/database-logical-schema-opply.png)

# How to run this project?

## Requirements

Before run this project you need to have the following dependencies installed

- Python 3.9
- Docker
- Docker-Compose
- Make (optional)

## Quick Start

To start this project you just need to run the following shortcut. It will start all the resources on docker, load the initial seed on the database, build and run the api.

```
make run-docker
```

Once the app is running you can authenticate in the Djando Admin and navigate to the apis using the DRF entrypoint route

1. Authenticate in the Django admin (user: opply / password: 123456)

```
http://localhost:8000/admin/
```

![alt text](assets/django-admin.png)

2. Navigate to the DRF entrypoint

```
http://localhost:8000/api/
```

![alt text](assets/drf-api-root.png)

> Most endpoints are protected and will require a Bearer header token if you are not authenticated in the Django admin.

## Endpoints

| Endpoint                 | Method | Description                                         |
| ------------------------ | ------ | --------------------------------------------------- |
| /api/identity/register/  | POST   | Create a new user                                   |
| /api/identity/token/     | POST   | Generates a new token to an existent user           |
| /api/identity/customers/ | \*     | All operations related to customers                 |
| /api/catalog/products/   | \*     | All operations related to products                  |
| /api/orders/orders/      | POST   | Place an order with order items                     |
| /api/orders/orders/      | GET    | Get a list of all orders for the authenticated user |
| /api/orders/orders/{id}  | GET    | Get details of a specific order                     |

## Development Workflow

During development, you can modify the Django code, and the **changes will be automatically detected and applied**. Any new dependency needs to be added to the `requirements.txt` using `pip freeze > ./opply_project/requirements.txt`.

## Configuration

**Django Settings**: The project-specific Django settings are located in the config/settings directory. You can modify these files to adjust the project's configuration based on your needs.

**Database**: This project uses PostgreSQL as the database. Each module tables are organized on different schemas (identity, products, orders) and are living on two different servers (Primary/Secondary) with auto-replication.

## Relevant libraries

- Django
- Django Rest Framework
- Django Environ
- Django Rest Framework Simple JWT
- Django Guid
- Pytest
- Pytest-Django

# Deployment instructions

### Django [deployment checklst](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)

- Run the check deploy script
- Provide a production secret key
- Make sure `debug` flag is disabled
- Configure a web server in front of Django application server
- Change `Allowed hosts` to only receive requests from the web server
- Review Django local `CACHE` configuration and move to a more scalable caching solution like Redis or MemCache
- Review `Database` configuration: Cluster, connection pool, secrets, etc
- Serve `Static files` from web server (if needed)
- Use HTTPS
- Review Performance optimizations
- Reduce `Logging` verbosity to production
- Review list and notifications to `Admins` and `Managers`

### Deployment to **AWS**

1. Straighforward option: Deploy to Elastic Beanstalk following the [step-by-step provided by AWS](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)

2. Cheaper and resilient option (preferable): EC2 + RDS (Aurora) + Nginx + Memcache

- Setup AWS account
- Launch a new EC2 instance
- Connect to the machine using SSH
- Install all the required dependencies (Python, pip, virtualenv)
- Setup a new virtualenv
- Upload app project files
- Install required packages from `requirements.txt`
- Setup Database on RDS
- Setup Memcache instances
- Setup ELB and autoscale groups
- Configure a webserver

## Next steps

- Primary / Secondary Postgres database (split read and writes requests)
- Cache (products)
  - Cache aside strategy (read from cache and fallback to db)
  - Updates to product inventory and orders re-writes the cache
- Retry with idempotency
  - Each request id is stored in memory
  - Duplicated requests return from cache
- Product Categories with filters
