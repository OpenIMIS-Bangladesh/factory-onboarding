from flask import Flask, render_template, session, request, redirect, flash, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSON
from datetime import datetime
from dotenv import load_dotenv
import uuid
import requests
import os


load_dotenv()

url_alias = os.getenv('URL_ALIAS')
if url_alias is not None and url_alias != '':
    app = Flask(__name__, static_url_path=f"/{url_alias}/static")
else:
    app = Flask(__name__)
    
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['file_upload_api'] = os.getenv('FILE_UPLOAD_API')
db = SQLAlchemy(app)

@app.context_processor
def inject_globals():
    return {
        'app_name': os.getenv('APP_NAME'),
        'developer': os.getenv('DEVELOPER'),
        'main_page': os.getenv('MAIN_PAGE'),
        'url_alias': url_alias
    }

# -------------------------------
# Model (represents tblLocations)
# -------------------------------
class Location(db.Model):
    __tablename__ = 'tblLocations'
    LocationCode = db.Column(db.String(50), nullable=False)
    LocationId = db.Column(db.Integer, primary_key=True)
    LocationName = db.Column(db.String(150), nullable=False)
    LocationType = db.Column(db.String(50))
    LocationUUID = db.Column(db.String(100))
    ParentLocationId = db.Column(db.Integer)
    ValidityFrom = db.Column(db.DateTime)
    ValidityTo = db.Column(db.DateTime, default=None)
    wCodeId = db.Column(db.Integer)
    def __repr__(self):
        return f"<Locations {self.LocationName}>"


# -------------------------------
# Model (represents workforce_employer_factories)
# -------------------------------
class Factories(db.Model):
    __tablename__ = 'workforce_employer_factories'

    UUID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    isDeleted = db.Column(db.Boolean, default=False)
    Json_ext = db.Column(JSON)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    DateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    employer_id = db.Column(db.Integer)
    employer_id_lima = db.Column(db.String(100))
    name_bn = db.Column(db.String(255))
    name_en = db.Column(db.String(255))
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(150))
    website = db.Column(db.String(255))
    status = db.Column(db.String(50))
    location_id = db.Column(db.Integer)
    UserCreatedUUID = db.Column(db.String(36))
    UserUpdatedUUID = db.Column(db.String(36))
    workforce_employer_id = db.Column(db.Integer)
    workforce_representative_id = db.Column(db.String(50))
    is_same_company_representative = db.Column(db.Integer, default=0)
    association_type = db.Column(db.String(100))

    def __repr__(self):
        return f"<Factories {self.name_bn}>"



# -------------------------------
# Model (Users)
# -------------------------------
class Users(db.Model):
    __tablename__ = 'tblUsers'

    AuditUserID = db.Column(db.Integer)
    DummyPwd = db.Column(db.String(255))
    EmailId = db.Column(db.String(255))
    HFID = db.Column(db.Integer)
    IsAssociated = db.Column(db.Boolean, default=False)
    LanguageID = db.Column(db.Integer)
    LastName = db.Column(db.String(255))
    LegacyID = db.Column(db.Integer)
    LoginName = db.Column(db.String(255))
    OtherNames = db.Column(db.String(255))
    PasswordValidity = db.Column(db.DateTime)
    Phone = db.Column(db.String(50))
    PrivateKey = db.Column(db.Text)
    StoredPassword = db.Column(db.String(255))
    RoleID = db.Column(db.Integer)
    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Use string-based UUID
    UserUUID = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False)

    ValidityFrom = db.Column(db.DateTime)
    ValidityTo = None
    password = db.Column(db.String(255))
    LastLogin = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Users {self.LoginName}>"
    


class CoreUsers(db.Model):
    __tablename__ = 'core_User'

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), unique=True, nullable=False, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    i_user_id = db.Column(db.Integer)
    t_user_id = db.Column(db.Integer)
    claim_admin_id = db.Column(db.Integer)
    officer_id = db.Column(db.Integer)
    LegacyID = db.Column(db.Integer)
    ValidityFrom = db.Column(db.DateTime, default=datetime.utcnow)
    ValidityTo = db.Column(db.DateTime, default=None)

    def __repr__(self):
        return f"<CoreUsers {self.username}>"
    
class UserRoles(db.Model):
    __tablename__ = 'tblUserRole'
    ValidityFrom = db.Column(db.DateTime, default=datetime.utcnow)
    ValidityTo = db.Column(db.DateTime, default=None)
    LegacyID = db.Column(db.Integer)
    UserRoleID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AudituserID = db.Column(db.Integer)
    RoleID = db.Column(db.Integer)
    UserID = db.Column(db.Integer)
    Assign = db.Column(db.Integer, default=None)

    def __repr__(self):
        return f"<UserRoles UserID={self.UserID}, RoleID={self.RoleID}>"

class UserDistrict(db.Model):
    __tablename__ = 'tblUsersDistricts'

    UserDistrictID = db.Column(db.Integer, primary_key=True)
    LegacyID = db.Column(db.Integer)
    ValidityFrom = db.Column(db.DateTime, default=datetime.utcnow)
    ValidityTo = db.Column(db.DateTime, default=None)
    AuditUserID = db.Column(db.Integer, nullable=False)
    LocationId = db.Column(db.Integer, nullable=False)
    UserID = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<UserDistrict {self.UserDistrictID} - UserID {self.UserID} - Location {self.LocationId}>"
    


# -------------------------------
# Model (represents workforce_employee)
# -------------------------------
class Employees(db.Model):
    __tablename__ = 'workforce_employee'

    # Primary key UUID
    UUID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    isDeleted = db.Column(db.Boolean, default=False)
    Json_ext = db.Column(db.JSON)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    DateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)
    global_id = db.Column(db.String(255))
    father_name_bn = db.Column(db.String(255))
    father_name_en = db.Column(db.String(255))
    gender = db.Column(db.String(50))
    marital_status = db.Column(db.String(50))
    photo_path = db.Column(db.String(255))
    photo_date = db.Column(db.DateTime)
    position = db.Column(db.String(255))
    monthly_earning = db.Column(db.Float)
    reference_salary = db.Column(db.Float)
    present_address = db.Column(db.Text)
    permanent_address = db.Column(db.Text)
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    nid = db.Column(db.String(100))
    birth_certificate_no = db.Column(db.String(100))
    passport_no = db.Column(db.String(100))
    status = db.Column(db.String(50))
    permanent_location_id = db.Column(db.Integer)
    present_location_id = db.Column(db.Integer)
    related_user_id = db.Column(db.Integer)
    
    # UUIDs for created/updated users
    UserCreatedUUID = db.Column(db.String(36))
    UserUpdatedUUID = db.Column(db.String(36))
    
    employee_id = db.Column(db.String(255))
    employee_id_lima = db.Column(db.String(255))
    employee_type = db.Column(db.String(100))
    citizenship = db.Column(db.String(100))
    first_name_bn = db.Column(db.String(255))
    first_name_en = db.Column(db.String(255))
    last_name_bn = db.Column(db.String(255))
    last_name_en = db.Column(db.String(255))
    mother_name_bn = db.Column(db.String(255))
    mother_name_en = db.Column(db.String(255))
    other_name = db.Column(db.String(255))
    privacy_law = db.Column(db.String(255))
    registration_date = db.Column(db.DateTime, onupdate=datetime.utcnow)
    spouse_name_bn = db.Column(db.String(255))
    spouse_name_en = db.Column(db.String(255))
    death_date = db.Column(db.Date)
    insurance_number = db.Column(db.String(255))
    life_status = db.Column(db.String(100))
    disability_status = db.Column(db.String(100))
    workforce_factory_id = db.Column(db.String(50))

    def __repr__(self):
        return f"<Employees {self.first_name_en} {self.last_name_en}>"

# -------------------------------
# Model (represents workforce_documents)
# -------------------------------

class Documents(db.Model):
    __tablename__ = 'workforce_documents'

    # Primary key UUID
    UUID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    isDeleted = db.Column(db.Boolean, default=False)
    Json_ext = db.Column(db.JSON)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    DateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)

    holder = db.Column(db.String(255))
    holder_type = db.Column(db.String(100))
    document_type = db.Column(db.String(255))
    path = db.Column(db.String(500))
    submission_date = db.Column(db.Date)
    verification_date = db.Column(db.Date)
    approval_date = db.Column(db.Date)
    remarks = db.Column(db.Text)
    status = db.Column(db.String(100))
    approver_id = db.Column(db.Integer)
    
    # UUIDs for created/updated users
    UserCreatedUUID = db.Column(db.String(100))
    UserUpdatedUUID = db.Column(db.String(100))
    
    verifier_id = db.Column(db.Integer)
    workforce_application_id = db.Column(db.String(255))
    url = db.Column(db.String(500))
    factory_id = db.Column(db.Integer)
    workforce_document_type_id = db.Column(db.Integer)
    workforce_dependent_id = db.Column(db.Integer)
    note = db.Column(db.Text)
    application_summary_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<Documents {self.document_type or 'Unknown Document'}>"


# -------------------------------
# Model (represents workforce_representative)
# -------------------------------
class Representatives(db.Model):
    __tablename__ = 'workforce_representative'

    # Primary key UUID
    UUID = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    isDeleted = db.Column(db.Boolean, default=False)
    Json_ext = db.Column(db.JSON)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    DateUpdated = db.Column(db.DateTime, onupdate=datetime.utcnow)
    version = db.Column(db.Integer, default=1)

    type = db.Column(db.String(100))
    name_bn = db.Column(db.String(255))
    name_en = db.Column(db.String(255))
    address = db.Column(db.Text)
    phone_number = db.Column(db.String(50))
    email = db.Column(db.String(255))
    nid = db.Column(db.String(100))
    passport_no = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    position = db.Column(db.String(255))
    status = db.Column(db.String(100))
    location_id = db.Column(db.Integer)
    related_user_id = db.Column(db.Integer)

    # UUIDs for created/updated users
    UserCreatedUUID = db.Column(db.String(36))
    UserUpdatedUUID = db.Column(db.String(36))

    def __repr__(self):
        return f"<Representatives {self.name_en or self.name_bn}>"    


# -------------------------------
# Routes
# -------------------------------
@app.route('/')
def index():
    locations = Location.query.filter_by(ParentLocationId=None, LocationType='R').all()
    form_data= session.pop('form_data', None)
    error= session.pop('error', None)
    message= session.pop('message', None)
    return render_template('index.html', locations=locations, form_data=form_data, message=message, error= error)


@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/api/get_locations', methods=['GET'])
def get_locations():
    parent_id = request.args.get('parent_id')
    locations = Location.query.filter_by(ParentLocationId=parent_id).all()
    results = []
    for loc in locations:
        results.append({
            "id": loc.LocationId,
            "name": loc.LocationName
        })
    
    return jsonify(results)

UPLOAD_API_URL = app.config['file_upload_api']


@app.route('/submit_form', methods=['POST'])
def submit_form():
    # --------------------------
    # 1. Get form fields
    # --------------------------
    association = request.form.get('association') if request.form.get('association')!="" else None
    factory_name_en = request.form.get('factory_name_en') if request.form.get('factory_name_en')!="" else None
    factory_name_bn = request.form.get('factory_name_bn') if request.form.get('factory_name_bn')!="" else None
    factory_phone = request.form.get('factory_phone') if request.form.get('factory_phone')!="" else None
    factory_email = request.form.get('factory_email') if request.form.get('factory_email')!="" else None
    factory_web = request.form.get('factory_web') if request.form.get('factory_web')!="" else None
    factory_address = request.form.get('factory_address') if request.form.get('factory_address')!="" else None
    factory_location = request.form.get('factory_ward') if request.form.get('factory_ward')!="" else None

    # Representative Information
    representative_name = request.form.get('representative_name') if request.form.get('representative_name')!="" else None
    representative_name_bn = request.form.get('representative_name_bn') if request.form.get('representative_name_bn')!="" else None
    representative_designation = request.form.get('representative_designation') if request.form.get('representative_designation')!="" else None
    representative_email = request.form.get('representative_email') if request.form.get('representative_email')!="" else None
    representative_passport = request.form.get('representative_passport') if request.form.get('representative_passport')!="" else None
    representative_phone = request.form.get('representative_phone') if request.form.get('representative_phone')!="" else None
    representative_nid = request.form.get('representative_nid') if request.form.get('representative_nid')!="" else None
    representative_dob = request.form.get('representative_dob') if request.form.get('representative_dob')!="" else None
    representative_address = request.form.get('representative_address') if request.form.get('representative_address')!="" else None
    representative_location = request.form.get('representative_ward') if request.form.get('representative_ward')!="" else None
    representative_district= request.form.get('representative_district') if request.form.get('representative_district')!="" else None

    # --------------------------
    # 2. Get file
    # --------------------------
    if 'file_upload' not in request.files:
        return "No file provided", 400
    file = request.files['file_upload']

    # --------------------------
    # 3. Send file to external upload API
    # --------------------------
    files = {'file': (file.filename, file.stream, file.content_type)}
    data = {'name': file.filename} 

    try:
        user = Users(
            AuditUserID=-1,
            LoginName=representative_phone,  # assuming login is name
            OtherNames=representative_name_bn,
            RoleID=25,  # example: set role ID for representative
            EmailId=representative_email,
            Phone=representative_phone,
            PrivateKey='C1C224B03CD9BC7B6A86D77F5DACE40191766C485CD55DC48CAF9AC873335D6F',  # store passport as temp password
            StoredPassword='59E66831C680C19E8736751D5480A7C3291BD8775DF47C19C4D0361FBC1C3438',
            password='x001699E55A06FA79F4CA0D06EF15096C02000000DF691E2CE66AA7ABDF65B3E6210C1C04CAAE1A3B1FEE5E266B5FAF4F7D4E95109C92E3205F0145CC',
            UserUUID=str(uuid.uuid4()),
            ValidityFrom=datetime.utcnow(),
            LastLogin=datetime.utcnow(),
            LanguageID='en',
            LastName=representative_name
        )


        db.session.add(user)
        userIdQ= Users.query.filter_by(LoginName=user.LoginName).first()
        user.UserID= userIdQ.UserID
        

        core_user = CoreUsers(
            id=str(uuid.uuid4()),
            username= user.LoginName,
            i_user_id= user.UserID,
        )

        db.session.add(core_user)


        user_district=  UserDistrict(
            UserID= user.UserID,
            LocationId= representative_district,
            AuditUserID= -1,
        )

        db.session.add(user_district)


        user_role= UserRoles(
            RoleID= 25,
            AudituserID= 1,
            UserID= user.UserID,
            # Assign= True
        )

        db.session.add(user_role)
        userRoleQ= UserRoles.query.filter_by(UserID=user.UserID).first()


        birth_date_str = request.form.get('representative_dob')
        birth_date_str= '10-10-1996'
        birth_date_obj = datetime.strptime(birth_date_str, "%d-%m-%Y")
        birth_date_formatted = birth_date_obj.strftime("%Y-%m-%d")


        representative= Representatives(
            UUID= str(uuid.uuid4()),
            type = 'admin',
            name_bn = representative_name_bn,
            name_en = representative_name,
            address = representative_address,
            phone_number = representative_phone,
            email = representative_email,
            nid = representative_nid,
            passport_no = representative_passport,
            birth_date = birth_date_formatted,
            position = representative_designation,
            location_id = representative_location,
            related_user_id = user.UserID,

            # UUIDs for created/updated users
            UserCreatedUUID = core_user.id,
            UserUpdatedUUID = core_user.id
        )

        db.session.add(representative)


        factory= Factories(
            UUID= str(uuid.uuid4()),
            name_bn = factory_name_bn,
            name_en = factory_name_en,
            address = factory_address,
            phone_number = factory_phone,
            email = factory_email,
            website = factory_web,
            status = 'draft',
            location_id = factory_location,
            UserCreatedUUID = core_user.id,
            UserUpdatedUUID = core_user.id,
            workforce_employer_id = None,
            workforce_representative_id = representative.UUID,
            association_type = association,
        )

        db.session.add(factory)



        

        employee = Employees(
            UUID= str(uuid.uuid4()),
            position = representative_designation,
            present_address = representative_address,
            permanent_address = representative_address,
            phone_number = representative_phone,
            email = representative_email,
            birth_date = birth_date_formatted,
            nid = representative_nid,
            passport_no = representative_passport,
            permanent_location_id = representative_location,
            present_location_id = representative_location,
            related_user_id = user.UserID,
            UserCreatedUUID = core_user.id,
            UserUpdatedUUID = core_user.id,
            citizenship = 'Bangladeshi',
            first_name_bn = representative_name_bn,
            first_name_en = representative_name,
            workforce_factory_id = factory.UUID
        )

        db.session.add(employee)
        

        api_response = requests.post(UPLOAD_API_URL, files=files, data=data)
        api_response.raise_for_status()
        response_data = api_response.json()

        uploaded_file = response_data
        

        document = Documents(
            UUID= str(uuid.uuid4()),
            holder=factory_name_en,
            holder_type="factory",
            document_type="factory_membership_certificate",
            path=uploaded_file.get("file_path"),
            url=uploaded_file.get("file_url"),
            submission_date=datetime.utcnow(),
            status="Submitted",
            Json_ext={
                "association": association,
                "factory_name_bn": factory_name_bn,
                "factory_phone": factory_phone,
                "factory_email": factory_email,
                "factory_web": factory_web,
                "factory_address": factory_address,
                "factory_location": factory_location,
                "representative_name": representative_name,
                "representative_name_bn": representative_name_bn,
                "representative_designation": representative_designation,
                "representative_email": representative_email,
                "representative_passport": representative_passport,
                "representative_phone": representative_phone,
                "representative_nid": representative_nid,
                "representative_dob": representative_dob,
                "representative_address": representative_address,
                "representative_location": representative_location,
            },
            UserCreatedUUID = core_user.id,
            UserUpdatedUUID = core_user.id
        )
        db.session.add(document)
        db.session.commit()

        return render_template('success.html')
    
    except requests.RequestException as e:
        return f"Error uploading file: {str(e)}", 500
    except Exception as db_error:
        return f"Error uploading file: {str(db_error)}", 500
        db.session.rollback()
        session['form_data'] = request.form.to_dict()
        session['error'] = True
        session['message'] = 'টাইপকৃত ই-মেইল অথবা ফোন নাম্বার অথবা পাসপোর্ট নাম্বার ইতিমধ্যে বিদ্যমান। দয়া করে আবার চেষ্টা করুন।'
        return redirect(url_for('index'))


# -------------------------------
# Run the app
# -------------------------------
if __name__ == '__main__':
    app.run(debug=True)
