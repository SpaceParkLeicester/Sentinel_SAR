import numpy as np
from shapely.wkt import loads

from src.data import AuthCredentials, OilTerminals
from src.utils import stitch_strings

class SearchSciHubData(AuthCredentials):
    """Functions to search data in scihub"""
    def __init__(
            self,             
            log: isinstance = None) -> None:
        """Inheriting and declaring variables
        
        Args:
            data_service: Name of the data service, eg: "Copernicus"
            log: Custom logger function
        """        
        super().__init__(log)
        self.api = super().scihub_auth()
    
    def footprint(
            self,
            half_side: np.int32 = 20,
            location_name: str = None)-> None:
        """Getting the foot print
        
        Args:
            half_side: Length of the half side of AOI in Km.
            location_name: Name of the location from xlsx file
        """
        # Initiating oil terminal data
        oil_terminals = OilTerminals()
        data_dict = oil_terminals.read_data()
        self.foot_print = oil_terminals.bounding_box(
            center_lat = data_dict[location_name][0],
            center_lon = data_dict[location_name][1],
            half_side = half_side)
        return self.foot_print
    
    def query(
            self,
            start_date:str = '2023-03-01',
            end_date:str = '2023-05-15',
            platform_name:str = 'Sentinel-1',
            product_type:str = 'GRD'):
        """Function to query scihub
        
        Args:
            start_date: Start date of the search. eg: 2023-02-01
            end_date: End date of the search, eg: 2023-03-30
            platformname: Name of the platform, Sentinel-1
            producttype: Type of the sentinel-1 data product, eg: 'SLC', 'GRD' 
        """
        # Getting the dates
        start_date = start_date.split('-')
        start_date = stitch_strings(start_date)
        end_date = end_date.split('-')
        end_date = stitch_strings(end_date)

        # Getting the polygon object
        self.aoi = loads(self.foot_print)

        # Getting the products
        self.products = self.api.query(self.aoi,
                     date=(start_date, end_date),
                     platformname=platform_name,
                     producttype=product_type)
        return self.api.to_dataframe(self.products) # Returning a dataframe of the results

    def swath_aoi_check(self):
        """This function helps to filter swaths which has AOI"""
        # Checking if the AOI falls within the downloadable swaths
        self.products_df = self.api.to_dataframe(self.products)
        swath_polygons = self.products_df['footprint'].values

        for i in range(len(swath_polygons)):
            multi_polygon = loads(swath_polygons[i])
            if self.aoi.within(multi_polygon):
                self.log.info("Desired swath has been identified!")
                self.uuid = self.products_df['uuid'][i]
                self.title = self.products_df['title'][i]
                break
            else:
                self.log.debug("No desired swath has been identified!")
                self.log.debug("Reduce the half-side, as desired AOI should not cross the footprint")
                self.log.debug("Happens if the desired AOI is near to the edge")
                self.log.debug("<========================================================>")
                self.log.debug("Expand the search parameters such as datetimes")
                self.log.debug("and make sure the foot print is on the land")
                self.uuid = None
                self.title = None
        
        return self.title, self.uuid 
        # Returns the title S1A_IW__XXX_XXXXXX
        # Returns uuid 3ae4b23xxxxxxxxxxxxxxxx
    
