import re
import spacy
# Load the SpaCy model
nlp = spacy.load("en_core_web_md")  # Replace with the appropriate model name
from typing import List
from icd_codes import target_code_list
import pandas as pd
from tqdm import tqdm
import ast 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import scispacy
from scispacy.abbreviation import AbbreviationDetector
from scispacy.linking import EntityLinker
# Download stopwords (run this once)
# nltk.download("stopwords")
# nltk.download("punkt")
# nltk.download("punkt_tab")
# Load SciSpacy medical NLP model (choose 'en_core_sci_md' or 'en_core_sci_lg' for better results)
nlp = spacy.load("en_core_sci_md")
# Add the abbreviation pipe to the spacy pipeline
nlp.add_pipe("abbreviation_detector")
# linker = EntityLinker()
# nlp.add_pipe('entityLinker')


# Stopwords (keep important medical terms)
stop_words = set(stopwords.words("english"))
medical_abbreviations = {
    "zes": "zotarolimus-eluting stent",
    "bp": "blood pressure",
    "cad": "coronary artery disease",
    "hba1c": "glycated hemoglobin"
}

def preprocess_clinical_text(text):
    """
    Preprocesses clinical notes by applying:
    - Lowercasing
    - Removing fancy characters
    - Expanding abbreviations
    - Tokenization
    - Removing non-medical stopwords
    - Lemmatization
    - Keeping numbers
    - Named Entity Recognition (NER) for medical terms
    """
      # 1. Lowercasing (Preserve case for known medical terms)
    text = text.lower()

    # 2. Expand medical abbreviations
    for abbr, full_form in medical_abbreviations.items():
        text = re.sub(r"\b" + re.escape(abbr) + r"\b", full_form, text)

    # 3. Remove unnecessary characters, keeping medical symbols
    text = re.sub(r"[^a-zA-Z0-9\s.%/-]", "", text)  # Keep %, /, and -

    # 4. Tokenization
    tokens = word_tokenize(text)

    # 5. Stopword Removal (except medical words)
    tokens = [word for word in tokens if word not in stop_words]

    # 6. Lemmatization
    doc = nlp(" ".join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]

    # 7. Reconstruct cleaned text
    cleaned_text = " ".join(lemmatized_tokens)

    
    # 7. Named Entity Recognition (NER) - Extract Diagnoses, Symptoms, Procedures
    """Fix it later 
    extracted_entities = {
        "diagnoses": [],
        "symptoms": [],
        "procedures": [],
        "medications": []
    }

    for ent in doc.ents:
        # Link entity to UMLS (Unified Medical Language System)
        if len(ent._.umls_ents) > 0:
            concept_id = ent._.umls_ents[0][0]  # Get UMLS concept ID
            extracted_entities["diagnoses"].append(ent.text) if "Disease" in concept_id else None
            extracted_entities["symptoms"].append(ent.text) if "Sign_or_Symptom" in concept_id else None
            extracted_entities["procedures"].append(ent.text) if "Procedure" in concept_id else None
            extracted_entities["medications"].append(ent.text) if "Drug_or_Chemical" in concept_id else None
    """
    return cleaned_text


def extract_medical_entities (text: str) -> List[str]:
    """Extract medical entities using SpaCy"""
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents 
                if ent.label_ in ['DISEASE', 'SYMPTOM', 'TREATMENT']]
    return entities


def preprocess_text(text: str) -> str:
    """Clean and preprocess clinical note text"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep important medical symbols
    text = re.sub(r'[^a-zA-Z0-9\s+\-\.%]', ' ', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text


def generate_labels(detected_codes: set, target_code_list: list) -> list:
    """
    Generate binary labels for ICD-10 codes based on detected codes.

    Args:
        detected_codes (set): A set of detected ICD-10 codes.
        all_codes (list): A list of all possible ICD-10 codes.

    Returns:
        list: A binary list indicating the presence (1) or absence (0) of each code.
    """
    return [1 if code in detected_codes else 0 for code in target_code_list]


def generate_labels_for_df(df: pd.DataFrame, target_code_list: list) -> pd.DataFrame:
    df['icd10_codes'] = df['icd10_codes'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df['labels'] = df['icd10_codes'].progress_apply(lambda x: generate_labels(x, target_code_list))
    df['target_codes_detected'] = df['icd10_codes'].apply(lambda x: set(x) & set(target_code_list))
    target_code_prefixes = {code[:3] for code in target_code_list}
    # Update the target_codes_detected to include common codes based on the first three characters
    df['target_codes_detected_uptil_3'] = df['icd10_codes'].apply(
        lambda x: set(code[:3] for code in x) & target_code_prefixes
    )
    return df

def validate_train_has_all_labels(df, target_code_list, label_column_name):
    # Count the occurrences of each target code in the balanced dataset
    target_code_counts = df[label_column_name].explode().value_counts()
    # Convert the counts to a DataFrame for better readability
    target_code_counts_df = target_code_counts.reset_index()
    target_code_counts_df.columns = ['target_code', 'count']
    # Display the counts of each target code
    print(target_code_counts_df)
    assert len(target_code_counts_df) == len(target_code_list), "Train data does not have all the labels"
