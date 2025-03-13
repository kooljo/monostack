import os
import argparse
import logging
import sys
from typing import Dict, Any, Optional

from .config.config_manager import ConfigManager
from .core.project_generator import ProjectGenerator
from .core.user_interface import UserInterface
from .utils.logger import setup_logging

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Monostack - CLI tool for generating full-stack projects")
    parser.add_argument("--name", type=str, help="Set the project name (default: mono-app)")
    parser.add_argument("--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                        default="INFO", help="Set the logging level")
    parser.add_argument("--log-file", type=str, help="Path to log file")
    parser.add_argument("--generate-hello-world", action="store_true",
                        help="Generate Hello World endpoints in backend and corresponding frontend code")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show verbose output during command execution")
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging(args.log_level, args.log_file)
    
    try:
        # Set project name and base directory
        project_name = args.name if args.name else "mono-app"
        base_dir = os.path.abspath(os.path.join(os.getcwd(), "..", project_name))
        
        # Initialize components
        config_manager = ConfigManager()
        user_interface = UserInterface()
        project_generator = ProjectGenerator()
        
        # Load technologies and prompt user
        technologies = config_manager.load_technologies()
        user_choices = user_interface.prompt_user(technologies)
        
        # Generate project structure
        if user_choices:
            success = project_generator.create_project_structure(
                base_dir, 
                user_choices,
                generate_hello_world=args.generate_hello_world,
                verbose=args.verbose
            )
            
            if success:
                logger.info(f"\n✅ Project structure for '{base_dir}' created successfully!")
                print(f"\n✅ Project structure for '{base_dir}' created successfully!")
                
                if args.generate_hello_world and "backend" in user_choices:
                    print(f"\n✅ Hello World example generated with {user_choices['backend']['framework']} backend")
                    frontend_count = 0
                    for module in ["frontend-web", "frontend-mobile", "frontend-desktop"]:
                        if module in user_choices:
                            frontend_count += 1
                    if frontend_count > 0:
                        print(f"  and {frontend_count} frontend{'s' if frontend_count > 1 else ''}")
            else:
                logger.error(f"\n❌ Failed to create project structure for '{base_dir}'")
                print(f"\n❌ Failed to create project structure for '{base_dir}'")
                sys.exit(1)
        else:
            logger.warning("No technologies selected, exiting.")
            print("No technologies selected, exiting.")
            sys.exit(0)
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\nOperation cancelled by user")
        sys.exit(130)
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print(f"\n❌ An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()