## JAI GANEHSHAY NAMAH
### basic information of the package:TRacking info, licence date, author name, maintaner name, version name
from setuptools import setup, find_packages
import os
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """Read requirements from a file and return them as a list."""
    requirements=[]
    with open(file_path, 'r') as file:
        requirements = file.readlines()
        requirements=[req.replace("\n","") for req in requirements
                      if req.strip() and not req.startswith("#")
                      ]
    return requirements
setup(
    name="DMART Project",
    version="0.0.1",
    author="Sweta KUmari",
    author_email="swetakumari071188@gmail.com",
    description="A package for object tracking using various algorithms.",
    install_requires=get_requirements('requirement.txt'),
    packages=find_packages()
    
)
