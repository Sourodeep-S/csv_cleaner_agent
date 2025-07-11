import pandas as pd
from fuzzywuzzy import process
import logging

# Use a module-specific logger
logger = logging.getLogger("correction_agent")
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers in case it's already added
if not logger.handlers:
    file_handler = logging.FileHandler('logs/correction_log.txt')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def is_valid_phone(phone):
    try:
        phone_str = str(int(float(str(phone).strip())))
        return phone_str.isdigit() and len(phone_str) == 10
    except:
        return False

def load_valid_countries(filepath='data/valid_countries.txt'):
    with open(filepath, 'r') as f:
        return [line.strip() for line in f.readlines()]

def correct_data(input_path='data/input.csv', output_path='data/output.csv'):
    df = pd.read_csv(input_path, dtype={'phone': str})
    original_len = len(df)

    # 1. Remove duplicates
    df = df.drop_duplicates()
    num_duplicates = original_len - len(df)
    if num_duplicates > 0:
        logger.info(f"Removed {num_duplicates} duplicate rows.")

    # 2. Standardize data
    for idx, row in df.iterrows():
        if pd.notna(row['name']):
            cleaned_name = str(row['name']).strip().title()
            if cleaned_name != row['name']:
                logger.info(f"Row {idx}: Name standardized from '{row['name']}' to '{cleaned_name}'")
                df.at[idx, 'name'] = cleaned_name

        if pd.notna(row['email']):
            cleaned_email = str(row['email']).strip().lower()
            if cleaned_email != row['email']:
                logger.info(f"Row {idx}: Email standardized from '{row['email']}' to '{cleaned_email}'")
                df.at[idx, 'email'] = cleaned_email

        if pd.notna(row['country']):
            cleaned_country = str(row['country']).strip()
            if cleaned_country != row['country']:
                logger.info(f"Row {idx}: Trimmed spaces in country '{row['country']}'")
                df.at[idx, 'country'] = cleaned_country

        if pd.notna(row['phone']):
            phone_str = str(row['phone']).strip()
            if not is_valid_phone(phone_str):
                logger.info(f"Row {idx}: Invalid phone '{row['phone']}' replaced with '0'")
                df.at[idx, 'phone'] = '0'


    # 3. Fuzzy correct invalid country names
    valid_countries = load_valid_countries()
    for idx, row in df.iterrows():
        country = str(row['country']).strip()
        if country and country not in valid_countries:
            best_match, score = process.extractOne(country, valid_countries)
            if score >= 80:
                logger.info(f"Row {idx}: Country '{country}' corrected to '{best_match}' (score={score})")
                df.at[idx, 'country'] = best_match
            else:
                logger.info(f"Row {idx}: Country '{country}' could not be confidently matched (score={score})")

    df.to_csv(output_path, index=False)
    return df
