"""
Core module for icon generation
"""

from .icon_base import IconBase, SimpleShapeIcon
from .svg_builder import SVGBuilder
from .validators import GeometryValidator, validate_icon_elements, ValidationError
from .utils import (
    calculate_luminance,
    calculate_contrast_ratio,
    scale_value,
    clamp,
    interpolate_color,
    create_gradient_id,
    ensure_min_size,
    round_to_half
)

__all__ = [
    'IconBase',
    'SimpleShapeIcon',
    'SVGBuilder',
    'GeometryValidator',
    'validate_icon_elements',
    'ValidationError',
    'calculate_luminance',
    'calculate_contrast_ratio',
    'scale_value',
    'clamp',
    'interpolate_color',
    'create_gradient_id',
    'ensure_min_size',
    'round_to_half'
]
