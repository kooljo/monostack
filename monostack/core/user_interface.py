import os
import logging
import subprocess
from typing import Dict, Any, List, Optional

class UserInterface:
    """
    Handles user interaction through the command line.
    Uses Gum for interactive selection or fallbacks to standard input.
    """
    def __init__(self):
        """Initialize the UserInterface with a logger."""
        self.logger = logging.getLogger(__name__)
        
    def _prompt_choice(self, prompt: str, options: List[str]) -> str:
        """
        Prompt the user to select from a list of options.
        
        Args:
            prompt: The prompt text to display
            options: List of options to choose from
            
        Returns:
            The selected option
        """
        try:
            # Check if gum is available
            try:
                subprocess.run(["gum", "--version"], check=True, capture_output=True)
                has_gum = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                has_gum = False
            
            if has_gum:
                # Use gum for interactive selection
                command = f"gum choose {' '.join(options)}"
                print(self.color_text(prompt, "34"))  # Blue
                
                result = subprocess.run(
                    command,
                    shell=True,
                    check=True,
                    capture_output=True,
                    text=True
                )
                return result.stdout.strip()
            else:
                # Fallback to standard input
                print(self.color_text(prompt, "34"))  # Blue
                print("Options:", " | ".join(options))
                choice = input("Enter your choice: ")
                
                # Validate input
                while choice not in options:
                    print(f"Invalid choice. Please select one of: {', '.join(options)}")
                    choice = input("Enter your choice: ")
                
                return choice
                
        except Exception as e:
            self.logger.error(f"Error during user interaction: {str(e)}")
            
            # Ultimate fallback
            print(self.color_text(prompt, "34"))  # Blue
            print("Options:", " | ".join(options))
            choice = input("Enter your choice: ")
            return choice
    
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
            # App type selection
            options = ["Mobile_App", "Web_App", "Desktop_App", "All"]
            app_type = self._prompt_choice("\nSelect the type of application you want to create:", options)
            
            # Mobile app selection
            if app_type in ["Mobile_App", "All"]:
                mobile_languages = list(technologies["frontend-mobile"].keys())
                mobile_language_choice = self._prompt_choice("\nChoose a frontend-mobile language:", mobile_languages)
                
                if mobile_language_choice in mobile_languages:
                    mobile_technologies = list(technologies["frontend-mobile"][mobile_language_choice].keys())
                    mobile_tech_choice = self._prompt_choice(
                        f"\nChoose a frontend-mobile framework for {mobile_language_choice}:", 
                        mobile_technologies
                    )
                    user_choices["frontend-mobile"] = {"language": mobile_language_choice, "framework": mobile_tech_choice}
            
            # Web app selection
            if app_type in ["Web_App", "All"]:
                web_languages = list(technologies["frontend-web"].keys())
                web_language_choice = self._prompt_choice("\nChoose a frontend-web language:", web_languages)
                
                if web_language_choice in web_languages:
                    web_technologies = list(technologies["frontend-web"][web_language_choice].keys())
                    web_tech_choice = self._prompt_choice(
                        f"\nChoose a frontend-web framework for {web_language_choice}:", 
                        web_technologies
                    )
                    user_choices["frontend-web"] = {"language": web_language_choice, "framework": web_tech_choice}
            
            # Desktop app selection
            if app_type in ["Desktop_App", "All"]:
                desktop_languages = list(technologies["frontend-desktop"].keys())
                desktop_language_choice = self._prompt_choice("\nChoose a frontend-desktop language:", desktop_languages)
                
                if desktop_language_choice in desktop_languages:
                    desktop_technologies = list(technologies["frontend-desktop"][desktop_language_choice].keys())
                    desktop_tech_choice = self._prompt_choice(
                        f"\nChoose a frontend-desktop framework for {desktop_language_choice}:", 
                        desktop_technologies
                    )
                    user_choices["frontend-desktop"] = {"language": desktop_language_choice, "framework": desktop_tech_choice}
            
            # Backend selection
            backend_choice = self._prompt_choice("\nDo you want to include a backend?", ["Yes", "No"])
            
            if backend_choice == "Yes":
                backend_languages = list(technologies["backend"].keys())
                language_choice = self._prompt_choice("\nChoose a backend language:", backend_languages)
                
                if language_choice in backend_languages:
                    backend_technologies = list(technologies["backend"][language_choice].keys())
                    tech_choice = self._prompt_choice(
                        f"\nChoose a backend framework for {language_choice}:", 
                        backend_technologies
                    )
                    user_choices["backend"] = {"language": language_choice, "framework": tech_choice}
            
            # Database selection
            db_choice = self._prompt_choice("\nDo you want to include a database?", ["Yes", "No"])
            
            if db_choice == "Yes":
                db_choices = list(technologies["databases"].keys())
                database_choice = self._prompt_choice("\nChoose a database:", db_choices)
                
                if database_choice in db_choices:
                    user_choices["database"] = {"type": database_choice}
            
            return user_choices
            
        except Exception as e:
            self.logger.error(f"Error during user interaction: {str(e)}")
            raise