import os
import logging
import subprocess
from typing import Dict, Any, List, Optional

class UserInterface:
    """
    Handles user interaction through the command line.
    Uses Gum for interactive selection.
    """
    def __init__(self):
        """Initialize the UserInterface with a logger."""
        self.logger = logging.getLogger(__name__)
        
    def _run_gum_command(self, command: str) -> str:
        """
        Run a Gum command and return the output.
        
        Args:
            command: The Gum command to run
            
        Returns:
            The command output (stripped)
            
        Raises:
            subprocess.CalledProcessError: If the command fails
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Gum command failed: {command}")
            self.logger.error(f"Error: {e.stderr}")
            raise
    
    def color_text(self, text: str, color_code: str) -> str:
        """
        Return colored text for terminal output.
        
        Args:
            text: The text to color
            color_code: ANSI color code
            
        Returns:
            Colored text string
        """
        return f"\033[{color_code}m{text}\033[0m"
    
    def prompt_user(self, technologies: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prompt the user for technology choices.
        
        Args:
            technologies: Available technology options
            
        Returns:
            Dictionary of user choices
        """
        user_choices = {}
        
        try:
            print(self.color_text("\nSelect the type of application you want to create:", "34"))  # Blue
            options = ["Mobile_App", "Web_App", "Desktop_App", "All"]
            app_type = self._run_gum_command(f'gum choose {" ".join(options)}')
            
            # Mobile app selection
            if app_type in ["Mobile_App", "All"]:
                print(self.color_text("\nChoose a frontend-mobile language:", "32"))  # Green
                mobile_languages = list(technologies["frontend-mobile"].keys())
                mobile_language_choice = self._run_gum_command(f'gum choose {" ".join(mobile_languages)}')
                
                if mobile_language_choice in mobile_languages:
                    mobile_technologies = list(technologies["frontend-mobile"][mobile_language_choice].keys())
                    print(self.color_text(f"\nChoose a frontend-mobile framework for {mobile_language_choice}:", "32"))
                    mobile_tech_choice = self._run_gum_command(f'gum choose {" ".join(mobile_technologies)}')
                    user_choices["frontend-mobile"] = {"language": mobile_language_choice, "framework": mobile_tech_choice}
            
            # Web app selection
            if app_type in ["Web_App", "All"]:
                print(self.color_text("\nChoose a frontend-web language:", "36"))  # Cyan
                web_languages = list(technologies["frontend-web"].keys())
                web_language_choice = self._run_gum_command(f'gum choose {" ".join(web_languages)}')
                
                if web_language_choice in web_languages:
                    web_technologies = list(technologies["frontend-web"][web_language_choice].keys())
                    print(self.color_text(f"\nChoose a frontend-web framework for {web_language_choice}:", "36"))
                    web_tech_choice = self._run_gum_command(f'gum choose {" ".join(web_technologies)}')
                    user_choices["frontend-web"] = {"language": web_language_choice, "framework": web_tech_choice}
            
            # Desktop app selection
            if app_type in ["Desktop_App", "All"]:
                print(self.color_text("\nChoose a frontend-desktop language:", "35"))  # Magenta
                desktop_languages = list(technologies["frontend-desktop"].keys())
                desktop_language_choice = self._run_gum_command(f'gum choose {" ".join(desktop_languages)}')
                
                if desktop_language_choice in desktop_languages:
                    desktop_technologies = list(technologies["frontend-desktop"][desktop_language_choice].keys())
                    print(self.color_text(f"\nChoose a frontend-desktop framework for {desktop_language_choice}:", "35"))
                    desktop_tech_choice = self._run_gum_command(f'gum choose {" ".join(desktop_technologies)}')
                    user_choices["frontend-desktop"] = {"language": desktop_language_choice, "framework": desktop_tech_choice}
            
            # Backend selection
            print(self.color_text("\nDo you want to include a backend?", "33"))  # Yellow
            backend_choice = self._run_gum_command(f'gum choose Yes No')
            
            if backend_choice == "Yes":
                print(self.color_text("\nChoose a backend language:", "33"))
                backend_languages = list(technologies["backend"].keys())
                language_choice = self._run_gum_command(f'gum choose {" ".join(backend_languages)}')
                
                if language_choice in backend_languages:
                    backend_technologies = list(technologies["backend"][language_choice].keys())
                    print(self.color_text(f"\nChoose a backend framework for {language_choice}:", "33"))
                    tech_choice = self._run_gum_command(f'gum choose {" ".join(backend_technologies)}')
                    user_choices["backend"] = {"language": language_choice, "framework": tech_choice}
            
            # Database selection
            print(self.color_text("\nDo you want to include a database?", "31"))  # Red
            db_choice = self._run_gum_command(f'gum choose Yes No')
            
            if db_choice == "Yes":
                print(self.color_text("\nChoose a database:", "31"))
                db_choices = list(technologies["databases"].keys())
                database_choice = self._run_gum_command(f'gum choose {" ".join(db_choices)}')
                
                if database_choice in db_choices:
                    user_choices["database"] = {"type": database_choice}
            
            return user_choices
            
        except Exception as e:
            self.logger.error(f"Error during user interaction: {str(e)}")
            raise