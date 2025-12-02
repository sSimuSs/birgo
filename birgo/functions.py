import random
import re
import string


def slugify(text):
    """
    Converts a string to a URL-friendly slug.
    """
    # Convert to lowercase and remove leading/trailing whitespace
    text = text.lower().strip()
    # Remove non-alphanumeric characters (except spaces and hyphens)
    text = re.sub(r'[^\w\s-]', '', text)
    # Replace spaces, underscores, and multiple hyphens with a single hyphen
    text = re.sub(r'[\s_-]+', '-', text)
    # Remove leading/trailing hyphens
    text = re.sub(r'^-+|-+$', '', text)
    return text

def get_random_integer(number) -> str:
    """
    Generates a random integer.
    """
    n = number
    return ''.join(random.choices(string.digits, k=n))
