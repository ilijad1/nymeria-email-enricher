class Config:
    SECRET_KEY = ""
    APP_PORT = "5055"
    APP_LOG_LOCATION = "nymeria_enricher.log"
    APP_LOG_LEVEL = "DEBUG"
    APP_LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    ELASTICSEARCH_HOST = "http://localhost"
    ELASTICSEARCH_PORT = "9200"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    NYMERIA_API_KEY = ""
    NYMERIA_EMAIL_API_URL = "https://www.nymeria.io/api/v2/emails"
    UPLOAD_UNPARSED_CSV_PATH = "/files/csv/unparsed"
    UPLOAD_PARSED_CSV_PATH = "/files/csv/parsed"



