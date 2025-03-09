import os
import argparse
import json

def load_technologies():
    config_path = os.path.join(os.path.dirname(__file__), "install_commands.json")
    with open(config_path, "r") as f:
        return json.load(f)

def load_docker_compose_template():
    template_path = os.path.join(os.path.dirname(__file__), "docker_compose_template.yml")
    with open(template_path, "r") as f:
        return f.read()

def prompt_user(technologies):
    user_choices = {}
    print("\nSelect technologies for each module:")
    
    # Step 1: Choose a backend language
    backend_languages = list(technologies["backend"].keys())
    print("\nChoose a backend language:")
    language_choice = os.popen(f'gum choose {" ".join(backend_languages)}').read().strip()
    
    if language_choice in backend_languages:
        backend_technologies = list(technologies["backend"][language_choice].keys())
        print(f"\nChoose a backend framework for {language_choice}:")
        tech_choice = os.popen(f'gum choose {" ".join(backend_technologies)}').read().strip()
        user_choices["backend"] = {"language": language_choice, "framework": tech_choice if tech_choice in backend_technologies else backend_technologies[0]}
    
    # Step 2: Choose frontend-web language and framework
    web_languages = list(technologies["frontend-web"].keys())
    print("\nChoose a frontend-web language:")
    web_language_choice = os.popen(f'gum choose {" ".join(web_languages)}').read().strip()
    
    if web_language_choice in web_languages:
        web_technologies = list(technologies["frontend-web"][web_language_choice].keys())
        print(f"\nChoose a frontend-web framework for {web_language_choice}:")
        web_tech_choice = os.popen(f'gum choose {" ".join(web_technologies)}').read().strip()
        user_choices["frontend-web"] = {"language": web_language_choice, "framework": web_tech_choice if web_tech_choice in web_technologies else web_technologies[0]}
    
    # Step 3: Choose frontend-mobile language and framework
    mobile_languages = list(technologies["frontend-mobile"].keys())
    print("\nChoose a frontend-mobile language:")
    mobile_language_choice = os.popen(f'gum choose {" ".join(mobile_languages)}').read().strip()
    
    if mobile_language_choice in mobile_languages:
        mobile_technologies = list(technologies["frontend-mobile"][mobile_language_choice].keys())
        print(f"\nChoose a frontend-mobile framework for {mobile_language_choice}:")
        mobile_tech_choice = os.popen(f'gum choose {" ".join(mobile_technologies)}').read().strip()
        user_choices["frontend-mobile"] = {"language": mobile_language_choice, "framework": mobile_tech_choice if mobile_tech_choice in mobile_technologies else mobile_technologies[0]}
    
    # Step 4: Choose frontend-desktop language and framework
    desktop_languages = list(technologies["frontend-desktop"].keys())
    print("\nChoose a frontend-desktop language:")
    desktop_language_choice = os.popen(f'gum choose {" ".join(desktop_languages)}').read().strip()
    
    if desktop_language_choice in desktop_languages:
        desktop_technologies = list(technologies["frontend-desktop"][desktop_language_choice].keys())
        print(f"\nChoose a frontend-desktop framework for {desktop_language_choice}:")
        desktop_tech_choice = os.popen(f'gum choose {" ".join(desktop_technologies)}').read().strip()
        user_choices["frontend-desktop"] = {"language": desktop_language_choice, "framework": desktop_tech_choice if desktop_tech_choice in desktop_technologies else desktop_technologies[0]}
    
    return user_choices

def initialize_git_repo(base_dir):
    """Initializes a Git repository in the generated project."""
    print("📦 Initializing Git repository...")
    
    os.system(f"cd {base_dir} && git init")
    os.system(f"cd {base_dir} && git add .")
    os.system(f"cd {base_dir} && git commit -m 'Initial commit with project structure'")
    
    print("✅ Git repository initialized successfully!")

def initialize_project(base_dir, module, choice, install_commands):
    project_path = os.path.join(base_dir, module)

    # Assure que le dossier existe avant toute opération
    os.makedirs(project_path, exist_ok=True)

    language = choice["language"]
    framework = choice["framework"]

    if module in install_commands and language in install_commands[module] and framework in install_commands[module][language]:
        install_command = install_commands[module][language][framework].replace("{module}", module)
        print(f"📦 Installing {framework} ({language}) in {module}...")
        os.system(f"cd {base_dir} && {install_command}")

        # Vérifie après l'installation si le dossier a été bien créé
        if not os.path.exists(project_path):
            os.makedirs(project_path, exist_ok=True)
    else:
        print(f"⚠️ No installation command found for {framework} in {language} ({module}). Skipping installation.")

    # Ajoute un README.md dans chaque dossier
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.write(f"# {module.capitalize()} - {framework} ({language})\n")

def generate_docker_compose(base_dir):
    docker_compose_content = load_docker_compose_template()
    infra_path = os.path.join(base_dir, "infra")
    os.makedirs(infra_path, exist_ok=True)
    
    with open(os.path.join(infra_path, "docker-compose.yml"), "w") as f:
        f.write(docker_compose_content)

def create_project_structure(base_dir, choices, install_commands):
    os.makedirs(base_dir, exist_ok=True)
    for module, choice in choices.items():
        initialize_project(base_dir, module, choice, install_commands)
    
    generate_docker_compose(base_dir)
    
    docs_path = os.path.join(base_dir, "docs")
    os.makedirs(docs_path, exist_ok=True)
    with open(os.path.join(docs_path, "README.md"), "w") as f:
        f.write("# Documentation\n\nAdd your project documentation here.")
    
    initialize_git_repo(base_dir)
    print(f"\n✅ Project structure for '{base_dir}' created successfully!")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, help="Set the project name (default: mono-app)")
    args = parser.parse_args()
    
    project_name = args.name if args.name else "mono-app"
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "..", project_name))
    install_commands = load_technologies()
    user_choices = prompt_user(install_commands)
    create_project_structure(base_dir, user_choices, install_commands)

if __name__ == "__main__":
    main()
