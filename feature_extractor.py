from urllib.parse import urlparse
import re

def extract_features(url):
    """
    Extract simple URL-based features for phishing detection.
    Returns a list of numeric features.
    """

    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    # Feature 1: Length of URL
    url_length = len(url)

    # Feature 2: Does URL use HTTPS?
    has_https = 1 if parsed.scheme == "https" else 0

    # Feature 3: Number of dots
    dot_count = url.count(".")

    # Feature 4: Number of hyphens
    hyphen_count = url.count("-")

    # Feature 5: Number of slashes
    slash_count = url.count("/")

    # Feature 6: Number of digits
    digit_count = sum(c.isdigit() for c in url)

    # Feature 7: Presence of @ symbol
    has_at_symbol = 1 if "@" in url else 0

    # Feature 8: Presence of IP address in URL
    ip_pattern = r"(\d{1,3}\.){3}\d{1,3}"
    has_ip = 1 if re.search(ip_pattern, url) else 0

    # Feature 9: Presence of suspicious words
    suspicious_words = [
        "login", "verify", "bank", "secure", "account",
        "update", "free", "bonus", "claim", "password"
    ]
    suspicious_word_count = sum(word in url.lower() for word in suspicious_words)

    # Feature 10: Domain length
    domain_length = len(domain)

    return [
        url_length,
        has_https,
        dot_count,
        hyphen_count,
        slash_count,
        digit_count,
        has_at_symbol,
        has_ip,
        suspicious_word_count,
        domain_length
    ]