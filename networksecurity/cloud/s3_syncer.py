import os
import shutil
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


class S3Sync:
    def sync_folder_to_s3(self, folder: str, aws_bucket_url: str) -> None:
        """
        Local fallback for environments without AWS/Dagshub deployment plumbing.
        Keeps the training pipeline importable and lets local runs finish.
        """
        try:
            if not os.path.exists(folder):
                logging.info(f"Skipping sync because folder does not exist: {folder}")
                return

            logging.info(f"Skipping remote sync for {folder} -> {aws_bucket_url} in local environment")
        except Exception as e:
            raise NetworkSecurityException(e, sys)
