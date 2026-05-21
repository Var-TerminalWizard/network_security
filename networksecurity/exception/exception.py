import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self,message,details:sys):
        self.message = message
        _, _, tb = details.exc_info()
        
        self.lineno = tb.tb_lineno
        self.filename = tb.tb_frame.f_code.co_filename
    
    def __str__(self):
        self.filename, self.lineno, str(self.error_message)
        return f"Error occurred in file: {self.filename} at line: {self.lineno} with message: {self.message}"

if __name__ == "__main__":
    try:
        logger.logging.info("This is a test log message.")
        a=1/0
        print("This will not be printed",a)
    except Exception as e:
        raise NetworkSecurityException(e,sys)