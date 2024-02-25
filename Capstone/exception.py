import sys 
from Capstone.logger import logging

def error_message_details(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    python_script = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = (f"Error occured in python script {python_script}, at line {line_number}, error message: {str(error)}")
    
    return error_message
    

class CustomException(Exception):
    def __init__(self, error_message, error_details:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_details)
        
    
    def __str__(self):
        return self.error_message
    
 
if __name__ == "__main__":   
    try:
        a = 1/0
    except Exception as e :
        logging.info("Divide by zero error")
        raise CustomException(e, sys)
        