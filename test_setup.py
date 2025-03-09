import unittest
import os
import json
from setup import load_technologies, load_docker_compose_template, create_project_structure

class TestSetupScript(unittest.TestCase):
    
    def setUp(self):
        self.base_dir = os.path.abspath("test_project")
        os.makedirs(self.base_dir, exist_ok=True)
        self.install_commands = load_technologies()
    
    def tearDown(self):
        if os.path.exists(self.base_dir):
            os.system(f"rm -rf {self.base_dir}")
    
    def test_load_technologies(self):
        technologies = load_technologies()
        self.assertIsInstance(technologies, dict)
        self.assertIn("backend", technologies)
        self.assertIn("frontend-web", technologies)
    
    def test_load_docker_compose_template(self):
        template_content = load_docker_compose_template()
        self.assertIsInstance(template_content, str)
        self.assertIn("services:", template_content)
    
    def test_create_project_structure(self):
        choices = {
            "backend": {"language": "java", "framework": "spring-boot"},
            "frontend-web": {"language": "javascript", "framework": "react"},
            "frontend-mobile": {"language": "javascript", "framework": "react-native"},
            "frontend-desktop": {"language": "javascript", "framework": "electron"}
        }
        create_project_structure(self.base_dir, choices, self.install_commands)
        
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "backend")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "frontend-web")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "frontend-mobile")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "frontend-desktop")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "infra", "docker-compose.yml")))
        self.assertTrue(os.path.exists(os.path.join(self.base_dir, "docs", "README.md")))

if __name__ == "__main__":
    unittest.main()