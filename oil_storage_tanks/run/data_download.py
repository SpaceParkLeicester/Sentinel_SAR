# """Datapipe for the data download"""
# from typing import Optional
# from oil_storage_tanks.data import (
#     s1_data_download,
#     oil_terminals
# )
# from oil_storage_tanks.data import bounding_box as bbox
# from torchdata.datapipes import functional_datapipe
# from torchdata.datapipes.iter import IterDataPipe

# @functional_datapipe("download_s1_data")
# class DownloadS1DataIterDatapipe(IterDataPipe):
#     """Datapipe to download S1 data"""
#     def __init__(
#             self,
#             path_to_terminals: str,
#             path_to_cred_file:str,
#             commence_download: Optional[bool] = False,
#             download_path:Optional[str] = None) -> None:
#         """
#         Declare the variables

#         Args:
#             path_to_terminal: Path to the Oil terminal file which has Lat and Lon
#             download_path: Set the download path
#             path_to_cred_file: Path to the credential file
#             commence_download: If true, starts downloading
#         """
#         self.path_to_terminals = path_to_terminals
#         self.download_path = download_path
#         self.path_to_cred_file = path_to_cred_file
#         self.commence_download = commence_download
    
#     def __iter__(self):
#         # Obtaining the dictionary
#         terminal_dict = oil_terminals(terminal_file_path = self.path_to_terminals)

#         for key, value in terminal_dict.items():
#             # Obtaining the WKT_aoi of the bounding box
#             lat, lon = value
#             wkt_aoi = bbox(
#                 center_lat = lat,
#                 center_lon = lon
#                 )            
#             s1_data = s1_data_download(wkt_aoi = wkt_aoi)
#             s1_data.s1_metadata()
#             if self.commence_download:
#                 # Downloading the data
#                 s1_data.download_data(
#                     download_path = self.download_path,
#                     path_to_cred_file = self.path_to_cred_file)
            
            
