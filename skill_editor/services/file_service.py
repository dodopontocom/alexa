import json
import os
import ast
from pathlib import Path

class FileService:
    def __init__(self, skills_config: dict):
        self.skills = skills_config

    def get_paths(self, skill_name: str):
        skill_dir = self.skills.get(skill_name)
        if not skill_dir:
            return None
        return {
            "model": skill_dir / "skill-package" / "interactionModels" / "custom" / "pt-BR.json",
            "handlers": skill_dir / "lambda" / "handlers" / "custom",
            "root": skill_dir
        }

    def read_json(self, path: Path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write_json(self, path: Path, data: dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def list_python_files(self, directory: Path):
        if not directory.exists():
            return []
        return [f for f in os.listdir(directory) if f.endswith('.py') and f != '__init__.py']

    def read_file(self, path: Path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    def write_file(self, path: Path, content: str):
        # Python syntax validation
        if path.suffix == '.py':
            ast.parse(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
