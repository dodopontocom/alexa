import subprocess
from datetime import datetime
from pathlib import Path

class GitService:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def sync(self, message: str):
        """Add, Commit and Push changes"""
        branch_name = "chore/skill-update"
        
        # Ensure branch exists and is checked out
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=str(self.base_dir))
        
        # Add all changes
        subprocess.run(["git", "add", "."], cwd=str(self.base_dir))
        
        # Commit
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subprocess.run(["git", "commit", "-m", f"{message} ({timestamp})"], cwd=str(self.base_dir))
        
        # Push
        subprocess.run(["git", "push", "origin", branch_name], cwd=str(self.base_dir))
        return branch_name
