import os
import logging
from bs4 import BeautifulSoup

from snapista import Graph
from snapista import Operator
from snapista import TargetBand
from snapista import TargetBandDescriptors


class esa_snap_graph():
    """Pre-process Graph of ESA SNAP"""
    def __init__(
            self, 
            xml_folder:str = None,
            log:isinstance = None) -> None:
        self.xml_folder = xml_folder
        self.graph = Graph()
        self.log = logging.getLogger(__name__)

    def read_grd(
            self,
            manifest_path:str = None)-> None:
        """Read the GRD S1-data manifest file

        Args:
            manifest_path: Path to the manifest file GRD S1
        """
        self.log.info(f"Reading the manifes file from {manifest_path}")
        self.read = Operator('Read')
        self.read.formatName = 'SENTINEL-1'
        self.read.file = manifest_path
    
    def apply_orbit_file(self)-> None:
        """Applying orbit file"""
        self.orbit = Operator('Apply-Orbit-File')
        self.orbit.orbitType = 'Sentinel Precise (Auto Download)'
        self.polyDegree = '3'
        self.continueOnFail = 'true'
    
    def remove_grd_border_noise(self)-> None:
        """Removing GRD_Border noise"""
        self.grd_border_noise = Operator('Remove-GRD-Border-Noise')
        self.grd_border_noise.borderLimit = '500'
        self.grd_border_noise.trimThreshold = '5'
    
    def calibration(self)-> None:
        """Calibrating"""
        self.calibrating = Operator('Calibration')
    
    def terrain_correction(self)-> None:
        """Terrain Correction"""
        self.terrain_correct = Operator('Terrain-Correction')
        self.terrain_correct.sourceBands = 'Remove-GRD-Border-Noise'
        self.terrain_correct.pixelSpacingInMeter = '10.0'
        self.terrain_correct.pixelSpacingInDegree = '8.983152841195215E-5'
    
    def subset(self, wkt_string)-> None:
        """Subsetting (clipping) the data with WKT"""
        self.spatial_subset = Operator('Subset')
        self.spatial_subset.sourceBands = 'Sigma0_VH'
        self.spatial_subset.region = '0,0,0,0'
        self.spatial_subset.geoRegion = wkt_string
        self.spatial_subset.copyMetadata = 'true'
    
    def speckle_filter(self)-> None:
        """Speckle filter for the subset"""
        self.speckle_filtering = Operator('Speckle-Filter')
        self.speckle_filtering.sourceBands = 'Sigma0_VH'
        self.speckle_filtering.filer = 'Refined Lee'
        self.speckle_filtering.estimateENL = 'true'
    
    def linear_to_from_db(self)-> None:
        """ Converts bands to/from dB"""
        self.linear_to_db = Operator('LinearToFromdB')
        self.linear_to_db.sourceBandNames = 'Sigma0_VH'
    
    def write_file(self, dim_file:str = None)-> None:
        """writes the data product of the file"""
        filepath = os.path.join(self.xml_folder, dim_file)
        self.write_data = Operator('Write')
        self.write_data.file = filepath

    def add_node(self)-> None:
        """Adding node to the graph"""
        self.log.info("Adding Read node to the graph")
        self.graph.add_node(
            operator = self.read,
            node_id = 'Read')
        self.log.info("Adding Orbit node to the graph")
        self.graph.add_node(
            operator = self.orbit,
            node_id = 'Apply-Orbit-File',
            source = 'Read')
        self.log.info("Adding 'Remove GRD Border Noise' node to the graph")
        self.graph.add_node(
            operator = self.grd_border_noise,
            node_id = 'Remove-GRD-Border-Noise',
            source = 'Apply-Orbit-File')
        self.log.info("Adding calibration node to the graph")
        self.graph.add_node(
            operator = self.calibrating,
            node_id = 'Calibration',
            source = 'Remove-GRD-Border-Noise')
        self.log.info("Adding 'terrain-correction' node to the graph")
        self.graph.add_node(
            operator = self.terrain_correct,
            node_id = 'Terrain-Correction',
            source = 'Calibration')
        self.log.info("Adding 'Subset' node to the graph")
        self.graph.add_node(
            operator = self.spatial_subset,
            node_id = 'Subset',
            source = 'Terrain-Correction')
        self.log.info("Adding 'speckle-filter' to the graph")
        self.graph.add_node(
            operator = self.speckle_filtering,
            node_id = 'Speckle-Filter',
            source = 'Subset')
        self.log.info("Adding 'LinearToFromdB' to the graph")
        self.graph.add_node(
            operator = self.linear_to_db,
            node_id = 'LinearToFromdB',
            source = 'Speckle-Filter')
        self.log.info("Adding 'Write' to the graph")
        self.graph.add_node(
            operator = self.write_data,
            node_id = 'Write',
            source = 'LinearToFromdB')
    
    def write_xml(
            self,
            filename:str = None)-> None:
        """Writing data into xml file"""
        filepath = os.path.join(self.xml_folder, filename)
        self.graph.save_graph(filename = filepath)

if __name__ == "__main__":
    manifest_path = 'data/SAFE/S1A_IW_GRDH_1SDV_20230301T175145_20230301T175210_047454_05B27C_E425.SAFE/manifest.safe'
    xml_folder = 'data/pre_process/graphs'
    filename = 'data.xml'
    dim_file = 'data.dim'
    wkt_string = 'POLYGON ((-3.1213777475678892 58.7484157729458332, -3.1213231887020512 58.7484157729458332, -3.1213231887020512 58.9282800941295761, -3.1213777475678892 58.9282800941295761, -3.1213777475678892 58.7484157729458332))'

    create_graph = esa_snap_graph(
        xml_folder = xml_folder)
    create_graph.read_grd(manifest_path = manifest_path)
    create_graph.apply_orbit_file()
    create_graph.remove_grd_border_noise()
    create_graph.calibration()
    create_graph.terrain_correction()
    create_graph.subset(wkt_string = wkt_string)
    create_graph.speckle_filter()
    create_graph.linear_to_from_db()
    create_graph.write_file(
        dim_file = dim_file)
    create_graph.add_node()
    create_graph.write_xml(filename = filename)