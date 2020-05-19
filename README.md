# Executor

An executor API to safely execute Python 3.8 code using Docker

## Requirements

Simple requirements render happy developers:

- Docker
- Docker Compose

## Architecture

Executor uses 2 services: an API service and an executor service. The API service serves as a safe API to call from an extarnal application that is guaranteed not to be touched by the executed code and to always return a response. The executor service is a service that gets called by the API service and `execs` the code contained inside the request body. If nothing fails, the executor service returns the content of the program's `stdout` to the API call and then the API service can return that content to the external application.

## Querying the API

To query the API and get the code evaluated, the `web` (API) service must be called using an HTTP `POST` request to the `/execute` endpoint, with a body containing the code inside the `content` key.

## Testing locally

To test this locally, first generate an environmental file and adjust its values:

```
cp .env.example .env
```

Then, build the container images:

```
docker-compose build
```

Finally, start the containers:

```
docker-compose up
```
