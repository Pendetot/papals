#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import getpass
import argparse
from pathlib import Path
import re

def create_github_repo(token, repo_name, description="", private=False):
    """
    Create a new GitHub repository
    
    Args:
        token (str): GitHub personal access token
        repo_name (str): Name for the new repository
        description (str): Repository description
        private (bool): Whether the repository should be private
        
    Returns:
        dict: Repository data if successful, None otherwise
    """
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": private,
        "auto_init": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"✅ Repository '{repo_name}' created successfully!")
        return response.json()
    else:
        print(f"❌ Failed to create repository. Status code: {response.status_code}")
        print(f"Error message: {response.json().get('message', 'Unknown error')}")
        return None

def run_git_command(command, cwd=None):
    """Run a git command and return the result"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def setup_git_credentials_helper(token, directory):
    """Setup temporary git credentials helper for this session"""
    # This will only store the credentials in memory for this session
    success, _ = run_git_command(["git", "config", "--local", "credential.helper", "cache"], directory)
    if not success:
        return False
    
    # Use a process with input piping to provide the credentials
    try:
        credential_process = subprocess.Popen(
            ["git", "credential", "approve"],
            stdin=subprocess.PIPE,
            cwd=directory,
            text=True
        )
        credential_input = "protocol=https\nhost=github.com\nusername=x-access-token\npassword={}\n\n".format(token)
        credential_process.communicate(input=credential_input)
        return True
    except subprocess.SubprocessError:
        return False

def check_for_tokens_in_file(file_path, token):
    """Check if a file contains the token or other sensitive information"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            # Check for the exact token
            if token in content:
                return True
            
            # Check for github token patterns
            token_patterns = [
                r'ghp_[a-zA-Z0-9]{36}',  # GitHub Personal Access Token
                r'github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}',  # GitHub Fine-grained PAT
                r'gho_[a-zA-Z0-9]{36}',  # GitHub OAuth Token
            ]
            
            for pattern in token_patterns:
                if re.search(pattern, content):
                    return True
            
            return False
    except (IOError, UnicodeDecodeError):
        # If we can't read the file, assume it's safe (it's probably binary)
        return False

def setup_and_push_repo(repo_url, directory, branch="main", token=None):
    """
    Initialize git repository and push to GitHub
    
    Args:
        repo_url (str): GitHub repository URL
        directory (str): Local directory to upload
        branch (str): Branch name to push to
        token (str): GitHub personal access token
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Change to the specified directory
    abs_directory = os.path.abspath(directory)
    
    # Check if git is already initialized
    is_git_repo, _ = run_git_command(["git", "rev-parse", "--is-inside-work-tree"], abs_directory)
    
    if not is_git_repo:
        # Initialize git repository
        success, output = run_git_command(["git", "init"], abs_directory)
        if not success:
            print(f"❌ Failed to initialize git repository: {output}")
            return False
        print("✅ Git repository initialized")
    else:
        print("ℹ️ Git repository already initialized")
    
    # Configure remote (without token in the URL)
    success, output = run_git_command(["git", "remote", "add", "origin", repo_url], abs_directory)
    if not success:
        # Check if remote already exists
        _, remote_output = run_git_command(["git", "remote", "-v"], abs_directory)
        if "origin" in remote_output:
            success, _ = run_git_command(["git", "remote", "set-url", "origin", repo_url], abs_directory)
            if not success:
                print(f"❌ Failed to update remote: {output}")
                return False
            print("✅ Remote updated")
        else:
            print(f"❌ Failed to add remote: {output}")
            return False
    else:
        print("✅ Remote added")
    
    # Set user info if not already set
    _, username_output = run_git_command(["git", "config", "user.name"], abs_directory)
    if not username_output.strip():
        run_git_command(["git", "config", "user.name", "GitHub Auto Uploader"], abs_directory)
    
    _, email_output = run_git_command(["git", "config", "user.email"], abs_directory)
    if not email_output.strip():
        run_git_command(["git", "config", "user.email", "auto-uploader@example.com"], abs_directory)
    
    # Setup git credentials helper (safer than putting token in URL)
    if token:
        setup_success = setup_git_credentials_helper(token, abs_directory)
        if not setup_success:
            print("⚠️ Warning: Failed to setup credentials helper. You may be prompted for credentials.")
    
    # Create a .gitignore file if it doesn't exist
    gitignore_path = os.path.join(abs_directory, '.gitignore')
    if not os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, 'w') as f:
                # Add common sensitive files and the script itself to gitignore
                f.write("# Auto-generated .gitignore by GitHub Auto Upload Tool\n")
                f.write("# Ignore this script\n")
                script_name = os.path.basename(sys.argv[0])
                f.write(f"{script_name}\n")
                f.write("# Ignore common sensitive files\n")
                f.write("*.env\n")
                f.write("*.token\n")
                f.write("*secret*\n")
                f.write("*credential*\n")
                f.write("*password*\n")
                f.write("*apikey*\n")
                f.write("*api_key*\n")
            print("✅ Created .gitignore file")
        except Exception as e:
            print(f"⚠️ Warning: Failed to create .gitignore file: {e}")
    
    # Scan files for tokens and exclude them
    token_files = []
    for root, _, files in os.walk(abs_directory):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, abs_directory)
            
            # Skip .git directory
            if '.git' in rel_path.split(os.path.sep):
                continue
                
            # Skip binary files and the script itself
            if os.path.samefile(file_path, os.path.abspath(sys.argv[0])) if os.path.exists(os.path.abspath(sys.argv[0])) else False:
                token_files.append(rel_path)
                continue
                
            # Check for tokens in text files
            if os.path.splitext(file)[1].lower() in ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.yaml', '.yml', '.env', '']:
                if token and check_for_tokens_in_file(file_path, token):
                    token_files.append(rel_path)
    
    # Add all files
    success, output = run_git_command(["git", "add", "."], abs_directory)
    if not success:
        print(f"❌ Failed to add files: {output}")
        return False
    print("✅ Files added to staging area")
    
    # Remove the script and files containing tokens from staging
    script_path = os.path.abspath(sys.argv[0])
    if os.path.isfile(script_path) and script_path.startswith(abs_directory):
        # Get relative path of the script to the repo directory
        rel_script_path = os.path.relpath(script_path, abs_directory)
        print(f"⚠️ Detected script in repository. Excluding it from commit to prevent token exposure.")
        run_git_command(["git", "reset", "HEAD", rel_script_path], abs_directory)
    
    # Exclude files with tokens
    for file_path in token_files:
        print(f"⚠️ Excluding file that may contain sensitive information: {file_path}")
        run_git_command(["git", "reset", "HEAD", file_path], abs_directory)
    
    # Commit - check if there are any changes to commit
    _, status_output = run_git_command(["git", "status", "--porcelain"], abs_directory)
    
    if not status_output.strip():
        print("⚠️ No changes to commit. Checking if there are any previous commits...")
        # Check if there are any commits at all
        success, commit_output = run_git_command(["git", "rev-parse", "HEAD"], abs_directory)
        if not success:
            print("❌ No commits found and no files to commit. Cannot push to GitHub.")
            # Create an empty commit
            print("Creating an empty initial commit...")
            success, output = run_git_command(
                ["git", "commit", "--allow-empty", "-m", "Initial empty commit from auto-upload script"],
                abs_directory
            )
            if not success:
                print(f"❌ Failed to create empty commit: {output}")
                return False
            print("✅ Created empty commit")
        else:
            print("✅ Found existing commits, proceeding with push")
    else:
        # We have changes, proceed with commit
        success, output = run_git_command(
            ["git", "commit", "-m", "Initial commit from auto-upload script"],
            abs_directory
        )
        if not success:
            print(f"❌ Failed to commit: {output}")
            return False
        print("✅ Changes committed")
    
    # Create and switch to the specified branch
    # First check if the branch exists
    _, branches_output = run_git_command(["git", "branch"], abs_directory)
    
    if branch in branches_output:
        # Branch exists, switch to it
        success, output = run_git_command(["git", "checkout", branch], abs_directory)
        if not success:
            print(f"❌ Failed to switch to branch '{branch}': {output}")
            return False
        print(f"✅ Switched to existing branch '{branch}'")
    else:
        # Branch doesn't exist, create it
        success, output = run_git_command(["git", "checkout", "-b", branch], abs_directory)
        if not success:
            print(f"❌ Failed to create branch '{branch}': {output}")
            return False
        print(f"✅ Created and switched to branch '{branch}'")
    
    # Push to GitHub
    success, output = run_git_command(
        ["git", "push", "-u", "origin", branch],
        abs_directory
    )
    if not success:
        print(f"❌ Failed to push to GitHub: {output}")
        return False
    
    print(f"✅ Successfully pushed to GitHub branch '{branch}'")
    return True

def main():
    parser = argparse.ArgumentParser(description="Create a GitHub repository and upload local files")
    parser.add_argument("-n", "--name", help="Repository name")
    parser.add_argument("-d", "--description", default="", help="Repository description")
    parser.add_argument("-p", "--private", action="store_true", help="Make repository private")
    parser.add_argument("-b", "--branch", default="main", help="Branch name (default: main)")
    parser.add_argument("-t", "--token", help="GitHub personal access token")
    parser.add_argument("-dir", "--directory", default=".", help="Directory to upload (default: current directory)")
    parser.add_argument("-i", "--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Set interactive mode to True by default if no specific options are provided
    interactive = True
    if args.name is not None or args.description or args.private or args.branch != "main" or args.token is not None:
        interactive = args.interactive  # Only use the flag if other options were specified

    # Get token - always prompt if not provided
    token = args.token
    if not token:
        print("You need a GitHub Personal Access Token with 'repo' scope permissions.")
        print("Create one at: https://github.com/settings/tokens")
        token = getpass.getpass("Enter your GitHub Personal Access Token: ")
    
    # Get repository name - always prompt if not provided
    repo_name = args.name
    if not repo_name:
        default_name = os.path.basename(os.path.abspath(args.directory))
        repo_name = input(f"Enter repository name (default: {default_name}): ").strip()
        if not repo_name:
            repo_name = default_name
            
    # Get privacy setting if in interactive mode
    is_private = args.private
    if interactive and not args.private:
        is_private_input = input("Make repository private? (y/N): ").strip().lower()
        is_private = is_private_input in ['y', 'yes']
        
    # Get description if in interactive mode
    description = args.description
    if interactive and not args.description:
        description = input("Enter repository description (optional): ").strip()
        
    # Get branch name if in interactive mode
    branch = args.branch
    if interactive and branch == "main":
        branch_input = input(f"Enter branch name (default: {branch}): ").strip()
        if branch_input:
            branch = branch_input
    
    # Create GitHub repository
    repo_data = create_github_repo(token, repo_name, description, is_private)
    if not repo_data:
        sys.exit(1)
    
    # Get repository URL
    repo_url = repo_data.get("clone_url")
    if not repo_url:
        print("❌ Could not get repository URL")
        sys.exit(1)
    
    # Setup and push repository
    success = setup_and_push_repo(repo_url, args.directory, branch, token)
    if success:
        print("\n✨ Success! Your files have been uploaded to GitHub.")
        print(f"📂 Repository URL: {repo_data.get('html_url')}")
    else:
        print("\n❌ Failed to upload files to GitHub.")
        sys.exit(1)

if __name__ == "__main__":
    print("🚀 GitHub Auto Upload Tool 🚀")
    print("----------------------------")
    main()
    print("----------------------------")