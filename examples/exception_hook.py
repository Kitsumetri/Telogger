from telogger import Telogger

def main():
    tlogger = Telogger()
    tlogger.enable_global_exception_hook()
    
    # Trigger an unhandled exception
    raise ValueError("Something went terribly wrong!")

if __name__ == "__main__":
    main()