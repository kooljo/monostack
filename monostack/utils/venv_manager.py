import os
import logging
import subprocess
from typing import Optional, Dict, Any, List

class VenvManager:
    """
    Manages creation and usage of virtual environments for different project types.
    Provides isolation for project dependencies.
    """
    def __init__(self):
        """Initialize the VenvManager with a logger."""
        self.logger = logging.getLogger(__name__)
    
    def create_venv(self, project_path: str, venv_name: str = "venv") -> bool:
        """
        Create a virtual environment in the specified project directory.
        
        Args:
            project_path: The project directory path
            venv_name: Name of the virtual environment directory
            
        Returns:
            True if successful, False otherwise
        """
        try:
            venv_path = os.path.join(project_path, venv_name)
            self.logger.info(f"Creating virtual environment at {venv_path}")
            
            # Use virtualenv to create the environment
            result = subprocess.run(
                f"python -m virtualenv {venv_path}",
                shell=True,
                check=True,
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            self.logger.debug(f"Virtual environment created at {venv_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create virtual environment: {e.stderr}")
            return False
            
        except Exception as e:
            self.logger.error(f"Unexpected error creating virtual environment: {str(e)}")
            return False
    
    def install_requirements(self, project_path: str, requirements: List[str], 
                             venv_name: str = "venv") -> bool:
        """
        Install packages in the virtual environment.
        
        Args:
            project_path: The project directory path
            requirements: List of packages to install
            venv_name: Name of the virtual environment directory
            
        Returns:
            True if successful, False otherwise
        """
        try:
            venv_path = os.path.join(project_path, venv_name)
            requirements_str = " ".join(requirements)
            
            # Source the virtual environment and install packages
            if os.name == 'nt':  # Windows
                activate_script = os.path.join(venv_path, "Scripts", "activate")
                command = f"{activate_script} && pip install {requirements_str}"
            else:  # Unix-like
                activate_script = os.path.join(venv_path, "bin", "activate")
                command = f"source {activate_script} && pip install {requirements_str}"
            
            self.logger.info(f"Installing packages: {requirements_str}")
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                cwd=project_path,
                capture_output=True,
                text=True
            )
            
            self.logger.debug(f"Packages installed successfully: {requirements_str}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install packages: {e.stderr}")
            return False
            
        except Exception as e:
            self.logger.error(f"Unexpected error installing packages: {str(e)}")
            return False
    
    def run_in_venv(self, project_path: str, command: str, venv_name: str = "venv") -> subprocess.CompletedProcess:
        """
        Run a command within the virtual environment.
        
        Args:
            project_path: The project directory path
            command: The command to run
            venv_name: Name of the virtual environment directory
            
        Returns:
            CompletedProcess instance with return code and output
        """
        venv_path = os.path.join(project_path, venv_name)
        
        if os.name == 'nt':  # Windows
            activate_script = os.path.join(venv_path, "Scripts", "activate")
            full_command = f"{activate_script} && {command}"
        else:  # Unix-like
            activate_script = os.path.join(venv_path, "bin", "activate")
            full_command = f"source {activate_script} && {command}"
        
        self.logger.debug(f"Running in virtualenv: {command}")
        try:
            result = subprocess.run(
                full_command,
                shell=True,
                check=True,
                cwd=project_path,
                capture_output=True,
                text=True
            )
            return result
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed in virtualenv: {e.stderr}")
            raise
            
        except Exception as e:
            self.logger.error(f"Unexpected error running command in virtualenv: {str(e)}")
            raise