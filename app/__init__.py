from datetime import date

from flask import Flask, request, session
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes.auth_routes import auth_bp
    from app.routes.members_routes import members_bp
    from app.routes.payments_routes import payments_bp
    from app.routes.checkin_routes import checkin_bp
    from app.routes.schedules_routes import schedules_bp
    from app.routes.packages_routes import packages_bp
    from app.routes.payment_reports_routes import payment_reports_bp
    from app.routes.pts_routes import pts_bp
    from app.routes.equipment_routes import equipment_bp
    from app.routes.reports_routes import reports_bp
    from app.routes.registrations_routes import registrations_bp
    from app.routes.accounts_routes import accounts_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(checkin_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(packages_bp)
    app.register_blueprint(payment_reports_bp)
    app.register_blueprint(pts_bp)
    app.register_blueprint(equipment_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(registrations_bp)
    app.register_blueprint(accounts_bp)

    from app.services.service_status_service import sync_registration_service_statuses
    from app.utils.permissions import permission_guard

    @app.before_request
    def before_request_handler():
        permission_result = permission_guard()

        if permission_result:
            return permission_result

        if request.endpoint == "static":
            return

        if request.endpoint and request.endpoint.startswith("auth."):
            return

        if not session.get("user_id"):
            return

        today = date.today().isoformat()

        if session.get("service_status_refreshed_on") != today:
            sync_registration_service_statuses()
            session["service_status_refreshed_on"] = today

    return app