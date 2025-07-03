from .db import Resume, SessionLocal

def save_resume_to_db(name, email, phone, linkedin, skills, experience, education):
    db = SessionLocal()
    resume = Resume(
        name=name,
        email=email,
        phone=phone,
        linkedin=linkedin,
        skills=skills,
        experience=experience,
        education=education
    )
    db.add(resume)
    db.commit()
    db.close()


def get_all_resumes():
    db = SessionLocal()
    resumes = db.query(Resume).all()
    db.close()
    return resumes