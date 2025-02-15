import os
from flask import Flask
from app.users.routes import blueprint as users_blueprint
from app.dashboard.routes import blueprint as dashboard_blueprint
from app.database.routes import blueprint as database_blueprint
from app.extensions import db, migrate, login_manager, bcrypt, cache
import app.exceptions as app_exception
from app.database.models import Project, Employee


def register_blueprint(app):
    app.register_blueprint(blueprint=users_blueprint)
    app.register_blueprint(blueprint=dashboard_blueprint)
    app.register_blueprint(blueprint=database_blueprint)


def register_error_handlers(app):
	app.register_error_handler(401, app_exception.unauthorized)
	app.register_error_handler(404, app_exception.page_not_found)
	app.register_error_handler(500, app_exception.server_error)


app = Flask(
    import_name=__name__,
    static_folder='assets',
    template_folder='templates'
)

register_blueprint(app)
register_error_handlers(app)
app.config.from_object('config.DevConfig')

db.init_app(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

from app.users.models import User
from app.database.models import Employee, Employer, ProjectStatus, Project
migrate.init_app(app=app, db=db)
login_manager.init_app(app=app)
bcrypt.init_app(app=app)
cache.init_app(app=app)

login_manager.login_view = 'users.login'
login_manager.login_message = 'لطفا ابتدا وارد حساب کاربری خود بشوید!'
login_manager.login_message_category = 'info'


# ---------------------------------------------------------------------------
# Template Filter
# ---------------------------------------------------------------------------

@app.template_filter('show_persian_date')
def show_persian_date(value):
    if value is None:
        return ""
    y, m, d = value.split('-')
    return f"{d}-{m}-{y}"


@app.template_filter('find_avatar')
def find_avatar(project_id):
    if project_id is None:
        return "user.png", "user.png"
    project = Project.query.get(project_id)
    if project is None:
        return "user.png", "user.png"
    pm = Employee.query.filter_by(full_name=project.project_manager).first()
    mc = Employee.query.filter_by(full_name=project.main_colleague).first()
    if pm is None and mc is None:
        return "user.png", "user.png"
    elif pm is None:
        return "user.png", mc.avatar
    elif mc is None:
        return pm.avatar, "user.png"
    else:
        return pm.avatar, mc.avatar
    

@app.template_filter('calc_received_employer')
def calc_received_employer(received_employer):    
    total_contract_requested = sum(re.requested_amount for re in received_employer)
    total_insurance = sum((re.requested_amount * re.insurance_percentage / 100) for re in received_employer)
    total_guarantee_performance = sum((re.requested_amount * re.guarantee_performance_percentage / 100) for re in received_employer)
    
    total_contract_received = sum(re.received_amount for re in received_employer)
    
    total_university_overhead = sum((re.received_amount * re.university_overhead_percentage / 100) for re in received_employer)
    total_weri_overhead = sum((re.received_amount * re.weri_overhead_percentage / 100) for re in received_employer)
    total_tax = sum((re.received_amount * re.tax_percentage / 100) for re in received_employer)
    
    total_manager_received = total_contract_received - total_university_overhead - total_weri_overhead - total_tax
    
    return total_contract_requested, total_insurance, total_guarantee_performance, total_contract_received, total_university_overhead, total_weri_overhead, total_tax, total_manager_received

@app.template_filter('calc_payment_employees')
def calc_payment_employees(payment_employees):
    total_payment_amount = sum(pe.payment_amount for pe in payment_employees)
    return total_payment_amount


@app.template_filter('sort_by')
def sort_by_attribute(items, attribute):
    return sorted(items, key=lambda x: getattr(x, attribute).lower())