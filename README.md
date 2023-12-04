# school-todo-backend
A simple todo rest api written in python for an exam in application security.
If nothing else is defined with an environemnt variable the username is admin, the password is admin and the admin role will also be called Admin.

This version of the api is very unsecure, I couldn't manage to create sqlinjection, I'm litteraly to secure at programming but XSS sure as hell will work in combination with the frontend oh welp and the secret_key for the JWT token isn't that secret I reccon. So here we have 2 major security implications.

The environementvariables are:
- ADMIN_USER
- ADMIN_PASSWORD

Development Server:
```bash
flask run --debug --port 8080
```
Build the docker container:
```bash
docker build -t school-todo-backend:1.0.0 .
```
Run in root directory of the project.

Best used with school-todo-frontend but can be independent.
docker-compose file on request available.