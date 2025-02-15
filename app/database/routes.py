import os
import secrets
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from app.database.forms import EmployeeForm, ProjectForm, ReceivedEmployerForm, PaymentEmployeesForm, AssignEmployeesToProjectForm, TimelineForm
from app.database.models import Employee, Employer, ProjectStatus, Project, ReceivedEmployer, PaymentEmployees, Timeline
from app.extensions import db
from sqlalchemy import or_, asc, desc
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_required
from app.users.routes import role_required
from PIL import Image


blueprint = Blueprint(
    name='database',
    import_name=__name__,
)


def virastarStr(x):
    x = str(x)
    x = x.rstrip()
    x = x.lstrip()
    x = x.replace(' +', ' ')
    return x


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join('app/assets/img/avatars', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def validate_phone_number(phone):    
    if len(phone) != 11:
        return False    
    elif phone == "00000000000":
        return False
    else:
        return True
    

def validate_iranian_national_code(code):
    code_len = len(code)
    if code_len > 10 or code_len < 8:
        return False

    if len(set(code)) == 1:
        return False

    if len(code) < 10:
        code = code.zfill(10)

    factors = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    checksum = sum(int(code[i]) * factors[i] for i in range(len(code) - 1))
    remainder = checksum % 11
    last_digit = int(code[-1])

    if remainder < 2:
        return remainder == last_digit
    else:
        return 11 - remainder == last_digit



@blueprint.route(rule='/database', methods=['GET', 'POST'])
@login_required
@role_required('کاربر عادی')
def home():
    
    # Project Form
    new_project_form = ProjectForm()
    
    # Employee Form
    new_employee_form = EmployeeForm()
    
    # Received from Employer Form
    new_received_employer_form = ReceivedEmployerForm()
    
    # Payment to Employees Form
    new_payment_employees_form = PaymentEmployeesForm()
    
    # Timeline Form
    new_timeline_form = TimelineForm()
    
    # Employees To Project
    new_assign_employees_to_project_form = AssignEmployeesToProjectForm()

    # Check if the form is submitted
    if request.method == 'POST':
        form_id = request.form.get('form_id')
        
        if form_id == 'project' and new_project_form.validate_on_submit():
            project = Project(
                name = virastarStr(new_project_form.name.data),
                employer = new_project_form.employer.data,
                employer_supervisor = virastarStr(new_project_form.employer_supervisor.data),
                project_manager = new_project_form.project_manager.data,
                main_colleague = new_project_form.main_colleague.data,
                contract_number_employer = virastarStr(new_project_form.contract_number_employer.data),
                contract_number_university = virastarStr(new_project_form.contract_number_university.data),
                contract_date = virastarStr(new_project_form.contract_date.data),
                contract_period = int(new_project_form.contract_period.data),
                contract_state = new_project_form.contract_state.data,
                contract_price = int(new_project_form.contract_price.data.replace(',', '')),
                contract_insurance_percentage = float(new_project_form.contract_insurance_percentage.data),
                contract_guarantee_performance_percentage = float(new_project_form.contract_guarantee_performance_percentage.data),
                contract_tax_percentage = float(new_project_form.contract_tax_percentage.data),
                contract_university_overhead_percentage = float(new_project_form.contract_university_overhead_percentage.data),
                contract_weri_overhead_percentage = float(new_project_form.contract_weri_overhead_percentage.data),
            )        
            db.session.add(project)
            db.session.commit()        
            flash(message='پروژه جدید ایجاد گردید.', category='success')
            return redirect(location=url_for(endpoint='database.home'))
        
        elif form_id == 'employee' and new_employee_form.validate_on_submit():
            if new_employee_form.avatar.data:
                avatar = save_picture(new_employee_form.avatar.data)
            else:
                avatar = 'user.png'
            employee = Employee(
                first_name = virastarStr(new_employee_form.first_name.data),
                last_name = virastarStr(new_employee_form.last_name.data),
                national_id = virastarStr(new_employee_form.national_id.data),
                phone_number = virastarStr(new_employee_form.phone_number.data),
                email = virastarStr(new_employee_form.email.data),
                university = virastarStr(new_employee_form.university.data),
                avatar = avatar
            )        
            db.session.add(employee)
            db.session.commit()        
            flash(message='پژوهشگر جدید ایجاد گردید.', category='success')
            return redirect(location=url_for(endpoint='database.home'))
        
        elif form_id == 'received_employer' and new_received_employer_form.validate_on_submit():
            
            requested_amount = int(new_received_employer_form.requested_amount.data.replace(',', ''))
            received_amount = int(new_received_employer_form.received_amount.data.replace(',', ''))
            insurance_percentage = float(new_received_employer_form.insurance_percentage.data)
            guarantee_performance_percentage = float(new_received_employer_form.guarantee_performance_percentage.data)
            
         
            if int(received_amount) != int(requested_amount * (100 - (insurance_percentage + guarantee_performance_percentage)) / 100):
                flash(message='حاصلضرب مقدار درخواستی در درصد بیمه و حسن انجام کار با مقدار دریافتی برابر نیست!', category='danger')
                return redirect(location=url_for(endpoint='database.home'))
            
            received_employer = ReceivedEmployer(
                re_project_id = int(new_received_employer_form.re_project_id.data),
                name = virastarStr(new_received_employer_form.name.data),
                requested_date = virastarStr(new_received_employer_form.requested_date.data),
                requested_amount = int(new_received_employer_form.requested_amount.data.replace(',', '')),
                requested_letter_number = virastarStr(new_received_employer_form.requested_letter_number.data),
                requested_description = virastarStr(new_received_employer_form.requested_description.data),
                received_date = virastarStr(new_received_employer_form.received_date.data),
                received_amount = int(new_received_employer_form.received_amount.data.replace(',', '')),
                received_letter_number = virastarStr(new_received_employer_form.received_letter_number.data),
                received_description = virastarStr(new_received_employer_form.received_description.data),
                insurance_percentage = float(new_received_employer_form.insurance_percentage.data),
                guarantee_performance_percentage = float(new_received_employer_form.guarantee_performance_percentage.data),
                university_overhead_percentage = float(new_received_employer_form.university_overhead_percentage.data),
                weri_overhead_percentage = float(new_received_employer_form.weri_overhead_percentage.data),
                tax_percentage = float(new_received_employer_form.tax_percentage.data),
            )
            db.session.add(received_employer)
            db.session.commit()        
            flash(message='واریزی جدید به دانشگاه ایجاد گردید.', category='success')
            return redirect(location=url_for(endpoint='database.home'))
        
        elif form_id == 'payment_employees' and new_payment_employees_form.validate_on_submit():
            payment_employees = PaymentEmployees(
                pe_employee_id = int(new_payment_employees_form.pe_employee_id.data),
                pe_project_id = int(new_payment_employees_form.pe_project_id.data),
                pe_received_employer_id = int(new_payment_employees_form.pe_received_employer_id.data),
                payment_date = virastarStr(new_payment_employees_form.payment_date.data),
                payment_amount = int(new_payment_employees_form.payment_amount.data.replace(',', '')),
                payment_description = virastarStr(new_payment_employees_form.payment_description.data),
            )
            db.session.add(payment_employees)
            db.session.commit()        
            flash(message='پرداختی جدید به پژوهشگر ایجاد گردید.', category='success')
            return redirect(location=url_for(endpoint='database.home'))
        
        elif form_id == 'timeline' and new_timeline_form.validate_on_submit():
            timeline = Timeline(
                t_project_id = int(new_timeline_form.t_project_id.data),
                name = virastarStr(new_timeline_form.name.data),
                date = virastarStr(new_timeline_form.date.data),
                description = virastarStr(new_timeline_form.description.data),
            )
            db.session.add(timeline)
            db.session.commit()        
            flash(message='تایم‌لاین جدید ایجاد گردید.', category='success')
            return redirect(location=url_for(endpoint='database.home'))
        
        elif form_id == 'employee_to_project' and new_assign_employees_to_project_form.validate_on_submit():
            project_id = int(new_assign_employees_to_project_form.project.data)
            employee_ids = [int(emp_id) for emp_id in new_assign_employees_to_project_form.employees.data]
            
            project = Project.query.get(project_id)
            employees = Employee.query.filter(Employee.id.in_(employee_ids)).all()
            
            if project and employees:
                for employee in employees:
                    if employee not in project.employee:
                        project.employee.append(employee)
                db.session.commit()
                flash(message='پژوهشگران با موفقیت به پروژه اضافه شدند.', category='success')
            else:
                flash(message='خطا در انتخاب پروژه یا پژوهشگران.', category='danger') 
                       
            return redirect(location=url_for(endpoint='database.home'))
    
    return render_template(
        template_name_or_list='database/home.html',
        new_project_form=new_project_form,
        new_employee_form=new_employee_form,
        new_received_employer_form=new_received_employer_form,
        new_payment_employees_form=new_payment_employees_form,
        new_assign_employees_to_project_form=new_assign_employees_to_project_form,
        new_timeline_form=new_timeline_form
    )



# -----------------------------------------------------------------------------
# API
# -----------------------------------------------------------------------------

@blueprint.route('/get_parameter_employee_payment/<int:project_id>')
def get_parameter_employee_payment(project_id):
    project_employee = Project.query.get(project_id).employee
    project_employee_list = [{'id': pe.id, 'name': pe.full_name} for pe in project_employee]
    
    project_received_employer = Project.query.get(project_id).received_employer
    project_received_employer_list = [{'id': pre.id, 'name': pre.name} for pre in project_received_employer]

    return jsonify({
        'project_employee': project_employee_list,
        'project_received_employer': project_received_employer_list
    })

@blueprint.route('/get_statutory_deductions/<int:project_id>')
def get_statutory_deductions(project_id):
    project = Project.query.get(project_id)
    return jsonify([{
        'contract_insurance_percentage': project.contract_insurance_percentage,
        'contract_guarantee_performance_percentage': project.contract_guarantee_performance_percentage,
        'contract_tax_percentage': project.contract_tax_percentage,
        'contract_university_overhead_percentage': project.contract_university_overhead_percentage,
        'contract_weri_overhead_percentage': project.contract_weri_overhead_percentage,
    }])
