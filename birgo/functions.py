import random
import re
import string


def slugify(text):
    """
    Converts a string to a URL-friendly slug.
    """
    text = text.lower().strip()  # Convert to lowercase and remove leading/trailing whitespace
    text = re.sub(r'[^\w\s-]', '', text)  # Remove non-alphanumeric characters (except spaces and hyphens)
    text = re.sub(r'[\s_-]+', '-', text)  # Replace spaces, underscores, and multiple hyphens with a single hyphen
    text = re.sub(r'^-+|-+$', '', text)  # Remove leading/trailing hyphens
    return text

def get_random_integer(number) -> str:
    N = number
    return ''.join(random.choices(string.digits, k=N))