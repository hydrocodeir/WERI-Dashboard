from flask_wtf import FlaskForm
from wtforms import  StringField, IntegerField, FloatField, SelectField, DecimalField, TextAreaField, SelectMultipleField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired, NumberRange, Email
from app.database.models import Employee, Employer, ProjectStatus, Project, ReceivedEmployer, PaymentEmployees


# -----------------------------------------------------------------------------
# Validate Functions                                          
# -----------------------------------------------------------------------------
def validate_phone_start(form, field):
    if not field.data.startswith('09'):
        raise ValidationError('شماره تلفن باید با 09 شروع شود!')


def validate_iranian_national_code(form, field):
    code = field.data
    code_len = len(code)
    
    if code_len > 10 or code_len < 8:
        raise ValidationError('کد ملی میتواند 8 تا 10 رقم باشد!')

    if len(set(code)) == 1:
        raise ValidationError('همه ارقام کدملی نمیتواند یکسان باشد!')

    if len(code) < 10:
        code = code.zfill(10)

    factors = [10, 9, 8, 7, 6, 5, 4, 3, 2]
    checksum = sum(int(code[i]) * factors[i] for i in range(len(code) - 1))
    remainder = checksum % 11
    last_digit = int(code[-1])

    if remainder < 2:
        if remainder != last_digit:
            raise ValidationError('کدملی اشتباه وارد شده است!')  
    else:
        if 11 - remainder != last_digit:
            raise ValidationError('کدملی اشتباه وارد شده است!') 


# -----------------------------------------------------------------------------
# Employee Form                                              
# -----------------------------------------------------------------------------
class EmployeeForm(FlaskForm):
    
    first_name = StringField(
        label='نام', 
        validators=[
            DataRequired(
                message="وارد کردن نام الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "نام را وارد کنید"
        }
    )
    
    last_name = StringField(
        label='نام خانوادگی',
        validators=[
            DataRequired(
                message="وارد کردن نام خانوادگی الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "نام خانوادگی را وارد کنید"
        }
    )
    
    national_id = StringField(
        label='کدملی',
        validators=[
            DataRequired(
                message="وارد کردن کدملی الزامیست!"
            ),
            validate_iranian_national_code
        ],
        render_kw={
            "placeholder": "کدملی را وارد کنید"
        }
    )
    
    phone_number = StringField(
        label='تلفن همراه',
        validators=[
            DataRequired(
                message="وارد کردن تلفن همراه الزامیست!"
            ),
            Length(
                min=11,
                max=11,
                message='تلفن همراه میتواند 11 کاراکتر باشد!'
            ),
            validate_phone_start
        ],
        render_kw={
            "placeholder": "تلفن همراه را وارد کنید"
        }
    )
    
    email = StringField(
        label='ایمیل',
        validators=[
            DataRequired(
                message="وارد کردن ایمیل الزامیست!"
            ),
            Email(
                message='ایمیل معتبر نیست!'
            ),
        ],
        render_kw={
            "placeholder": "ایمیل را وارد کنید"
        }
    )
        
    university = StringField(
        label='دانشگاه',
        validators=[
            DataRequired(
                message="وارد کردن نام دانشگاه الزامیست!"
            ),
        ],
        render_kw={
            "placeholder": "نام دانشگاه را وارد کنید"
        }
    )
    
    avatar = FileField(
        label='عکس پروفایل',
        validators=[
            FileAllowed(['jpg', 'png'])
        ],
    )


# -----------------------------------------------------------------------------
# Project Form                                              
# -----------------------------------------------------------------------------        
class ProjectForm(FlaskForm):
    
    name = StringField(
        label='عنوان پروژه',
        validators=[
            DataRequired(
                message="وارد کردن عنوان پروژه الزامیست!"
            ),
            Length(
                max=300,
                message='حداکثر 300 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "عنوان پروژه را وارد کنید"
        }
    )
    
    
    employer = SelectField(
        label='کارفرمای پروژه',
        validators=[
            DataRequired(
                message="انتخاب کارفرمای پروژه الزامیست!"
            ),
            Length(
                max=150,
                message='حداکثر 150 کاراکتر!'
            )
        ],
        default='',
        render_kw={
            "data-placeholder": "کارفرمای پروژه را انتخاب کنید"
        }
    )
    
    
    employer_supervisor = StringField(
        label='ناظر پروژه',
        validators=[
            DataRequired(
                message="وارد کردن نام ناظر پروژه الزامیست!"
            ),
            Length(
                max=150,
                message='حداکثر 150 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "نام ناظر پروژه را وارد کنید"
        }
    )
    
    project_manager = SelectField(
        label='مدیر پروژه',
        validators=[
            DataRequired(
                message="انتخاب مدیر پروژه الزامیست!"
            ),
            Length(
                max=150,
                message='حداکثر 150 کاراکتر!'
            )
        ],
        default='',
        render_kw={
            "data-placeholder": "مدیر پروژه را انتخاب کنید"
        }
    )
    
    main_colleague = SelectField(
        label='همکار اصلی پروژه',
        validators=[
            DataRequired(
                message="انتخاب همکار اصلی پروژه الزامیست!"
            ),
        ],
        default='',
        render_kw={
            "data-placeholder": "همکار اصلی پروژه را انتخاب کنید"
        }
    )
       
    contract_number_employer = StringField(
        label='شماره قرارداد کارفرما',
        validators=[
            DataRequired(
                message="وارد کردن شماره قرارداد کارفرما الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "شماره قرارداد کارفرما را وارد کنید"
        }
    )
       
    contract_number_university = StringField(
        label='شماره قرارداد دانشگاه',
        validators=[
            DataRequired(
                message="وارد کردن شماره قرارداد دانشگاه الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "شماره قرارداد دانشگاه را وارد کنید"
        }
    )
       
    contract_date = StringField(
        label='تاریخ ابلاغ قرارداد',
        validators=[
            DataRequired(
                message="وارد کردن تاریخ ابلاغ قرارداد الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "تاریخ ابلاغ قرارداد را انتخاب کنید",
            'data-jdp': 'true'
        }
    )
    
    contract_period = SelectField(
        label='طول مدت قرارداد (ماه)',
        validators=[
            DataRequired(
                message="وارد کردن طول مدت قرارداد الزامیست!"
            ),
        ],
        choices=list(range(1, 37)),
        default=12,
        render_kw={
            "placeholder": "طول مدت قرارداد را انتخاب کنید (ماه)"
        }
    )
    
    contract_state = SelectField(
        label='وضعیت قرارداد',
        validators=[
            DataRequired(
                message="انتخاب وضعیت قرارداد الزامیست!"
            ),
        ],
        default='',
        render_kw={
            "data-placeholder": "وضعیت قرارداد را انتخاب کنید"
        }
    )
    
    contract_price = StringField(
        label='مبلغ کل قرارداد (ریال)',
        validators=[
            DataRequired(
                message="وارد کردن مبلغ کل قرارداد الزامیست!"
            ),
        ],
        render_kw={
            "placeholder": "مبلغ کل قرارداد را وارد کنید (ریال)",
        }
    )
    
    contract_insurance_percentage = FloatField(
        label='درصد بیمه قرارداد',
        validators=[
            InputRequired(
                message="وارد کردن درصد بیمه قرارداد الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد بیمه قرارداد را وارد کنید"
        }
    )
    
    contract_guarantee_performance_percentage = FloatField(
        label='درصد حسن انجام کار قرارداد',
        validators=[
            InputRequired(
                message="وارد کردن درصد حسن انجام کار قرارداد الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد حسن انجام کار قرارداد را وارد کنید"
        }
    )
    
    contract_tax_percentage = FloatField(
        label='درصد مالیات قرارداد',
        validators=[
            InputRequired(
                message="وارد کردن درصد مالیات قرارداد الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد مالیات قرارداد را وارد کنید"
        }
    )
    
    contract_university_overhead_percentage = FloatField(
        label='درصد بالاسری دانشگاه',
        validators=[
            InputRequired(
                message="وارد کردن درصد بالاسری دانشگاه الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد بالاسری دانشگاه را وارد کنید"
        }
    )
    
    contract_weri_overhead_percentage = FloatField(
        label='درصد بالاسری پژوهشکده',
        validators=[
            InputRequired(
                message="وارد کردن درصد بالاسری پژوهشکده الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد بالاسری پژوهشکده را وارد کنید"
        }
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.employer.choices = [('', 'انتخاب کارفرما...')] + [(p.name, p.name) for p in Employer.query.all()]
        self.project_manager.choices = [('', 'انتخاب مجری...')] + [(p.full_name, p.full_name) for p in Employee.query.all()]
        self.main_colleague.choices = [('', 'انتخاب همکار اصلی...')] + [(p.full_name, p.full_name) for p in Employee.query.all()]
        self.contract_state.choices = [('', 'انتخاب وضعیت پروژه...')] + [(p.name, p.name) for p in ProjectStatus.query.all()]


# -----------------------------------------------------------------------------
# Received from Employer Form                                              
# ----------------------------------------------------------------------------- 
class ReceivedEmployerForm(FlaskForm):
    
    re_project_id = SelectField(
        label='شناسه پروژه',
        validators=[
            DataRequired(
                message="انتخاب پروژه الزامیست!"
            ),
        ],
        default='',
        render_kw={
            "data-placeholder": "پروژه را انتخاب کنید"
        }
    )
    
    name = StringField(
        label='نام مرحله درخواستی از کارفرما',
        validators=[
            DataRequired(
                message="وارد کردن «نام مرحله درخواستی از کارفرما» الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "نام مرحله درخواستی از کارفرما را وارد کنید"
        }
    )
    
    requested_date = StringField(
        label='تاریخ درخواست از کارفرما',
        validators=[
            DataRequired(
                message="وارد کردن «تاریخ درخواست از کارفرما» الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "تاریخ درخواست از کارفرما را انتخاب کنید",
            'data-jdp': 'true'
        }
    )
    
    requested_amount = StringField(
        label='مبلغ درخواستی از کارفرما',
        validators=[
            DataRequired(
                message="وارد کردن «مبلغ درخواستی از کارفرما» الزامیست!"
            ),
        ],
        render_kw={
            "placeholder": "مبلغ درخواستی از کارفرما را وارد کنید (ریال)",
        }
    )
    
    requested_letter_number = StringField(
        label='شماره نامه درخواست از کارفرما',
        validators=[
            DataRequired(
                message="وارد کردن «شماره نامه درخواست از کارفرما» الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "شماره نامه درخواست از کارفرما را وارد کنید"
        }
    )
    
    requested_description = TextAreaField(
        label='توضیحات اضافی درخواستی از کارفرما',
        render_kw={
            "placeholder": "توضیحات اضافی را در صورت نیاز در این قسمت وارد کنید"
        }
    )
    
    received_date = StringField(
        label='تاریخ واریز به دانشگاه',
        validators=[
            DataRequired(
                message="وارد کردن «تاریخ واریز به دانشگاه» الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "تاریخ واریز به دانشگاه را انتخاب کنید",
            'data-jdp': 'true'
        }
    )
    
    received_amount = StringField(
        label='مبلغ واریز به دانشگاه',
        validators=[
            DataRequired(
                message="وارد کردن «مبلغ واریز به دانشگاه» الزامیست!"
            ),
        ],
        render_kw={
            "placeholder": "مبلغ واریز به دانشگاه را وارد کنید (ریال)",
        }
    )
    
    received_letter_number = StringField(
        label='شماره فیش پرداختی به دانشگاه',
        validators=[
            DataRequired(
                message="وارد کردن «شماره فیش پرداختی به دانشگاه» الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "شماره فیش پرداختی به دانشگاه را وارد کنید"
        }
    )
    
    received_description = TextAreaField(
        label='توضیحات واریز به دانشگاه',
        render_kw={
            "placeholder": "توضیحات اضافی را در صورت نیاز در این قسمت وارد کنید"
        }
    )
    
    insurance_percentage = FloatField(
        label='درصد بیمه',
        validators=[
            InputRequired(
                message="وارد کردن درصد بیمه الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد بیمه را وارد کنید"
        }
    )
    
    guarantee_performance_percentage = FloatField(
        label='درصد حسن انجام کار',
        validators=[
            InputRequired(
                message="وارد کردن درصد حسن انجام کار الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد حسن انجام کار را وارد کنید"
        }
    )
    
    university_overhead_percentage = FloatField(
        label='درصد بالاسری دانشگاه',
        validators=[
            InputRequired(
                message="وارد کردن درصد بالاسری دانشگاه الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد بالاسری دانشگاه را وارد کنید"
        }
    )
    
    weri_overhead_percentage = FloatField(
        label='درصد بالاسری پژوهشکده',
        validators=[
            InputRequired(
                message="وارد کردن درصد بالاسری پژوهشکده الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد بالاسری پژوهشکده را وارد کنید"
        }
    )
    
    tax_percentage = FloatField(
        label='درصد مالیات',
        validators=[
            InputRequired(
                message="وارد کردن درصد مالیات الزامیست!"
            ),
            NumberRange(min=0, max=100, message="درصد باید بین 0 و 100 باشد.")
        ],
        render_kw={
            "placeholder": "درصد مالیات را وارد کنید"
        }
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.re_project_id.choices = [('', 'انتخاب پروژه...')] + [(p.id, p.name) for p in Project.query.all()]


# -----------------------------------------------------------------------------
# Received from Employer Form                                              
# ----------------------------------------------------------------------------- 
class PaymentEmployeesForm(FlaskForm):
    
    pe_employee_id = SelectField(
        label='انتخاب پژوهشگر',
        choices=[],
        # coerce=int,
        validate_choice=False,
        validators=[
            DataRequired(
                message="انتخاب پژوهشگر الزامیست!"
            ),
        ],
        default='',
        render_kw={
            "data-placeholder": "پژوهشگر را انتخاب کنید"
        }
    )
    
    pe_project_id = SelectField(
        label='انتخاب پروژه',
        choices=[],
        # coerce=int,
        validate_choice=False,
        validators=[
            DataRequired(
                message="انتخاب پروژه الزامیست!"
            ),
        ],
        default='',
        render_kw={
            "data-placeholder": "یک پروژه را انتخاب کنید",
        }
    )
    
    pe_received_employer_id = SelectField(
        label='انتخاب شناسه واریزی به دانشگاه',
        choices=[],
        # coerce=int,
        validate_choice=False,
        validators=[
            DataRequired(
                message="انتخاب شناسه واریزی به دانشگاه الزامیست!"
            ),
        ],
        default='',
        render_kw={
            "data-placeholder": "شناسه واریزی به دانشگاه را انتخاب کنید",
        }
    )
    
    payment_date = StringField(
        label='تاریخ پرداخت',
        validators=[
            DataRequired(
                message="وارد کردن «تاریخ پرداخت» الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "تاریخ پرداخت را انتخاب کنید",
            'data-jdp': 'true'
        }
    )
    
    payment_amount = StringField(
        label='مبلغ پرداختی',
        validators=[
            DataRequired(
                message="وارد کردن «مبلغ پرداختی» الزامیست!"
            ),
        ],
        render_kw={
            "placeholder": "مبلغ پرداختی را وارد کنید (ریال)",           
        }
    )
    
    payment_description = TextAreaField(
        label='توضیحات پرداخت',
        render_kw={
            "placeholder": "توضیحات اضافی را در صورت نیاز در این قسمت وارد کنید"
        }
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pe_project_id.choices = [('', 'انتخاب پروژه...')] + [(p.id, p.name) for p in Project.query.all()]
        self.pe_employee_id.choices = []
        self.pe_received_employer_id.choices = []
    

# -----------------------------------------------------------------------------
# Employees to Project                                              
# ----------------------------------------------------------------------------- 
class AssignEmployeesToProjectForm(FlaskForm):
    
    project = SelectField(
        label='انتخاب پروژه',
        choices=[],
        validators=[
            DataRequired(
                message="انتخاب یک پروژه الزامیست!"
            )
        ],
        render_kw={
            "data-placeholder": "یک پروژه را انتخاب کنید"
        }
    )

    employees = SelectMultipleField(
        label='انتخاب پژوهشگران',
        choices=[],
        validators=[
            DataRequired(
                message="حداقل انتخاب یک پژوهشگر الزامیست!"
            )
        ],
        render_kw={
            "data-placeholder": "حداقل یک پژوهشگر را انتخاب کنید"
        }
    )

    def __init__(self, *args, **kwargs):
        super(AssignEmployeesToProjectForm, self).__init__(*args, **kwargs)
        self.project.choices = [('', 'انتخاب پروژه...')] + [(p.id, p.name) for p in Project.query.all()]
        self.employees.choices = [('', 'انتخاب پژوهشگر...')] + [(e.id, e.full_name) for e in Employee.query.all()]


# -----------------------------------------------------------------------------
# Timeline Form                                              
# ----------------------------------------------------------------------------- 
class TimelineForm(FlaskForm):
    
    t_project_id = SelectField(
        label='انتخاب پروژه',
        choices=[],
        # coerce=int,
        validate_choice=False,
        validators=[
            DataRequired(
                message="انتخاب پروژه الزامیست!"
            ),
        ],
        default='',
        render_kw={
            "data-placeholder": "یک پروژه را انتخاب کنید",
        }
    )
    
    name = StringField(
        label='نام مرحله',
        validators=[
            DataRequired(
                message="وارد کردن «نام مرحله» الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "نام مرحله را وارد کنید"
        }
    )
    
    date = StringField(
        label='تاریخ مرحله',
        validators=[
            DataRequired(
                message="وارد کردن «تاریخ مرحله الزامیست!"
            ),
            Length(
                max=100,
                message='حداکثر 100 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "تاریخ مرحله را انتخاب کنید",
            'data-jdp': 'true'
        }
    )

    description = StringField(
        label='توضیحات مرحله',
        validators=[
            DataRequired(
                message="وارد کردن توضیحات مرحله» الزامیست!"
            ),
            Length(
                max=200,
                message='حداکثر 200 کاراکتر!'
            )
        ],
        render_kw={
            "placeholder": "توضیحات مرحله را وارد کنید"
        }
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.t_project_id.choices = [('', 'انتخاب پروژه...')] + [(p.id, p.name) for p in Project.query.all()]