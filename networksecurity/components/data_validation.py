from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import os
import sys
import pandas as pd
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                data_ingestion_config:DataIngestionConfig):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_config = data_ingestion_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self._schema_config["columns"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {dataframe.columns}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def detect_dataset_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame,threshold=0.05)->dict:
        try:
            drift_report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                p_value = ks_2samp(d1,d2).pvalue
                drift_report[column] = {
                    "p_value":float(p_value),
                    "drift_status":p_value <= threshold
                }
                dir_path = os.path.dirname(self.data_validation_config.drift_report_file_path)
                os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(self.data_validation_config.drift_report_file_path, drift_report)
            return drift_report
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initialize_data_validation(self)->DataValidationArtifact:
        try:
            trained_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path
        
            train_df = DataValidation.read_data(trained_file_path)
            test_df = DataValidation.read_data(test_file_path)
        
            train_status = self.validate_number_of_columns(dataframe=train_df)
            test_status = self.validate_number_of_columns(dataframe=test_df)
            validation_status = train_status and test_status

            self.detect_dataset_drift(base_df=train_df,current_df=test_df)

            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)

            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)
            
            data_validation_artifact = DataValidationArtifact(
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                validation_status=validation_status,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
