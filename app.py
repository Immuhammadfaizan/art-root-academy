from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory, abort
from werkzeug.utils import secure_filename
from sqlalchemy import text, create_engine
import os
import uuid

DATABASE_URL = os.environ['DATABASE_URL']

# Database configuration
DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_HOSTNAME = os.environ['DB_HOSTNAME']
DB_NAME = os.environ['DB_NAME']

engine_url = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'
engine = create_engine(engine_url)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size 16MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Ensure that the uploads folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Course Details Pages
@app.route('/graphic_design')
def graphic_design():
    return render_template('graphic_design.html')

@app.route('/drawing')
def drawing():
    return render_template('drawing.html')

@app.route('/calligraphy')
def calligraphy():
    return render_template('calligraphy.html')

@app.route('/oracle')
def oracle():
    return render_template('oracle.html')

@app.route('/advance_oracle')
def advance_oracle():
    return render_template('advance_oracle.html')

# About Us Page
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# Contact Us Page
@app.route('/contact')
def contact():
    return render_template('contactus.html')

# Registration Form
@app.route('/registration', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        dob = request.form.get('dob')
        email = request.form.get('email')
        phone = request.form.get('phone')
        contact_method = request.form.get('contact_method')
        course_category = request.form.get('course_category')
        courses = request.form.getlist('courses')
        referral = request.form.get('referral')
        prior_experience = request.form.get('prior_experience')
        experience_details = request.form.get('experience_details') if prior_experience == 'YES' else None
        payment_method = request.form.get('payment_method')
        agree = request.form.get('agree')

        # Ensure courses is not empty, set it to None if no course is selected
        courses_str = ','.join(courses) if courses else None

        # Check if mandatory fields are filled
        if not all([full_name, email, phone, agree]):
            flash("All fields are required!", 'error')
            return redirect(url_for('register'))

        try:
            with engine.connect() as conn:
                trans = conn.begin()

                query = text("""
                    INSERT INTO registrations 
                    (full_name, dob, email, phone, contact_method, course_category, course, referral, 
                     experience, experience_details, payment_method, agree) 
                    VALUES (
                        :full_name, :dob, :email, :phone, :contact_method, :course_category, :courses, 
                        :referral, :experience, :experience_details, :payment_method, :agree
                    )
                """)

                conn.execute(query, {
                    "full_name": full_name,
                    "dob": dob,
                    "email": email,
                    "phone": phone,
                    "contact_method": contact_method,
                    "course_category": course_category,
                    "courses": courses_str,
                    "referral": referral,
                    "experience": prior_experience,
                    "experience_details": experience_details,
                    "payment_method": payment_method,
                    "agree": agree
                })

                trans.commit()
                flash("Registration successful!", "success")
                return redirect(url_for('home'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('register'))

    return render_template('form.html')

# View Application
@app.route('/view_application', methods=['POST', 'GET'])
def view_application():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')

        try:
            with engine.connect() as conn:
                query = text("""
                    SELECT * FROM registrations 
                    WHERE full_name = :full_name AND email = :email
                """)

                result = conn.execute(query, {"full_name": full_name, "email": email}).fetchone()

                if result:
                    application = {
                        "full_name": result.full_name,
                        "dob": result.dob,
                        "email": result.email,
                        "phone": result.phone,
                        "contact_method": result.contact_method,
                        "course_category": result.course_category,
                        "course": result.course,
                        "referral": result.referral,
                        "experience": result.experience,
                        "experience_details": result.experience_details,
                        "payment_method": result.payment_method,
                        "agree": result.agree,
                        "created_at": result.created_at,
                    }
                    return render_template('view_application.html', application=application)
                else:
                    flash("No application found with the provided details.", "error")
                    return redirect(url_for('view_application'))

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('view_application'))

    return render_template('view_application.html')

# Payment Section
@app.route('/payment')
def payment():
    return render_template('payment.html')  # Display payment form

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    payment_method = request.form['payment_method']
    receipt_path = None  # Initialize receipt path

    # Handle Bank Transfer Receipt
    if payment_method == 'bank_transfer':
        bank_receipt = request.files.get('bank_receipt')
        if bank_receipt and allowed_file(bank_receipt.filename):
            # Save the image in the UPLOAD_FOLDER with a unique filename
            receipt_filename = secure_filename(bank_receipt.filename)
            bank_receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], receipt_filename))
            receipt_path = receipt_filename  # Store only the filename

    # Handle JazzCash Receipt
    elif payment_method == 'jazzcash':
        jazzcash_receipt = request.files.get('jazzcash_receipt')
        if jazzcash_receipt and allowed_file(jazzcash_receipt.filename):
            # Save the image in the UPLOAD_FOLDER with a unique filename
            receipt_filename = secure_filename(jazzcash_receipt.filename)
            jazzcash_receipt.save(os.path.join(app.config['UPLOAD_FOLDER'], receipt_filename))
            receipt_path = receipt_filename  # Store only the filename

    # Redirect to payment gateway if Credit Card selected
    elif payment_method == 'credit_card':
        return redirect("https://stripe.com")

    # Insert payment details into the database
    try:
        with engine.connect() as conn:
            trans = conn.begin()
            query = text("""
                INSERT INTO payments (name, email, payment_method, receipt_path)
                VALUES (:name, :email, :payment_method, :receipt_path)
            """)
            conn.execute(query, {
                "name": name,
                "email": email,
                "payment_method": payment_method,
                "receipt_path": receipt_path  # Store only the filename here
            })
            trans.commit()
            flash("Payment details submitted successfully! Now move back to the REGISTRATIONS page to submit your complete application.", "success")
            return redirect(url_for('payment'))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        return redirect(url_for('payment'))

@app.route('/admin', methods=['GET'])
def admin():
    try:
        with engine.connect() as conn:
            # Fetch registrations
            registration_query = text("""
                SELECT full_name, dob, email, phone, contact_method, course_category, course, referral, 
                       experience, experience_details, payment_method, agree, created_at 
                FROM registrations
            """)
            registrations = conn.execute(registration_query).fetchall()
            
            # Fetch payments
            payment_query = text("""
                SELECT name, email, payment_method, receipt_path, created_at 
                FROM payments
            """)
            payments = conn.execute(payment_query).fetchall()
            
        # Pass the results to the template for rendering
        return render_template('view_admin.html', registrations=registrations, payments=payments)
    
    except Exception as e:
        flash(f"An error occurred while fetching admin data: {str(e)}", 'error')
        return redirect(url_for('home'))

@app.route('/view_image/<path:filename>')
def view_image(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
    