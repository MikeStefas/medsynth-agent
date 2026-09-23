def clinical_rule_extractor_user_prompt(
    target_class: str,
    feature_name: str,
    column_info_str: str,
    pubmed_relevant_abstracts_block: str,
) -> str:
    return f"""TARGET CLINICAL COHORT:
{target_class}

TARGET FEATURE TO EXTRACT RULES FOR:
{column_info_str}

RETRIEVED PUBMED LITERATURE:
{pubmed_relevant_abstracts_block}

TASK:
Extract ONLY numerical clinical cutoffs, diagnostic thresholds, or reference bounds for '{feature_name}' in patients with {target_class}.

STRICT NEGATIVE CONSTRAINTS (DO NOT VIOLATE):
1. FEATURE NAME STRICTNESS:
   - The 'feature_name' in your output MUST be EXACTLY "{feature_name}".
   - NEVER extract rules for other biomarkers mentioned in the text (e.g. DO NOT extract HbA1c, HOMA-IR, FPG, or insulin sensitivity indices unless the target feature is explicitly that biomarker).
2. UNIT & SCALE CONSISTENCY:
   - Ensure the extracted number matches the physical scale and unit of '{feature_name}'.
   - Do NOT convert percentage or mmol/L values into mg/dL or vice versa.
3. NO RULES FOUND:
   - If the literature does not mention a concrete numerical cutoff specifically for '{feature_name}', return an empty list: []
"""