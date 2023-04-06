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
            log = None) -> None:
        """Declaring variables
        
        Args:
            data_service: Type of the data serivce, eg: 'EARTHDATA', 'scihub'
            path_to_cred_file: Path to the crednetial file
            log: Custom logging configuration
        """
        self.data_service = data_service
        self.path_to_cred_file = path_to_cred_file
        self.log = log
    
    def credentials(self)-> None:
        """Set the credentials"""
        if not os.path.exists(self.path_to_cred_file):
            self.log.info(f"Enter {self.data_service} details below")
            self.log.info("Enter you username")
            self.username = input("Username:")
            self.password = getpass("Password:")

    def earthdata_auth(self):
        """Earthdata authentication with credentials"""
        if os.path.exists(self.path_to_cred_file):
            self.log.info("Getting info from the credential file")
            with open(self.path_to_cred_file) as f:
                earthdata = json.load(f)
                self.username = earthdata['earthdata_user']
                self.password = earthdata['password']
                f.close()             

        try:
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
            # Reading the credential file
            self.log.info("Getting info from the credential file")
            with open(self.path_to_cred_file) as f:
                scihub = json.load(f)
                self.username = scihub['scihub_user']
                self.password = scihub['password']
                f.close()
            
            try:
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