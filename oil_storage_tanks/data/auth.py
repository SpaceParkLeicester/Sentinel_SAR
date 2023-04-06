"""Function to Authenticate EARTH DATA credentials"""
import os
import json
from getpass import getpass
import asf_search as asf
from sentinelsat import SentinelAPI, SentinelAPIError


class auth_credentials():
    """Authenticating crednetials"""
    def __init__(
            self,
            data_service: str = None,
            path_to_cred_file: str = None,
            username:str = None,
            password:str = None,
            log = None) -> None:
        """Declaring variables
        
        Args:
            data_service: Type of the data serivce, eg: 'EARTHDATA', 'scihub'
            path_to_cred_file: Path to the crednetial file
            username: USERNAME of the service, earthdata or scihub
            password: PASSWORD of the service, earthdata or scihub
            log: Custom logging configuration
        """
        self.data_service = data_service
        self.path_to_cred_file = path_to_cred_file
        self.log = log
        if not os.path.exists(self.path_to_cred_file):
            assert username is not None
            assert password is not None
            self.username = username
            self.password = password


    def credentials(self)-> None:
        """Get the credentials"""
        assert os.path.exists(self.path_to_cred_file) is True
        self.log.info("Getting info from the credential file")
        with open(self.path_to_cred_file) as f:
            credentials_data = json.load(f)
            self.earthdata_username = credentials_data['earthdata_username']
            self.earthdata_password = credentials_data['earthdata_password']
            self.scihub_username = credentials_data['scihub_username']
            self.scihub_password = credentials_data['scihub_password']
            f.close()


    def earthdata_auth(self):
        """Earthdata authentication with credentials"""
        if os.path.exists(self.path_to_cred_file):
            self.username = self.earthdata_username
            self.password = self.earthdata_password
        try:
            self.log.info("Authenticating EARTHDATA account!")
            self.user_pass_session = asf.ASFSession().auth_with_creds(
                username = self.username,
                password = self.password
            )
        except asf.ASFAuthenticationError as e:
            self.log.error(f"Authentication failed:\n{e}")
            earthdata_link = "https://www.earthdata.nasa.gov/"
            self.log.debug(f"For details, visit: {earthdata_link}")
            return e
        else:
            self.log.info("User Authentication Successful!")
            return self.user_pass_session
    
    def scihub_auth(self):
        """Copernicus scihub authentication"""
        if os.path.exists(self.path_to_cred_file):
            self.username = self.scihub_username
            self.password = self.scihub_password
         
        try:
            self.log.info("Authenticating Copernicus scihub account!")
            # Initiate Sentinel API
            schihub_link = 'https://scihub.copernicus.eu/dhus'
            self.api = SentinelAPI(
                self.username, self.password,
                schihub_link)
        except SentinelAPIError as e:
            self.log.error(f"Authentication error: {e}")
            return e
        else:
            self.log.info("Authentication successful!")
            return self.api
