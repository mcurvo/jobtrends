# processing/normalize_skills.py

def normalize_skills(skills_list, mapping):
    """
    Normalize a list of skills using the provided mapping dictionary.
    - Converts skills to lowercase
    - Maps variations to canonical names
    - Capitalizes the final skill names
    - Removes duplicates
    """
    if not isinstance(skills_list, list):
        return []

    cleaned_skills = set()
    for skill in skills_list:
        if not isinstance(skill, str):
            continue
        skill_lower = skill.lower().strip()
        normalized = mapping.get(skill_lower, skill_lower.capitalize())
        cleaned_skills.add(normalized)

    return list(cleaned_skills)


# Example skill mapping dictionary
skill_mapping = {
    'js': 'JavaScript',
    'javascript': 'JavaScript',
    'py': 'Python',
    'python3': 'Python',
    'html5': 'HTML',
    'css3': 'CSS',
    'sql': 'SQL',
    'reactjs': 'React',
    'react.js': 'React',
    'node': 'Node.js',
    'nodejs': 'Node.js',
    'typescript': 'TypeScript',
    'ts': 'TypeScript',
    'docker': 'Docker',
    'k8s': 'Kubernetes',
    'kubernetes': 'Kubernetes',
    'aws': 'AWS',
    'azure': 'Azure',
    'gcp': 'GCP',
    'google cloud': 'GCP',
    'machine learning': 'Machine Learning',
    'ml': 'Machine Learning',
    'deep learning': 'Deep Learning',
    'nlp': 'Natural Language Processing',
    'natural language processing': 'Natural Language Processing',
}

# Usage example:
# normalized = normalize_skills(['js', 'Python3', 'ML'], skill_mapping)
# print(normalized)  # ['JavaScript', 'Python', 'Machine Learning']
