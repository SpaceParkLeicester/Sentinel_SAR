from oil_storage_tanks.jobs.sar_data import sar_download

class preprocess_sar(sar_download):
    """Inheriting SAR download pipeline"""
    def __init__(self) -> None:
        super().__init__()