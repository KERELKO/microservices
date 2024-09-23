# Microservices example

*Simple microservices example of communication through gRPC and RabbitMQ*

### Overview
![image](https://github.com/user-attachments/assets/f2c25a16-f6e9-499f-b62f-c13425db5eb3)

## Technologies
1. [gRPC](https://grpc.io/)
2. [FastAPI](https://fastapi.tiangolo.com/)
3. [RabbitMQ](https://www.rabbitmq.com/)
4. [MongoDB](https://www.mongodb.com/)
5. [PostgreSQL](https://www.postgresql.org/)
6. [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## How to Use

### Requirements
1. [Docker](https://www.docker.com/)
2. [Docker Compose](https://docs.docker.com/compose/)

### Install & Run
1. Clone the repository
```
git clone https://github.com/KERELKO/microservices
```
2. Add `.env` files and fill them with proper variables in `.env.example` in each service. Run this commands from the root directory
```
cd product_service
cat .env.example > .env
cd ../auth_service
cat .env.example > .env
```
3. Run services with *Docker* in the root directory with command
```
./entrypoint.sh
```
### Usage
After installing and running *Docker containers* you must see API docs on your 
local machine on the url `http://127.0.0.1:8001/api/docs` (*auth-service*) and `http://127.0.0.1:8000/api/docs` (*product-service*)

## Testing
To test functionality of the services you can use `Postman` or `pytest`, also you can use swagger, but only for endpoints that does not have `Cookie` requirements
> [!IMPORTANT]
> On the moment (*23.09.2024*) API docs (swagger) cannot set cookies, so it will always throw `401 Unauthorized` to *product-service* api calls

### Pytest
You can run tests with pytest in *product-service* with command (only in `product_service` directory) 
```
pytest tests/
```
this command will execute all available tests for the *product-service*  
there are available e2e tests that ensure communication with *auth-service* and *product-service*
## Project Structure
```
.
├── auth_service
│   ├── docker-compose.yaml
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── grpc_
│   │   ├── __init__.py
│   │   ├── unary_auth_pb2_grpc.py
│   │   ├── unary_auth_pb2.py
│   │   ├── unary_auth_pb2.pyi
│   │   └── unary_auth.proto
│   ├── Makefile
│   ├── poetry.lock
│   ├── pyproject.toml
│   └── src
│       ├── common
│       │   ├── config.py
│       │   ├── db
│       │   │   ├── __init__.py
│       │   │   └── sqlalchemy
│       │   │       ├── config.py
│       │   │       ├── __init__.py
│       │   │       └── models.py
│       │   ├── di.py
│       │   ├── dto.py
│       │   ├── exceptions.py
│       │   ├── __init__.py
│       │   └── utils.py
│       ├── entrypoints
│       │   ├── fastapi_app.py
│       │   ├── grpc_server.py
│       │   ├── __init__.py
│       │   └── rabbitmq_consumer.py
│       ├── services
│       │   ├── auth.py
│       │   ├── exceptions.py
│       │   └── __init__.py
│       ├── storages
│       │   ├── __init__.py
│       │   └── repositories
│       │       ├── base.py
│       │       └── impl.py
│       └── web
│           ├── exceptions.py
│           ├── handlers.py
│           ├── __init__.py
│           └── schemas.py
├── entrypoint.sh
├── LICENSE
├── Makefile
├── message_broker
│   ├── docker-compose.yaml
│   └── rabbitmq
│       └── log
├── product_service
│   ├── docker-compose.yaml
│   ├── Dockerfile
│   ├── grpc_
│   │   ├── __init__.py
│   │   ├── unary_auth_pb2_grpc.py
│   │   ├── unary_auth_pb2.py
│   │   ├── unary_auth_pb2.pyi
│   │   └── unary_auth.proto
│   ├── main.py
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── src
│   │   ├── common
│   │   │   ├── config.py
│   │   │   ├── container.py
│   │   │   ├── dto.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── repositories
│   │   │   ├── base.py
│   │   │   ├── __init__.py
│   │   │   └── mongo.py
│   │   ├── services
│   │   │   ├── base.py
│   │   │   ├── exceptions.py
│   │   │   ├── impl.py
│   │   │   └── __init__.py
│   │   └── web
│   │       ├── handlers.py
│   │       ├── __init__.py
│   │       ├── middlewares.py
│   │       ├── schemas.py
│   │       └── utils.py
│   └── tests
│       ├── e2e
│       │   ├── conftest.py
│       │   ├── __init__.py
│       │   └── test_gw_communication.py
│       └── __init__.py
└── README.md

24 directories, 71 files
```
