import os
import click
import pandas as pd
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data.asf_data import search_earthdata
from oil_storage_tanks.data.asf_data import download_asf


class search_results_datapipe():
    """Datapipe to download and save search results"""
    def __init__(
            self,
            path_to_uk_terminals: str = None,
            csv_file_save_path: str = None,
            start_date:str = None,
            end_date:str = None) -> None:
        
        """Defining the variables"""    
        self.path_to_uk_terminals = path_to_uk_terminals
        self.csv_file_save_path = csv_file_save_path
        self.start_date = start_date
        self.end_date = end_date
        self.log = logger()
    
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
                start_date = self.start_date,
                end_date = self.end_date,
                log = self.log
                )
            search.metadata()
            self.csv_search_results_path = search.save_search(
                csv_file_save_path = self.csv_file_save_path)
            
            # Updating path list
            self.csv_path_list.append(self.csv_search_results_path)
        
        return self.csv_path_list

@click.command()
@click.option('--start_date')
@click.option('--end_date')
@click.option('--path_to_uk_terminals', type=click.Path(exists=True), default = 'data/uk_oil_terminals.xlsx')
@click.option('--csv_file_save_path', type=click.Path(exists=True), default = 'data/s1_data_search_results')
def search(
    path_to_uk_terminals,
    csv_file_save_path,
    start_date, 
    end_date):
    datapipe = search_results_datapipe(
        path_to_uk_terminals = path_to_uk_terminals,
        csv_file_save_path = csv_file_save_path,
        start_date = start_date,
        end_date = end_date
    )
    datapipe.get_dictionary()
    datapipe.write_search()

if __name__ == "__main__":
    search()