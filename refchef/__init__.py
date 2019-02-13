import os
from dotenv import load_dotenv
import oyaml as yaml

__version__ = '0.1.3'

# load dotenv in the base root
APP_ROOT = os.path.join(os.path.dirname(__file__), '..')   # refers to application_top
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
