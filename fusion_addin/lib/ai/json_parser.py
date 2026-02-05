"""
JSON parser for extracting structured data from LLM responses
"""

import json
import re

def extract_json_from_response(response):
    """
    Extract JSON from LLM response text
    
    Handles cases where:
    - JSON is wrapped in markdown code blocks
    - JSON has text before/after it
    - Multiple JSON objects exist
    
    Args:
        response: LLM response text
    
    Returns:
        dict or list: Parsed JSON object, or None if parsing fails
    """
    if not response:
        return None
    
    # Try direct parsing first
    try:
        return json.loads(response)
    except:
        pass
    
    # Remove markdown code blocks
    response = re.sub(r'```json\s*', '', response)
    response = re.sub(r'```\s*', '', response)
    
    # Find JSON objects or arrays
    json_patterns = [
        r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Nested objects
        r'\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]'  # Arrays
    ]
    
    for pattern in json_patterns:
        matches = re.finditer(pattern, response, re.DOTALL)
        for match in matches:
            try:
                json_str = match.group(0)
                return json.loads(json_str)
            except:
                continue
    
    # Try finding bounds manually
    try:
        start_idx = response.find('{')
        end_idx = response.rfind('}') + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
    except:
        pass
    
    # Array format
    try:
        start_idx = response.find('[')
        end_idx = response.rfind(']') + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
    except:
        pass
    
    return None

def validate_furniture_params(params):
    """
    Validate and normalize furniture parameters
    
    Args:
        params: Dictionary of furniture parameters
    
    Returns:
        dict: Validated and normalized parameters
    """
    defaults = {
        'type': 'base',
        'width': 800,
        'height': 720,
        'depth': 580,
        'material_thickness': 18,
        'has_back': True,
        'back_thickness': 3,
        'shelves_count': 0,
        'divisions_count': 0
    }
    
    validated = defaults.copy()
    
    if not isinstance(params, dict):
        return validated
    
    # Validate type
    if params.get('type') in ['base', 'wall', 'tall', 'column']:
        validated['type'] = params['type']
    
    # Validate dimensions (must be positive)
    for key in ['width', 'height', 'depth', 'material_thickness', 'back_thickness']:
        if key in params:
            try:
                value = float(params[key])
                if value > 0:
                    validated[key] = value
            except:
                pass
    
    # Validate counts (must be non-negative integers)
    for key in ['shelves_count', 'divisions_count']:
        if key in params:
            try:
                value = int(params[key])
                if value >= 0:
                    validated[key] = value
            except:
                pass
    
    # Validate booleans
    if 'has_back' in params:
        validated['has_back'] = bool(params['has_back'])
    
    return validated
