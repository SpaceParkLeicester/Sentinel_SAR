from oil_storage_tanks.utils import logger
from sar_pre_processing.sar_pre_processor import *
import warnings
warnings.filterwarnings("ignore")

class steps():
    """Pre-processing steps defined"""
    def __init__(
            self,
            test_config_path:str = None,
            log = None)-> None:
        """ Definig variables

        Args:
            Define path to the test config path from yaml.py
        """
        self.test_config_path = test_config_path
        self.log = log
    
    def preprocessor(self)-> None:
        """Workflow of the pre-processing"""
        processing = SARPreProcessor(config = self.test_config_path)
        processing.create_processing_file_list()
        self.log.info('start step 1')
        processing.pre_process_step1()
        self.log.info('start step 2')
        processing.pre_process_step2()
        self.log.info('start step 3')
        processing.pre_process_step3()
        self.log.info('start add netcdf information')
        processing.add_netcdf_information()
        self.log.info('start create netcdf stack')
        processing.create_netcdf_stack()

if __name__ == "__main__":
    test_config_path = 'data/config/test_config_file.yaml'
    preprocess = steps(
        test_config_path = test_config_path,
        log = logger()
    )
    preprocess.preprocessor()