# utils/filters.py
"""
Filtering utilities for JobTrends dashboard.
"""

def filter_jobs_by_skills_and_location(df, selected_skills, selected_location):
    """
    Filters the DataFrame by selected_skills and selected_location.
    - selected_skills: list of skills to filter by; if empty, no skill filtering applied.
    - selected_location: string representing the city to filter by; if 'All Locations', no location filtering.
    Returns the filtered DataFrame.
    """
    # Filter by skills
    if selected_skills:
        df = df[df['skills'].apply(lambda s_list: any(s in s_list for s in selected_skills))]

    # Filter by location
    if selected_location and selected_location != 'All Locations':
        df = df[df['locations'].apply(lambda locs: selected_location in locs)]

    return df
