import pandas as pd
import re
import logging

# Module-specific logger
logger = logging.getLogger("detection_agent")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler("logs/detection_log.txt")
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def load_valid_countries(filepath='data/valid_countries.txt'):
    with open(filepath, 'r') as f:
        return [line.strip().lower() for line in f.readlines()]

def is_valid_email(email):
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.match(pattern, email.strip()) is not None

def is_valid_phone(phone):
    try:
        phone_str = str(int(float(str(phone).strip())))
        return phone_str.isdigit() and len(phone_str) == 10
    except:
        return False

def detect_issues(input_path='data/input.csv'):
    df = pd.read_csv(input_path, dtype={'phone': str})  # Read phone as string
    valid_countries = load_valid_countries()

    issues = []

    for idx, row in df.iterrows():
        row_issues = []

        # Name check
        name = str(row['name']).strip() if pd.notna(row['name']) else ''
        if name == '':
            row_issues.append("Missing name")

        # Email check
        email = str(row['email']).strip() if pd.notna(row['email']) else ''
        if email == '':
            row_issues.append("Missing email")
        elif not is_valid_email(email):
            row_issues.append("Malformed email")

        # Phone check
        phone = str(row['phone']).strip() if pd.notna(row['phone']) else ''
        if phone == '':
            row_issues.append("Missing phone")
        elif not is_valid_phone(phone):
            row_issues.append("Invalid phone number")

        # Country check
        country = str(row['country']).strip() if pd.notna(row['country']) else ''
        if country == '':
            row_issues.append("Missing country")
        elif country.lower() not in valid_countries:
            row_issues.append("Invalid country")

        if row_issues:
            logger.info(f"Row {idx}: " + ", ".join(row_issues))
            issues.append((idx, row_issues))

    # Duplicate detection
    duplicates = df[df.duplicated(keep=False)]
    for idx in duplicates.index:
        logger.info(f"Row {idx}: Duplicate row detected")
        issues.append((idx, ["Duplicate row"]))

    return issues