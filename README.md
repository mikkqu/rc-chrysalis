# Social Chrysalis

Social Chrysalis is a Flask-based social network to encourage pairing activities at Recurse Center.

## Getting started

A preferable way to get started:

- Make sure your python3 version is up to date (3.7.0 supported but latest should be fine)
- Make sure your mongodb is up to date and running well (4.0.1 supported but latest should be fine)
- Create a python virtual environment: `python -m venv venv/`
- Activate the environment: `. venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- For local development, copy example config `cp config.py.ex config.py` and fill the configuration values as shown below:

```
DEBUG               # true or false
SECRET_KEY          # long secret string for flask security purposes
CONSUMER_KEY        # app key from RC directory
CONSUMER_SECRET     # app secret from RC directory
MONGO_URI           # mongo uri in a format: mongodb://server:port/db
```

- Start by running the app `python run.py`

First logging in may take a long time, up to a few minutes, due to fetching resources from RC server into database. Get yourself a coffee.
