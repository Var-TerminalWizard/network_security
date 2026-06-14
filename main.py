from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

import sys

if __name__=='__main__':
    try:
        training_pipeline_config = TrainingPipelineConfig()

        data_ingestion_config = DataIngestionConfig(
            training_pipeline_config=training_pipeline_config
        )

        data_ingestion = DataIngestion(
            data_ingestion_config=data_ingestion_config
        )

        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

        print(training_pipeline_config.pipeline_name)
        print(training_pipeline_config.artifact_name)
        print(data_ingestion_artifact)

        logging.info(f"Data validation started")
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(
            data_validation_config=data_validation_config,
            data_ingestion_config=data_ingestion_config
        )
        logging.info(f"Initiate Data validation")
        data_validation_artifact = data_validation.initialize_data_validation()
        logging.info(f"Data validation completed")
        print(data_validation_artifact)
    except Exception as e:
            raise NetworkSecurityException(e,sys)
