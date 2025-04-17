# utils/formatters.py

import re
import html

# Acronyms to remain uppercase
ACRONYMS = {"HTML", "CSS", "SQL", "AWS", "API", "UI", "UX", "CI", "CD", "JSON", "XML", "HTTP"}

def format_tags(tags_list):
    """Convert list of tags into a comma-separated string."""
    return ", ".join(tags_list)


def format_skills(skills_list):
    """
    Capitalize skills, keep acronyms uppercase, remove duplicates, preserve order.
    """
    formatted = []
    for s in skills_list:
        s_strip = s.strip()
        candidate = s_strip.upper() if s_strip.upper() in ACRONYMS else s_strip.capitalize()
        if candidate not in formatted:
            formatted.append(candidate)
    return formatted


def format_description(html_text):
    """
    Clean HTML description to plain text with paragraphs and bullets.
    """
    text = html_text or ""
    # Unescape HTML entities
    text = html.unescape(text)
    # Fix potential mojibake
    try:
        text = text.encode('latin-1').decode('utf-8')
    except Exception:
        pass

    # Convert paragraphs and lists
    text = text.replace('</p><p>', '\n\n').replace('<p>', '').replace('</p>', '\n\n')
    text = text.replace('<li>', '\n- ').replace('</li>', '')

    # Remove remaining HTML tags and entities
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&[a-zA-Z0-9#]+;', ' ', text)

    # Convert numbered lists to bullets
    text = re.sub(r'(?m)^\s*\d+\.\s*', '- ', text)
    # Bold headings (lines ending with colon)
    text = re.sub(r'(?m)^(.*?):\s*$', r'**\1:**', text)
    # Collapse multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()
