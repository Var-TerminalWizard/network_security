from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.config_entity import ModelTrainerConfig


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
        logging.info(f"Data transformation started")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(
            data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config
        )
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info(f"Data transformation completed")
        
        logging.info("Model Training started")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")
    except Exception as e:
            raise NetworkSecurityException(e,sys)
