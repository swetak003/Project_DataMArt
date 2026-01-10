import os ###generic code for path management
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO)###generice information logging
logger = logging.getLogger(__name__)
project_name="DMARTProject"

list_of_files=[
    ".github/workflows/.gitkeep",###github indication that git hub workflow is there
    f"src/{project_name}/__init__.py",###init file for package
    f"src/{project_name}/components/__init__.py",###init file for components
    f"src/{project_name}/components/data_ingestion.py",###data ingestion file
    f"src/{project_name}/components/data_validation.py",###data validation file
    f"src/{project_name}/components/data_transformation.py",###data transformation file
    f"src/{project_name}/components/model_trainer.py",###model trainer file
    f"src/{project_name}/components/model_evaluation.py",###model evaluation file
    f"src/{project_name}/pipelines/__int__.py",###pipeline init file
    f"src/{project_name}/pipelines/training_pipeline.py",###training pipeline file
    f"src/{project_name}/pipelines/prediction_pipeline.py",###prediction pipeline file
    f"src/{project_name}/utils/__init__.py",###utils init file
    f"src/{project_name}/utils/common.py",###common utility file
    f"src/{project_name}/loggers/__init__.py",###loggers init file
    f"src/{project_name}/loggers/logger.py",###logger file
    "app.py",###main file
    "requirement.txt",###requirement file
    "setup.py",###setup file for package
    "exception.py",###custom exception file
    "config.py"###configuration file
]

for filepath in list_of_files:
    filepath=Path(filepath)###path management
    filedir,filename=os.path.split(filepath)###splitting the path into directory and file name
    
    if filedir!="":
        os.makedirs(filedir,exist_ok=True)###making directories if not exist
        logger.info(f"Creating directory:{filedir} for file:{filename}")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):###checking if file exists or is empty
        with open (filepath,'w') as fp:
            pass###creating empty file
            logger.info(f"Creating empty file:{filepath}")
    else:
        logger.info(f"File already exists:{filepath},skipping creation.")