"""
Module for generating appropriate .gitignore files for different project types.
"""
import os
import logging
from typing import Dict, Any

class GitignoreGenerator:
    """
    Generates appropriate .gitignore files for different project types.
    """
    def __init__(self):
        """Initialize the GitignoreGenerator with a logger."""
        self.logger = logging.getLogger(__name__)
        
    def add_gitignore(self, project_dir: str, module_type: str, language: str, framework: str) -> bool:
        """
        Add an appropriate .gitignore file to the project directory.
        
        Args:
            project_dir: Project directory path
            module_type: Type of module (backend, frontend-web, etc.)
            language: Programming language
            framework: Framework or library used
            
        Returns:
            True if successful, False otherwise
        """
        try:
            gitignore_content = self._get_gitignore_content(module_type, language, framework)
            
            if not gitignore_content:
                self.logger.warning(f"No gitignore template found for {language}/{framework}")
                gitignore_content = self._get_generic_gitignore(language)
            
            gitignore_path = os.path.join(project_dir, ".gitignore")
            
            # Check if file already exists and has content
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r') as f:
                    existing_content = f.read()
                
                # Append our content without duplicating
                combined_content = existing_content
                for line in gitignore_content.split('\n'):
                    if line.strip() and line not in existing_content:
                        combined_content += f"\n{line}"
                
                with open(gitignore_path, 'w') as f:
                    f.write(combined_content)
            else:
                # Create new gitignore file
                with open(gitignore_path, 'w') as f:
                    f.write(gitignore_content)
            
            self.logger.info(f"Added .gitignore to {project_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding .gitignore: {str(e)}")
            return False
    
    def add_root_gitignore(self, base_dir: str, choices: Dict[str, Any]) -> bool:
        """
        Add a root .gitignore file to the project that combines patterns for all selected technologies.
        
        Args:
            base_dir: Base project directory
            choices: User technology choices
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Start with common patterns
            gitignore_content = """# General
.DS_Store
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Editor directories and files
.idea
.vscode
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?
*.sublime-*
.project

# Deployment
/dist
/build
/out
.vercel
.netlify

"""
            # Add specific patterns for selected technologies
            for module, choice in choices.items():
                if module != "database" and "language" in choice and "framework" in choice:
                    language = choice["language"]
                    framework = choice["framework"]
                    
                    patterns = self._get_gitignore_content(module, language, framework)
                    if patterns:
                        gitignore_content += f"\n# {module.upper()} - {framework} ({language})\n"
                        gitignore_content += patterns + "\n"
            
            # Add patterns for database if selected
            if "database" in choices and "type" in choices["database"]:
                db_type = choices["database"]["type"]
                
                gitignore_content += f"\n# DATABASE - {db_type}\n"
                if db_type == "postgres":
                    gitignore_content += "*.dump\n*.sql\n"
                elif db_type == "mongodb":
                    gitignore_content += "*.bson\n*.mongodump\n"
                elif db_type == "sqlite":
                    gitignore_content += "*.sqlite\n*.sqlite3\n*.db\n"
            
            # Write the file
            gitignore_path = os.path.join(base_dir, ".gitignore")
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            
            self.logger.info(f"Added root .gitignore to {base_dir}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding root .gitignore: {str(e)}")
            return False
    
    def _get_gitignore_content(self, module_type: str, language: str, framework: str) -> str:
        """
        Get the appropriate .gitignore content for a specific language and framework.
        
        Args:
            module_type: Type of module (backend, frontend-web, etc.)
            language: Programming language
            framework: Framework or library used
            
        Returns:
            String containing the appropriate .gitignore content
        """
        # JavaScript/TypeScript frameworks (common patterns for Node.js projects)
        if language == "javascript":
            if framework in ["react", "nextjs", "angular", "vuejs", "svelte", "express", "nestjs"]:
                return """# Dependencies
/node_modules
/.pnp
.pnp.js
/package-lock.json
/yarn.lock
/yarn-error.log

# Testing
/coverage

# Production
/build
/dist
/out
/.next
/.nuxt
/.svelte-kit

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Misc
.DS_Store
.turbo

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*"""
                
            elif framework in ["react-native", "expo"]:
                return """# Dependencies
/node_modules
/.pnp
.pnp.js
/package-lock.json
/yarn.lock
/yarn-error.log

# Testing
/coverage

# Production
/build
/dist

# Configuration
.expo/
.expo-shared/
metro.config.*

# Generated files
*.jsbundle
*.tsbuildinfo
.DS_Store

# Environment variables
.env
.env.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Native
*.orig.*
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.orig.*

# Android
/android/app/debug
/android/app/release
.gradle
local.properties
*.iml

# iOS
/ios/Pods/
/ios/build/
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata
*.xccheckout
*.moved-aside
DerivedData
*.hmap
*.ipa
*.xcuserstate
project.xcworkspace
"""
                
            elif framework in ["electron", "tauri"]:
                return """# Dependencies
/node_modules
/.pnp
.pnp.js
/package-lock.json
/yarn.lock
/yarn-error.log

# Testing
/coverage

# Production
/build
/dist
/out
/out-tsc

# Generated files
/.webpack
/.quasar

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS specific
.DS_Store
desktop.ini
thumbs.db

# Environment variables
.env
.env.local
"""
        
        # Python frameworks
        elif language == "python":
            if framework in ["django", "flask", "fastapi"]:
                return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
"""
                
            elif framework in ["kivy", "beeware"]:
                return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Buildozer 
.buildozer/
bin/

# Briefcase
iOS/
macOS/
windows/
android/
linux/
"""
        
        # Java frameworks
        elif language == "java":
            if framework in ["spring-boot", "quarkus", "micronaut"]:
                return """# Compiled class file
*.class

# Log file
*.log

# BlueJ files
*.ctxt

# Mobile Tools for Java (J2ME)
.mtj.tmp/

# Package Files #
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# virtual machine crash logs
hs_err_pid*
replay_pid*

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# Gradle
.gradle
**/build/
!src/**/build/
gradle-app.setting
!gradle-wrapper.jar
.gradletasknamecache

# IntelliJ IDEA
.idea/
*.iws
*.iml
*.ipr
out/
!**/src/main/**/out/
!**/src/test/**/out/

# Eclipse
.settings/
.classpath
.project
.metadata
bin/
tmp/
*.tmp
*.bak
*.swp
*~.nib
.loadpath
.recommenders

# Spring Boot
.spring-boot-devtools
"""
        
        # Go frameworks
        elif language == "go":
            return """# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool, specifically when used with LiteIDE
*.out

# Dependency directories (remove the comment below to include it)
vendor/

# Go workspace file
go.work

# IDE files
.idea/
.vscode/
*.iml
*.swp
*.swo

# OS specific
.DS_Store
"""
        
        # PHP frameworks
        elif language == "php":
            if framework in ["laravel", "symfony"]:
                return """# Laravel/Symfony
/vendor/
node_modules/
npm-debug.log
yarn-error.log

# Laravel specific
public/storage
public/hot
storage/*.key
.env
.env.backup
Homestead.yaml
Homestead.json
/.vagrant
.phpunit.result.cache

# Symfony specific
/public/bundles/
/var/
/bin/*
!bin/console
!bin/symfony_requirements
/app/config/parameters.yml
/phpunit.xml
/.web-server-pid

# Composer
composer.phar
/vendor/

# IDE
/.idea
/.vscode
*.sublime-project
*.sublime-workspace
"""
        
        # Ruby frameworks
        elif language == "ruby":
            if framework in ["rails", "sinatra"]:
                return """# Ruby/Rails
*.rbc
capybara-*.html
.rspec
/db/*.sqlite3
/db/*.sqlite3-journal
/db/*.sqlite3-[0-9]*
/public/system
/coverage/
/spec/tmp
*.orig
rerun.txt
pickle-email-*.html

# Ignore all logfiles and tempfiles.
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep

# Environment configurations
/.env
/.bundle
/vendor/bundle

# RVM
.rvmrc

# Rails specific
/config/master.key
/config/credentials/*.key
/config/master.key
/public/packs
/public/packs-test
/public/assets
/storage/*
!/storage/.keep
.byebug_history
/node_modules
/yarn-error.log
yarn-debug.log*
.yarn-integrity
"""
        
        # Rust frameworks
        elif language == "rust":
            return """# Generated files
/target/
**/*.rs.bk
Cargo.lock

# These are backup files generated by rustfmt
**/*.rs.bk

# MSVC Windows builds of rustc generate these, which store debugging information
*.pdb

# IDE
.idea/
.vscode/
*.iml
"""
        
        # Flutter
        elif language == "dart":
            return """# Miscellaneous
*.class
*.log
*.pyc
*.swp
.DS_Store
.atom/
.buildlog/
.history
.svn/
migrate_working_dir/

# IntelliJ related
*.iml
*.ipr
*.iws
.idea/

# Visual Studio Code related
.classpath
.project
.settings/
.vscode/

# Flutter/Dart/Pub related
**/doc/api/
**/ios/Flutter/.last_build_id
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
.pub-cache/
.pub/
/build/
/windows/flutter/ephemeral/

# Symbolication related
app.*.symbols

# Obfuscation related
app.*.map.json

# Android related
**/android/**/gradle-wrapper.jar
**/android/.gradle
**/android/captures/
**/android/gradlew
**/android/gradlew.bat
**/android/local.properties
**/android/**/GeneratedPluginRegistrant.java
**/android/key.properties

# iOS/XCode related
**/ios/**/*.mode1v3
**/ios/**/*.mode2v3
**/ios/**/*.moved-aside
**/ios/**/*.pbxuser
**/ios/**/*.perspectivev3
**/ios/**/*sync/
**/ios/**/.sconsign.dblite
**/ios/**/.tags*
**/ios/**/.vagrant/
**/ios/**/DerivedData/
**/ios/**/Icon?
**/ios/**/Pods/
**/ios/**/.symlinks/
**/ios/**/profile
**/ios/**/xcuserdata
**/ios/.generated/
**/ios/Flutter/App.framework
**/ios/Flutter/Flutter.framework
**/ios/Flutter/Generated.xcconfig
**/ios/Flutter/app.flx
**/ios/Flutter/app.zip
**/ios/Flutter/flutter_assets/
**/ios/ServiceDefinitions.json
**/ios/Runner/GeneratedPluginRegistrant.*
"""
        
        # .NET frameworks
        elif language == ".net":
            return """# Visual Studio files
.vs/
*.user
*.userosscache
*.suo
*.userprefs
*.dbmdl
*.dbproj.schemaview
*.jfm
*.pfx
*.publishsettings

# Build results
[Dd]ebug/
[Dd]ebugPublic/
[Rr]elease/
[Rr]eleases/
x64/
x86/
[Ww][Ii][Nn]32/
[Aa][Rr][Mm]/
[Aa][Rr][Mm]64/
bld/
[Bb]in/
[Oo]bj/
[Ll]og/
[Ll]ogs/

# NuGet Packages
*.nupkg
# NuGet Symbol Packages
*.snupkg
# The packages folder can be ignored because of Package Restore
**/[Pp]ackages/*
# except build/, which is used as an MSBuild target.
!**/[Pp]ackages/build/
*.nuget.props
*.nuget.targets

# MSTest test Results
[Tt]est[Rr]esult*/
[Bb]uild[Ll]og.*

# .NET Core
project.lock.json
project.fragment.lock.json
artifacts/
"""
        
        # Return empty string if no match
        return ""
    
    def _get_generic_gitignore(self, language: str) -> str:
        """
        Get generic .gitignore content for a language when no specific framework is matched.
        
        Args:
            language: Programming language
            
        Returns:
            String containing generic .gitignore content
        """
        if language == "javascript":
            return """# Dependencies
/node_modules
/.pnp
.pnp.js

# Testing
/coverage

# Production
/build
/dist

# Misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
        
        elif language == "python":
            return """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
dist/
build/
*.egg-info/

# Virtual environments
venv/
env/
.env/
.venv/

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/

# Environments
.env
.env.local
"""
        
        elif language == "java":
            return """# Compiled class file
*.class

# Log file
*.log

# Package Files
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# Maven
target/

# Gradle
.gradle
build/

# IDE
.idea/
.eclipse/
"""
        
        # Default fallback for any language
        return """# OS files
.DS_Store
Thumbs.db
Desktop.ini

# Editor files
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log

# Environment variables
.env
.env.local
"""