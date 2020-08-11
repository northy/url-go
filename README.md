# URL Go

URL Go is a simple python3 flask application designed to provide an open source url shortener service.

You can check for a live demo of URL Go on [go.northy.xyz](https://go.northy.xyz)

## How to install

To install URL Go , you need to:
```sh
git clone https://github.com/northy/url-go.git
cd url-go
```

### Installing dependencies

URL Go uses pipenv to manage dependencies, so install pipenv with:
```sh
sudo pip install -r requirements.txt
```
or:
```sh
sudo pip install pipenv pipenv-shebang
```

## Configuration

To configure URL Go, you need to edit `url_go/settings.py`, with the options being as follows:

* SERVER_NAME (string) - The URL for the server to listen requests on. This can be your domain if you are hosting on one.
* SQLALCHEMY_DATABASE_URI (string) - [RFC-1738](https://www.ietf.org/rfc/rfc1738.txt) compilant URL that indicates SQLAlchemy how to connect to the database. For more information on how to create the url, check [this link](https://docs.sqlalchemy.org/en/13/core/engines.html)
* HCAPTCHA_ENABLED (boolean) - True or False value to enable hCaptcha service when creating new shortened URLs.
  - HCAPTCHA_SITE_KEY (string) - Site key for hcaptcha.
  - HCAPTCHA_SECRET_KEY (string) - Secret key for hcaptcha.
* LIMIT_SHORTENS (boolean) - True or False value that indicates if you want to limit how much shortens an user is able to make until a refresh request is made.
  - LIMIT_COUNT (integer) - The numeric value of how much shortens the user can make.
* MINIMUM_URL_LENGTH (integer) - Numeric value that represents the minimum length of the shortened URL.
* URL_OFFSET (integer) - Numeric offset for the first URL value.
* URL_ALPHABET (string) - String of characters that will be used to create the shortened URLs.

### Example configuration file:

```python
import string

SERVER_NAME = "127.0.0.1:5001"
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

HCAPTCHA_ENABLED = False
HCAPTCHA_SITE_KEY = ''
HCAPTCHA_SECRET_KEY = ''

LIMIT_SHORTENS = False
LIMIT_COUNT = 0

MINIMUM_URL_LENGTH = 4
URL_OFFSET = 0
URL_ALPHABET = string.ascii_letters + string.digits
```

### Configuring database:

After changing the configuration file, run `create_db.py` to generate the tables on the database.

```sh
pipenv run python create_db.py
```

## Running URL Go

If you are running URL Go on a test environment, you can use the following command to run the server:

```sh
pipenv run flask run
```

However, that's not recommended by flask, so you should use a production WSGI server instead. A WSGI configuration file is present as `webapp.wsgi`, where you should change `"/PATH/TO/APP/"` to the path of the URL Go folder.

### WSGI on apache

If you are running apache, you can install [mod_wsgi](https://modwsgi.readthedocs.io/en/develop/) to run the application.

An example Virtual Host configuration for apache would be:
```
<VirtualHost *:80>
    ServerAdmin admin@SERVER_NAME
    ServerName SERVER_NAME
    WSGIScriptAlias / /PATH/TO/APP/webapp.wsgi
    <Directory /PATH/TO/APP/>
        Options FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

### Refreshing the url limit
To refresh the url limits, just make a web request to SERVER_NAME/refresh.
```sh
curl SERVER_NAME/refresh
```

You can also add a cron job to do this periodically. An example cron job for running each hour would be:
```
0 * * * * /usr/bin/curl --silent --show-error -m 120 SERVER_NAME/refresh &>/dev/null
```

Note that the refresh job will only be completed if the issuer address is `127.0.0.1`

## Libraries used:
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Main web framework
* [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) - Install and manage environments
* [pipenv-shebang](https://pypi.org/project/pipenv-shebang/) - Shebang for pipenv
* [SQLAlchemy](https://www.sqlalchemy.org/) - Manage SQL Database
* [python-dotenv](https://pypi.org/project/python-dotenv/) - Load environment files
* [requests](https://requests.readthedocs.io/en/master/) - Manage requests
* [passlib](https://passlib.readthedocs.io/en/stable/) - Hash and verify passwords