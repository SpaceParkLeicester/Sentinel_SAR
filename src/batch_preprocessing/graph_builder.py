import os
from snapista import Graph
from snapista import Operator


class esa_snap_graph():
    """Pre-process Graph of ESA SNAP"""
    def __init__(
            self, 
            xml_folder:str = 'data/pre_process/graphs',
            processed_data_folder:str = 'data/pre_process/processed',
            safe_folder_path:str = None,                      
            log:isinstance = None) -> None:
        """Defining variables

        Args:
            xml_folder: folder to save xml graphs
            processed_data_folder: folder to the processed files
            safe_folder_path: Path to the SAFE folder
            manifest_path: Path to the manifest file GRD S1        
        """
        self.xml_folder = xml_folder
        self.safe_folder_path = safe_folder_path
        self.processed_data_folder = processed_data_folder
        self.graph = Graph()
        self.log = log

    def read_grd(self)-> None:
        """Read the GRD S1-data manifest file"""
        self.read = Operator('Read')
        self.read.formatName = 'SENTINEL-1'
        self.read.file = self.safe_folder_path

    def polarisation_stamp(self)-> None:
        """Determining the polarisation stamp of the file"""
        # Getting the filename
        self.manifest_path = os.path.join(self.safe_folder_path, 'manifest.safe')
        self.uuid = os.path.basename(os.path.dirname(self.manifest_path))
        self.polstamp = self.uuid.split("_")[3]
        self.polarization = self.polstamp[2:4]
        if self.polarization == 'DV':
            self.pols = ['VH','VV']
        elif self.polarization == 'DH':
            self.pols = ['HH','HV']
        elif self.polarization == 'SH' or self.polarization == 'HH':
            self.pols = ['HH']
        elif self.polarization == 'SV':
            self.pols = ['VV']
        else:
            self.pols = None
            self.log.error("Polarization error!")
        
        if not self.pols is None:
            self.log.info(f"Product {self.uuid} is of polarisation {self.pols}")

    def sourcing_polarisation(
            self,
            band_type: str = None)-> None:
        """Sourcing bands
        
        Args:
            band_type: Selecting a polarisation, eg: VV, VH, HH, HV
        """
        if band_type in self.pols:
            self.sourcebands = f'Sigma0_{band_type}'
        else:
            self.sourcebands = None
            self.log.debug(f"Polarisation '{band_type}' is not present")
            self.log.debug(f"in the file {self.safe_folder_path}")
    
    def apply_orbit_file(self)-> None:
        """Applying orbit file"""
        self.orbit = Operator('Apply-Orbit-File')
        self.orbit.orbitType = 'Sentinel Precise (Auto Download)'
        self.continueOnFail = 'true'
    
    def remove_grd_border_noise(self)-> None:
        """Removing GRD_Border noise"""
        self.grd_border_noise = Operator('Remove-GRD-Border-Noise')
    
    def calibration(self)-> None:
        """Calibrating"""
        self.calibrating = Operator('Calibration')
        self.calibrating.auxFile = 'Product Auxiliary File'
    
    def terrain_correction(self)-> None:
        """Terrain Correction"""
        self.terrain_correct = Operator('Terrain-Correction')
        # self.terrain_correct.sourceBands = 'Remove-GRD-Border-Noise'
        self.terrain_correct.pixelSpacingInMeter = '10.0'
        self.terrain_correct.pixelSpacingInDegree = '8.983152841195215E-5'
    
    def subset(
            self, 
            wkt_string)-> None:
        """Subsetting (clipping) the data with WKT
        
        Args:
            wkt_string: Polygon string of an AOI
        """
        self.spatial_subset = Operator('Subset')
        self.spatial_subset.sourceBands = self.sourcebands
        self.spatial_subset.geoRegion = wkt_string
        self.spatial_subset.copyMetadata = 'true'
    
    def speckle_filter(self)-> None:
        """Speckle filter for the subset"""
        self.speckle_filtering = Operator('Speckle-Filter')
        self.speckle_filtering.sourceBands = self.sourcebands
        self.speckle_filtering.filter = 'Refined Lee'
        self.speckle_filtering.estimateENL = 'true'
    
    def linear_to_from_db(self)-> None:
        """ Converts bands to/from dB"""
        self.linear_to_db = Operator('LinearToFromdB')
        self.linear_to_db.sourceBands = self.sourcebands
    
    def write_file(
            self,
            output_filename:str = None)-> None:
        """writes the data product of the file
        
        Args:
            output_filename: Location name as the output filename
        """
        processed_data = os.path.join(self.processed_data_folder, output_filename)
        processed_data = os.path.join(os.getcwd(), processed_data)
        if not os.path.exists(processed_data):
            os.makedirs(processed_data)
        self.write_data = Operator('Write')
        self.write_data.file = os.path.join(processed_data, output_filename)

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
            graph_xml:str = None)-> None:
        """Writing data into xml file
        
        Args:
            graph_xml: put location name as Filename of the graph file
        """
        filepath = os.path.join(self.xml_folder, graph_xml+'.xml')
        filepath = os.path.join(os.getcwd(), filepath)
        self.graph.save_graph(filename = filepath)
        return filepath
    
    def graph_view(self)-> None:
        """Run the Graph"""
        # Viewing the graph
        self.log.info("The Graph XML")
        self.graph.view()


if __name__ == "__main__":
    xml_folder = 'data/pre_process/graphs'
    filename = 'data.xml'
    wkt_string = 'POLYGON ((-0.1906563590715226 53.68193630164516, -0.1906563590715226 53.60662686944885, -0.3176973248804094 53.60662686944885, -0.3176973248804094 53.68193630164516, -0.1906563590715226 53.68193630164516))'
    create_graph = esa_snap_graph(
        xml_folder = xml_folder)
    create_graph.read_grd()
    create_graph.polarisation_stamp()
    create_graph.apply_orbit_file()
    create_graph.remove_grd_border_noise()
    create_graph.calibration()
    create_graph.terrain_correction()
    create_graph.subset(wkt_string = wkt_string)
    create_graph.speckle_filter()
    create_graph.linear_to_from_db()
    create_graph.write_file()
    create_graph.add_node()
    create_graph.write_xml(filename = filename)