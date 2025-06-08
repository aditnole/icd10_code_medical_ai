import re
from typing import Dict, List

def load_icd10_codes(file_path: str) -> Dict[str, str]:
    """
    Load and parse ICD-10 codes from file
    
    Args:
        file_path: Path to ICD-10 codes file
        
    Returns:
        Dictionary mapping ICD-10 codes to their descriptions
    """
    codes_dict = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Assuming format: "CODE DESCRIPTION"
                code, description = line.strip().split(' ', 1)
                codes_dict[code] = description
    except FileNotFoundError:
        print(f"Error: ICD-10 codes file not found at {file_path}")
        raise
    except Exception as e:
        print(f"Error reading ICD-10 codes file: {str(e)}")
        raise
        
    return codes_dict

def get_target_codes() -> Dict[str, Dict[str, str]]:
    """Define target ICD-10 code categories"""
    return {
        'cardiovascular': {
            'I10': 'Hypertension',
            'I25.10': 'Coronary Artery Disease',
            'I50.9': 'Congestive Heart Failure',
            'I48.91': 'Atrial Fibrillation'
        },
        'respiratory': {
            'J44.9': 'Chronic Obstructive Pulmonary Disease',
            'J45.909': 'Asthma',
            'J84.10': 'Pulmonary Fibrosis'
        },
        'endocrine': {
            'E10.9': 'Type 1 Diabetes Mellitus',
            'E11.9': 'Type 2 Diabetes Mellitus',
            'E03.9': 'Hypothyroidism',
            'E78.5': 'Hyperlipidemia',
            'E66.9': 'Obesity'
        }
    }

def get_code_keywords() -> Dict[str, List[str]]:
    """Define keywords for each ICD-10 code"""
    return {
        'I10': ['hypertension', 'high blood pressure', 'elevated bp', 'htn'],
        'I25.10': ['coronary artery disease', 'cad', 'coronary heart disease', 'chd'],
        'I50.9': ['heart failure', 'chf', 'cardiac failure', 'congestive heart'],
        'I48.91': ['atrial fibrillation', 'afib', 'a-fib'],
        'J44.9': ['copd', 'chronic obstructive pulmonary disease'],
        'J45.909': ['asthma', 'reactive airway'],
        'J84.10': ['pulmonary fibrosis', 'lung fibrosis'],
        'E10.9': ['type 1 diabetes', 't1dm', 'type i diabetes'],
        'E11.9': ['type 2 diabetes', 't2dm', 'type ii diabetes'],
        'E03.9': ['hypothyroidism', 'underactive thyroid'],
        'E78.5': ['hyperlipidemia', 'high cholesterol', 'dyslipidemia'],
        'E66.9': ['obesity', 'overweight', 'high bmi']
    }

def preprocess_text(text: str) -> str:
    """Clean and preprocess clinical note text"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters but keep important medical symbols
    text = re.sub(r'[^a-zA-Z0-9\s+\-\.%]', ' ', text)
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    return text 