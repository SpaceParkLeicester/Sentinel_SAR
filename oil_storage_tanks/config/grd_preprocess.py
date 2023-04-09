# Code taken from this github repo - https://github.com/wajuqi/Sentinel-1-preprocessing-using-Snappy
from snappy import ProductIO
from snappy import HashMap
import os, gc
from snappy import GPF
from oil_storage_tanks.utils import logger
from oil_storage_tanks.data import oil_terminals
from oil_storage_tanks.data import bounding_box as bbox

## UTM projection parameters
proj = '''PROJCS["UTM Zone 4 / World Geodetic System 1984",GEOGCS["World Geodetic System 1984",DATUM["World Geodetic System 1984",SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]],UNIT["degree", 0.017453292519943295],AXIS["Geodetic longitude", EAST],AXIS["Geodetic latitude", NORTH]],PROJECTION["Transverse_Mercator"],PARAMETER["central_meridian", -159.0],PARAMETER["latitude_of_origin", 0.0],PARAMETER["scale_factor", 0.9996],PARAMETER["false_easting", 500000.0],PARAMETER["false_northing", 0.0],UNIT["m", 1.0],AXIS["Easting", EAST],AXIS["Northing", NORTH]]'''

def do_apply_orbit_file(source, log):
    log.info('\tApply orbit file...')
    parameters = HashMap()
    parameters.put('Apply-Orbit-File', True)
    output = GPF.createProduct('Apply-Orbit-File', parameters, source)
    return output

def do_thermal_noise_removal(source, log):
    log.info('\tThermal noise removal...')
    parameters = HashMap()
    parameters.put('removeThermalNoise', True)
    output = GPF.createProduct('ThermalNoiseRemoval', parameters, source)
    return output

def do_calibration(source, polarization, pols, log):
    log.info('\tCalibration...')
    parameters = HashMap()
    parameters.put('outputSigmaBand', True)
    if polarization == 'DH':
        parameters.put('sourceBands', 'Intensity_HH,Intensity_HV')
    elif polarization == 'DV':
        parameters.put('sourceBands', 'Intensity_VH,Intensity_VV')
    elif polarization == 'SH' or polarization == 'HH':
        parameters.put('sourceBands', 'Intensity_HH')
    elif polarization == 'SV':
        parameters.put('sourceBands', 'Intensity_VV')
    else:
        log.error("different polarization!")
    parameters.put('selectedPolarisations', pols)
    parameters.put('outputImageScaleInDb', False)
    output = GPF.createProduct("Calibration", parameters, source)
    return output

def do_speckle_filtering(source, log):
    log.info('\tSpeckle filtering...')
    parameters = HashMap()
    parameters.put('filter', 'Lee')
    parameters.put('filterSizeX', 5)
    parameters.put('filterSizeY', 5)
    output = GPF.createProduct('Speckle-Filter', parameters, source)
    return output

def do_terrain_correction(source, proj, downsample, log):
    log.info('\tTerrain correction...')
    parameters = HashMap()
    parameters.put('demName', 'GETASSE30')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('mapProjection', proj)       # comment this line if no need to convert to UTM/WGS84, default is WGS84
    parameters.put('saveProjectedLocalIncidenceAngle', True)
    parameters.put('saveSelectedSourceBand', True)
    while downsample == 1:                      # downsample: 1 -- need downsample to 40m, 0 -- no need to downsample
        parameters.put('pixelSpacingInMeter', 40.0)
        break
    output = GPF.createProduct('Terrain-Correction', parameters, source)
    return output

def do_subset(source, wkt, log):
    log.info('\tSubsetting...')
    parameters = HashMap()
    parameters.put('geoRegion', wkt)
    output = GPF.createProduct('Subset', parameters, source)
    return output

class pre_process():
    """Pipeline of GRD data pre-process"""
    def __init__(
            self,
            grd_folder_path:str = None,
            processed_folder:str = None,
            wkt_string:str = None,
            log = None) -> None:
        """Initiating the variables
        
        Args:
            grd_file_path: Folder path to GRD whcih ends with .SAFE
            processed_folder: Folder to save processed files
            wkr_string: Polygon WKT string of desired AOI
        """
        self.grd_folder_path = grd_folder_path
        self.processed_folder = processed_folder
        self.wkt_string = wkt_string
        self.log = log

        # Grabage collect
        gc.enable()
        gc.collect()

    def collect_data(self)-> None:
        """Collecting from mainfest.safe file"""
        self.manifest_safe_file = os.path.join(self.grd_folder_path, 'manifest.safe')
        self.safe_folder = os.path.basename(self.grd_folder_path)
        if os.path.exists(self.manifest_safe_file):
            self.log.info(f"Reading {self.safe_folder} with snappy python package")
            self.sentinel_1 = ProductIO.readProduct(self.manifest_safe_file)

            ## Extract mode, product type, and polarizations from filename
            self.modestamp = self.safe_folder.split("_")[1]
            self.productstamp = self.safe_folder.split("_")[2]
            self.polstamp = self.safe_folder.split("_")[3]
        else:
            self.log.error(f"No such file exsists {self.manifest_safe_file}")
            self.log.debug("Check the unzipped SAR data")
    
    def polarisation(self)-> None:
        """Determining the polarisation"""
        self.polarization = self.polstamp[2:4]
        if self.polarization == 'DV':
            self.pols = 'VH,VV'
        elif self.polarization == 'DH':
            self.pols = 'HH,HV'
        elif self.polarization == 'SH' or self.polarization == 'HH':
            self.pols = 'HH'
        elif self.polarization == 'SV':
            self.pols = 'VV'
        else:
            self.pols = None
            self.log.error("Polarization error!")
        
        if not self.pols is None:
            self.log.info(f"Product {self.safe_folder} is of polarisation {self.pols}")

    def start_preprocess(self)-> None:
        """Pre-processing steps"""
        self.applyorbit = do_apply_orbit_file(self.sentinel_1, self.log)
        self.thermalremoved = do_thermal_noise_removal(self.applyorbit, self.log)
        self.calibrated = do_calibration(self.thermalremoved, self.polarization, self.pols, self.log)
        self.down_filtered = do_speckle_filtering(self.calibrated, self.log)
        del self.applyorbit
        del self.thermalremoved
        del self.calibrated
    
    def downsample(self)-> None:
        """Downasmpling from 10m to 40m"""
        # IW images are downsampled from 10m to 40m (the same resolution as EW images).
        if (self.modestamp == 'IW' and self.productstamp == 'GRDH') or (self.modestamp == 'EW' and self.productstamp == 'GRDH'):
            self.down_tercorrected = do_terrain_correction(self.down_filtered, proj, 1, self.log)
            self.down_subset = do_subset(self.down_tercorrected, self.wkt_string, self.log)
            del self.down_filtered
            del self.down_tercorrected
        elif self.modestamp == 'EW' and self.productstamp == 'GRDM':
            self.tercorrected = do_terrain_correction(self.down_filtered, proj, 0, self.log)
            self.subset = do_subset(self.tercorrected, self.wkt_string, self.log)
            del self.down_filtered
            del self.tercorrected
        else:
            self.log.debug("Different spatial resolution is found.")
    
    def geotiff_conversion(self)-> None:
        """Get the data in GeoTIFF format"""
        self.geotiff_path_10m = os.path.join(self.processed_folder, self.safe_folder[:-5] + '_10')
        self.geotiff_path_40m = os.path.join(self.processed_folder, self.safe_folder[:-5] + '_40')

        try:
            self.down_subset
            self.log.info(f"Writing the file to {self.geotiff_path_10m}")
            ProductIO.writeProduct(self.down_subset, self.geotiff_path_10m, 'GeoTIFF')
            del self.down_subset
            self.log.info("Writing into GeoTiff is Finished!")
        except NameError:
            self.subset
            self.log.info(f"Writing the file to {self.geotiff_path_40m}")
            ProductIO.writeProduct(self.subset, self.geotiff_path_40m, 'GeoTIFF')
            del self.subset
            self.log.info("Writing into GeoTiff is Finished!")

        self.sentinel_1.dispose()
        self.sentinel_1.closeIO()

if __name__ == "__main__":
    grd_folder_path = 'data/SAFE/S1A_IW_GRDH_1SDV_20230301T175145_20230301T175210_047454_05B27C_E425.SAFE'
    processed_folder = 'data/pre_process'
    terminal_file_path = 'data/uk_oil_terminals.xlsx'
    location_name = 'flotta'
    termial_dict = oil_terminals(terminal_file_path = terminal_file_path)
    for loaction, coords in termial_dict.items():
        if loaction == location_name:
            center_coords_lat = coords[0]
            center_coords_lon = coords[1]
            break
    wkt_string = bbox(
        half_side = 10,
        center_lat = center_coords_lat,
        center_lon = center_coords_lon)
    preprocess = pre_process(
        grd_folder_path = grd_folder_path,
        processed_folder = processed_folder,
        wkt_string = wkt_string,
        log = logger())
    preprocess.collect_data()
    preprocess.polarisation()
    preprocess.start_preprocess()
    preprocess.downsample()
    preprocess.geotiff_conversion()