# dashboard/app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from processing.extract_skills import extract_and_save_skills
from utils.filters import filter_jobs_by_skills_and_location
from utils.formatters import format_tags, format_skills, format_description
from utils.location import parse_and_normalize
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast

# --- Configuration ---
DATA_PATH = "data/with_skills_spacy.csv"
JOBS_PER_PAGE = 5

# --- Data Loading & Caching ---
@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)

    # existing code for skills and locations parsing here...
    df["skills"] = df["skills"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x if isinstance(x, list) else []
    )
    df["skills"] = df["skills"].apply(format_skills)

    df["locations"] = df["location"].apply(parse_and_normalize)

    # Fix tags column here:
    df["tags"] = df["tags"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x if isinstance(x, list) else []
    )

    return df

@st.cache_data
def filter_data(df: pd.DataFrame, skills: list[str], location: str) -> pd.DataFrame:
    """
    Apply skill and location filters to the DataFrame.
    """
    return filter_jobs_by_skills_and_location(df, skills, location)

# --- Main Application ---

def main():
    st.set_page_config(page_title="JobTrends", layout="wide")
    st.title("JobTrends - Tech Job Market Analyzer")

    # Load data
    df = load_data()

    # Sidebar: Filters
    st.sidebar.header("Filters")
    # Skills filter: ordered by frequency
    skill_counts = df["skills"].explode().value_counts()
    all_skills = skill_counts.index.tolist()
    selected_skills = st.sidebar.multiselect(
        "Skills", options=all_skills, default=all_skills[:5]
    )

    # Location filter
    all_locations = sorted({loc for locs in df["locations"] for loc in locs})
    all_locations.insert(0, "All Locations")
    selected_location = st.sidebar.selectbox(
        "Location", options=all_locations, index=0
    )

    # Extraction trigger
    if st.sidebar.button("Re-run Skill Extraction"):
        try:
            extract_and_save_skills()
            st.sidebar.success("Extraction complete. Please refresh.")
        except Exception as e:
            st.sidebar.error(f"Extraction failed: {e}")

    # Apply filters
    df_filtered = filter_data(df, selected_skills, selected_location)

    # Display summary
    st.markdown(f"### {len(df_filtered)} job listings found")

    # Pagination
    total = len(df_filtered)
    pages = max(1, (total + JOBS_PER_PAGE - 1) // JOBS_PER_PAGE)
    page = st.slider("Page", 1, pages, 1) if pages > 1 else 1
    start = (page - 1) * JOBS_PER_PAGE
    end = start + JOBS_PER_PAGE
    page_data = df_filtered.iloc[start:end]

    # Display jobs
    for _, job in page_data.iterrows():
        display_job(job)

    # Quick stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Top Skills")
    skill_df = skill_counts.reset_index()
    skill_df.columns = ["Skill", "Count"]
    fig = px.bar(
        skill_df.head(10), x="Skill", y="Count", title="Top 10 Skills"
    )
    st.sidebar.plotly_chart(fig, use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Word Cloud")
    if not skill_df.empty:
        wc = WordCloud(width=300, height=200, background_color="white").generate(
            " ".join(skill_df["Skill"])
        )
        fig_wc, ax_wc = plt.subplots()
        ax_wc.imshow(wc, interpolation="bilinear")
        ax_wc.axis("off")
        st.sidebar.pyplot(fig_wc)
    else:
        st.sidebar.write("No skills to display.")


def display_job(job: pd.Series) -> None:
    """
    Render a single job listing in an expander with two-column layout.
    """
    title = job["position"]
    company = job["company"]
    locations = job["locations"]
    date_posted = job.get("date", "")
    tags_str = format_tags(job.get("tags", []))
    skills_str = ", ".join(job["skills"])
    description = format_description(job.get("description", ""))
    apply_url = job.get("url", "#")

    with st.expander(f"{title} at {company}"):
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"#### {title}")
            st.markdown(f"**Company:** {company}")
            if locations:
                st.markdown(f"**Locations:** {format_tags(locations)}")
            if date_posted:
                st.markdown(f"**Date Posted:** {date_posted}")
            st.markdown("---")
            st.markdown("**Tags:**")
            st.write(tags_str)
            st.markdown("**Skills:**")
            st.write(skills_str)
        with col2:
            st.markdown("**Job Description**")
            for paragraph in description.split("\n\n"):
                st.write(paragraph)
            st.markdown(f"[Apply Here]({apply_url})")
        st.markdown("---")


if __name__ == "__main__":
    main()
