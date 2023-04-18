from datetime import datetime
from typing import List
import numpy as np
def date_filter(
            start_date:str = None,
            end_date: str = None):
      """Building filters for the API call"""
      # Date time objects
      format = "%Y-%m-%dT%H:%M:%S%z"
      start_date = datetime.strptime(start_date, "%y-%m-%d")
      end_date = datetime.strptime(end_date, "%y-%m-%d")
      # Date Filter
      filter = {
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                "gt": start_date.strftime(format),
                "lte": end_date.strftime(format)
                }
            }
      return filter

def cloud_cover(
            lower_than: np.int32 = None,
            greater_than: np.int32 = None):
      """Filtering the cloud cover"""
      lt = lower_than/100
      gt = greater_than/100
      filter = {
            "type": "RangeFilter",
            "field_name": "cloud_cover",
            "config": {
                "lt": lt,
                "gt": gt
                }
            }
      return filter

def string_in_filter():
      """Filtering instrument"""
      filter = {
            "type": "StringInFilter",
            "field_name": "instrument",
            "config": ["PS2"]
            }
      return filter

def permission_filter():
      """Permission filter"""
      filter = {
            "type": "PermissionFilter",
            "config": ["assets.analytic:download"]
            }
      return filter

def geometry_filter(coordinates_bbox: List = None):
      """Filtering with an AOI
      
      Args:
        coordinates_bbox: List of the bbox coordinates[Lon, Lat]
      """
      filter = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": {
                "type": "Polygon",
                "coordinates": [coordinates_bbox]}
            }
      return filter