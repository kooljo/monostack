import os
import argparse

def prompt_user():
    choices = {
        "backend": ["spring-boot", "nestjs", "django"],
        "frontend-web": ["nextjs", "vuejs"],
        "frontend-mobile": ["react-native", "flutter"],
        "frontend-desktop": ["tauri", "electron"]
    }
    
    user_choices = {}
    print("\nSelect technologies for each module:")
    for module, options in choices.items():
        print(f"\nAvailable options for {module}:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        while True:
            choice = input(f"Enter the number for {module} (default: {options[0]}): ")
            if choice.isdigit() and 1 <= int(choice) <= len(options):
                user_choices[module] = options[int(choice) - 1]
                break
            elif choice == "":
                user_choices[module] = options[0]
                break
            else:
                print("Invalid choice. Please select a valid number.")
    
    return user_choices

def create_project_structure(choices):
    base_dir = "sport-app"
    os.makedirs(base_dir, exist_ok=True)
    
    structure = {
        "backend": choices["backend"],
        "frontend-web": choices["frontend-web"],
        "frontend-mobile": choices["frontend-mobile"],
        "frontend-desktop": choices["frontend-desktop"],
        "infra": "infrastructure",
        "docs": "documentation"
    }
    
    for key, value in structure.items():
        path = os.path.join(base_dir, key)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, "README.md"), "w") as f:
            f.write(f"# {key.capitalize()} - {value.capitalize()}\n")
    
    print(f"\n✅ Project structure for '{base_dir}' created successfully!")
    print("\nFolders created:")
    for folder in structure.keys():
        print(f"- {base_dir}/{folder} ({structure[folder]})")

def main():
    parser = argparse.ArgumentParser(description="Generate a full-stack project structure interactively.")
    parser.add_argument("--default", action="store_true", help="Use default technologies without prompting")
    args = parser.parse_args()
    
    if args.default:
        user_choices = {
            "backend": "spring-boot",
            "frontend-web": "nextjs",
            "frontend-mobile": "react-native",
            "frontend-desktop": "tauri"
        }
        print("\nUsing default technologies:")
        for key, value in user_choices.items():
            print(f"{key}: {value}")
    else:
        user_choices = prompt_user()
    
    create_project_structure(user_choices)

if __name__ == "__main__":
    main()
