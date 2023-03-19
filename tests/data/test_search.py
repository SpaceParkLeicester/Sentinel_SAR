from oil_storage_tanks.data.asf_data import asf_search

def test_asf_search():
    """Testing asf search"""
    asf_data = asf_search()
    asf_data.metadata()