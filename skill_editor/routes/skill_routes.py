from flask import Blueprint, request, jsonify
from pathlib import Path

def create_skill_blueprint(file_service, git_service):
    bp = Blueprint('skills', __name__)

    @bp.route('/api/skills', methods=['GET'])
    def list_skills():
        return jsonify(list(file_service.skills.keys()))

    @bp.route('/api/skill/<skill_name>/model', methods=['GET'])
    def get_model(skill_name):
        paths = file_service.get_paths(skill_name)
        if not paths or not paths["model"].exists():
            return jsonify({"error": "Model not found"}), 404
        return jsonify(file_service.read_json(paths["model"]))

    @bp.route('/api/skill/<skill_name>/model', methods=['POST'])
    def update_model(skill_name):
        try:
            paths = file_service.get_paths(skill_name)
            data = request.json
            file_service.write_json(paths["model"], data)
            git_service.sync(f"Update {skill_name} interaction model")
            return jsonify({"message": "Model updated and pushed!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @bp.route('/api/skill/<skill_name>/handlers', methods=['GET'])
    def list_handlers(skill_name):
        paths = file_service.get_paths(skill_name)
        if not paths:
            return jsonify({"error": "Skill not found"}), 404
        return jsonify(file_service.list_python_files(paths["handlers"]))

    @bp.route('/api/skill/<skill_name>/handler/<filename>', methods=['GET'])
    def get_handler(skill_name, filename):
        paths = file_service.get_paths(skill_name)
        file_path = paths["handlers"] / filename
        if not file_path.exists():
            return jsonify({"error": "File not found"}), 404
        return jsonify({"content": file_service.read_file(file_path)})

    @bp.route('/api/skill/<skill_name>/handler/<filename>', methods=['POST'])
    def update_handler(skill_name, filename):
        try:
            paths = file_service.get_paths(skill_name)
            content = request.json.get("content")
            file_path = paths["handlers"] / filename
            file_service.write_file(file_path, content)
            git_service.sync(f"Update {skill_name} handler: {filename}")
            return jsonify({"message": "Handler updated and pushed!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return bp
