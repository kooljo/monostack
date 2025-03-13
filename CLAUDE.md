# Monostack Development Guide

## Build & Test Commands
- Run main script: `python monostack.py`
- Run with project name: `python monostack.py --name myproject`
- Run with Hello World examples: `python monostack.py --generate-hello-world`
- Run with verbose output: `python monostack.py -v` or `python monostack.py --verbose`
- Run with logging: `python monostack.py --log-level DEBUG --log-file monostack.log`
- Run all tests: `python -m unittest test_setup.py`
- Run specific test: `python -m unittest test_setup.TestMonostack.test_load_technologies`

## Code Style Guidelines
- **Imports**: Standard library first, then third-party, then local
- **Spacing**: 4-space indentation, line length ~80 characters
- **Functions**: Use clear, descriptive function names that indicate purpose
- **Classes**: Use CamelCase for class names, methods have descriptive names
- **Variables**: Use snake_case for variable names
- **Error Handling**: Use try/except blocks with specific exception types
- **Type Hints**: Use typing hints for function parameters and return values
- **Logging**: Use the logging module instead of print statements
- **Documentation**: Add docstrings to all classes and functions

## Project Organization
The codebase follows a modular architecture with:
- `monostack/config/`: Configuration management classes
- `monostack/core/`: Core functionality and business logic
- `monostack/utils/`: Utility functions and helper classes
- `monostack/templates/`: Template management and rendering

## Development Practices
- Use subprocess.run instead of os.system for running commands
- Create virtual environments for Python components
- Use explicit error handling with informative error messages
- Employ comprehensive logging for better debugging
- Follow SOLID principles and clean code practices