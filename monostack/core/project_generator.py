import os
import logging
import json
from typing import Dict, Any, Optional

from ..config.config_manager import ConfigManager
from ..utils.command_runner import CommandRunner
from ..utils.venv_manager import VenvManager
from ..templates.template_manager import TemplateManager

class ProjectGenerator:
    """
    Main class responsible for generating project structures based on user choices.
    Coordinates all the components needed for project generation.
    """
    def __init__(self):
        """Initialize the ProjectGenerator with required managers."""
        self.logger = logging.getLogger(__name__)
        self.config_manager = ConfigManager()
        self.command_runner = CommandRunner()
        self.venv_manager = VenvManager()
        self.template_manager = TemplateManager()
    
    def initialize_project(self, base_dir: str, module: str, choice: Dict[str, Any], 
                          install_commands: Dict[str, Any]) -> bool:
        """
        Initialize a specific module (backend, frontend-web, etc.) in the project.
        
        Args:
            base_dir: The base directory for the project
            module: The module type (backend, frontend-web, etc.)
            choice: User's technology choices for this module
            install_commands: Available installation commands
            
        Returns:
            True if successful, False otherwise
        """
        try:
            project_path = os.path.join(base_dir, module)
            os.makedirs(project_path, exist_ok=True)
            
            # Verify if language and framework are provided
            if "language" not in choice or "framework" not in choice:
                self.logger.warning(f"Skipping {module} as no valid choice was made.")
                return False
            
            language = choice["language"]
            framework = choice["framework"]
            
            # Check if an installation command exists
            if (module in install_commands and 
                language in install_commands[module] and 
                framework in install_commands[module][language]):
                
                command_template = install_commands[module][language][framework]
                variables = {"module": module}
                
                # Render the installation command with variables
                install_command = self.template_manager.render_install_command(command_template, variables)
                
                self.logger.info(f"Installing {framework} ({language}) in {module}...")
                result = self.command_runner.run(install_command, cwd=base_dir)
                
                if result.returncode != 0:
                    self.logger.error(f"Installation failed for {framework} ({language}) in {module}.")
                    self.logger.error(f"Error: {result.stderr}")
                    return False
            else:
                self.logger.warning(f"No installation command found for {framework} in {language} ({module}).")
                
            # Set up virtual environment if it's a Python project
            if language == "python":
                self.logger.info(f"Setting up virtual environment for {module}...")
                if not self.venv_manager.create_venv(project_path):
                    self.logger.warning(f"Failed to create virtual environment for {module}, continuing anyway.")
            
            # Add a README.md file
            with open(os.path.join(project_path, "README.md"), "w") as f:
                f.write(f"# {module.capitalize()} - {framework} ({language})\n\n")
                f.write(f"This directory contains the {module} part of the project using {framework} ({language}).\n")
                f.write("\n## Setup\n\n")
                f.write("Instructions for setting up this component...\n")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing {module}: {str(e)}")
            return False
    
    def generate_docker_compose(self, base_dir: str, choices: Dict[str, Any]) -> bool:
        """
        Generate a Docker Compose file for the selected services.
        
        Args:
            base_dir: The base directory for the project
            choices: User's technology choices
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load Docker Compose template
            docker_template = self.config_manager.load_docker_compose_template()
            
            # Render the template with the user's choices
            docker_compose_content = self.template_manager.render_docker_compose(docker_template, choices)
            
            # Create infra directory and write the file
            infra_path = os.path.join(base_dir, "infra")
            os.makedirs(infra_path, exist_ok=True)
            
            with open(os.path.join(infra_path, "docker-compose.yml"), "w") as f:
                f.write(docker_compose_content)
                
            self.logger.info(f"Generated Docker Compose file at {os.path.join(infra_path, 'docker-compose.yml')}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating Docker Compose file: {str(e)}")
            return False
    
    def initialize_git_repo(self, base_dir: str) -> bool:
        """
        Initialize a Git repository in the project directory.
        
        Args:
            base_dir: The base directory for the project
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info("Initializing Git repository...")
            
            # Initialize Git repository
            git_init = self.command_runner.run("git init", cwd=base_dir)
            if git_init.returncode != 0:
                self.logger.error("Failed to initialize Git repository")
                return False
                
            # Add all files to Git
            git_add = self.command_runner.run("git add .", cwd=base_dir)
            if git_add.returncode != 0:
                self.logger.error("Failed to add files to Git repository")
                return False
                
            # Create initial commit
            git_commit = self.command_runner.run(
                'git commit -m "Initial commit with project structure"', 
                cwd=base_dir
            )
            if git_commit.returncode != 0:
                self.logger.error("Failed to create initial commit")
                return False
                
            self.logger.info("Git repository initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing Git repository: {str(e)}")
            return False
    
    def create_project_structure(self, base_dir: str, choices: Dict[str, Any]) -> bool:
        """
        Create the entire project structure based on user choices.
        
        Args:
            base_dir: The base directory for the project
            choices: User's technology choices
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.logger.info(f"Creating project structure at {base_dir}")
            
            # Create the base directory
            os.makedirs(base_dir, exist_ok=True)
            
            # Load installation commands
            install_commands = self.config_manager.load_technologies()
            
            # Initialize each module
            for module, choice in choices.items():
                if module != "database":  # Handle database separately
                    success = self.initialize_project(base_dir, module, choice, install_commands)
                    if not success:
                        self.logger.warning(f"Failed to initialize {module}, continuing with other modules")
            
            # Generate Docker Compose file
            self.generate_docker_compose(base_dir, choices)
            
            # Create docs directory
            docs_path = os.path.join(base_dir, "docs")
            os.makedirs(docs_path, exist_ok=True)
            
            # Create main README
            with open(os.path.join(docs_path, "README.md"), "w") as f:
                f.write("# Project Documentation\n\n")
                f.write("Add your project documentation here.\n\n")
                f.write("## Project Structure\n\n")
                f.write("```\n")
                f.write(f"📦 {os.path.basename(base_dir)}\n")
                for module in choices.keys():
                    if module != "database":
                        f.write(f"├── 📁 {module}\n")
                f.write("├── 📁 infra\n")
                f.write("│   └── docker-compose.yml\n")
                f.write("├── 📁 docs\n")
                f.write("└── 📜 README.md\n")
                f.write("```\n")
            
            # Create main README
            with open(os.path.join(base_dir, "README.md"), "w") as f:
                f.write(f"# {os.path.basename(base_dir)}\n\n")
                f.write("This is a full-stack application generated with Monostack.\n\n")
                
                f.write("## Project Structure\n\n")
                for module, choice in choices.items():
                    if module != "database" and "language" in choice and "framework" in choice:
                        f.write(f"- **{module}**: {choice['framework']} ({choice['language']})\n")
                
                if "database" in choices:
                    f.write(f"- **Database**: {choices['database']['type']}\n\n")
                
                f.write("## Getting Started\n\n")
                f.write("1. See documentation in each component directory\n")
                f.write("2. Run services with Docker Compose:\n\n")
                f.write("```bash\n")
                f.write("cd infra\n")
                f.write("docker-compose up --build -d\n")
                f.write("```\n")
            
            # Initialize Git repository
            self.initialize_git_repo(base_dir)
            
            self.logger.info(f"Project structure created successfully at {base_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating project structure: {str(e)}")
            return False