import os
import subprocess 
from pathlib import Path
from oil_storage_tanks.utils import unzip_s1data, logger
from oil_storage_tanks.data import OilTerminals
from oil_storage_tanks.batch_preprocessing import esa_snap_graph 

class preprocess_sar:
    """SAR-preprocessing"""
    def __init__(
            self,
            path_to_zip_file:str = None,
            log:isinstance = None) -> None:
        """Declaring variables
        
        Args:
            path_to_zip_file: Path to the downloaded S1 zip file
            log: Custom log function
        """
        self.path_to_zip_file = path_to_zip_file
        self.log = log
    
    def unzipping_s1data(self)-> None:
        """Unzip the S1 data"""
        self.download_path = Path(self.path_to_zip_file).parent.absolute()
        self.unzip_dir_filename = Path(self.path_to_zip_file).stem
        self.safe_folder_path = unzip_s1data(
            download_path = self.download_path,
            path_to_zip_file = self.path_to_zip_file,
            unzip_dir_filename = self.unzip_dir_filename,
            log = self.log)
        
        # Location name
        self.location_name = os.path.basename(self.download_path)
        # Getting the WKT string
        oilterminal_data = OilTerminals()
        terminal_data = oilterminal_data.read_data()
        location_coords = terminal_data[self.location_name]
        self.wkt_string = oilterminal_data.bounding_box(
            center_lat = location_coords[0],
            center_lon = location_coords[1])
    
    def graph_build(
            self,
            band_type: str = None)-> None:
        """Building the graph for S1 data
        
        Args:
            band_type: Type of the polarisation
        """
        graph = esa_snap_graph(
            safe_folder_path = self.safe_folder_path,
            log = self.log)
        graph.read_grd()
        graph.polarisation_stamp()
        graph.sourcing_polarisation(band_type = band_type)
        graph.apply_orbit_file()
        graph.remove_grd_border_noise()
        graph.calibration()
        graph.terrain_correction()
        graph.subset(wkt_string = self.wkt_string)
        graph.speckle_filter()
        graph.linear_to_from_db()
        graph.write_file(
            output_filename = self.location_name)
        graph.add_node()
        self.xml_filepath = graph.write_xml(graph_xml = self.location_name)


if __name__ == "__main__":
    path_to_zip_file = '/mnt/disks/diss_dir/SAFE/stanlow/S1A_IW_GRDH_1SDV_20230327T062258_20230327T062323_047826_05BF02_706A.zip'
    log = logger()
    sar = preprocess_sar(
        path_to_zip_file = path_to_zip_file,
        log = log)
    sar.unzipping_s1data()
    sar.graph_build(
        band_type = 'VH')
    sar.preprocess()