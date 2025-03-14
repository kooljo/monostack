import subprocess
import logging
import os
from typing import Optional, List, Dict, Union

class CommandRunner:
    """
    A utility class to safely run external commands with proper error handling.
    Replaces os.system with subprocess for better security and control.
    """
    def __init__(self):
        """Initialize the CommandRunner with a logger."""
        self.logger = logging.getLogger(__name__)
    
    def run(self, command: str, cwd: Optional[str] = None, env: Optional[Dict[str, str]] = None,
            timeout: Optional[int] = None, check: bool = True, 
            show_output: bool = True) -> subprocess.CompletedProcess:
        """
        Run a shell command with subprocess and handle errors appropriately.
        
        Args:
            command: The command string to execute
            cwd: Current working directory to run the command in
            env: Environment variables for the command
            timeout: Timeout in seconds for the command
            check: Whether to raise an exception if the command fails
            show_output: Whether to show output in real-time (for long-running commands)
            
        Returns:
            CompletedProcess instance with return code and output
            
        Raises:
            subprocess.CalledProcessError: If the command fails and check=True
            subprocess.TimeoutExpired: If the command times out
        """
        try:
            self.logger.info(f"Running command: {command}")
            print(f"\n⚙️  Executing: {command}")
            
            if show_output:
                # Run with real-time output
                process = subprocess.Popen(
                    command,
                    shell=True,
                    cwd=cwd,
                    env=env,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=1,
                    universal_newlines=True
                )
                
                stdout = []
                stderr = []
                
                # Print output in real-time
                print("\n--- Command Output ---")
                for line in process.stdout:
                    print(f">> {line}", end='')  # Add prefix for better visibility
                    stdout.append(line)
                
                # Get the return code
                process.wait()
                
                # Collect any stderr after process completion
                if process.stderr:
                    print("\n--- Error Output ---")
                    for line in process.stderr:
                        print(f"!! {line}", end='')  # Add prefix for errors
                        stderr.append(line)
                
                # Create a CompletedProcess-like object
                class CustomCompletedProcess:
                    def __init__(self, returncode, stdout, stderr):
                        self.returncode = returncode
                        self.stdout = ''.join(stdout)
                        self.stderr = ''.join(stderr)
                
                result = CustomCompletedProcess(process.returncode, ''.join(stdout), ''.join(stderr))
                
                if check and result.returncode != 0:
                    raise subprocess.CalledProcessError(result.returncode, command, 
                                                       result.stdout, result.stderr)
            else:
                # Use standard run for simple commands
                result = subprocess.run(
                    command, 
                    shell=True, 
                    check=check, 
                    cwd=cwd, 
                    env=env, 
                    timeout=timeout,
                    text=True,
                    capture_output=True
                )
            
            # Log results
            if result.returncode == 0:
                print(f"\n✅ Command completed successfully")
                self.logger.debug(f"Command completed successfully: {command}")
                if result.stdout and not show_output:
                    self.logger.debug(f"Command output: {result.stdout}")
            else:
                print(f"\n❌ Command failed with exit code {result.returncode}")
                self.logger.warning(f"Command returned non-zero exit code {result.returncode}: {command}")
                if result.stderr and not show_output:
                    print(f"Error: {result.stderr}")
                    self.logger.warning(f"Command error output: {result.stderr}")
            
            return result
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Command failed with exit code {e.returncode}: {command}")
            if e.stderr:
                self.logger.error(f"Error output: {e.stderr}")
            raise
        
        except subprocess.TimeoutExpired as e:
            self.logger.error(f"Command timed out after {timeout} seconds: {command}")
            raise
        
        except Exception as e:
            self.logger.error(f"Unexpected error running command '{command}': {str(e)}")
            raise
    
    def create_virtual_env(self, project_path: str, venv_name: str = "venv") -> bool:
        """
        Create a virtual environment in the specified project directory.
        
        Args:
            project_path: The project directory path
            venv_name: Name of the virtual environment directory
            
        Returns:
            True if successful, False otherwise
        """
        try:
            venv_path = os.path.join(project_path, venv_name)
            self.logger.info(f"Creating virtual environment at {venv_path}")
            
            result = self.run(f"python -m virtualenv {venv_path}", cwd=project_path)
            return result.returncode == 0
        
        except Exception as e:
            self.logger.error(f"Failed to create virtual environment: {str(e)}")
            return False
    
    def run_in_virtualenv(self, command: str, project_path: str, venv_name: str = "venv") -> subprocess.CompletedProcess:
        """
        Run a command within a virtual environment.
        
        Args:
            command: The command to run
            project_path: The project directory path
            venv_name: Name of the virtual environment directory
            
        Returns:
            CompletedProcess instance with return code and output
        """
        venv_path = os.path.join(project_path, venv_name)
        activate_cmd = f"source {venv_path}/bin/activate && {command}"
        
        return self.run(activate_cmd, cwd=project_path)