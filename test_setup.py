import unittest
import os
import json
import shutil
import logging

from monostack.config.config_manager import ConfigManager
from monostack.core.project_generator import ProjectGenerator

# Disable logging for tests
logging.basicConfig(level=logging.ERROR)

class TestMonostack(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test."""
        self.base_dir = os.path.abspath("test_project")
        os.makedirs(self.base_dir, exist_ok=True)
        self.config_manager = ConfigManager()
        self.project_generator = ProjectGenerator()
    
    def tearDown(self):
        """Clean up test environment after each test."""
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)
    
    def test_load_technologies(self):
        """Test loading technologies configuration."""
        technologies = self.config_manager.load_technologies()
        self.assertIsInstance(technologies, dict)
        self.assertIn("backend", technologies)
        self.assertIn("frontend-web", technologies)
    
    def test_load_docker_compose_template(self):
        """Test loading Docker Compose template."""
        template_content = self.config_manager.load_docker_compose_template()
        self.assertIsInstance(template_content, str)
        self.assertIn("services:", template_content)
    
    def test_create_project_structure(self):
        """Test creating project structure."""
        choices = {
            "backend": {"language": "python", "framework": "flask"},
            "frontend-web": {"language": "javascript", "framework": "react"},
            "frontend-mobile": {"language": "javascript", "framework": "react-native"},
            "frontend-desktop": {"language": "javascript", "framework": "electron"}
        }
        
        # Mock command execution to avoid actually running commands
        def mock_run(*args, **kwargs):
            class MockResult:
                returncode = 0
                stdout = ""
                stderr = ""
            return MockResult()
        
        # Replace the actual command runner with our mock
        original_run = self.project_generator.command_runner.run
        self.project_generator.command_runner.run = mock_run
        
        try:
            # Test project creation
            result = self.project_generator.create_project_structure(self.base_dir, choices)
            self.assertTrue(result)
            
            # Check if directories were created
            self.assertTrue(os.path.exists(os.path.join(self.base_dir, "backend")))
            self.assertTrue(os.path.exists(os.path.join(self.base_dir, "frontend-web")))
            self.assertTrue(os.path.exists(os.path.join(self.base_dir, "frontend-mobile")))
            self.assertTrue(os.path.exists(os.path.join(self.base_dir, "frontend-desktop")))
            self.assertTrue(os.path.exists(os.path.join(self.base_dir, "infra", "docker-compose.yml")))
            self.assertTrue(os.path.exists(os.path.join(self.base_dir, "docs", "README.md")))
            
        finally:
            # Restore the original command runner
            self.project_generator.command_runner.run = original_run

if __name__ == "__main__":
    unittest.main()