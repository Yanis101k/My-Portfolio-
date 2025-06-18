# import Flask to create the web application using flask framework 
from flask import Flask 


# import the logging setup function to enable centralized logging for debugging and monitoring
from logging_config import setup_logging 

from routes.auth_routes import api_auth 
from routes.project_routes import api_project_routes
from routes.frontend_routes import frontend  # ✅ Import your frontend blueprint

from dotenv import load_dotenv
load_dotenv()  # This loads the default .env for production

# import my custom Config class to load environment variables from the .env file
from config import Config 
# step 1 : Create the Flask app instance 

app = Flask( __name__ )

# step 2 : Load configuration settings from the config class ( includes secret key, DB path, admin username and password etc.)
app.config.from_object(Config)


# step 3: Set up logging ( creates a log file and writes important events )
setup_logging()


app.register_blueprint( api_project_routes )
app.register_blueprint( api_auth )
app.secret_key = Config.get_secret_key()

# ✅ Register your blueprint for the frontend routes
app.register_blueprint(frontend)

#Step 5 : Run the app the app only if this file is executed directly ( not imported )

if __name__ == '__main__':
    # Start the Flask development server with debug mode (controlled by the config)
    app.run(debug=app.config['DEBUG'])