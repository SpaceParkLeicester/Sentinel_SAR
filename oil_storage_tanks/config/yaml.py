"""Data Pre-processing workflow"""
import yaml
from typing import List
import os

class yaml_config():
    """Functions for the SAR pre-process workflow"""
    def __init__(
            self,
            path_to_download:str = None,
            pre_process_output:str = None,
            gpt_location:str = None) -> None:
        """Define the variables
        
        Args:
            path_to_downloads: Folder the downloaded zip file (eg: "~/Downloads")
            pre_process_output: Folder where the preprocessed data need to be stored
            gpt_location: gpt application located in the bin folder of snap ('~/snam/bin/gpt')
        """
        self.path_to_download = path_to_download
        self.pre_process_output = pre_process_output
        self.gpt_location = gpt_location
    
    def test_config_file(
            self,
            config_folder:str = None)-> None:
        """Create the config file
        
        Args:
            config_folder: Path to all  config files folder
        """
        # Creating a config file for the pre-process
        self.sample_config_path = os.path.join(config_folder, 'sample_config_file.yaml')
        with open(self.sample_config_path) as stream:
            self.data = yaml.safe_load(stream)
            self.data['input_folder'] = self.path_to_download
            self.data['output_folder'] = self.pre_process_output
            self.data['gpt_location'] = self.gpt_location
            stream.close()
        
        self.test_config_path = os.path.join(config_folder, 'test_config_file.yaml')
        with open(self.test_config_path, 'wb') as stream:
            yaml.safe_dump(
                self.data, stream, default_flow_style=False,
                explicit_start=True, allow_unicode=True, 
                encoding='utf-8')
            stream.close()
    
    def load_config(
            self,
            bbox: List = None)-> None:
        """Load the config file with user input
        
        Args:
            bbox: A list containing the four corner coordinates
        """
        # Getting the coords
        lower_lat = bbox[0][1]
        lower_lon = bbox[0][0]
        upper_lat = bbox[2][1]
        upper_lon = bbox[2][0]

        # Configuring the test config file with Lat and Lon
        with open(self.test_config_path) as stream:
            self.data = yaml.safe_load(stream)
            self.data['region']['lr']['lat'] = lower_lat
            self.data['region']['lr']['lon'] = lower_lon
            self.data['region']['ul']['lat'] = upper_lat
            self.data['region']['ul']['lon'] = upper_lon

            self.data['single_file'] = 'yes'
            stream.close()
        
        # Dumping new info
        with open(self.test_config_path, 'wb') as stream:
            yaml.safe_dump(
                self.data, stream, default_flow_style=False, 
                explicit_start=True, allow_unicode=True, encoding='utf-8')
            stream.close()
    
            
