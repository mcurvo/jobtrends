# Expanded skill list with more specific tools, technologies, and libraries
skill_dict = {
    "python": ["python", "py", "python3", "py3"],
    "javascript": ["javascript", "js", "node.js", "node js"],
    "java": ["java", "javac"],
    "c#": ["c#", "csharp"],
    "c++": ["c++", "cpp"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js"],
    "angular": ["angular", "angular.js"],
    "django": ["django", "django-rest-framework"],
    "flask": ["flask"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "sqlite"],
    "nosql": ["mongodb", "cassandra", "firebase", "couchdb"],
    "docker": ["docker"],
    "aws": ["aws", "amazon web services", "aws lambda", "aws s3"],
    "azure": ["azure", "microsoft azure"],
    "kubernetes": ["kubernetes", "k8s"],
    "linux": ["linux", "ubuntu", "debian"],
    "bash": ["bash", "bash scripting"],
    "machine learning": ["machine learning", "ml", "tensorflow", "pytorch", "sklearn"],
    "data science": ["data science", "data analysis", "data wrangling", "numpy", "pandas", "matplotlib"],
    "artificial intelligence": ["artificial intelligence", "ai", "deep learning", "neural networks", "reinforcement learning"],
    "r": ["r", "r programming"]
}


def extract_skills(description):
    found_skills = []
    # Process the job description using spaCy
    doc = nlp(description)

    # Search for matches in the description
    for token in doc:
        for skill, variants in skill_dict.items():
            if token.text.lower() in [variant.lower() for variant in variants]:
                if skill not in found_skills:
                    found_skills.append(skill)

    return found_skills

def extract_and_save_skills():
    # Load raw job data
    df = pd.read_csv("data/raw_jobs.csv")

    # Extract skills from job descriptions
    df['skills'] = df['description'].apply(extract_skills)

    # Save to new CSV file
    df.to_csv("data/with_skills_spacy.csv", index=False)
    print(f"Skills extracted and saved to data/with_skills_spacy.csv")

if __name__ == "__main__":
    extract_and_save_skills()