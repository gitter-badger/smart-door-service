import os
import re
import yaml


path_matcher = re.compile(r'\${([^}^{]+)\}')


# Extract the matched value, expand env variable, and replace the match
def path_constructor(loader, node):
    value = node.value
    match = path_matcher.match(value)
    env_var = match.group()[2:-1]

    if os.environ.get(env_var) is "" or os.environ.get(env_var) is None:
        return ""

    return os.environ.get(env_var) + value[match.end():]


# Load database configuration from app/config/database.yml file
def get_database_adapter(base_dir):
    with open(os.path.join(base_dir + "/app/config", "database.yml")) as stream:
        try:

            yaml.add_implicit_resolver('!path', path_matcher)
            yaml.add_constructor('!path', path_constructor)

            config = yaml.load(stream)

            if os.getenv("DB_ADAPTER") == "mysql":
                return mysql(config.get("mysql"))

            if os.getenv("DB_ADAPTER") == "sqlite3":
                return sqlite3(config.get("sqlite3"))

            if os.getenv("DB_ADAPTER") == "postgresql":
                return postgresql(config.get("postgresql"))

        except yaml.YAMLError as exc:
            print(exc)


# Mysql configration data
def mysql(config):
    return {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config['name'],
            'USER': config['user'],
            'PASSWORD': config['password'],
            'HOST': config['host'],
            'PORT': config['port'],
        }
    }


# Sqlite3 configration data
def sqlite3(config):
    return {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': config['name'],
        }
    }


# Postgresql configration data
def postgresql(config):
    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config['name'],
            'USER': config['user'],
            'PASSWORD': config['password'],
            'HOST': config['host'],
            'PORT': config['port'],
        }
    }
