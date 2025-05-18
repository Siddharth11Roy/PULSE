from flask import Flask

def create_app():
    app = Flask(_name_)

    # Import blueprint
    from .route.home import home_bp

    # Register blueprint
    app.register_blueprint(home_bp)

    return app
