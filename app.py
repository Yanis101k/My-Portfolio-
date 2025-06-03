# import Flask to create the web application using flask framework 
from flask import Flask 

# import my custom Config class to load environment variables from the .env file
from config import Config 

# import the logging setup function to enable centralized logging for debugging and monitoring
from logging_config import setup_logging 

# step 1 : Create the Flask app instance 

app = Flask( __name__ )

# step 2 : Load configuration settings from the config class ( includes secret key, DB path, admin username and password etc.)
app.config.from_object(Config)


# step 3: Set up logging ( creates a log file and writes important events )
setup_logging()

# test logging 
import logging 
@app.route('/logtest')
def logtest():
    logging.debug("Debug message from /logtest route")
    logging.info("Info message from /logtest route")
    logging.error("Error message from /logtest route")
    return "Logging test completed"


# Step 4 : Define a Simple  route to check if the server is runing
@app.route('/')
def home() : 
    return "Portfolio Home Page - Flask App is Running"


#Step 5 : Run the app the app only if this file is executed directly ( not imported )

if __name__ == '__main__':
    # Start the Flask development server with debug mode (controlled by the config)
    app.run(debug=app.config['DEBUG'])