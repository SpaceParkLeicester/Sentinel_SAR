"""Function to Authenticate EARTH DATA credentials"""
import os
import asf_search as asf
from sentinelsat import SentinelAPI, SentinelAPIError


class AuthCredentials():
    """Authenticating credentials"""
    def __init__(self,log: isinstance = None) -> None:
        """Declaring variables
        
        Args:
            log: Custom logging configuration
        """
        self.log = log

        # EARTHDATA Credentials
        self.EARTHDATA_USERNAME = os.environ.get('EARTHDATA_USERNAME')
        self.EARTHDATA_PASSWORD = os.environ.get('EARTHDATA_PASSWORD')

        # Copernicus scihub account credentials
        self.SCIHUB_USERNAME = os.environ.get('SCIHUB_USERNAME')
        self.SCIHUB_PASSWORD = os.environ.get('SCIHUB_PASSWORD')

        # Planet API KEY
        self.PLANET_APIKEY = os.environ.get('PLANET_APIKEY')


    def earthdata_auth(self)-> None:
        """Earthdata authentication with credentials"""
        try:
            assert self.EARTHDATA_USERNAME is not None
            assert self.EARTHDATA_PASSWORD is not None
        except AssertionError as e:
            self.log.debug("Make sure EARTHDATA credentials are added to env variables")
            self.log.debug("Create an EARTHDATA account in the below link")
            self.log.debug("http://urs.earthdata.nasa.gov.")

        try:       
            self.log.info("Authenticating EARTHDATA account!")
            self.user_pass_session = asf.ASFSession().auth_with_creds(
                username = self.EARTHDATA_USERNAME,
                password = self.EARTHDATA_PASSWORD)
        except asf.ASFAuthenticationError as e:
            self.log.error(f"Authentication failed:\n{e}")
            earthdata_link = "https://www.earthdata.nasa.gov/"
            self.log.debug(f"For details, visit: {earthdata_link}")
            return None
        else:
            self.log.info("User Authentication Successful!")
            return self.user_pass_session
    
    def scihub_auth(self):
        """Copernicus scihub authentication"""
        try:
            assert self.SCIHUB_USERNAME is not None
            assert self.SCIHUB_PASSWORD is not None
        except AssertionError as e:
            self.log.debug("Make sure scihub credentials are added as env variables")
            self.log.debug("Create scihub account by visiting the link below")
            self.log.debug("https://scihub.copernicus.eu/dhus/#/self-registration")
         
        try:
            self.log.info("Authenticating Copernicus scihub account!")
            # Initiate Sentinel API
            scihub_link = 'https://scihub.copernicus.eu/dhus'
            self.api = SentinelAPI(
                self.SCIHUB_USERNAME, self.SCIHUB_PASSWORD,
                scihub_link)
        except SentinelAPIError as e:
            self.log.error(f"Authentication error: {e}")
            return e
        else:
            self.log.info("Authentication successful!")
            return self.api