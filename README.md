# auv-control-api

This is main API code for managing AUV's, planning trips, logging data.

## Development

### With Docker

```bash
$ docker-compose build
$ docker-compose run web python manage.py migrate
$ docker-compose run web python manage.py createsuperuser
$ docker-compose up
```

### Without Docker

```bash
$ export DEBUG=True
$ export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME`
$ export SECRET_KEY=somethingsecret
```

For other database backends see: 
https://github.com/kennethreitz/dj-database-url

### Run migrations
```bash
$ python manage.py migrate
```

### Create Superuser
```bash
$ python manage.py createsuperuser
```

### Run Development Server
```bash
$ python manage.py runserver
```

### Create AUV
Go to `localhost:8000/admin` and create an AUV for testing with the Frontend.


