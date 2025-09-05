import pandas as pd
import re

def clean_comment(text):
    if pd.isna(text):
        return None
    
    # delete mention (@username)
    text = re.sub(r'@\w+', '', text)

    # lowercase
    text = text.lower()
    
    # delete link
    text = re.sub(r'http\S+|www\S+', '', text)
    
    # delete non-printable characters except emoticons
    text = re.sub(r'[^\x00-\x7F]+', lambda m: m.group(0), text)
    
    # delete whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text if text else None