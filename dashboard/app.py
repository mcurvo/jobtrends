# dashboard/app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from processing.extract_skills import extract_and_save_skills
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Load the processed job data
df = pd.read_csv("data/with_skills_spacy.csv")

# Check if the 'skills' column contains valid lists and clean the data
df['skills'] = df['skills'].apply(lambda x: eval(x) if isinstance(x, str) else x)  # Ensure it's a list

# Remove NaN and empty lists from the 'skills' column
df_cleaned = df[df['skills'].apply(lambda x: isinstance(x, list) and len(x) > 0)]

# Capitalize each skill in the 'skills' column
df_cleaned['skills'] = df_cleaned['skills'].apply(lambda skills: [skill.capitalize() for skill in skills])

# Optionally, remove any duplicate skills within a single row
df_cleaned['skills'] = df_cleaned['skills'].apply(lambda skills: list(set(skills)))

# Display the title
st.title('JobTrends - Tech Job Market Analyzer')
st.subheader('Job Listings')

# Display job data
st.dataframe(df)

# Button to re-run skill extraction
if st.button('Re-run Skill Extraction'):
    extract_and_save_skills()
    st.success('Skills extraction complete!')

# --- Skill and City Filters ---
st.subheader('Search for Jobs by Skills and City')

# --- Skill Selection ---
skills = df_cleaned['skills'].explode().unique()  # Get all unique skills
if len(skills) == 0:
    st.warning("No skills found in the dataset.")
else:
    selected_skills = st.multiselect(
        'Select Skills to Search for',
        options=skills,
        default=skills[:5]  # Default to the first 5 skills for convenience
    )

    # --- City Selection ---
    cities = df_cleaned['location'].dropna().unique()  # Get all unique locations
    cities = list(cities)  # Convert to list for easier manipulation
    cities.insert(0, 'All Locations')  # Add 'All Locations' as the first option

    selected_city = st.selectbox(
        'Select City to Search for',
        options=cities,
        index=0  # Default to 'All Locations'
    )

    # Filter the data based on the selected skills and city
    if selected_skills:
        filtered_df = df_cleaned[df_cleaned['skills'].apply(lambda x: any(skill in x for skill in selected_skills))]
    else:
        filtered_df = df_cleaned

    if selected_city != 'All Locations':
        filtered_df = filtered_df[filtered_df['location'] == selected_city]

    # Display filtered data
    st.dataframe(filtered_df)

    # --- Top Skills Visualization (Filtered) ---
    st.subheader('Top Skills in the Filtered Data')

    # Get the skill frequency from the filtered data
    filtered_skills_counts = filtered_df['skills'].explode().value_counts()

    # Convert to DataFrame for Plotly compatibility
    skills_counts_df = filtered_skills_counts.reset_index()
    skills_counts_df.columns = ['Skill', 'Frequency']

    # Create the bar chart using Plotly
    fig = px.bar(
        skills_counts_df.head(10),  # Take top 10 most frequent skills
        x='Skill',  # Use 'Skill' as the x-axis
        y='Frequency',  # Use 'Frequency' as the y-axis
        title=f'Top 10 Skills in {selected_city} with Selected Skills',
        labels={'Skill': 'Skills', 'Frequency': 'Frequency'}
    )

    # Display the plot
    st.plotly_chart(fig)

    # --- Word Cloud Visualization for Filtered Data ---
    st.subheader('Skills Word Cloud for Filtered Data')

    # Combine all skills into a single string for the word cloud
    all_filtered_skills = ' '.join(filtered_df['skills'].explode())

    # Generate a word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_filtered_skills)

    # Display the word cloud
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")  # Hide axes
    st.pyplot(fig)

    # --- Skill Distribution by Job Type ---
    st.subheader('Skill Distribution by Job Type')

    # Get job type or tags from the filtered data
    job_types = filtered_df['tags'].dropna().explode().value_counts()

    # Create a Pie chart with Plotly
    fig_pie = px.pie(
        job_types, 
        values=job_types.values, 
        names=job_types.index, 
        title=f"Skill Distribution by Job Type in {selected_city}"
    )

    st.plotly_chart(fig_pie)
