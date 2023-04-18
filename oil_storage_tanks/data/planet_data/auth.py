import os
import requests
import logging
import json
from pprint import pprint

def planet_auth()-> None:
    """Authenticating Planet with API KEY"""
    log = logging.getLogger(__name__)
    PLANET_APIKEY = os.environ.get('PLANET_APIKEY')
    try:
        assert PLANET_APIKEY is not None
    except AssertionError as e:
        log.debug("Make sure to add PLANET APIKEY as the env variable")
    
    # Base URL
    base_url = 'https://api.planet.com/data/v1'
    session = requests.session()
    session.auth = (PLANET_APIKEY, "")

    # Making a request
    req = session.get(base_url)

    if req.status_code == 200:
        log.info("Planet data Authentication successful")
    else:
        log.debug("Planet data authentication unsuccessful")
    
    return req

if __name__ == "__main__":
    p = planet_auth()
    pprint(p.json())
