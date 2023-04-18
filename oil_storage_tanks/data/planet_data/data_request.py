import os
import planet
from planet import Auth, Session
import asyncio
from typing import List


def create_request(
        location_name: str = None,
        coordinates_bbox:List = None,
        order_items: List = None):
        """Creating a JSON schema to request
    
        Args:
            location_name: Name of the location
            coordinates_bbox: A list of bounding box coordinates
            order_item: A list of item ids # Search them here https://www.planet.com/explorer/
        """
        # Building an aoi
        aoi = {
            "type":
            "Polygon",
            "coordinates":[coordinates_bbox]
        }
        # Building argument of products
        products = planet.order_request.product(
            item_ids = order_items,
            product_bundle = 'analytic_3b_udm2',
            item_type = 'PSScene')
        order = planet.order_request.build_request(
            name = location_name,
            products = [products],
            tools = [planet.order_request.clip_tool(aoi = aoi)])
        return order

async def main(order):
        auth = Auth.from_env()
        async with planet.Session(auth = auth) as session:
            cl = session.client('orders')
            api_order = await cl.create_order(order)
            
if __name__ == "__main__":
      location_name = 'flotta'
      coordinates_bbox = [
             [-3.148045,58.813194],
             [-3.148045,58.849586],
             [-3.064338,58.849586],
             [-3.064338,58.813194],
             [-3.148045,58.813194]]
      order_items = ['20230415_110555_20_247f', '20230415_110553_01_247f']
      order = create_request(
             location_name = location_name,
             coordinates_bbox = coordinates_bbox,
             order_items = order_items)
      asyncio.run(main(order = order))

        