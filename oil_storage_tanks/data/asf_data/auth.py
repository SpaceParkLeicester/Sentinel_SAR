"""Function to Authenticate EARTH DATA credentials"""
import os
import numpy as np
import json
import logging
from getpass import getpass
try:
    import asf_search as asf
    from oil_storage_tanks.utils import logger
except ImportError as e:
    logging.debug(f"Import error: {e}")


class earthdata_auth():
    """Authenticating crednetials"""
    def __init__(
            self,
            path_to_cred_file: str = None,
            log = None) -> None:
        """Declaring variables
        
        Args:
            path_to_cred_file: Path to the crednetial file
            log: Custom logging configuration
        """
        self.path_to_cred_file = path_to_cred_file
        try:
            self.log = logger()
        except NameError as e:
            self.log = logging.getLogger(__name__)
            self.log.debug(f"Resolve the bug: {e}")
    
    def auth(self) -> np.int64:
        """Authenticating the EARTHDATA login details"""
        # Checking the path to the credential file
        if not os.path.exists(self.path_to_cred_file):
            # Setting up the username and password
            earthdata_link = "https://www.earthdata.nasa.gov/"
            self.log.debug(f"For details, visit: {earthdata_link}")
            self.log.info("Enter you EARTHDATA username")
            username = input("Username:")
            self.log.info("Enter your EARTHDATA password")
            password = getpass("Password:")
        else:
            self.log.info("Getting info from the credential file")
            with open(self.path_to_cred_file) as f:
                earthdata = json.load(f)
                username = earthdata['username']
                password = earthdata['password']
                f.close()          

        try:
            self.user_pass_session = asf.ASFSession().auth_with_creds(
                username = username,
                password = password
            )
        except asf.ASFAuthenticationError as e:
            self.log.debug(f"Authentication failed:\n{e}")
            return 401
        else:
            self.log.info("User Authentication Successful!")
            return self.user_pass_session

if __name__ == "__main__":
   path_to_cred_file = ".private/earthdata_cred.json"
   earthdata = earthdata_auth(
       path_to_cred_file = path_to_cred_file)
   earthdata.auth()
