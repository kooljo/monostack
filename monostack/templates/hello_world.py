"""
Module containing templates and logic for generating Hello World examples
across different frameworks and languages.
"""
import os
import logging
from typing import Dict, Any, Optional

class HelloWorldGenerator:
    """
    Generates Hello World examples for different backend and frontend frameworks.
    """
    def __init__(self):
        """Initialize the HelloWorldGenerator with a logger."""
        self.logger = logging.getLogger(__name__)
        
    def generate_backend(self, base_dir: str, language: str, framework: str) -> bool:
        """
        Generate a Hello World API endpoint for the specified backend framework.
        
        Args:
            base_dir: The base directory of the project
            language: The programming language (python, javascript, etc)
            framework: The backend framework (flask, express, etc)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            backend_dir = os.path.join(base_dir, "backend")
            
            # Create backend code based on the language and framework
            if language == "python":
                return self._generate_python_backend(backend_dir, framework)
            elif language == "javascript":
                return self._generate_js_backend(backend_dir, framework)
            elif language == "java":
                return self._generate_java_backend(backend_dir, framework)
            elif language == "go":
                return self._generate_go_backend(backend_dir, framework)
            elif language == "php":
                return self._generate_php_backend(backend_dir, framework)
            elif language == "rust":
                return self._generate_rust_backend(backend_dir, framework)
            elif language == "ruby":
                return self._generate_ruby_backend(backend_dir, framework)
            elif language == ".net":
                return self._generate_dotnet_backend(backend_dir, framework)
            else:
                self.logger.warning(f"Hello World generation not supported for {language} backends")
                return False
                
        except Exception as e:
            self.logger.error(f"Error generating Hello World backend: {str(e)}")
            return False
    
    def generate_frontend(self, base_dir: str, module: str, language: str, 
                         framework: str, backend_language: str, backend_framework: str) -> bool:
        """
        Generate a Hello World frontend that consumes the backend API.
        
        Args:
            base_dir: The base directory of the project
            module: The module type (frontend-web, frontend-mobile, etc)
            language: The programming language (javascript, dart, etc)
            framework: The frontend framework (react, flutter, etc)
            backend_language: The backend language (for documentation)
            backend_framework: The backend framework (for documentation)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            frontend_dir = os.path.join(base_dir, module)
            
            # Create frontend code based on the module type, language and framework
            if module == "frontend-web":
                if language == "javascript":
                    return self._generate_js_web_frontend(frontend_dir, framework, backend_language, backend_framework)
                elif language == "python":
                    return self._generate_python_web_frontend(frontend_dir, framework, backend_language, backend_framework)
                # Add other web frontend languages
            
            elif module == "frontend-mobile":
                if language == "javascript":
                    return self._generate_js_mobile_frontend(frontend_dir, framework, backend_language, backend_framework)
                elif language == "dart":
                    return self._generate_dart_mobile_frontend(frontend_dir, framework, backend_language, backend_framework)
                # Add other mobile frontend languages
            
            elif module == "frontend-desktop":
                if language == "javascript":
                    return self._generate_js_desktop_frontend(frontend_dir, framework, backend_language, backend_framework)
                # Add other desktop frontend languages
            
            self.logger.warning(f"Hello World generation not supported for {language} {module} with {framework}")
            return False
            
        except Exception as e:
            self.logger.error(f"Error generating Hello World frontend: {str(e)}")
            return False
    
    # Backend template methods
    def _generate_python_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for Python backends"""
        if framework == "flask":
            return self._generate_flask_hello_world(backend_dir)
        elif framework == "django":
            return self._generate_django_hello_world(backend_dir)
        elif framework == "fastapi":
            return self._generate_fastapi_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for Python {framework}")
            return False
    
    def _generate_js_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for JavaScript backends"""
        if framework == "express":
            return self._generate_express_hello_world(backend_dir)
        elif framework == "nestjs":
            return self._generate_nestjs_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for JavaScript {framework}")
            return False
    
    def _generate_java_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for Java backends"""
        if framework == "spring-boot":
            return self._generate_spring_boot_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for Java {framework}")
            return False
            
    def _generate_spring_boot_hello_world(self, backend_dir: str) -> bool:
        """Generate Hello World for Spring Boot"""
        try:
            # Find the main application class and package structure
            main_app_file = None
            package_name = "com.example"
            
            for root, dirs, files in os.walk(backend_dir):
                for file in files:
                    if file.endswith("Application.java"):
                        main_app_file = os.path.join(root, file)
                        rel_path = os.path.relpath(root, backend_dir)
                        package_name = rel_path.replace(os.path.sep, ".")
                        if package_name.startswith("src.main.java."):
                            package_name = package_name[len("src.main.java."):]
                        break
                if main_app_file:
                    break
            
            # Create controllers directory if it doesn't exist
            controller_dir = os.path.join(backend_dir, "src", "main", "java", *package_name.split("."), "controllers")
            os.makedirs(controller_dir, exist_ok=True)
            
            # Create HelloWorldController.java
            controller_file = os.path.join(controller_dir, "HelloWorldController.java")
            controller_content = f"""package {package_name}.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.CrossOrigin;
import java.util.HashMap;
import java.util.Map;

@RestController
@CrossOrigin(origins = "*")
public class HelloWorldController {{

    @GetMapping("/hello")
    public Map<String, String> helloWorld() {{
        Map<String, String> response = new HashMap<>();
        response.put("message", "Hello, World!");
        return response;
    }}
}}
"""
            with open(controller_file, 'w') as f:
                f.write(controller_content)
            
            # Update pom.xml to ensure web dependency
            pom_file = os.path.join(backend_dir, "pom.xml")
            if os.path.exists(pom_file):
                with open(pom_file, 'r') as f:
                    pom_content = f.read()
                    
                # Check if spring-boot-starter-web dependency is already included
                if "<artifactId>spring-boot-starter-web</artifactId>" not in pom_content:
                    # Add web dependency if not present
                    if "<dependencies>" in pom_content:
                        web_dependency = """
        <!-- Spring Web Dependency -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>"""
                        pom_content = pom_content.replace("<dependencies>", f"<dependencies>{web_dependency}")
                        
                        with open(pom_file, 'w') as f:
                            f.write(pom_content)
            
            # Create README for Hello World API
            readme_file = os.path.join(backend_dir, "HELLO_WORLD_README.md")
            readme_content = """# Spring Boot Hello World API

This project includes a simple Hello World REST API endpoint.

## Endpoint

- **URL**: `/hello`
- **Method**: `GET`
- **Response**: `{"message": "Hello, World!"}`

## Running the Application

1. Navigate to the backend directory
2. Run `mvn spring-boot:run`
3. Access the API at http://localhost:8080/hello

## Testing with cURL

```bash
curl http://localhost:8080/hello
```

## CORS Configuration

CORS is enabled for all origins to allow frontend applications to connect to this API.
"""
            with open(readme_file, 'w') as f:
                f.write(readme_content)
                
            self.logger.info(f"Generated Spring Boot Hello World endpoint in {controller_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error generating Spring Boot Hello World: {str(e)}")
            return False
            
    def _generate_go_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for Go backends"""
        if framework == "gin":
            return self._generate_gin_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for Go {framework}")
            return False
    
    def _generate_php_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for PHP backends"""
        if framework == "laravel":
            return self._generate_laravel_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for PHP {framework}")
            return False
    
    def _generate_rust_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for Rust backends"""
        if framework == "actix-web":
            return self._generate_actix_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for Rust {framework}")
            return False
    
    def _generate_ruby_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for Ruby backends"""
        if framework == "rails":
            return self._generate_rails_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for Ruby {framework}")
            return False
    
    def _generate_dotnet_backend(self, backend_dir: str, framework: str) -> bool:
        """Generate Hello World for .NET backends"""
        if framework == "aspnet-core":
            return self._generate_aspnet_hello_world(backend_dir)
        else:
            self.logger.warning(f"Hello World not supported for .NET {framework}")
            return False
    
    # Frontend template methods
    def _generate_js_web_frontend(self, frontend_dir: str, framework: str, 
                                 backend_language: str, backend_framework: str) -> bool:
        """Generate Hello World for JavaScript web frontends"""
        if framework == "react":
            return self._generate_react_hello_world(frontend_dir, backend_language, backend_framework)
        elif framework == "nextjs":
            return self._generate_nextjs_hello_world(frontend_dir, backend_language, backend_framework)
        elif framework == "vuejs":
            return self._generate_vue_hello_world(frontend_dir, backend_language, backend_framework)
        elif framework == "angular":
            return self._generate_angular_hello_world(frontend_dir, backend_language, backend_framework)
        else:
            self.logger.warning(f"Hello World not supported for JavaScript {framework}")
            return False
    
    def _generate_js_mobile_frontend(self, frontend_dir: str, framework: str,
                                   backend_language: str, backend_framework: str) -> bool:
        """Generate Hello World for JavaScript mobile frontends"""
        if framework == "react-native":
            return self._generate_react_native_hello_world(frontend_dir, backend_language, backend_framework)
        elif framework == "expo":
            return self._generate_expo_hello_world(frontend_dir, backend_language, backend_framework)
        else:
            self.logger.warning(f"Hello World not supported for JavaScript {framework}")
            return False
    
    def _generate_dart_mobile_frontend(self, frontend_dir: str, framework: str,
                                     backend_language: str, backend_framework: str) -> bool:
        """Generate Hello World for Dart mobile frontends"""
        if framework == "flutter":
            return self._generate_flutter_hello_world(frontend_dir, backend_language, backend_framework)
        else:
            self.logger.warning(f"Hello World not supported for Dart {framework}")
            return False
    
    def _generate_js_desktop_frontend(self, frontend_dir: str, framework: str,
                                    backend_language: str, backend_framework: str) -> bool:
        """Generate Hello World for JavaScript desktop frontends"""
        if framework == "electron":
            return self._generate_electron_hello_world(frontend_dir, backend_language, backend_framework)
        elif framework == "tauri":
            return self._generate_tauri_hello_world(frontend_dir, backend_language, backend_framework)
        else:
            self.logger.warning(f"Hello World not supported for JavaScript {framework}")
            return False
    
    # Specific framework implementations
    def _generate_flask_hello_world(self, backend_dir: str) -> bool:
        """Generate Hello World for Flask"""
        try:
            app_file = self._find_file(backend_dir, "app.py")
            if not app_file:
                app_file = os.path.join(backend_dir, "app.py")
                
            flask_content = """
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    app.run(debug=True)
"""
            
            if os.path.exists(app_file):
                with open(app_file, 'r') as f:
                    content = f.read()
                
                if 'def hello_world():' not in content:
                    # Add imports if they don't exist
                    if 'from flask_cors import CORS' not in content:
                        content = content.replace('from flask import', 'from flask import Flask, jsonify\nfrom flask_cors import CORS')
                    if 'CORS(app)' not in content:
                        content = content.replace('app = Flask(__name__)', 'app = Flask(__name__)\nCORS(app)  # Enable CORS for all routes')
                    
                    # Add the route
                    route_code = """
@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({"message": "Hello, World!"})
"""
                    # Add before if __name__ == '__main__' or at the end if not found
                    if 'if __name__ == ' in content:
                        content = content.replace('if __name__ == ', route_code + '\nif __name__ == ')
                    else:
                        content += '\n' + route_code
                    
                    with open(app_file, 'w') as f:
                        f.write(content)
            else:
                with open(app_file, 'w') as f:
                    f.write(flask_content)
                    
            # Add requirements
            requirements_file = os.path.join(backend_dir, "requirements.txt")
            requirements = ["flask", "flask-cors"]
            
            if os.path.exists(requirements_file):
                with open(requirements_file, 'r') as f:
                    content = f.read()
                
                for req in requirements:
                    if req not in content:
                        with open(requirements_file, 'a') as f:
                            f.write(f"\n{req}")
            else:
                with open(requirements_file, 'w') as f:
                    f.write("\n".join(requirements))
            
            self.logger.info(f"Generated Flask Hello World endpoint in {app_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating Flask Hello World: {str(e)}")
            return False
    
    def _generate_express_hello_world(self, backend_dir: str) -> bool:
        """Generate Hello World for Express.js"""
        try:
            app_file = self._find_file(backend_dir, "app.js") or self._find_file(backend_dir, "index.js")
            if not app_file:
                app_file = os.path.join(backend_dir, "app.js")
                
            express_content = """
const express = require('express');
const cors = require('cors');
const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

app.get('/hello', (req, res) => {
  res.json({ message: 'Hello, World!' });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
"""
            
            if os.path.exists(app_file):
                with open(app_file, 'r') as f:
                    content = f.read()
                
                if "app.get('/hello'" not in content and 'app.get("/hello"' not in content:
                    # Add cors if it doesn't exist
                    if 'cors' not in content:
                        content = content.replace('const express = require', "const cors = require('cors');\nconst express = require")
                    if 'app.use(cors())' not in content:
                        content = content.replace('const app = express()', "const app = express();\napp.use(cors());")
                    
                    # Add the route before the app.listen
                    if 'app.listen' in content:
                        route_code = """
app.get('/hello', (req, res) => {
  res.json({ message: 'Hello, World!' });
});
"""
                        content = content.replace('app.listen', route_code + '\napp.listen')
                    else:
                        content += """
app.get('/hello', (req, res) => {
  res.json({ message: 'Hello, World!' });
});
"""
                    
                    with open(app_file, 'w') as f:
                        f.write(content)
            else:
                with open(app_file, 'w') as f:
                    f.write(express_content)
                    
            # Add package.json if it doesn't exist
            package_file = os.path.join(backend_dir, "package.json")
            if not os.path.exists(package_file):
                package_content = """{
  "name": "express-hello-world",
  "version": "1.0.0",
  "description": "Express Hello World API",
  "main": "app.js",
  "scripts": {
    "start": "node app.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "cors": "^2.8.5"
  }
}
"""
                with open(package_file, 'w') as f:
                    f.write(package_content)
            else:
                # Update package.json to add dependencies
                import json
                with open(package_file, 'r') as f:
                    package_data = json.load(f)
                
                if 'dependencies' not in package_data:
                    package_data['dependencies'] = {}
                
                if 'express' not in package_data['dependencies']:
                    package_data['dependencies']['express'] = "^4.17.1"
                
                if 'cors' not in package_data['dependencies']:
                    package_data['dependencies']['cors'] = "^2.8.5"
                
                with open(package_file, 'w') as f:
                    json.dump(package_data, f, indent=2)
            
            self.logger.info(f"Generated Express Hello World endpoint in {app_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating Express Hello World: {str(e)}")
            return False
    
    def _generate_react_hello_world(self, frontend_dir: str, backend_language: str, backend_framework: str) -> bool:
        """Generate Hello World for React"""
        try:
            # Create HelloWorld component
            components_dir = os.path.join(frontend_dir, "src", "components")
            os.makedirs(components_dir, exist_ok=True)
            
            component_file = os.path.join(components_dir, "HelloWorld.js")
            component_content = """import React, { useState, useEffect } from 'react';
import './HelloWorld.css';

function HelloWorld() {
  const [message, setMessage] = useState('Loading...');
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:3000/hello')
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setMessage(data.message);
      })
      .catch(error => {
        console.error('Error fetching hello world:', error);
        setError('Failed to fetch message from backend');
      });
  }, []);

  return (
    <div className="hello-world-container">
      <h1>Hello World Example</h1>
      {error ? (
        <div className="error-message">
          <p>{error}</p>
          <p>Make sure your {backend_framework} backend is running!</p>
        </div>
      ) : (
        <div className="message-container">
          <p>Message from {backend_framework} backend:</p>
          <div className="message">{message}</div>
        </div>
      )}
    </div>
  );
}

export default HelloWorld;
"""
            
            with open(component_file, 'w') as f:
                f.write(component_content)
            
            # Create CSS file
            css_file = os.path.join(components_dir, "HelloWorld.css")
            css_content = """.hello-world-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
  border-radius: 10px;
  background-color: #f5f5f5;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.message-container {
  margin-top: 1.5rem;
}

.message {
  font-size: 1.5rem;
  font-weight: bold;
  padding: 1rem;
  border-radius: 5px;
  background-color: #e6f7ff;
  border: 1px solid #91d5ff;
  color: #0050b3;
}

.error-message {
  color: #f5222d;
  padding: 1rem;
  border-radius: 5px;
  background-color: #fff2f0;
  border: 1px solid #ffccc7;
}
"""
            
            with open(css_file, 'w') as f:
                f.write(css_content)
            
            # Update App.js to include the component
            app_file = self._find_file(frontend_dir, "App.js")
            if app_file:
                with open(app_file, 'r') as f:
                    app_content = f.read()
                
                if 'HelloWorld' not in app_content:
                    # Add import
                    if 'import React' in app_content:
                        app_content = app_content.replace('import React', "import React from 'react';\nimport HelloWorld from './components/HelloWorld';")
                    else:
                        app_content = "import React from 'react';\nimport HelloWorld from './components/HelloWorld';\n" + app_content
                    
                    # Add component to the return statement
                    if 'return (' in app_content:
                        app_content = app_content.replace('return (', 'return (\n      <HelloWorld />')
                    
                    with open(app_file, 'w') as f:
                        f.write(app_content)
            
            self.logger.info(f"Generated React Hello World component in {component_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating React Hello World: {str(e)}")
            return False
    
    def _generate_react_native_hello_world(self, frontend_dir: str, backend_language: str, backend_framework: str) -> bool:
        """Generate Hello World for React Native"""
        try:
            # Create HelloWorld component
            components_dir = os.path.join(frontend_dir, "src", "components")
            os.makedirs(components_dir, exist_ok=True)
            
            component_file = os.path.join(components_dir, "HelloWorld.js")
            component_content = """import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';

const HelloWorld = () => {
  const [message, setMessage] = useState('Loading...');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHelloWorld();
  }, []);

  const fetchHelloWorld = async () => {
    try {
      // Use 10.0.2.2 for Android emulator to access localhost
      // Use localhost for iOS simulator
      const response = await fetch('http://10.0.2.2:3000/hello');
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();
      setMessage(data.message);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching hello world:', error);
      setError('Failed to fetch message from backend');
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Hello World Example</Text>
      
      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : error ? (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Text style={styles.errorText}>Make sure your {backend_framework} backend is running!</Text>
        </View>
      ) : (
        <View style={styles.messageContainer}>
          <Text style={styles.label}>Message from {backend_framework} backend:</Text>
          <Text style={styles.message}>{message}</Text>
        </View>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  messageContainer: {
    marginTop: 20,
    padding: 15,
    borderRadius: 10,
    backgroundColor: '#e6f7ff',
    width: '100%',
    alignItems: 'center',
  },
  label: {
    fontSize: 16,
    marginBottom: 10,
  },
  message: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#0050b3',
  },
  errorContainer: {
    marginTop: 20,
    padding: 15,
    borderRadius: 10,
    backgroundColor: '#fff2f0',
    width: '100%',
    alignItems: 'center',
  },
  errorText: {
    color: '#f5222d',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 5,
  },
});

export default HelloWorld;
"""
            
            with open(component_file, 'w') as f:
                f.write(component_content)
            
            # Update App.js to include the component
            app_file = self._find_file(frontend_dir, "App.js")
            if app_file:
                with open(app_file, 'r') as f:
                    app_content = f.read()
                
                if 'HelloWorld' not in app_content:
                    # Add import
                    if 'import React' in app_content:
                        app_content = app_content.replace('import React', "import React from 'react';\nimport HelloWorld from './src/components/HelloWorld';")
                    else:
                        app_content = "import React from 'react';\nimport HelloWorld from './src/components/HelloWorld';\n" + app_content
                    
                    # Add component to the return statement
                    if 'return (' in app_content:
                        app_content = app_content.replace('return (', 'return (\n      <HelloWorld />')
                    elif '<View' in app_content:
                        app_content = app_content.replace('<View', '<HelloWorld />\n      <View')
                    
                    with open(app_file, 'w') as f:
                        f.write(app_content)
                        
            # Add README with instructions for backend connection
            readme_file = os.path.join(frontend_dir, "HELLO_WORLD_README.md")
            readme_content = f"""# Hello World Example with {backend_framework}

This React Native application fetches data from the {backend_framework} backend's Hello World API.

## Backend Connection
- The app connects to the backend at `http://10.0.2.2:3000/hello` for Android emulators.
- For iOS simulators, it uses `http://localhost:3000/hello`.
- For real devices, you'll need to update the URL to your development machine's IP address.

## Troubleshooting
- Make sure your {backend_framework} backend is running.
- Check that the backend has CORS enabled.
- Verify that the port number matches your backend configuration.
"""
            
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            
            self.logger.info(f"Generated React Native Hello World component in {component_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error generating React Native Hello World: {str(e)}")
            return False
    
    def _find_file(self, directory: str, filename: str) -> Optional[str]:
        """Find a file in the directory structure"""
        for root, dirs, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
        return None