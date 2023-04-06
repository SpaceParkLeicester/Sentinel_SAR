"""Functions to visualise SAR data"""
import numpy as np
import netCDF4 as nc
from ipywidgets import interactive
import matplotlib.pyplot as plt


class sar_visualisation():
    """Visualisation of SAR data"""
    def __init__(
            self,
            path_to_nc_file:str = None,
            log = None) -> None:
        """Defining variables"""
        self.path_to_nc_file = path_to_nc_file
        self.log = log
    
    def load_nc(self)-> None:
        """Loading the netcdf file"""
        self.data = nc.Dataset(self.path_to_nc_file, mode = 'r')
        self.data.variables['orbitdirection'][:]
        self.data.variables['time'][:]
        lons = self.data.variables['lon'][:]
        lats = self.data.variables['lat'][:]
        self.vv = self.data.variables['sigma0_vv_single'][:]

        vv_units = self.data.variables['sigma0_vv_single'].units
        self.data.close()       