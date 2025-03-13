import os
import json
import logging
from typing import Dict, Any, Optional

class ConfigManager:
    """
    Class to manage all configuration aspects of the Monostack application.
    Handles loading and accessing configuration files.
    """
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize the ConfigManager with the configuration directory.
        
        Args:
            config_dir: Path to the configuration directory. If None, uses the default.
        """
        self.logger = logging.getLogger(__name__)
        self.config_dir = config_dir or os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.technologies = None
        self.docker_template = None
    
    def load_technologies(self) -> Dict[str, Any]:
        """
        Load the technologies configuration from the install_commands.json file.
        
        Returns:
            Dict containing the technologies configuration.
        
        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            json.JSONDecodeError: If the configuration file is not valid JSON.
        """
        if self.technologies is not None:
            return self.technologies
            
        try:
            config_path = os.path.join(self.config_dir, "install_commands.json")
            self.logger.debug(f"Loading technologies from {config_path}")
            
            with open(config_path, "r") as f:
                self.technologies = json.load(f)
            return self.technologies
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in configuration file: {config_path}")
            raise
    
    def load_docker_compose_template(self) -> str:
        """
        Load the Docker Compose template from the docker_compose_template.yml file.
        
        Returns:
            String containing the Docker Compose template.
            
        Raises:
            FileNotFoundError: If the template file doesn't exist.
        """
        if self.docker_template is not None:
            return self.docker_template
            
        try:
            template_path = os.path.join(self.config_dir, "docker_compose_template.yml")
            self.logger.debug(f"Loading Docker Compose template from {template_path}")
            
            with open(template_path, "r") as f:
                self.docker_template = f.read()
            return self.docker_template
        except FileNotFoundError:
            self.logger.error(f"Template file not found: {template_path}")
            raise