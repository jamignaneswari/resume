from backend.operations import save_resume_to_db, get_all_resumes
import streamlit as st
from fpdf import FPDF
from pathlib import Path
import os

# Page config
st.set_page_config(
    page_title="Resume Builder + Job Recommender",
    page_icon="https://www.codester.com/static/uploads/items/000/041/41164/icon.png",
    layout="centered"
)

# Background styling
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://m.media-amazon.com/images/I/91PNBBkROqL.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
.resume-box {
    background-color: rgba(255,255,255,0.95);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    max-width: 800px;
    margin: auto;
}
.job-highlight {
    background-color: #e0f7fa;
    padding: 1.5rem;
    border-left: 10px solid #00bcd4;
    font-size: 1.5rem;
    font-weight: bold;
    color: #004d40;
    border-radius: 10px;
    text-align: center;
    margin-top: 1rem;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Logo & Title
st.markdown("""
<div style="text-align:center;">
    <img src="https://www.codester.com/static/uploads/items/000/041/41164/icon.png" width="100">
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="resume-box">' "<h2 style='text-align: center; color: #000;'>📄 RESUME BUILDER & JOB MATCHER </h2>", unsafe_allow_html=True)
st.title("🧑‍💼 Resume Builder & Job Recommender")
st.markdown("✨ Fill your details below to generate resume & get job suggestions.")

# Resume input form
with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    linkedin = st.text_input("LinkedIn Profile URL")
    skills = st.text_area("Skills (comma separated)")
    experience = st.text_area("Work Experience")
    education = st.text_area("Education")
    submit = st.form_submit_button("📄 Generate Resume & Suggest Jobs")

# Job Matching
job_data = {
    'Python, ML, Data Science, Analytics, NumPy, Pandas, Scikit-learn': '👨‍💻 Data Scientist at AI Corp',
    'HTML, CSS, JavaScript, Frontend Developer, UI Design, Bootstrap': '🌐 Frontend Developer at WebWorks',
    'Java, Spring, Hibernate, Backend Developer, REST API, MySQL': '🖥 Backend Developer at CodeBase',
    'C, C++, C#, Object-Oriented Programming, Algorithms': '🧠 Software Engineer at LogicSoft',
    'React, Node, MongoDB, Express, Full Stack, MERN': '🚀 Full Stack Developer at DevHub',
    'Excel, MS Excel, Pivot Table, Data Entry, Accounting, Tally': '📊 Financial Analyst at FinServe',
    'MS Word, MS Office, PowerPoint, Documentation, Admin': '📁 Administrative Assistant at OfficePro',
    'SQL, MySQL, PostgreSQL, Data Modelling, Database': '🗃️ Database Analyst at DataPlus',
    'Communication, Leadership, Teamwork, Problem Solving': '🤝 HR Associate at PeopleFirst',
    'Cloud, AWS, Azure, Google Cloud, DevOps, Docker, Kubernetes': '☁️ Cloud Engineer at CloudifyTech',
    'Cybersecurity, Network Security, Ethical Hacking, Firewalls': '🛡 Cybersecurity Analyst at SecureNet',
    'AI, Deep Learning, Neural Networks, TensorFlow, PyTorch': '🧠 AI Engineer at BrainWare',
    'Photoshop, Illustrator, Canva, UI/UX, Adobe': '🎨 Graphic Designer at Creatix Studio',
    'Content Writing, Copywriting, Blogging, SEO, Editing': '📝 Content Writer at WordWave',
    'Public Speaking, Presentation, Customer Service, Negotiation': '📣 Sales Executive at MarketMinds'
}

def match_job(skills_text):
    user_skills = [skill.strip().lower() for skill in skills_text.split(',')]
    for key in job_data:
        job_keywords = [k.strip().lower() for k in key.split(',')]
        if any(skill in job_keywords for skill in user_skills):
            return job_data[key]
    return "❗ No exact match found. Try refining your skill keywords."


# PDF Generation
def create_pdf(name, email, phone, linkedin, skills, experience, education):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=name, ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, txt=f"Email: {email} | Phone: {phone}", ln=1, align='C')
    pdf.cell(200, 10, txt=f"LinkedIn: {linkedin}", ln=1, align='C')
    pdf.ln(10)

    def section(title, content):
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, title, ln=1)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, content)
        pdf.ln()

    section("Skills", skills)
    section("Experience", experience)
    section("Education", education)

    file_path = "resume.pdf"
    pdf.output(file_path)
    return file_path

# On form submit
if submit:
    save_resume_to_db(name, email, phone, linkedin, skills, experience, education)

    st.markdown("----")
    st.subheader("🎯 Job Match Based on Your Skills:")
    matched = match_job(skills)
    st.markdown(f"<div class='job-highlight'>{matched}</div>", unsafe_allow_html=True)

    st.subheader("📄 Resume Preview:")
    st.markdown(f"**Name:** {name}")
    st.markdown(f"**Email:** {email}")
    st.markdown(f"**Phone:** {phone}")
    st.markdown(f"**LinkedIn:** {linkedin}")
    st.markdown(f"**Skills:** {skills}")
    st.markdown(f"**Experience:** {experience}")
    st.markdown(f"**Education:** {education}")

   pdf_path = create_pdf(name, email, phone, linkedin, skills, experience, education)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Download Your Resume (PDF)", f, file_name="my_resume.pdf", mime="application/pdf")


# 🛡 ADMIN-ONLY: View All Resumes
with st.expander("🔐 Admin Login to View All Submitted Resumes"):
    admin_user = st.text_input("Admin Username")
    admin_pass = st.text_input("Admin Password", type="password")
    if st.button("Login"):
        if admin_user == "admin" and admin_pass == "yourpassword":  # <-- Change this!
            resumes = get_all_resumes()
            if resumes:
                st.success("✅ Logged in as Admin")
                for r in resumes:
                    st.markdown(f"**👤 Name:** {r.name}")
                    st.markdown(f"**📧 Email:** {r.email}")
                    st.markdown(f"**📞 Phone:** {r.phone}")
                    st.markdown(f"**🔗 LinkedIn:** {r.linkedin}")
                    st.markdown(f"**🛠 Skills:** {r.skills}")
                    st.markdown(f"**💼 Experience:** {r.experience}")
                    st.markdown(f"**🎓 Education:** {r.education}")
                    st.markdown("---")
            else:
                st.warning("No resumes found.")
        else:
            st.error("🚫 Invalid admin credentials")



st.markdown("</div>", unsafe_allow_html=True)

