"""Basic functions needed"""
from typing import List

def stitch_strings(
        strings: List, 
        separator: str):
    """Function to stich strings"""
    return separator.join(strings)