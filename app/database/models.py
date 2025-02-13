from app.db import BaseModel
from app.extensions import db
from flask_login import UserMixin
from sqlalchemy import event


# -----------------------------------------------------------------------------
# Employee Model                                              
# -----------------------------------------------------------------------------
class Employee(BaseModel, UserMixin):
    
    __tablename__ = "employee"
           
    first_name = db.Column(
        db.String(100), unique=False, nullable=False, info={'verbose_name': 'نام'}
    )
    last_name = db.Column(
        db.String(100), unique=False, nullable=False, info={'verbose_name': 'نام خانوادگی'}
    )
    full_name = db.Column(
        db.String(200), unique=False, nullable=False, info={'verbose_name': 'نام و نام خانوادگی'}
    )
    national_id = db.Column(
        db.String(10), unique=True, nullable=False, info={'verbose_name': 'کد ملی'}
    )
    phone_number = db.Column(
        db.String(11), unique=True, nullable=False, info={'verbose_name': 'شماره تلفن'}
    )
    email = db.Column(
        db.String(100), unique=True, nullable=False, info={'verbose_name': 'ایمیل'}
    )
    university = db.Column(
        db.String(100), unique=False, nullable=False, info={'verbose_name': 'دانشگاه'}
    )
    avatar = db.Column(
        db.String(50), nullable=True, default='user.png'
    )
    payment_employees = db.relationship(
        'PaymentEmployees', backref='employee'
    )
       
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.first_name} {self.last_name}, {self.national_id})'

@event.listens_for(Employee, 'before_insert')
@event.listens_for(Employee, 'before_update')
def set_full_name(mapper, connection, target):
    target.full_name = f"{target.first_name} {target.last_name}"


# -----------------------------------------------------------------------------
# Employer Model                                              
# -----------------------------------------------------------------------------
class Employer(BaseModel, UserMixin):
    
    __tablename__ = "employer"
    
    name = db.Column(
        db.String(100), unique=True, nullable=False
    )
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'


# -----------------------------------------------------------------------------
# Project Status Model                                              
# -----------------------------------------------------------------------------
class ProjectStatus(BaseModel):
    
    __tablename__ = "project_status"
    
    name = db.Column(
        db.String(100), unique=True, nullable=False
    )
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name})'


# -----------------------------------------------------------------------------
# Project Model                                              
# -----------------------------------------------------------------------------
class Project(BaseModel, UserMixin):
    
    __tablename__ = "project"
    
    name = db.Column(
        db.String(300), unique=True, nullable=False, info={'verbose_name': 'عنوان پروژه'}
    )
    employer = db.Column(
        db.String(150), unique=False, nullable=False, info={'verbose_name': 'کارفرمای پروژه'}
    )
    employer_supervisor = db.Column(
        db.String(150), unique=False, nullable=False, info={'verbose_name': 'ناظر پروژه'}
    )
    project_manager = db.Column(
        db.String(150), unique=False, nullable=False, info={'verbose_name': 'مدیر پروژه'}
    )
    main_colleague = db.Column(
        db.String(150), unique=False, nullable=False, info={'verbose_name': 'همکار اصلی پروژه'}
    )
    contract_number_employer = db.Column(
        db.String(100), unique=True, nullable=False, info={'verbose_name': 'شماره قرارداد کارفرما'}
    )
    contract_number_university = db.Column(
        db.String(100), unique=True, nullable=False, info={'verbose_name': 'شماره قرارداد دانشگاه'}
    )
    contract_date = db.Column(
        db.String(100), unique=False, nullable=False, info={'verbose_name': 'تاریخ ابلاغ قرارداد'}
    )
    contract_period = db.Column(
        db.String(100), unique=False, nullable=False, info={'verbose_name': 'طول مدت قرارداد'}
    )
    contract_state = db.Column(
        db.String(100), unique=False, nullable=False, info={'verbose_name': 'وضعیت قرارداد'}
    )
    contract_price = db.Column(
        db.Integer, unique=False, nullable=False, info={'verbose_name': 'مبلغ کل قرارداد'}
    )
    contract_insurance_percentage = db.Column(
        db.Float, unique=False, nullable=False, info={'verbose_name': 'درصد بیمه قرارداد'} 
    )
    contract_guarantee_performance_percentage = db.Column(
        db.Float, unique=False, nullable=False, info={'verbose_name': 'درصد حسن انجام کار قرارداد'}
    )
    contract_tax_percentage = db.Column(
        db.Float, unique=False, nullable=False, info={'verbose_name': 'درصد مالیات قرارداد'}
    )
    contract_university_overhead_percentage = db.Column(
        db.Float, unique=False, nullable=False, info={'verbose_name': 'درصد بالاسری دانشگاه'}
    )
    contract_weri_overhead_percentage = db.Column(
        db.Float, unique=False, nullable=False, info={'verbose_name': 'درصد بالاسری پژوهشکده'}
    )
    received_employer = db.relationship(
        'ReceivedEmployer', backref='project',
    )
    payment_employees = db.relationship(
        'PaymentEmployees', backref='project',
    )
    timeline = db.relationship(
        'Timeline', backref='project',
    )
    employee = db.relationship(
        'Employee', secondary='project_employee', backref='project',
    )

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.name[:30]}, {self.employer}, {self.project_manager})'


# -----------------------------------------------------------------------------
# Join Tables: Project - Employee                                            
# -----------------------------------------------------------------------------

project_employee = db.Table(
  'project_employee',
  db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
  db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'))
)


# -----------------------------------------------------------------------------
# Received from Employer                                            
# -----------------------------------------------------------------------------

class ReceivedEmployer(BaseModel, UserMixin):
    
    __tablename__ = "received_employer"
    
    re_project_id = db.Column(
        db.Integer, db.ForeignKey('project.id'), nullable=False, info={'verbose_name': 'شناسه پروژه'}
    )
    name = db.Column(
        db.String(100), nullable=False, info={'verbose_name': 'نام مرحله درخواستی از کارفرما'} 
    )   
    requested_date = db.Column(
        db.String(100), nullable=False, info={'verbose_name': 'تاریخ درخواستی از کارفرما'}
    )
    requested_amount = db.Column(
        db.Integer, nullable=False, info={'verbose_name': 'مبلغ درخواستی از کارفرما'}
    )
    requested_letter_number = db.Column(
        db.String(100), nullable=False, info={'verbose_name': 'شماره نامه درخواستی از کارفرما'}
    )
    requested_description = db.Column(
        db.Text, nullable=False, info={'verbose_name': 'توضیحات اضافی درخواستی از کارفرما'}
    )
    received_date = db.Column(
        db.String(100), nullable=False, info={'verbose_name': 'تاریخ واریزی به دانشگاه'}
    )
    received_amount = db.Column(
        db.Integer, nullable=False, info={'verbose_name': 'مبلغ واریزی به دانشگاه'}
    )
    received_letter_number = db.Column(
        db.String(100), nullable=False, info={'verbose_name': 'شماره فیش پرداختی به دانشگاه'}
    )
    received_description = db.Column(
        db.String(500), nullable=False, info={'verbose_name': 'توضیحات واریزی به دانشگاه'}
    )
    insurance_percentage = db.Column(
        db.Float, nullable=False, info={'verbose_name': 'درصد بیمه'}
    )
    guarantee_performance_percentage = db.Column(
        db.Float, nullable=False, info={'verbose_name': 'درصد حسن انجام کار'}
    )
    university_overhead_percentage = db.Column(
        db.Float, nullable=False, info={'verbose_name': 'درصد بالاسری دانشگاه'}
    )
    weri_overhead_percentage = db.Column(
        db.Float, nullable=False, info={'verbose_name': 'درصد بالاسری پژوهشکده'}
    )
    tax_percentage = db.Column(
        db.Float, nullable=False, info={'verbose_name': 'درصد مالیات'}
    )
    payment_employees = db.relationship(
        'PaymentEmployees', backref='received_employer'
    )
        
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.re_project_id}, {self.received_date}, {self.received_amount})'


# -----------------------------------------------------------------------------
# Payment to Employees                                          
# -----------------------------------------------------------------------------

class PaymentEmployees(BaseModel, UserMixin):
    
    __tablename__ = "payment_employees"
    
    pe_employee_id = db.Column(
        db.Integer, db.ForeignKey('employee.id'), nullable=False, info={'verbose_name': 'شناسه پژوهشگر'}
    )
    pe_project_id = db.Column(
        db.Integer, db.ForeignKey('project.id'), nullable=False, info={'verbose_name': 'شناسه پروژه'}
    )
    pe_received_employer_id = db.Column(
        db.Integer, db.ForeignKey('received_employer.id'), nullable=False, info={'verbose_name': 'شناسه واریزی به دانشگاه'}
    )    
    payment_date = db.Column(
        db.String(100), nullable=False, info={'verbose_name': 'تاریخ پرداخت'}
    )
    payment_amount = db.Column(
        db.Integer, nullable=False, info={'verbose_name': 'مبلغ پرداختی'}
    )
    payment_description = db.Column(
        db.Text, nullable=False, info={'verbose_name': 'توضیحات پرداخت'}
    )
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.pe_employee_id}, {self.pe_project_id}, {self.payment_amount})'


class Timeline(BaseModel, UserMixin):
    
    __tablename__ = "timeline"
    
    t_project_id = db.Column(
        db.Integer, db.ForeignKey('project.id'), nullable=False, info={'verbose_name': 'شناسه پروژه'}
    )
    name = db.Column(
        db.String(100), nullable=False, unique=True, info={'verbose_name': 'نام مرحله'}
    )
    date = db.Column(
        db.String(100), nullable=False, info={'verbose_name': 'تاریخ مرحله'}
    )
    description = db.Column(
        db.String(200), nullable=False, info={'verbose_name': 'توضیحات مرحله'}
    )
    
    def __repr__(self):
        return f'{self.__class__.__name__} ({self.t_project_id}, {self.name}, {self.date})'