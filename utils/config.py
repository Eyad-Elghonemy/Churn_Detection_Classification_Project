from dotenv import load_dotenv
import os


load_dotenv(override=True)

# .env Variables
APP_NAME = os.getenv('APP_NAME')
VERSION = os.getenv('VERSION')
SECRET_KEY_TOKEN = os.getenv('SECRET_KEY_TOKEN')



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_FOLDER_PATH = os.path.join(BASE_DIR, "models")


# Models
preprocessor = os.path.join(MODELS_FOLDER_PATH, "preprocessor.pkl")
forest_model = os.path.join(MODELS_FOLDER_PATH, "forest_tuned.pkl")
xgboost_model = os.path.join(MODELS_FOLDER_PATH, "xgb-tuned.pkl")