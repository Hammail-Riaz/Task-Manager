from flask import Flask, request, redirect, url_for, flash
from app.blueprints.main.routes import main
from app.blueprints.auth.routes import auth
from app.blueprints.auth.models import User
from app.blueprints.profile.routes import prof
from app.blueprints.tasks.routes import tasks
from .extensions import db, login_manager, migrate

def create_app(config_class="app.config.ProdConfig"):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    migrate.init_app(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(uid):
        return User.query.get(int(uid))
    
    app.register_blueprint(main, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(prof, url_prefix="/profile")
    app.register_blueprint(tasks, url_prefix="/task")
    

    # Map endpoint → custom unauthorized message
    UNAUTHORIZED_MESSAGES = {
        "profile.dashboard": ("🚫 Unauthorized user! Please log in first.", "danger"),
        "auth.logout": ("⚠️ You need to log in before logging out.", "warning")
    }

    @login_manager.unauthorized_handler
    def unauthorized():
        endpoint = request.endpoint  
        # If endpoint has a custom message, use it
        if endpoint in UNAUTHORIZED_MESSAGES:
            message, category = UNAUTHORIZED_MESSAGES[endpoint]
            flash(message, category)
        else:
            # Default fallback
            flash("⚠️ Please log in to access this page.", "warning")

        return redirect(url_for("auth.login"))

    
    return app
    