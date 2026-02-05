"""
Layout generation prompt templates
"""

def create_layout_prompt(params):
    """
    Create prompt for generating room layout
    
    Args:
        params: Layout parameters dict
            - room_width: Room width in mm
            - room_depth: Room depth in mm
            - room_type: kitchen, bedroom, bathroom, living
            - layout_style: L, U, linear, island, galley
            - appliances: List of required appliances
            - budget: Budget constraint
    
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    room_width = params.get('room_width', 3600)
    room_depth = params.get('room_depth', 3000)
    room_type = params.get('room_type', 'kitchen')
    layout_style = params.get('layout_style', 'L')
    appliances = params.get('appliances', [])
    budget = params.get('budget', 0)
    
    system_prompt = """You are an expert furniture layout designer and space planner.
You understand ergonomics, workflow, and standard furniture dimensions.
Generate optimized layouts that maximize functionality and aesthetics.
All dimensions must be in millimeters (mm).
Return ONLY valid JSON, no other text."""

    appliances_str = ', '.join(appliances) if appliances else 'standard appliances'
    budget_str = f', budget: €{budget}' if budget > 0 else ''

    user_prompt = f"""Design a {room_type} layout with these specifications:

Room dimensions: {room_width}mm × {room_depth}mm
Layout style: {layout_style}
Required appliances: {appliances_str}{budget_str}

Create a complete furniture layout. Return JSON:
{{
  "cabinets": [
    {{
      "id": "<unique_id>",
      "type": "base|wall|tall",
      "position": {{
        "x": <x coordinate in mm from origin>,
        "y": <y coordinate in mm from origin>,
        "rotation": <rotation in degrees, 0-360>
      }},
      "dimensions": {{
        "width": <width in mm>,
        "height": <height in mm>,
        "depth": <depth in mm>
      }},
      "configuration": {{
        "doors": <number of doors>,
        "drawers": <number of drawers>,
        "shelves": <number of shelves>
      }},
      "function": "<sink_base|cooktop|oven|refrigerator|storage|corner|etc>"
    }}
  ],
  "total_cost": <estimated cost in EUR>,
  "notes": "<layout explanation and tips>"
}}

Follow these rules:
1. Base cabinets: height 720mm, depth 580mm
2. Wall cabinets: height 720mm, depth 320mm
3. Tall cabinets: height 2100mm, depth 580mm
4. Standard widths: 300, 400, 450, 600, 800, 900mm
5. Maintain ergonomic spacing and workflow triangle (for kitchens)
6. Leave space for appliances and circulation"""

    return system_prompt, user_prompt

def create_optimization_prompt(current_layout, constraints):
    """
    Create prompt for optimizing existing layout
    
    Args:
        current_layout: Current layout dict
        constraints: Optimization constraints
    
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    system_prompt = """You are a furniture layout optimization expert.
Improve layouts for better workflow, ergonomics, and space utilization."""

    user_prompt = f"""Optimize this furniture layout:

Current layout: {current_layout}

Constraints: {constraints}

Provide an optimized version with same JSON structure, including:
- Improved positioning
- Better workflow
- Space efficiency
- Cost optimization if applicable

Return ONLY the optimized JSON layout."""

    return system_prompt, user_prompt
