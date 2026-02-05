"""
Windows-compatible SVG to PNG converter
Uses svglib + reportlab instead of cairosvg (which requires Cairo DLLs)
"""

import os
import sys
from pathlib import Path
from typing import Optional

def convert_svg_to_png(svg_path: str, png_path: str, width: int = None, height: int = None) -> bool:
    """
    Convert SVG to PNG using svglib + reportlab (Windows-compatible)
    
    Args:
        svg_path: Path to input SVG file
        png_path: Path to output PNG file
        width: Optional output width (not used with svglib, uses SVG native size)
        height: Optional output height (not used with svglib, uses SVG native size)
        
    Returns:
        True if conversion succeeded, False otherwise
    """
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        
        # Convert SVG to ReportLab Drawing
        drawing = svg2rlg(svg_path)
        
        if drawing is None:
            print(f"Error: Could not parse SVG file: {svg_path}")
            return False
        
        # Render to PNG
        renderPM.drawToFile(drawing, png_path, fmt='PNG')
        
        return True
        
    except ImportError as e:
        print(f"Error: Required libraries not installed: {e}")
        print("Install with: pip install svglib reportlab")
        return False
    except Exception as e:
        print(f"Error converting {svg_path} to PNG: {e}")
        return False


def convert_directory(svg_dir: str, png_dir: str, verbose: bool = True) -> tuple[int, int]:
    """
    Convert all SVG files in a directory to PNG
    
    Args:
        svg_dir: Directory containing SVG files
        png_dir: Directory for output PNG files
        verbose: Print progress messages
        
    Returns:
        Tuple of (successful_count, failed_count)
    """
    svg_dir = Path(svg_dir)
    png_dir = Path(png_dir)
    
    # Create output directory
    png_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all SVG files
    svg_files = list(svg_dir.glob("*.svg"))
    
    if verbose:
        print(f"\nConverting {len(svg_files)} SVG files to PNG...")
        print("-" * 60)
    
    successful = 0
    failed = 0
    
    for svg_file in svg_files:
        # Create PNG filename (same name, different extension)
        png_file = png_dir / f"{svg_file.stem}.png"
        
        if convert_svg_to_png(str(svg_file), str(png_file)):
            successful += 1
            if verbose:
                print(f"  ✓ {svg_file.name} → {png_file.name}")
        else:
            failed += 1
            if verbose:
                print(f"  ✗ {svg_file.name} FAILED")
    
    if verbose:
        print("-" * 60)
        print(f"Conversion complete: {successful} successful, {failed} failed")
    
    return successful, failed


def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert SVG files to PNG (Windows-compatible)"
    )
    parser.add_argument(
        'svg_path',
        help="Path to SVG file or directory containing SVG files"
    )
    parser.add_argument(
        'png_path',
        help="Path to output PNG file or directory"
    )
    parser.add_argument(
        '--width',
        type=int,
        help="Output width (optional, uses SVG native size if not specified)"
    )
    parser.add_argument(
        '--height',
        type=int,
        help="Output height (optional, uses SVG native size if not specified)"
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help="Suppress progress messages"
    )
    
    args = parser.parse_args()
    
    svg_path = Path(args.svg_path)
    png_path = Path(args.png_path)
    
    if svg_path.is_dir():
        # Convert entire directory
        successful, failed = convert_directory(
            str(svg_path),
            str(png_path),
            verbose=not args.quiet
        )
        sys.exit(0 if failed == 0 else 1)
    else:
        # Convert single file
        success = convert_svg_to_png(
            str(svg_path),
            str(png_path),
            width=args.width,
            height=args.height
        )
        if not args.quiet:
            if success:
                print(f"✓ Converted {svg_path.name} to {png_path.name}")
            else:
                print(f"✗ Failed to convert {svg_path.name}")
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
