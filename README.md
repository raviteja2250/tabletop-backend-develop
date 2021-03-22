# tabletop-backend

## Installation

1/ Ensure you have python, postgres in your OS

2/ Setup virtual environment (optional)

```sh
    python3 -m venv `path/to/environment`
```

3/ Installl requirements (Should load virtual env if you use it)

```sh
    cd path/to/repository
    pip install -r requirements.txt
```

3/ Setup database

```sh
    psql postgres
    CREATE ROLE user WITH LOGIN ENCRYPTED PASSWORD 'password';
    CREATE DATABASE database_name;
    GRANT ALL PRIVILEGES ON DATABASE database_name TO user;
```

4/ Setup and migrate database

```sh
    make migrate
```

**If you meet any errors in this step, plese use those command**

```sh
    python manage.py make_migrations
    python manage.py migrate
```

5/ Create superuser (This is the super user to login the admin site) (Should load virtual env if you use it)

```sh
    python manage.py createsuperuser
```

## Environment (In case you use virtual environment)

1/ Load environment

```sh
    source `path/to/environment/bin/activate`
```

2/ Deactivate environment

```sh
    deactivate
```

## Run Server (Should load virtual env if you use it)

1/ Run server (development)

```sh
    make run_dev
```

2/ Run server (production)

```sh
    make run_prod
```
