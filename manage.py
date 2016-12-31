from flask_script import Manager
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
from app import app
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
