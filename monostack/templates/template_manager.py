import os
import logging
import yaml
from string import Template
from typing import Dict, Any, Optional

class TemplateManager:
    """
    Manages templates for installation commands and Docker Compose files.
    Allows for more flexible configuration of project generation.
    """
    def __init__(self, template_dir: Optional[str] = None):
        """
        Initialize the TemplateManager.
        
        Args:
            template_dir: Optional path to the template directory
        """
        self.logger = logging.getLogger(__name__)
        self.template_dir = template_dir or os.path.dirname(__file__)
    
    def render_install_command(self, command_template: str, variables: Dict[str, Any]) -> str:
        """
        Render an installation command template with the given variables.
        
        Args:
            command_template: The command template string
            variables: Dictionary of variables to substitute in the template
            
        Returns:
            Rendered command string
        """
        try:
            module_value = variables.get("module", "")
            
            # Direct replacement - simplest and most reliable approach
            rendered_command = command_template
            
            # Replace all variable patterns we might encounter
            replacements = [
                ("${module}", module_value),  # Standard shell variable
                ("$${module}", module_value),  # Escaped shell variable
                ("{module}", module_value),    # Python format string
                ("$module", module_value),     # Plain shell variable
            ]
            
            for pattern, replacement in replacements:
                rendered_command = rendered_command.replace(pattern, replacement)
            
            self.logger.debug(f"Rendered command after direct replacements: {rendered_command}")
            
            # Double-check that all variables were replaced
            if any(pattern in rendered_command for pattern, _ in replacements):
                self.logger.warning(f"Some variables may not have been replaced: {rendered_command}")
                
                # Final attempt with string.Template
                try:
                    template = Template(rendered_command)
                    rendered_command = template.safe_substitute(variables)
                    self.logger.debug(f"After Template safe_substitute: {rendered_command}")
                except Exception as e:
                    self.logger.error(f"Template substitution failed: {e}")
                
            self.logger.debug(f"Final rendered command: {rendered_command}")
            return rendered_command
        except KeyError as e:
            self.logger.error(f"Missing required variable in template: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error rendering template: {str(e)}")
            raise
    
    def render_docker_compose(self, template: str, services: Dict[str, Any]) -> str:
        """
        Render a Docker Compose template with the selected services.
        
        Args:
            template: The Docker Compose template as a string
            services: Dictionary of services to include
            
        Returns:
            Rendered Docker Compose file content
        """
        try:
            # Parse the template as YAML
            docker_config = yaml.safe_load(template)
            
            # Start with the basic structure
            result = {
                "version": docker_config.get("version", "3"),
                "services": {}
            }
            
            # Add the needed services from the template
            base_services = docker_config.get("services", {})
            
            # Add backend service if selected
            if "backend" in services:
                backend = services["backend"]
                language = backend.get("language")
                framework = backend.get("framework")
                
                if f"backend-{language}-{framework}" in base_services:
                    result["services"][f"backend-{framework}"] = base_services[f"backend-{language}-{framework}"]
                elif "backend-generic" in base_services:
                    # Use generic template with replacements
                    service = dict(base_services["backend-generic"])
                    service["image"] = service["image"].replace("${BACKEND_FRAMEWORK}", framework)
                    result["services"][f"backend-{framework}"] = service
            
            # Add frontend web service if selected
            if "frontend-web" in services:
                web = services["frontend-web"]
                language = web.get("language")
                framework = web.get("framework")
                
                if f"frontend-web-{language}-{framework}" in base_services:
                    result["services"][f"frontend-web-{framework}"] = base_services[f"frontend-web-{language}-{framework}"]
                elif "frontend-web-generic" in base_services:
                    service = dict(base_services["frontend-web-generic"])
                    service["image"] = service["image"].replace("${FRONTEND_WEB_FRAMEWORK}", framework)
                    result["services"][f"frontend-web-{framework}"] = service
            
            # Add database if selected
            if "database" in services:
                db_type = services["database"].get("type")
                if db_type in base_services:
                    result["services"][db_type] = base_services[db_type]
            
            # Add networks and volumes from the template
            if "networks" in docker_config:
                result["networks"] = docker_config["networks"]
            
            if "volumes" in docker_config:
                result["volumes"] = docker_config["volumes"]
                
            # Convert back to YAML
            return yaml.dump(result, default_flow_style=False)
            
        except yaml.YAMLError as e:
            self.logger.error(f"Invalid YAML in Docker Compose template: {str(e)}")
            raise
        except KeyError as e:
            self.logger.error(f"Missing required key in template: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error rendering Docker Compose template: {str(e)}")
            raise