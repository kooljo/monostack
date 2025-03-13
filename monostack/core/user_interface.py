import os
import logging
import sys
from typing import Dict, Any, List, Optional
import inquirer
from colorama import Fore, Style, init as colorama_init

# Initialize colorama
colorama_init()

class UserInterface:
    """
    Handles user interaction through the command line using Inquirer.
    Provides a rich interactive interface for technology selection.
    """
    def __init__(self):
        """Initialize the UserInterface with a logger."""
        self.logger = logging.getLogger(__name__)
        
    def _prompt_choice(self, message: str, choices: List[str]) -> str:
        """
        Prompt the user to select from a list of choices using Inquirer.
        
        Args:
            message: The prompt message to display
            choices: List of options to choose from
            
        Returns:
            The selected option
        """
        try:
            questions = [
                inquirer.List('choice',
                    message=message,
                    choices=choices,
                )
            ]
            
            answers = inquirer.prompt(questions)
            
            if answers and 'choice' in answers:
                return answers['choice']
            else:
                # Fallback in case inquirer has issues
                self._print_colored(message, Fore.BLUE)
                for i, choice in enumerate(choices):
                    print(f"{i+1}. {choice}")
                
                while True:
                    try:
                        idx = int(input("Enter number: ")) - 1
                        if 0 <= idx < len(choices):
                            return choices[idx]
                        else:
                            print(f"Please enter a number between 1 and {len(choices)}")
                    except ValueError:
                        print("Please enter a valid number")
                        
        except Exception as e:
            self.logger.error(f"Error with interactive prompt: {str(e)}")
            
            # Ultimate fallback
            self._print_colored(message, Fore.BLUE)
            for i, choice in enumerate(choices):
                print(f"{i+1}. {choice}")
            
            while True:
                try:
                    idx = int(input("Enter number: ")) - 1
                    if 0 <= idx < len(choices):
                        return choices[idx]
                    else:
                        print(f"Please enter a number between 1 and {len(choices)}")
                except ValueError:
                    print("Please enter a valid number")
    
    def _print_colored(self, text: str, color: str) -> None:
        """Print colored text to the console."""
        print(f"{color}{text}{Style.RESET_ALL}")
    
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
            app_type = self._prompt_choice("Select the type of application you want to create:", options)
            
            # Mobile app selection
            if app_type in ["Mobile_App", "All"]:
                mobile_languages = list(technologies["frontend-mobile"].keys())
                mobile_language_choice = self._prompt_choice("Choose a frontend-mobile language:", mobile_languages)
                
                if mobile_language_choice in mobile_languages:
                    mobile_technologies = list(technologies["frontend-mobile"][mobile_language_choice].keys())
                    mobile_tech_choice = self._prompt_choice(
                        f"Choose a frontend-mobile framework for {mobile_language_choice}:", 
                        mobile_technologies
                    )
                    user_choices["frontend-mobile"] = {"language": mobile_language_choice, "framework": mobile_tech_choice}
            
            # Web app selection
            if app_type in ["Web_App", "All"]:
                web_languages = list(technologies["frontend-web"].keys())
                web_language_choice = self._prompt_choice("Choose a frontend-web language:", web_languages)
                
                if web_language_choice in web_languages:
                    web_technologies = list(technologies["frontend-web"][web_language_choice].keys())
                    web_tech_choice = self._prompt_choice(
                        f"Choose a frontend-web framework for {web_language_choice}:", 
                        web_technologies
                    )
                    user_choices["frontend-web"] = {"language": web_language_choice, "framework": web_tech_choice}
            
            # Desktop app selection
            if app_type in ["Desktop_App", "All"]:
                desktop_languages = list(technologies["frontend-desktop"].keys())
                desktop_language_choice = self._prompt_choice("Choose a frontend-desktop language:", desktop_languages)
                
                if desktop_language_choice in desktop_languages:
                    desktop_technologies = list(technologies["frontend-desktop"][desktop_language_choice].keys())
                    desktop_tech_choice = self._prompt_choice(
                        f"Choose a frontend-desktop framework for {desktop_language_choice}:", 
                        desktop_technologies
                    )
                    user_choices["frontend-desktop"] = {"language": desktop_language_choice, "framework": desktop_tech_choice}
            
            # Backend selection
            backend_choice = self._prompt_choice("Do you want to include a backend?", ["Yes", "No"])
            
            if backend_choice == "Yes":
                backend_languages = list(technologies["backend"].keys())
                language_choice = self._prompt_choice("Choose a backend language:", backend_languages)
                
                if language_choice in backend_languages:
                    backend_technologies = list(technologies["backend"][language_choice].keys())
                    tech_choice = self._prompt_choice(
                        f"Choose a backend framework for {language_choice}:", 
                        backend_technologies
                    )
                    user_choices["backend"] = {"language": language_choice, "framework": tech_choice}
            
            # Database selection
            db_choice = self._prompt_choice("Do you want to include a database?", ["Yes", "No"])
            
            if db_choice == "Yes":
                db_choices = list(technologies["databases"].keys())
                database_choice = self._prompt_choice("Choose a database:", db_choices)
                
                if database_choice in db_choices:
                    user_choices["database"] = {"type": database_choice}
            
            return user_choices
            
        except Exception as e:
            self.logger.error(f"Error during user interaction: {str(e)}")
            raise