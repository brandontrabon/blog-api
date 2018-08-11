import datetime

APPLICATION_CONFIG = {
    'DB_USER': 'btrabon',
    'DB_PASSWORD': 'btrabon',
    'DB_URI': '127.0.0.1',
    'DB_DATABASE_NAME': 'news_blog'
}

DATABASE_URI = 'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_URI}/{DB_DATABASE_NAME}'.format(**APPLICATION_CONFIG)

# TODO: Need to implement a public/private key pair like this
with open('id_rsa_dev.pub', 'r') as f:
    JWT_PUBLIC_KEY = f.read()
with open('id_rsa_dev', 'r') as f:
    JWT_PRIVATE_KEY = f.read()

JWT_EXPIRATION_TIMESPAN = datetime.timedelta(hours=9)
API_KEY_EXPIRATION_TIMESPAN = datetime.timedelta(days=365)
