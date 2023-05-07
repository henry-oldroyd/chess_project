# code from: https://realpython.com/python-logging/

import logging

def logging_decorator_factory(lgr):
    def decorator(function):
        name = function.__name__
        
        def wrapper(*args, **kwargs):
            lgr.info(f"Beginning execution of function:  {name}  with arguments  {(args, kwargs)}")
            try:
                result = function(*args, **kwargs)  
            except Exception as e:
                lgr.error(f"execution of function: {name}  with arguments  {(args, kwargs)} failed with exception  {str(e)[:80]}")
                raise
            else:
                out = str(result).replace("\n", " ").replace("\t", " ")[:200]
                lgr.info(f" function  {name}  finished and returned:   {out}")
                return result

        wrapper.__name__ = name
        
        return wrapper
    return decorator



# def setup_logger(name, file_path='log.log', c_level='INFO', f_level='INFO'):
def setup_logger(name, log_file_dir, level="INFO", clear=True):
    # clear log file:
    if clear:
        with open(log_file_dir, 'w') as file:
            file.write("")
    
    
    # Create a custom logger
    logger = logging.getLogger(name)
    # Create handlers
    c_handler = logging.StreamHandler()


    f_handler = logging.FileHandler(log_file_dir)
    # f_handler.setLevel(file_level)
    # c_handler.setLevel(console_level)
    logger.setLevel(level)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    
    logger.info(f"this logger named {name} created")

    return logger




if __name__ == "__main__":
    setup_logger(name=__name__)