# dashboard/skill_manager.py
import streamlit as st

# List of skills (this can be expanded as necessary)
skills = [
    "python", "javascript", "java", "c#", "c++", "html", "css", "react",
    "node.js", "django", "flask", "sql", "nosql", "docker", "aws", "azure",
    "kubernetes", "linux", "bash", "machine learning", "data science", "r"
]

def show_skill_manager():
    st.subheader("Manage Skills")

    # Add new skill
    new_skill = st.text_input("Add a new skill:")
    if st.button("Add Skill") and new_skill:
        skills.append(new_skill.lower())
        st.success(f"Added: {new_skill.lower()}")

    # Remove skill
    skill_to_remove = st.selectbox("Remove a skill", skills)
    if st.button("Remove Skill"):
        skills.remove(skill_to_remove)
        st.success(f"Removed: {skill_to_remove}")
    
    # Display current skill list
    st.write("Current Skills List:", skills)
