from flask import Flask, request, jsonify, send_from_directory
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

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

def validate_model(model_data):
    """Lint simples para o modelo da Alexa"""
    try:
        # Verifica estrutura básica
        im = model_data.get("interactionModel", {})
        lm = im.get("languageModel", {})
        if not lm.get("intents") or not lm.get("invocationName"):
            return False, "Modelo inválido: 'intents' ou 'invocationName' ausentes."
        
        # Verifica se invocation name segue regras básicas (ex: sem letras maiúsculas)
        inv_name = lm.get("invocationName")
        if any(c.isupper() for c in inv_name):
            return False, "Erro de Lint: 'invocationName' deve ser minúsculo."
            
        return True, "Validado"
    except Exception as e:
        return False, str(e)

@app.route('/api/skill/<skill_name>/model', methods=['POST'])
def update_model(skill_name):
    try:
        paths = get_skill_paths(skill_name)
        if not paths:
            return jsonify({"error": "Skill not found"}), 404
        
        new_model = request.json
        
        # Lint
        is_valid, message = validate_model(new_model)
        if not is_valid:
            return jsonify({"error": message}), 400

        # Git: Criar branch com timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch_name = f"chore/skill-update-{timestamp}"
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=str(BASE_DIR))

        # Salvar arquivo
        with open(paths["model"], 'w', encoding='utf-8') as f:
            json.dump(new_model, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            "message": f"Branch '{branch_name}' criada e arquivo salvo. Verifique com 'git status'.",
            "branch": branch_name,
            "path": str(paths["model"])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=3000, debug=True)
