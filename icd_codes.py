
# ICD-10 Category Mapping
icd10_category_mapping = {
    "A": "Certain infectious and parasitic diseases",
    "B": "Certain infectious and parasitic diseases",
    "C": "Neoplasms",
    "D": "Diseases of the blood and blood-forming organs and certain disorders involving the immune mechanism",
    "E": "Endocrine, nutritional and metabolic diseases",
    "F": "Mental, Behavioral and Neurodevelopmental disorders",
    "G": "Diseases of the nervous system",
    "H": "Diseases of the eye and adnexa",
    "I": "Diseases of the circulatory system",
    "J": "Diseases of the respiratory system",
    "K": "Diseases of the digestive system",
    "L": "Diseases of the skin and subcutaneous tissue",
    "M": "Diseases of the musculoskeletal system and connective tissue",
    "N": "Diseases of the genitourinary system",
    "O": "Pregnancy, childbirth and the puerperium",
    "P": "Certain conditions originating in the perinatal period",
    "Q": "Congenital malformations, deformations and chromosomal abnormalities",
    "R": "Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified",
    "S": "Injury, poisoning and certain other consequences of external causes",
    "T": "Injury, poisoning and certain other consequences of external causes",
    "U": "Codes for special purposes",
    "V": "External causes of morbidity",
    "W": "External causes of morbidity",
    "X": "External causes of morbidity",
    "Y": "External causes of morbidity",
    "Z": "Factors influencing health status and contact with health services"
}


target_categories = {
    "Cardiovascular": {
        "code_range": "I00-I99",
        "codes": {
            "I10": "Essential Hypertension",
            "I25.10": "Coronary Artery Disease",
            "I50.9": "Heart Failure, unspecified",
            "I48.91": "Atrial Fibrillation, unspecified"
        }
    },
    "Respiratory": {
        "code_range": "J00-J99",
        "codes": {
            "J44.9": "Chronic Obstructive Pulmonary Disease, unspecified",
            "J45.909": "Unspecified Asthma, uncomplicated",
            "J84.10": "Pulmonary Fibrosis, unspecified"
        }
    },
    "Endocrine": {
        "code_range": "E00-E89",
        "codes": {
            "E10.9": "Type 1 Diabetes Mellitus without complications",
            "E11.9": "Type 2 Diabetes Mellitus without complications",
            "E03.9": "Hypothyroidism, unspecified",
            "E78.5": "Hyperlipidemia, unspecified",
            "E66.9": "Obesity, unspecified"
        }
    }
}

target_code_list = ['I10', 'I25.10', 'I50.9', 'I48.91', 'J44.9', 'J45.909', 'J84.10', 'E10.9', 'E11.9', 'E03.9', 'E78.5', 'E66.9']

keyword_bank = icd_codes = {
    "I10": {
        "description": "Hypertension",
        "keywords": ["hypertension", "high blood pressure", "HTN", "elevated BP", "hypertensive"]
    },
    "I25.10": {
        "description": "Coronary Artery Disease (CAD)",
        "keywords": ["CAD", "coronary artery disease", "ischemic heart disease", "blocked arteries", "atherosclerosis", "angina", "myocardial ischemia"]
    },
    "I50.9": {
        "description": "Congestive Heart Failure (CHF)",
        "keywords": ["CHF", "heart failure", "congestive heart disease", "cardiac failure", "fluid retention", "edema", "dyspnea", "left ventricular dysfunction"]
    },
    "I48.91": {
        "description": "Atrial Fibrillation",
        "keywords": ["AFib", "atrial fibrillation", "irregular heartbeat", "arrhythmia", "palpitations", "rapid heartbeat"]
    },
    "J44.9": {
        "description": "Chronic Obstructive Pulmonary Disease (COPD)",
        "keywords": ["COPD", "chronic bronchitis", "emphysema", "obstructive lung disease", "dyspnea", "wheezing", "chronic cough", "smoking-related lung disease"]
    },
    "J45.909": {
        "description": "Asthma",
        "keywords": ["asthma", "bronchial asthma", "wheezing", "shortness of breath", "allergic asthma", "reactive airway disease", "inhaler use"]
    },
    "J84.10": {
        "description": "Pulmonary Fibrosis",
        "keywords": ["pulmonary fibrosis", "lung scarring", "interstitial lung disease (ILD)", "restrictive lung disease", "idiopathic pulmonary fibrosis (IPF)"]
    },
    "E10.9": {
        "description": "Type 1 Diabetes Mellitus",
        "keywords": ["type 1 diabetes", "T1D", "insulin-dependent diabetes", "juvenile diabetes", "autoimmune diabetes", "high blood sugar"]
    },
    "E11.9": {
        "description": "Type 2 Diabetes Mellitus",
        "keywords": ["type 2 diabetes", "T2D", "non-insulin-dependent diabetes", "adult-onset diabetes", "metabolic syndrome", "high blood glucose"]
    },
    "E03.9": {
        "description": "Hypothyroidism",
        "keywords": ["hypothyroidism", "underactive thyroid", "thyroid hormone deficiency", "Hashimoto's disease", "low TSH", "fatigue", "weight gain"]
    },
    "E78.5": {
        "description": "Hyperlipidemia",
        "keywords": ["hyperlipidemia", "high cholesterol", "high LDL", "dyslipidemia", "lipid disorder", "triglycerides", "atherosclerosis"]
    },
    "E66.9": {
        "description": "Obesity",
        "keywords": ["obesity", "overweight", "BMI >30", "excessive weight", "metabolic obesity", "bariatric", "weight management"]
    }           
}

