# Development server

- ### Set environment variables

  - `cp .env.example .env`

- ### Build docker

  - `docker-compose build`


### Set up 

  - ### Run python migrations

      - `docker-compose run server python manage.py migrate`

  - ### Create superuser

      - `docker-compose run server python manage.py createsuperuser`

  - ### Run docker

      - `docker-compose up`

