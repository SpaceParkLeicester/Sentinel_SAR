from snapista import Graph
from snapista import Operator
from snapista import TargetBand
from snapista import TargetBandDescriptors
import logging
# from oil_storage_tanks.utils import logger

class esa_snap_graph():
    """Pre-process Graph of ESA SNAP"""
    def __init__(self, log:isinstance = None) -> None:
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
    
    def terrain_coorection(self)-> None:
        """Terrain Correction"""
        self.terrain_correct = Operator('Terrain-Correction')
        self.terrain_correct.sourceBands = ['Sigma0_VH','Sigma0_VV']    
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
            source = 'Apply-Orbit-File'
        )
        self.log.info('Adding calibration node to the graph')
        self.graph.add_node(
            operator = self.calibrating,
            node_id = 'Calibration',
            source = 'Remove-GRD-Border-Noise'
        )

        self.graph.view()


if __name__ == "__main__":
    manifest_path = 'data/SAFE/S1A_IW_GRDH_1SDV_20230301T175145_20230301T175210_047454_05B27C_E425.SAFE/manifest.safe'
    graph_view = esa_snap_graph()
    graph_view.read_grd(manifest_path = manifest_path)
    graph_view.apply_orbit_file()
    graph_view.add_node()