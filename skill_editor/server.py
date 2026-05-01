from flask import Flask, request, jsonify, send_from_directory
import os
import json
import subprocess
from pathlib import Path

app = Flask(__name__, static_folder='static')

# Configurações
BASE_DIR = Path(__file__).parent.parent.absolute()
SKILLS = {
    "Bora": BASE_DIR / "Bora",
    "Finances": BASE_DIR / "Finances"
}

def get_skill_paths(skill_name):
    skill_dir = SKILLS.get(skill_name)
    if not skill_dir:
        return None
    return {
        "model": skill_dir / "skill-package" / "interactionModels" / "custom" / "pt-BR.json",
        "lambda": skill_dir / "lambda"
    }

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/skills', methods=['GET'])
def list_skills():
    return jsonify(list(SKILLS.keys()))

@app.route('/api/skill/<skill_name>/model', methods=['GET'])
def get_model(skill_name):
    paths = get_skill_paths(skill_name)
    if not paths or not paths["model"].exists():
        return jsonify({"error": "Skill or model not found"}), 404
    
    with open(paths["model"], 'r', encoding='utf-8') as f:
        return jsonify(json.load(f))

@app.route('/api/skill/<skill_name>/model', methods=['POST'])
def update_model(skill_name):
    paths = get_skill_paths(skill_name)
    if not paths:
        return jsonify({"error": "Skill not found"}), 404
    
    new_model = request.json
    
    # Salvar arquivo
    with open(paths["model"], 'w', encoding='utf-8') as f:
        json.dump(new_model, f, indent=2, ensure_ascii=False)
    
    # Git operations
    try:
        # Pega a branch atual ou usa uma padrão que o workflow monitore
        # O workflow atual monitora chore/*
        branch_name = "chore/skill-update"
        
        # Check if branch exists
        res = subprocess.run(["git", "rev-parse", "--verify", branch_name], capture_output=True, cwd=str(BASE_DIR))
        if res.returncode != 0:
            subprocess.run(["git", "checkout", "-b", branch_name], cwd=str(BASE_DIR))
        else:
            subprocess.run(["git", "checkout", branch_name], cwd=str(BASE_DIR))

        subprocess.run(["git", "add", str(paths["model"])], cwd=str(BASE_DIR))
        commit_msg = f"Update {skill_name} interaction model via Web Editor"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(BASE_DIR))
        
        # Push para disparar workflow
        subprocess.run(["git", "push", "origin", branch_name], cwd=str(BASE_DIR))
        
        return jsonify({"message": "Model updated and pushed to GitHub!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
