# Run the webapp and kernel_program in separate processes

# webapp is a Flask app (in webapp/main.py relative to this main.py)
# kernel_program is a Python script (in kernel_program/main.py relative to this main.py)

import sys
import logging
import asyncio
import time
import webbrowser

from multiprocessing import Process

from gpt_code_ui.webapp.main import app, APP_PORT
from gpt_code_ui.kernel_program.main import main as kernel_program_main, cleanup_kernel_program

APP_URL = "http://localhost:%s" % APP_PORT

def run_webapp():
    try:
        app.run(host="0.0.0.0", port=APP_PORT, use_reloader=False)
    except Exception as e:
        logging.exception("Error running the webapp:")
        sys.exit(1)

def run_kernel_program():
    try:
        asyncio.run(kernel_program_main())
    except Exception as e:
        logging.exception("Error running the kernel_program:")
        sys.exit(1)

def setup_logging():
    log_format = "%(asctime)s [%(levelname)s]: %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    log_filename = "app.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)

def print_color(text, color="gray"):
    # Default to gray
    code="242"

    if color == "green":
        code="35"
    
    gray_code = "\033[38;5;%sm" % code
    reset_code = "\033[0m"
    print(f"{gray_code}{text}{reset_code}")


def print_banner():
        
        print("""
  ___  _____  ___  _____   _____           _         
 / _ \|  _  |/ _ \|_   _| /  __ \         | |        
/ /_\ \ | | / /_\ \ | |   | /  \/ ___   __| | ___    
|  _  | | | |  _  | | |   | |    / _ \ / _` |/ _ \   
| | | \ \_/ / | | |_| |_  | \__/\ (_) | (_| |  __/   
\_| |_/\___/\_| |_/\___/   \____/\___/ \__,_|\___|   
                                                     
                                                     
 _____      _                           _            
|_   _|    | |                         | |           
  | | _ __ | |_ ___ _ __ _ __  _ __ ___| |_ ___ _ __ 
  | || '_ \| __/ _ \ '__| '_ \| '__/ _ \ __/ _ \ '__|
 _| || | | | ||  __/ |  | |_) | | |  __/ ||  __/ |   
 \___/_| |_|\__\___|_|  | .__/|_|  \___|\__\___|_|   
                        | |                          
                        |_|                          
        """)

        print("> Open AOAI Code Interpreter in your browser %s" % APP_URL)
        print("")
        print("You can inspect detailed logs in app.log.")
        print("")
        print_color("Forked from GPT-Code UI at https://github.com/shawnmittal/gpt-code-ui-azure")
        print_color("AOAI Code Budgeter at https://github.com/jogeorg/gpt-code-budget")

def main():
    setup_logging()

    webapp_process = Process(target=run_webapp)
    kernel_program_process = Process(target=run_kernel_program)

    try:
        webapp_process.start()
        kernel_program_process.start()

        # Poll until the webapp is running
        while True:
            try:
                app.test_client().get("/")
                break
            except:
                time.sleep(0.1)
        
        print_banner()    
        
        webbrowser.open(APP_URL)

        webapp_process.join()
        kernel_program_process.join()

        
    except KeyboardInterrupt:
        print("Terminating processes...")
        
        cleanup_kernel_program()
        kernel_program_process.terminate()

        webapp_process.terminate()

        webapp_process.join()
        kernel_program_process.join()

        print("Processes terminated.")
        
if __name__ == '__main__':
    main()
