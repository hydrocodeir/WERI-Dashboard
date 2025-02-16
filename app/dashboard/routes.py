from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.database.models import Employee, Employer, ProjectStatus, Project, ReceivedEmployer, PaymentEmployees, Timeline
from app.database.forms import ProjectForm, ReceivedEmployerForm, PaymentEmployeesForm
from app.extensions import db, cache
from sqlalchemy import distinct
from sqlalchemy import func, case
from sqlalchemy.orm import aliased


blueprint = Blueprint(
    name='dashboard',
    import_name=__name__,
)

def virastarStr(x):
    x = str(x)
    x = x.rstrip()
    x = x.lstrip()
    x = x.replace(' +', ' ')
    return x


@blueprint.route('/')
@login_required
def home():
    projects = Project.query.all()
    return render_template(
        template_name_or_list='dashboard/home.html',
        projects=projects
    )


@blueprint.route('/project/<int:project_id>')
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    
    # c: Contract
    # empr: Employer
    # empe: Employees
    # re: Received Employer
    # pe: Payment Employees
    # perc: Percentage
    # ins: Insurance
    # gp: Guarantee Performance
    # tax: Tax
    # uo: University Overhead
    # wo: WERI Overhead
    # t: Total
    # uni: University
    # s: Sum
    # proj: Project
    
       
    results = {
        "c_empr": project.contract_price,
        "c_empr_ins_perc": project.contract_insurance_percentage,
        "c_empr_ins": project.contract_price * project.contract_insurance_percentage / 100,
        "c_empr_gp_perc": project.contract_guarantee_performance_percentage,
        "c_empr_gp": project.contract_price * project.contract_guarantee_performance_percentage / 100,        
        "c_uni": project.contract_price - (project.contract_price * project.contract_insurance_percentage / 100),
        "c_uni_uo_perc": project.contract_university_overhead_percentage,
        "c_uni_uo": project.contract_university_overhead_percentage / 100 * (project.contract_price - (project.contract_price * project.contract_insurance_percentage / 100)),
        "c_uni_wo_perc": project.contract_weri_overhead_percentage,
        "c_uni_wo": project.contract_weri_overhead_percentage / 100 * (project.contract_price - (project.contract_price * project.contract_insurance_percentage / 100)),
        "c_uni_tax_perc": project.contract_tax_percentage,
        "c_uni_tax": project.contract_tax_percentage / 100 * (project.contract_price - (project.contract_price * project.contract_insurance_percentage / 100)),
    }
    
    results['t'] = results['c_empr']
    results['t_ins'] = results['c_empr_ins']
    results['t_ins_perc'] = results['c_empr_ins_perc']    
    results['t_uo'] = results['c_uni_uo']
    results['t_uo_perc'] = 100 * results['t_uo'] / results['t']
    results['t_wo'] = results['c_uni_wo']
    results['t_wo_perc'] = 100 * results['t_wo'] / results['t']
    results['t_tax'] = results['c_uni_tax']
    results['t_tax_perc'] = 100 * results['t_tax'] / results['t']
    results['t_proj'] = results['t'] - results['t_ins'] - results['t_uo'] - results['t_wo'] - results['t_tax']
    results['t_proj_perc'] = 100 * results['t_proj'] / results['t']
    
    
    return render_template(
        template_name_or_list='dashboard/project.html',
        project=project,
        results=results
    )
    

@blueprint.route('/project/delete/<int:project_id>', methods=['GET'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project:
        db.session.delete(project)
        db.session.commit()
        flash(message='پروژه با موفقیت حذف شد.', category='success')
        return redirect(location=url_for(endpoint='dashboard.home'))
    else:
        flash(message='پروژه پیدا نشد!', category='danger')
        return redirect(location=url_for(endpoint='dashboard.home'))


@blueprint.route('/project/update/<int:project_id>', methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.name = virastarStr(form.name.data)
        project.employer = virastarStr(form.employer.data)
        project.employer_supervisor = virastarStr(form.employer_supervisor.data)
        project.project_manager = virastarStr(form.project_manager.data)
        project.main_colleague = virastarStr(form.main_colleague.data)
        project.contract_number_employer = virastarStr(form.contract_number_employer.data)
        project.contract_number_university = virastarStr(form.contract_number_university.data)
        project.contract_date = virastarStr(form.contract_date.data)
        project.contract_period = int(form.contract_period.data)
        project.contract_state = virastarStr(form.contract_state.data)
        project.contract_price = int(form.contract_price.data.replace(',', ''))
        project.contract_insurance_percentage = float(form.contract_insurance_percentage.data)
        project.contract_guarantee_performance_percentage = float(form.contract_guarantee_performance_percentage.data)
        project.contract_tax_percentage = float(form.contract_tax_percentage.data)
        project.contract_university_overhead_percentage = float(form.contract_university_overhead_percentage.data)
        project.contract_weri_overhead_percentage = float(form.contract_weri_overhead_percentage.data)
        
        db.session.commit()
        
        flash(message='مشخصات پروژه با موفقیت بروزرسانی شد.', category='success')
        return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))
    
    elif request.method == 'GET':    
        form.name.data = project.name
        form.employer.data = project.employer
        form.employer_supervisor.data = project.employer_supervisor
        form.project_manager.data = project.project_manager
        form.main_colleague.data = project.main_colleague
        form.contract_number_employer.data = project.contract_number_employer
        form.contract_number_university.data = project.contract_number_university
        form.contract_date.data = project.contract_date
        form.contract_period.data = project.contract_period
        form.contract_state.data = project.contract_state
        form.contract_price.data = project.contract_price
        form.contract_insurance_percentage.data = project.contract_insurance_percentage
        form.contract_guarantee_performance_percentage.data = project.contract_guarantee_performance_percentage
        form.contract_tax_percentage.data = project.contract_tax_percentage
        form.contract_university_overhead_percentage.data = project.contract_university_overhead_percentage
        form.contract_weri_overhead_percentage.data = project.contract_weri_overhead_percentage
    
    return render_template(
        template_name_or_list='dashboard/update_project.html',
        form=form
    )
    

@blueprint.route('/employee/delete/<int:project_id>/<int:employee_id>', methods=['GET'])
@login_required
def delete_employee(project_id, employee_id):
    project = Project.query.get(project_id)
    employee = Employee.query.get(employee_id)
    if project and employee:
        if project.project_manager == employee.full_name or project.main_colleague == employee.full_name:
            flash(message='پژوهشگر مورد نظر، مدیر یا همکار اصلی پروژه می‌باشد!', category='danger')
            return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))
        elif any(pe.pe_employee_id == employee_id for pe in project.payment_employees):
            flash(message='پژوهشگر مورد نظر، در لیست پرداخت‌ها موجود می‌باشد!', category='danger')
            return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))
        else:
            project.employee.remove(employee)
            db.session.commit()
            flash(message='پژوهشگر با موفقیت از پروژه حذف شد.', category='success')
            return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))
    else:
        flash(message='خطایی رخ داده است!', category='danger')
        return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))


@blueprint.route('/received_employer/delete/<int:project_id>/<int:received_employer_id>', methods=['GET'])
@login_required
def delete_received_employer(project_id, received_employer_id):
    project = Project.query.get_or_404(project_id)
    if project:
        received_employer = next((re for re in project.received_employer if re.id == received_employer_id), None)
        if received_employer:
            if received_employer.payment_employees:
                flash(message='از این صورتحساب پرداختی به پژوهشگران صورت گرفته است.', category='danger')
                return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))
            else:
                db.session.delete(received_employer)
                db.session.commit()
                flash(message='صورتحساب با موفقیت حذف شد..', category='success')
                return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))
        else:
            flash(message='مبلغ دریافتی پیدا نشد!', category='danger')
            return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))
    else:
        flash(message='پروژه پیدا نشد!', category='danger')
        return redirect(location=url_for(endpoint='dashboard.project', project_id=project.id))




        
@blueprint.route('/received_employer/update/<int:received_employer_id>', methods=['GET', 'POST'])
@login_required
def update_received_employer(received_employer_id):
    form_id = request.form.get('form_id')
    received_employer = ReceivedEmployer.query.get_or_404(received_employer_id)
    form = ReceivedEmployerForm()
    
    form.re_project_id.choices = [(p.id, p.name) for p in Project.query.all() if p.id == received_employer.re_project_id]
    
    if form_id == 'update_received_employer' and form.validate_on_submit():
        requested_amount = int(form.requested_amount.data.replace(',', ''))
        received_amount = int(form.received_amount.data.replace(',', ''))
        insurance_percentage = float(form.insurance_percentage.data)
        guarantee_performance_percentage = float(form.guarantee_performance_percentage.data)
        
        if int(received_amount) != isinstance(requested_amount * (100 - (insurance_percentage + guarantee_performance_percentage)) / 100):
            flash(message='حاصلضرب مقدار درخواستی در درصد بیمه و حسن انجام کار با مقدار دریافتی برابر نیست!', category='danger')
            return redirect(location=url_for(endpoint='dashboard.project', project_id=received_employer.re_project_id))
        
        received_employer.re_project_id = int(form.re_project_id.data)
        received_employer.name = virastarStr(form.name.data)
        received_employer.requested_date = virastarStr(form.requested_date.data)
        received_employer.requested_amount = int(form.requested_amount.data.replace(',', ''))
        received_employer.requested_letter_number = virastarStr(form.requested_letter_number.data)
        received_employer.requested_description = virastarStr(form.requested_description.data)
        received_employer.received_date = virastarStr(form.received_date.data)
        received_employer.received_amount =  int(form.received_amount.data.replace(',', ''))
        received_employer.received_letter_number = virastarStr(form.received_letter_number.data)
        received_employer.received_description = virastarStr(form.received_description.data)
        received_employer.insurance_percentage = float(form.insurance_percentage.data)
        received_employer.guarantee_performance_percentage = float(form.guarantee_performance_percentage.data)
        received_employer.university_overhead_percentage = float(form.university_overhead_percentage.data)
        received_employer.weri_overhead_percentage = float(form.weri_overhead_percentage.data)
        received_employer.tax_percentage = float(form.tax_percentage.data)
        
        db.session.commit()
        flash(message='مشخصات صورتحساب با موفقیت بروزرسانی شد.', category='success')
        return redirect(location=url_for(endpoint='dashboard.project', project_id=received_employer.re_project_id))
    
    elif request.method == 'GET':    
        form.re_project_id.data = received_employer.re_project_id
        form.name.data = received_employer.name
        form.requested_date.data = received_employer.requested_date
        form.requested_amount.data = received_employer.requested_amount
        form.requested_letter_number.data = received_employer.requested_letter_number
        form.requested_description.data = received_employer.requested_description
        form.received_date.data = received_employer.received_date
        form.received_amount.data = received_employer.received_amount
        form.received_letter_number.data = received_employer.received_letter_number
        form.received_description.data = received_employer.received_description
        form.insurance_percentage.data = received_employer.insurance_percentage
        form.guarantee_performance_percentage.data = received_employer.guarantee_performance_percentage
        form.university_overhead_percentage.data = received_employer.university_overhead_percentage
        form.weri_overhead_percentage.data = received_employer.weri_overhead_percentage
        form.tax_percentage.data = received_employer.tax_percentage
    
    return render_template(
        template_name_or_list='dashboard/update_received_employer.html',
        form=form
    )


@blueprint.route('/payment_employees/delete/<int:payment_employees_id>', methods=['GET'])
@login_required
def delete_payment_employees(payment_employees_id):
    payment_employees = PaymentEmployees.query.get_or_404(payment_employees_id)
    if payment_employees:
        project_id = payment_employees.pe_project_id
        db.session.delete(payment_employees)
        db.session.commit()
        flash(message='پرداختی با موفقیت حذف شد.', category='success')
        return redirect(location=url_for(endpoint='dashboard.project', project_id=project_id))
    else:
        flash(message='پرداختی پیدا نشد!', category='danger')
        return redirect(location=url_for(endpoint='dashboard.home'))


@blueprint.route('/payment_employees/update/<int:payment_employees_id>', methods=['GET', 'POST'])
@login_required
def update_payment_employees(payment_employees_id):
    form_id = request.form.get('form_id')
    payment_employees = PaymentEmployees.query.get_or_404(payment_employees_id)
    form = PaymentEmployeesForm()
    
    form.pe_project_id.choices = [(p.id, p.name) for p in Project.query.all() if p.id == payment_employees.pe_project_id]
    
    form.pe_employee_id.choices = [(p.id, p.full_name) for p in Project.query.get(payment_employees.pe_project_id).employee]
    
    form.pe_received_employer_id.choices = [(p.id, p.name) for p in Project.query.get(payment_employees.pe_project_id).received_employer]
    
    if form_id == 'update_payment_employees' and form.validate_on_submit():
        payment_employees.pe_employee_id = int(form.pe_employee_id.data)
        payment_employees.pe_project_id = int(form.pe_project_id.data)
        payment_employees.pe_received_employer_id = int(form.pe_received_employer_id.data)
        payment_employees.payment_date = virastarStr(form.payment_date.data)
        payment_employees.payment_amount = int(form.payment_amount.data.replace(',', ''))
        payment_employees.payment_description = virastarStr(form.payment_description.data)

        db.session.commit()
        flash(message='مشخصات پرداختی با موفقیت بروزرسانی شد.', category='success')
        return redirect(location=url_for(endpoint='dashboard.project', project_id=payment_employees.pe_project_id))
    
    elif request.method == 'GET':
        print("Selected Employee ID:", payment_employees.pe_employee_id)
    
        form.pe_employee_id.title = payment_employees.pe_employee_id
        form.pe_project_id.data = payment_employees.pe_project_id
        form.pe_received_employer_id.data = payment_employees.pe_received_employer_id
        form.payment_date.data = payment_employees.payment_date
        form.payment_amount.data = payment_employees.payment_amount
        form.payment_description.data = payment_employees.payment_description
    
    return render_template(
        template_name_or_list='dashboard/update_payment_employees.html',
        form=form
    )



@blueprint.route('/timeline/delete/<int:project_id>', methods=['GET'])
@login_required
def delete_timeline(project_id):
    timeline = Timeline.query.filter_by(t_project_id=project_id).all()
    if timeline:
        for t in timeline:
            db.session.delete(t)
        db.session.commit()
        flash(message='تایم‌لاین با موفقیت حذف شد.', category='success')
        return redirect(location=url_for(endpoint='dashboard.project', project_id=project_id))
    else:
        flash(message='پروژه پیدا نشد!', category='danger')
        return redirect(location=url_for(endpoint='dashboard.home'))