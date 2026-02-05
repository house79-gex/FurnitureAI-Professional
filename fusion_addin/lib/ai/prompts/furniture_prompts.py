"""
Furniture generation prompt templates
"""

def create_furniture_parsing_prompt(description):
    """
    Create prompt for parsing furniture description
    
    Args:
        description: Natural language furniture description
    
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = """You are an expert furniture designer and manufacturing specialist.
You understand furniture terminology, standard dimensions, and construction methods.
Extract furniture parameters from descriptions and return them as valid JSON.
Use standard Italian furniture dimensions (all in mm):
- Base cabinets: height 720mm, depth 580mm
- Wall cabinets: height 720-900mm, depth 320mm
- Tall cabinets: height 2100-2400mm, depth 580mm
- Material thickness: typically 18mm for panels, 3mm for back panels

Always respond with ONLY a valid JSON object, no other text."""

    user_prompt = f"""Analyze this furniture description and extract parameters:

"{description}"

Return a JSON object with these fields:
{{
  "type": "base|wall|tall",
  "width": <width in mm>,
  "height": <height in mm>,
  "depth": <depth in mm>,
  "material_thickness": <thickness in mm, default 18>,
  "has_back": <true|false>,
  "back_thickness": <thickness in mm, default 3>,
  "shelves_count": <number of internal shelves>,
  "divisions_count": <number of vertical divisions>,
  "doors_count": <number of doors>,
  "drawers_count": <number of drawers>,
  "style": "<modern|classic|rustic|minimal|etc>",
  "finish": "<wood type, laminate, lacquer, etc>",
  "notes": "<any special features>"
}}

Use reasonable defaults for any missing information."""

    return system_prompt, user_prompt

def create_dimension_extraction_prompt(text):
    """
    Create prompt for extracting dimensions from text
    
    Args:
        text: Text containing dimension information
    
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = """You are an expert at extracting measurements and dimensions from text.
Convert all measurements to millimeters (mm).
Return results as valid JSON."""

    user_prompt = f"""Extract dimensions from this text:

"{text}"

Return JSON:
{{
  "width": <value in mm or null>,
  "height": <value in mm or null>,
  "depth": <value in mm or null>
}}"""

    return system_prompt, user_prompt

def create_style_analysis_prompt(description):
    """
    Create prompt for analyzing furniture style
    
    Args:
        description: Furniture description
    
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = """You are an interior design and furniture style expert.
Identify furniture styles, finishes, and design elements."""

    user_prompt = f"""Analyze the style of this furniture:

"{description}"

Return JSON:
{{
  "style": "<primary style: modern, classic, rustic, industrial, scandinavian, etc>",
  "sub_style": "<more specific style if applicable>",
  "finish": "<wood type, color, material>",
  "door_style": "<flat, shaker, raised panel, glass, etc>",
  "hardware": "<handles, knobs, or handleless>",
  "features": ["<list of notable features>"]
}}"""

    return system_prompt, user_prompt
