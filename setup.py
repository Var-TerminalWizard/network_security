from setuptools import setup, find_packages
from typing import List

def get_requirements() -> List[str]:
    """Reads requirements.txt and returns a list of requirements."""
    
    requirement_lst: List[str] = []

    try:
        with open('requirements.txt', 'r') as file:
            for line in file.readlines():
                requirement = line.strip()

                if requirement != '-e .':
                    requirement_lst.append(requirement)

    except FileNotFoundError:
        print("requirements.txt file not found.")

    return requirement_lst

setup(
    name="Network-Scanner",
    version="0.0.1",
    author="Varun Sai",
    packages=find_packages(),
    install_requires=get_requirements()
)