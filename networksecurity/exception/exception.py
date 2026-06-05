import sys
from networksecurity.logging.logger import logging


class NetworkSecurityException(Exception):
    def __init__(self, error_message: Exception, details=sys):
        super().__init__(str(error_message))
        self.error_message = error_message
        self.filename = None
        self.lineno = None
        try:
            exc_type, exc_value, tb = details.exc_info()
            if tb is not None:
                self.lineno = tb.tb_lineno
                self.filename = tb.tb_frame.f_code.co_filename
        except Exception:
            # fail-safe: keep filename/lineno as None
            pass

    def __str__(self) -> str:
        return (
            f"Error occurred in file: {self.filename} at line: {self.lineno} with message: {self.error_message}"
        )


if __name__ == "__main__":
    try:
        logging.info("This is a test log message.")
        a = 1 / 0
        print("This will not be printed", a)
    except Exception as e:
        raise NetworkSecurityException(e, sys)