from flask import Flask, send_from_directory
from pathlib import Path
from services.file_service import FileService
from git.git_service import GitService
from routes.skill_routes import create_skill_blueprint

def create_app():
    app = Flask(__name__, static_folder='../static', static_url_path='')
    
    BASE_DIR = Path(__file__).parent.parent.parent.absolute()
    SKILLS_CONFIG = {
        "Bora": BASE_DIR / "Bora",
        "Finances": BASE_DIR / "Finances"
    }

    # Initialize Services
    file_service = FileService(SKILLS_CONFIG)
    git_service = GitService(BASE_DIR)

    # Register Blueprints
    app.register_blueprint(create_skill_blueprint(file_service, git_service))

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    return app
