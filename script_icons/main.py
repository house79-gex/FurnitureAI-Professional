"""
Main entry point for FurnitureAI Icon Generation System
Generates all 47 icons in 4 resolutions (16, 32, 64, 128)
"""

import os
import sys
import time
import json
from typing import Dict, List
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import RESOLUTIONS, ICON_PANELS, OUTPUT_DIR, SVG_DIR, PNG_DIR
from generators import ICON_REGISTRY


def ensure_output_dirs():
    """Create output directories if they don't exist"""
    dirs = [OUTPUT_DIR, SVG_DIR]
    
    for size in RESOLUTIONS:
        dirs.append(f'{PNG_DIR}/{size}')
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")


def generate_icon(icon_name: str, icon_class, output_dir: str) -> Dict:
    """
    Generate a single icon at all resolutions
    
    Args:
        icon_name: Name of the icon
        icon_class: Icon class to instantiate
        output_dir: Base output directory
        
    Returns:
        Dictionary with generation results
    """
    result = {
        'name': icon_name,
        'status': 'success',
        'files': [],
        'errors': []
    }
    
    try:
        # Create icon instance
        icon = icon_class()
        
        # Generate SVG for each resolution
        for size in RESOLUTIONS:
            try:
                # Generate SVG
                builder = icon.generate(size)
                
                # Validate
                is_valid, errors = builder.validate()
                if not is_valid:
                    result['errors'].extend([f"Size {size}: {err}" for err in errors])
                    print(f"  ⚠️  Validation warnings for {icon_name} at {size}px")
                
                # Save SVG
                svg_filename = f"{SVG_DIR}/{icon_name}_{size}.svg"
                builder.save(svg_filename)
                result['files'].append(svg_filename)
                
                print(f"  ✓ Generated {icon_name} at {size}×{size}px")
                
            except Exception as e:
                error_msg = f"Size {size}: {str(e)}"
                result['errors'].append(error_msg)
                result['status'] = 'partial'
                print(f"  ✗ Error generating {icon_name} at {size}px: {e}")
        
    except Exception as e:
        result['status'] = 'failed'
        result['errors'].append(f"Failed to instantiate icon: {str(e)}")
        print(f"  ✗ Failed to generate {icon_name}: {e}")
    
    return result


def generate_all_icons() -> Dict:
    """
    Generate all icons in the system
    
    Returns:
        Dictionary with generation statistics
    """
    print("\n" + "="*60)
    print("🎨 FurnitureAI Icon Generation System")
    print("="*60 + "\n")
    
    start_time = time.time()
    
    # Ensure output directories exist
    print("Creating output directories...")
    ensure_output_dirs()
    print()
    
    # Statistics
    stats = {
        'total_icons': 0,
        'successful': 0,
        'partial': 0,
        'failed': 0,
        'total_files': 0,
        'results': []
    }
    
    # Generate icons by panel
    for panel_key, panel_info in ICON_PANELS.items():
        print(f"\n📂 {panel_info['name']} Panel ({panel_info['count']} icons)")
        print("-" * 60)
        
        for icon_name in panel_info['icons']:
            stats['total_icons'] += 1
            
            # Check if icon is implemented
            if icon_name not in ICON_REGISTRY:
                print(f"  ⚠️  {icon_name} - Not yet implemented (stub needed)")
                stats['failed'] += 1
                continue
            
            # Generate icon
            icon_class = ICON_REGISTRY[icon_name]
            result = generate_icon(icon_name, icon_class, OUTPUT_DIR)
            
            # Update statistics
            if result['status'] == 'success':
                stats['successful'] += 1
                stats['total_files'] += len(result['files'])
            elif result['status'] == 'partial':
                stats['partial'] += 1
                stats['total_files'] += len(result['files'])
            else:
                stats['failed'] += 1
            
            stats['results'].append(result)
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Generation Summary")
    print("="*60)
    print(f"Total icons:          {stats['total_icons']}")
    print(f"Successfully generated: {stats['successful']} ✓")
    print(f"Partially generated:  {stats['partial']} ⚠️")
    print(f"Failed:               {stats['failed']} ✗")
    print(f"Total files created:  {stats['total_files']}")
    print(f"Generation time:      {elapsed_time:.2f} seconds")
    print("="*60 + "\n")
    
    # Save metadata
    metadata_file = f"{OUTPUT_DIR}/metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({
            'generation_time': time.strftime('%Y-%m-%d %H:%M:%S'),
            'elapsed_seconds': elapsed_time,
            'statistics': {
                'total_icons': stats['total_icons'],
                'successful': stats['successful'],
                'partial': stats['partial'],
                'failed': stats['failed'],
                'total_files': stats['total_files']
            },
            'results': stats['results']
        }, f, indent=2)
    
    print(f"✓ Metadata saved to {metadata_file}")
    
    return stats


def generate_preview_html():
    """Generate HTML preview of all icons"""
    html_content = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FurnitureAI Icons Preview</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        
        .panel {
            background: white;
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .panel-title {
            color: #0696D7;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #0696D7;
        }
        
        .icons-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .icon-card {
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            background: #fafafa;
        }
        
        .icon-name {
            font-weight: 600;
            margin-bottom: 10px;
            color: #333;
            font-size: 14px;
        }
        
        .icon-sizes {
            display: flex;
            gap: 10px;
            align-items: flex-end;
            padding: 10px;
            background: white;
            border-radius: 5px;
        }
        
        .icon-size {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }
        
        .icon-size img {
            border: 1px solid #ddd;
            border-radius: 3px;
            background: white;
        }
        
        .size-label {
            font-size: 10px;
            color: #666;
            font-weight: 500;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #0696D7;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: 700;
            color: #0696D7;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <header>
        <h1>🎨 FurnitureAI Professional Icons</h1>
        <p class="subtitle">Multi-Resolution Icon System - 47 Icons in 4 Resolutions</p>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">47</div>
                <div class="stat-label">Total Icons</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">4</div>
                <div class="stat-label">Resolutions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">188</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">9</div>
                <div class="stat-label">Panels</div>
            </div>
        </div>
    </header>
"""
    
    # Add panels
    for panel_key, panel_info in ICON_PANELS.items():
        html_content += f"""
    <div class="panel">
        <div class="panel-title">
            {panel_info['name']} ({panel_info['count']} icons)
        </div>
        <div class="icons-grid">
"""
        
        for icon_name in panel_info['icons']:
            if icon_name in ICON_REGISTRY:
                html_content += f"""
            <div class="icon-card">
                <div class="icon-name">{icon_name}</div>
                <div class="icon-sizes">
"""
                for size in RESOLUTIONS:
                    svg_path = f"svg/{icon_name}_{size}.svg"
                    html_content += f"""
                    <div class="icon-size">
                        <img src="{svg_path}" width="{size}" height="{size}" alt="{icon_name} {size}px">
                        <span class="size-label">{size}×{size}</span>
                    </div>
"""
                
                html_content += """
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    # Save HTML
    html_file = f"{OUTPUT_DIR}/preview.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Preview HTML saved to {html_file}")


def main():
    """Main entry point"""
    try:
        # Generate all icons
        stats = generate_all_icons()
        
        # Generate preview HTML
        print("\nGenerating preview HTML...")
        generate_preview_html()
        
        # Success message
        print("\n" + "="*60)
        print("✨ Icon generation complete!")
        print("="*60)
        print(f"\n📁 Output directory: {OUTPUT_DIR}/")
        print(f"🖼️  SVG files:        {SVG_DIR}/")
        print(f"📄 Metadata:         {OUTPUT_DIR}/metadata.json")
        print(f"🌐 Preview:          {OUTPUT_DIR}/preview.html")
        print("\nOpen preview.html in your browser to view all icons.")
        print("="*60 + "\n")
        
        # Exit code based on success
        if stats['failed'] == 0:
            return 0
        elif stats['successful'] > 0:
            return 1  # Partial success
        else:
            return 2  # Complete failure
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        return 130
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
