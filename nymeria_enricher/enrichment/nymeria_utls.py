import requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from flask import flash, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from nymeria_enricher.config import Config

connections.configure(
    # TODO Create profiles and externalize in GLOBAL config
    default={'hosts': 'localhost'},
    dev={
        'hosts': ['localhost:9200'],
        'sniff_on_start': True
    }
)

# nymeria_response = search_nymeria_api_for_emails(linkedin_link, stackoverflow_link, github_link)
#         nymeria_response_status = nymeria_response['status']
#
#         if nymeria_response_status == 'success':


def enrich_candidate_email_init(linkedin_link):
    linkedin_link = ""
    stackoverflow_link = ""
    github_link = ""




def get_email(linkedin_link):
    API_KEY = Config.NYMERIA_API_KEY
    nymeria_api_url = Config.NYMERIA_EMAIL_API_URL

    params = {
        "api_key": API_KEY,
        "linkedin_url": linkedin_link
    }
    # get the response as json format
    response = requests.get(nymeria_api_url, params=params)
    data = response.json()
    #save_raw_nymeria_response(data)

    if data['status'] == 'success' and len(data['data']['emails']) > 0:
        return data['data']['emails'][0]['email']
    else:
        return ""


def save_raw_nymeria_response(nymeria_response):
    es = Elasticsearch()
    # TODO Figure out a way to bypass duplicate entries of same person
    es.index(index="nymeria_emails", body=nymeria_response)
    pass

