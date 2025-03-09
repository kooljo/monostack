import os
import argparse
import json

def load_technologies():
    config_path = os.path.join(os.path.dirname(__file__), "technologies_config.json")
    with open(config_path, "r") as f:
        return json.load(f)

def prompt_user(technologies):
    user_choices = {}
    print("\nSelect technologies for each module:")
    for module, options in technologies.items():
        options_str = ' '.join(options)
        choice = os.popen(f'gum choose {options_str}').read().strip()
        
        if choice in options:
            user_choices[module] = choice
        else:
            user_choices[module] = options[0]
    
    return user_choices

def initialize_project(directory, tech, module):
    os.makedirs(directory, exist_ok=True)
    print(f"\n📦 Initializing {tech} in {module}...")
    
    if module == "backend":
        if tech == "spring-boot":
            os.system(f'cd {directory} && mvn archetype:generate -DgroupId=com.example -DartifactId=backend -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false')
        elif tech == "nestjs":
            os.system(f'cd {directory} && npx @nestjs/cli new backend --skip-git')
        elif tech == "django":
            os.system(f'cd {directory} && django-admin startproject backend')
    
    elif module == "frontend-web":
        if tech == "nextjs":
            os.system(f'cd {directory} && npx create-next-app@latest frontend-web --ts --use-npm')
        elif tech == "vuejs":
            os.system(f'cd {directory} && npm create vue@latest frontend-web')
    
    elif module == "frontend-mobile":
        if tech == "react-native":
            os.system(f'cd {directory} && npx react-native init frontend-mobile')
        elif tech == "flutter":
            os.system(f'cd {directory} && flutter create frontend-mobile')
    
    elif module == "frontend-desktop":
        if tech == "tauri":
            os.system(f'cd {directory} && cargo install create-tauri-app && create-tauri-app frontend-desktop')
        elif tech == "electron":
            os.system(f'cd {directory} && npx create-electron-app frontend-desktop')

def create_project_structure(base_dir, choices):
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
        initialize_project(path, value, key)
    
    generate_docker_compose(base_dir, choices)
    initialize_git_repo(base_dir)
    
    print(f"\n✅ Project structure for '{base_dir}' created successfully!")
    print("\nFolders created:")
    for folder in structure.keys():
        print(f"- {base_dir}/{folder} ({structure[folder]})")

def generate_docker_compose(base_dir, choices):
    template_path = os.path.join(os.path.dirname(__file__), "docker_compose_template.yml")
    with open(template_path, "r") as f:
        docker_compose_content = f.read()
    
    docker_compose_content = docker_compose_content.replace("{{backend}}", choices["backend"])
    docker_compose_content = docker_compose_content.replace("{{frontend-web}}", choices["frontend-web"])
    docker_compose_content = docker_compose_content.replace("{{frontend-mobile}}", choices["frontend-mobile"])
    docker_compose_content = docker_compose_content.replace("{{frontend-desktop}}", choices["frontend-desktop"])
    
    infra_path = os.path.join(base_dir, "infra")
    os.makedirs(infra_path, exist_ok=True)
    with open(os.path.join(infra_path, "docker-compose.yml"), "w") as f:
        f.write(docker_compose_content)
    print("\n✅ docker-compose.yml generated!")

def initialize_git_repo(base_dir):
    os.system(f"cd {base_dir} && git init")
    os.system(f"cd {base_dir} && git add .")
    os.system(f"cd {base_dir} && git commit -m 'Initial commit with project structure' ")
    print("\n✅ Git repository initialized!")

def main():
    parser = argparse.ArgumentParser(description="Generate a full-stack project structure interactively.")
    parser.add_argument("--default", action="store_true", help="Use default technologies without prompting")
    parser.add_argument("--name", type=str, help="Set the project name (default: mono-app)")
    args = parser.parse_args()
    
    project_name = args.name if args.name else "mono-app"
    base_dir = os.path.abspath(os.path.join(os.getcwd(), "..", project_name))
    
    technologies = load_technologies()
    
    if args.default:
        user_choices = {module: options[0] for module, options in technologies.items()}
        print("\nUsing default technologies:")
        for key, value in user_choices.items():
            print(f"{key}: {value}")
    else:
        user_choices = prompt_user(technologies)
    
    create_project_structure(base_dir, user_choices)

if __name__ == "__main__":
    main()
