import os
from openai import OpenAI
from llm_prompts import SYSTEM_PROMPT_v2, ICD10_DETECTION_PROMPT_v2, SUMMARIZATION_PROMPT
from models import ICD10Response, SummaryResponse
from typing import List, Dict, Any
from tqdm import tqdm
tqdm.pandas()
import pandas as pd
from config import LLM_MODEL
import time


def analyze_clinical_note(clinical_note: str) -> ICD10Response:
    """
    Analyze clinical note to detect ICD-10 codes with concise references
    
    Args:
        clinical_note: The clinical note text
        
    Returns:
        ICD10Response object containing detected codes with their references
    """
    user_prompt = ICD10_DETECTION_PROMPT_v2.format(clinical_note=clinical_note)

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Update the system prompt to request concise references
         
        response = client.beta.chat.completions.parse(
            model= LLM_MODEL,  # or another model that supports JSON response format
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_v2},
                {"role": "user", "content": user_prompt}
            ],
            response_format=ICD10Response,
            
        )
        
        # Get the response content
        event = response.choices[0].message.parsed
        # print(event)
        return event
    
    except Exception as e:
            if "Rate limit reached" in str(e):
                print("Rate limit reached. Waiting before retrying...")
                time.sleep(1)  # Wait for 1 second before retrying
            else:
                print(f"Error analyzing clinical note: {str(e)}")
                return "Error"  
            



def extract_codes_from_response(response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract primary and secondary ICD-10 codes from the LLM response.
    
    Args:
        response: The response from the LLM containing identified codes.
        
    Returns:
        List of dictionaries containing code, code_type, description, confidence, and supporting_keyword_evidence.
    """
    extracted_codes = []
    extracted_json = []

    for code_info in response.identified_codes:
        code = code_info.code
        code_type = code_info.code_type
        description = code_info.description
        confidence = code_info.confidence
        supporting_evidence = code_info.supporting_keyword_evidence
        
        extracted_json.append({
            "code": code,
            "code_type": code_type,
            "description": description,
            "confidence": confidence,
            "supporting_keyword_evidence": supporting_evidence
        })
        if code is not None and code != '':
            extracted_codes.append(code)
        else:
            print(f"No code found for {code_info}")

    extracted_codes = set(extracted_codes)
    
    return extracted_codes, extracted_json

def summarize_clinical_note(clinical_note: str) -> str:
    """
    Summarize the clinical note using the provided prompt.
    Args: clinical note
    """
    summarization_prompt = SUMMARIZATION_PROMPT.format(clinical_note=clinical_note)

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))        
        response = client.beta.chat.completions.parse(
            model="gpt-4o",  # or another model that supports JSON response format
            messages=[
                {"role": "system", "content": summarization_prompt},
                {"role": "user", "content": clinical_note}
            ],    
            response_format=SummaryResponse,
            
        )
        # Get the response content
        event = response.choices[0].message.parsed
        return event.summary
    
    except Exception as e:
        print(f"Error analyzing clinical note: {str(e)}")
        return "Error"
    
def get_icd10_code_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get the ICD-10 code dataframe from the provided dataframe.
    """
    df['icd10_codes'] = None  
    df['raw_llm_response'] = df['patient'].progress_apply(analyze_clinical_note)
    df['json_llm'] = df['raw_llm_response'].progress_apply(extract_codes_from_response)
    df['icd10_codes'] = df['json_llm'].progress_apply(lambda x: x[0])
    df['json_llm'] = df['json_llm'].progress_apply(lambda x: x[1])
    return df
        

