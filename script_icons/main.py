"""
Main entry point for icon generation
FIXED: Flat PNG output structure (all icons in one folder per format)
"""

import os
import sys
import time
from pathlib import Path

# Add script_icons to path
sys.path.insert(0, str(Path(__file__).parent))

from core.icon_base import IconGenerationSystem
from core.utils import create_preview_html

def create_output_directories():
    """
    Create output directory structure
    FIXED: Single flat PNG directory (no size subdirectories)
    """
    output_dir = Path('output')
    
    # Create main directories - FLAT STRUCTURE
    directories = [
        output_dir,
        output_dir / 'svg',
        output_dir / 'png',  # ← Single PNG directory for all sizes
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def main():
    """Main function"""
    print()
    print("=" * 60)
    print("🎨 FurnitureAI Icon Generation System")
    print("=" * 60)
    print()
    
    # Create directories
    print("Creating output directories...")
    create_output_directories()
    print()
    
    # Initialize generation system
    system = IconGenerationSystem()
    
    # Generate all icons
    start_time = time.time()
    results = system.generate_all()
    elapsed_time = time.time() - start_time
    
    # Print summary
    print()
    print("=" * 60)
    print("📊 Generation Summary")
    print("=" * 60)
    
    total_icons = len(results['icons'])
    successful = sum(1 for icon in results['icons'].values() 
                    if all(icon['sizes'].values()))
    partial = sum(1 for icon in results['icons'].values() 
                 if any(icon['sizes'].values()) and not all(icon['sizes'].values()))
    failed = total_icons - successful - partial
    
    # Count total files
    total_files = sum(
        sum(1 for success in icon['sizes'].values() if success)
        for icon in results['icons'].values()
    )
    
    print(f"Total icons:          {total_icons}")
    print(f"Successfully generated: {successful} ✓")
    if partial > 0:
        print(f"Partially generated:  {partial} ⚠️")
    if failed > 0:
        print(f"Failed:               {failed} ✗")
    print(f"Total files created:  {total_files}")
    print(f"Generation time:      {elapsed_time:.2f} seconds")
    print("=" * 60)
    print()
    
    # Save metadata
    import json
    metadata_path = Path('output') / 'metadata.json'
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Metadata saved to {metadata_path}")
    print()
    
    # Generate preview HTML
    print("Generating preview HTML...")
    preview_path = Path('output') / 'preview.html'
    create_preview_html(results, preview_path)
    print(f"✓ Preview HTML saved to {preview_path}")
    print()
    
    print("=" * 60)
    print("✨ Icon generation complete!")
    print("=" * 60)
    print()
    print(f"📁 Output directory: output/")
    print(f"🖼️  SVG files:        output/svg/ (all sizes in one folder)")
    print(f"🖼️  PNG files:        output/png/ (all sizes in one folder)")
    print(f"📄 Metadata:         output/metadata.json")
    print(f"🌐 Preview:          output/preview.html")
    print()
    print("All icon files use naming: IconName_SIZE.svg/png")
    print("Example: FAI_LayoutIA_16.png, FAI_LayoutIA_32.png, etc.")
    print()
    print("Open preview.html in your browser to view all icons.")
    print("=" * 60)
    print()

if __name__ == '__main__':
    main()
