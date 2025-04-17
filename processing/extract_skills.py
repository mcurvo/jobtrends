# processing/extract_skills.py

import pandas as pd
from scraper.remote_scraper import fetch_remoteok_jobs
from processing.normalize_skills import normalize_skills, skill_mapping

def extract_and_save_skills(output_path="data/with_skills_spacy.csv"):
    """
    Fetch job listings from RemoteOK API, normalize skills via skill_mapping,
    and save the cleaned DataFrame to CSV for the dashboard.
    """
    # 1. Fetch raw job data
    df = fetch_remoteok_jobs()

    # 2. Ensure 'skills' column is a list
    df['skills'] = df['skills'].apply(
        lambda x: eval(x) if isinstance(x, str) else (x if isinstance(x, list) else [])
    )

    # 3. Normalize each list of skills
    df['skills'] = df['skills'].apply(lambda skills: normalize_skills(skills, skill_mapping))

    # 4. Drop any jobs without skills
    df = df[df['skills'].apply(lambda lst: isinstance(lst, list) and len(lst) > 0)]

    # 5. Save to CSV
    df.to_csv(output_path, index=False)
    print(f"Saved processed job data with skills to {output_path}")

if __name__ == "__main__":
    extract_and_save_skills()
