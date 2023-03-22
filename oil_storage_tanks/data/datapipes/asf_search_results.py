import os
import pandas as pd
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import search_earthdata
from oil_storage_tanks.data.asf_data import download_asf


class search_results_datapipe():
    """Datapipe to download and save search results"""
    def __init__(
            self, 
            path_to_cred_file: str = None, 
            log = None,
            path_to_uk_terminals: str = None,
            csv_file_save_path: str = None) -> None:
        
        """Defining the variables"""    
        self.path_to_cred_file = path_to_cred_file
        self.path_to_uk_terminals = path_to_uk_terminals
        self.csv_file_save_path = csv_file_save_path
        self.log = log
    
    def get_dictionary(self) -> None:
        """Loading the data into a dictionary"""
        if not os.path.exists(self.path_to_uk_terminals):
            self.log.debug(f"No file detected: {self.path_to_uk_terminals}")
        else:
            self.uk_terminal_df = pd.read_excel(self.path_to_uk_terminals, skiprows=1)
            # Getting data in a dcitionary
            self.regions = self.uk_terminal_df["Region"].tolist()
            self.coords = list(zip(
                self.uk_terminal_df['Lat'],
                self.uk_terminal_df['Lon']))
            self.uk_dict = dict(zip(self.regions, self.coords))
            self.log.info("UK terminal data has been stored in a dict.")
    
    def write_search(self):
        """Writing the search results"""
        # Saving search results for each region"
        self.csv_path_list = []
        for region, coords in self.uk_dict.items():
            self.log.info(f"Searching for {region} oil terminal")
            filename = region.split(',')[0]
            lat, lon = coords
            # Getting the search results into a file.csv
            search = search_earthdata(
                location_name = filename,
                center_coords_lat = lat,
                center_coords_lon = lon,
                log = self.log
                )
            search.metadata()
            self.csv_search_results_path = search.save_search(
                csv_file_save_path = self.csv_file_save_path)
            
            # Updating path list
            self.csv_path_list.append(self.csv_search_results_path)
        
        return self.csv_path_list
            

if __name__ == "__main__":
    path_to_cred_file = ".private/earthdata_cred.json"
    path_to_uk_terminal = "data/uk_oil_terminals.xlsx"
    csv_file_save_path = "data/s1_data_search_results"
    datapipe = search_results_datapipe(
        path_to_cred_file = path_to_cred_file,
        path_to_uk_terminals = path_to_uk_terminal,
        csv_file_save_path = csv_file_save_path,
        log = logger())
    datapipe.get_dictionary()
    datapipe.write_search()