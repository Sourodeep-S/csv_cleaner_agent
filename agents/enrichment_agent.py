import pandas as pd
import logging

logger = logging.getLogger("enrichment_agent")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler("logs/enrichment_log.txt")
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def infer_name_from_email(email):
    try:
        prefix = email.split('@')[0]
        parts = prefix.replace('.', ' ').replace('_', ' ').split()
        return ' '.join([p.capitalize() for p in parts])
    except:
        return None

def enrich_data(input_path='data/output.csv', output_path='data/output_enriched.csv'):
    df = pd.read_csv(input_path, dtype={'phone': str})

    for idx, row in df.iterrows():
        # Enrich missing name using email
        if pd.isna(row['name']) or str(row['name']).strip() == '':
            if pd.notna(row['email']):
                inferred_name = infer_name_from_email(row['email'])
                if inferred_name:
                    df.at[idx, 'name'] = inferred_name
                    logger.info(f"Row {idx}: Name inferred as '{inferred_name}' from email '{row['email']}'")

        # Enrich missing email – set to placeholder
        if pd.isna(row['email']) or str(row['email']).strip() == '':
            df.at[idx, 'email'] = 'unknown@example.com'
            logger.info(f"Row {idx}: Missing email filled with placeholder 'unknown@example.com'")

        # Enrich missing phone – set to 0
        if pd.isna(row['phone']) or str(row['phone']).strip() == '':
            df.at[idx, 'phone'] = '0'
            logger.info(f"Row {idx}: Missing phone filled with '0'")

    df.to_csv(output_path, index=False)
    return df
