# Recurse Center disco Community Server

## how to dev

### setting up the project locally

- create a new postgres database locally
- in this repo directory, duplicate `.env.example` to `.env` and fill it out
- run:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

- start the server with `python manage.py runserver`
- do good work

### running the project (after you've set it up)

```bash
source venv/bin/activate
python manage.py runserver
```

---

### deploying this with disco

[See the documentation](https://docs.letsdisco.dev/deployment-guides/django-site) to deploy this with Disco.

-----

[powered by minimalish django starter](https://github.com/gregsadetsky/minimalish-django-starter) 