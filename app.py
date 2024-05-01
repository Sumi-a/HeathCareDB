import mysql.connector
import gradio as gr

# Database connection
def get_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306, 
        user='root',  
        password='ForevaEva2',  
        database='HealthcareDB'
    )

# Function to execute queries
def execute_query(query, params):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = "Recorded successfully!"
    cursor.close()
    conn.close()
    return result

def add_appointment(patient_id, provider_id, datetime, reason, outcome_notes):
    # Check if the provider_id exists in the Providers table
    provider_exists_query = "SELECT COUNT(*) FROM Providers WHERE ProviderID = %s"
    params = (provider_id,)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(provider_exists_query, params)
    provider_exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    if not provider_exists:
        return "Error: Provider ID does not exist."

    # Proceed with adding the appointment if provider_id exists
    query = """
    INSERT INTO Appointments (PatientID, ProviderID, AppointmentDateTime, ReasonForVisit, OutcomeNotes)
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (patient_id, provider_id, datetime, reason, outcome_notes)
    return execute_query(query, params)



# Function to fetch all appointments
def fetch_appointments():
    query = "SELECT * FROM Appointments"
    records = fetch_data(query)
    return records

# Function to fetch data
def fetch_data(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    formatted_result = [dict(zip(columns, row)) for row in records]
    cursor.close()
    conn.close()
    return formatted_result


# Function to add a patient
def add_patient(full_name, dob, gender, phone, email, emergency_contact_name, emergency_contact_phone, medical_history, current_medications):
    query = """
    INSERT INTO Patients (FullName, DateOfBirth, Gender, PhoneNumber, Email, EmergencyContactName, EmergencyContactPhone, MedicalHistory, CurrentMedications)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (full_name, dob, gender, phone, email, emergency_contact_name, emergency_contact_phone, medical_history, current_medications)
    return execute_query(query, params)

# Function to add a provider
def add_provider(full_name, specialty, contact_phone, email, credentials, availability):
    query = """
    INSERT INTO Providers (FullName, Specialty, ContactPhone, Email, Credentials, Availability)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (full_name, specialty, contact_phone, email, credentials, availability)
    return execute_query(query, params)

# Function to add a staff member
def add_staff(role, contact_phone, email, work_schedule):
    query = """
    INSERT INTO Staff (Role, ContactPhone, Email, WorkSchedule)
    VALUES (%s, %s, %s, %s)
    """
    params = (role, contact_phone, email, work_schedule)
    return execute_query(query, params)

# Function to add an access log entry
def add_access_log(user_id, access_time, access_type):
    # Check if the user_id exists in the Staff table
    staff_exists_query = "SELECT COUNT(*) FROM Staff WHERE StaffID = %s"
    params = (user_id,)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(staff_exists_query, params)
    staff_exists = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    if not staff_exists:
        return "Error: Staff member with the provided ID does not exist."

    # Proceed with adding the access log entry if user_id exists
    query = """
    INSERT INTO Access_Log (UserID, AccessTime, AccessType)
    VALUES (%s, %s, %s)
    """
    params = (user_id, access_time, access_type)
    return execute_query(query, params)


# Function to add a compliance check entry
def add_compliance_check(patient_id, check_date, outcome):
    query = """
    INSERT INTO Compliance_Checks (PatientID, CheckDate, Outcome)
    VALUES (%s, %s, %s)
    """
    params = (patient_id, check_date, outcome)
    return execute_query(query, params)

# Function to fetch data
def fetch_data(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    formatted_result = [dict(zip(columns, row)) for row in records]
    cursor.close()
    conn.close()
    return formatted_result

# Setup Gradio app interface
def setup_gradio_interface():
    with gr.Blocks() as app:
        gr.Markdown("# Healthcare Management System")

        with gr.Tab("Appointments"):
            gr.Markdown("## Manage Appointments")
            with gr.Column():
                patient_id = gr.Number(label="Patient ID")
                provider_id = gr.Number(label="Provider ID")
                datetime = gr.Textbox(label="Appointment Date and Time (YYYY-MM-DD HH:MM:SS)")
                reason = gr.Textbox(label="Reason for Visit")
                outcome_notes = gr.Textbox(label="Outcome Notes")
                add_appointment_btn = gr.Button("Add Appointment")
                view_appointments_btn = gr.Button("View Appointments")
                output_text = gr.Textbox(label="Result")
                output_data = gr.Dataframe(label="Appointments")
                add_appointment_btn.click(
                    add_appointment,
                    inputs=[patient_id, provider_id, datetime, reason, outcome_notes],
                    outputs=output_text
                )
                view_appointments_btn.click(
                    fetch_appointments,
                    inputs=[],
                    outputs=output_data
                )

        with gr.Tab("Patients"):
            gr.Markdown("## Manage Patients")
            with gr.Column():
                full_name = gr.Textbox(label="Full Name")
                dob = gr.Textbox(label="Date of Birth (YYYY-MM-DD)")
                gender = gr.Radio(choices=["Male", "Female", "Other"], label="Gender")
                phone = gr.Textbox(label="Phone Number")
                email = gr.Textbox(label="Email")
                emergency_contact_name = gr.Textbox(label="Emergency Contact Name")
                emergency_contact_phone = gr.Textbox(label="Emergency Contact Phone")
                medical_history = gr.Textbox(label="Medical History", lines=3)
                current_medications = gr.Textbox(label="Current Medications", lines=3)
                add_patient_btn = gr.Button("Add Patient")
                output_text_patients = gr.Textbox(label="Result")
                add_patient_btn.click(
                    add_patient,
                    inputs=[full_name, dob, gender, phone, email, emergency_contact_name, emergency_contact_phone, medical_history, current_medications],
                    outputs=output_text_patients
                )

        with gr.Tab("Providers"):
            gr.Markdown("## Manage Providers")
            with gr.Column():
                full_name = gr.Textbox(label="Full Name")
                specialty = gr.Textbox(label="Specialty")
                contact_phone = gr.Textbox(label="Contact Phone")
                email = gr.Textbox(label="Email")
                credentials = gr.Textbox(label="Credentials")
                availability = gr.Textbox(label="Availability")
                add_provider_btn = gr.Button("Add Provider")
                output_text_providers = gr.Textbox(label="Result")
                add_provider_btn.click(
                    add_provider,
                    inputs=[full_name, specialty, contact_phone, email, credentials, availability],
                    outputs=output_text_providers
                )

        with gr.Tab("Staff"):
            gr.Markdown("## Manage Staff")
            with gr.Column():
                role = gr.Textbox(label="Role")
                contact_phone = gr.Textbox(label="Contact Phone")
                email = gr.Textbox(label="Email")
                work_schedule = gr.Textbox(label="Work Schedule")
                add_staff_btn = gr.Button("Add Staff Member")
                output_text_staff = gr.Textbox(label="Result")
                add_staff_btn.click(
                    add_staff,
                    inputs=[role, contact_phone, email, work_schedule],
                    outputs=output_text_staff
                )

        with gr.Tab("Access Log"):
            gr.Markdown("## Access Log")
            with gr.Column():
                user_id = gr.Number(label="User ID")
                access_time = gr.Textbox(label="Access Time (YYYY-MM-DD HH:MM:SS)")
                access_type = gr.Radio(choices=["Read", "Write"], label="Access Type")
                add_access_log_btn = gr.Button("Add Access Log Entry")
                output_text_access_log = gr.Textbox(label="Result")
                add_access_log_btn.click(
                    add_access_log,
                    inputs=[user_id, access_time, access_type],
                    outputs=output_text_access_log
                )

        with gr.Tab("Compliance Checks"):
            gr.Markdown("## Compliance Checks")
            with gr.Column():
                patient_id = gr.Number(label="Patient ID")
                check_date = gr.Textbox(label="Check Date (YYYY-MM-DD)")
                outcome = gr.Textbox(label="Outcome")
                add_compliance_check_btn = gr.Button("Add Compliance Check Entry")
                output_text_compliance_check = gr.Textbox(label="Result")
                add_compliance_check_btn.click(
                    add_compliance_check,
                    inputs=[patient_id, check_date, outcome],
                    outputs=output_text_compliance_check
                )

    return app
if __name__ == "__main__":
    app = setup_gradio_interface()
    app.launch(share=True)


