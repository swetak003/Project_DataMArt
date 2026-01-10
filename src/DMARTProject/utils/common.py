import os
from pathlib import Path

def create_directories(path: str, verbose: bool = True):
    """
    Create directories if they do not exist.
    """
    try:
        os.makedirs(path, exist_ok=True)
        if verbose:
            print(f"Directory created or already exists at: {path}")
    except Exception as e:
        raise e
    
