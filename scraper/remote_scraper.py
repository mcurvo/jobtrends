# scraper/remoteok_scraper.py
import requests
import pandas as pd

def fetch_remoteok_jobs():
    url = "https://remoteok.io/api"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    jobs = response.json()[1:]  # Skip metadata

    extracted = []
    for job in jobs:
        extracted.append({
            "date": job.get("date"),
            "company": job.get("company"),
            "position": job.get("position"),
            "location": job.get("location"),
            "tags": job.get("tags"),
            "description": job.get("description"),
            "url": job.get("url")
        })

    df = pd.DataFrame(extracted)
    df.to_csv("data/raw_jobs.csv", index=False)
    print(f"Saved {len(df)} jobs to data/raw_jobs.csv")

if __name__ == "__main__":
    fetch_remoteok_jobs()
