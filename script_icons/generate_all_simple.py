"""
Simple Icon Generation Script
Generates all FurnitureAI icons with clear progress and error reporting
"""

import os
import sys
import time
from pathlib import Path

# Add script_icons to path
sys.path.insert(0, str(Path(__file__).parent))

from core.icon_base import IconGenerationSystem
from core.utils import create_preview_html


def print_header():
    """Print welcome header"""
    print()
    print("=" * 60)
    print("🎨 FurnitureAI Icon Generator")
    print("=" * 60)
    print()


def print_footer(results, elapsed_time):
    """Print summary footer"""
    print()
    print("=" * 60)
    print("✅ Generation Complete!")
    print("=" * 60)
    
    # Count files
    total_icons = len(results['icons'])
    svg_files = sum(len(icon['sizes']) for icon in results['icons'].values())
    png_files = sum(sum(1 for s in icon['sizes'].values() if s) for icon in results['icons'].values())
    
    print(f"Total icons:  {total_icons}")
    print(f"SVG files:    {svg_files}")
    print(f"PNG files:    {png_files}")
    print(f"Time:         {elapsed_time:.1f} seconds")
    print(f"Output:       output/svg/ and output/png/")
    print("=" * 60)
    print()
    
    # Show file structure
    print("📁 Output Structure:")
    print("   output/")
    print("   ├── svg/")
    print("   │   ├── FAI_LayoutIA_16.svg")
    print("   │   ├── FAI_LayoutIA_32.svg")
    print("   │   ├── FAI_LayoutIA_64.svg")
    print("   │   ├── FAI_LayoutIA_128.svg")
    print("   │   └── ... (all icons × 4 sizes)")
    print("   ├── png/")
    print("   │   ├── FAI_LayoutIA_16.png")
    print("   │   ├── FAI_LayoutIA_32.png")
    print("   │   ├── FAI_LayoutIA_64.png")
    print("   │   ├── FAI_LayoutIA_128.png")
    print("   │   └── ... (all icons × 4 sizes)")
    print("   ├── preview.html")
    print("   └── metadata.json")
    print()


def create_output_directories():
    """Create output directories with flat structure"""
    output_dir = Path('output')
    
    directories = [
        output_dir,
        output_dir / 'svg',
        output_dir / 'png',  # Flat PNG directory
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    return output_dir


def main():
    """Main generation function"""
    # Print header
    print_header()
    
    # Create output directories
    print("📂 Creating output directories...")
    output_dir = create_output_directories()
    print(f"   ✓ Created: {output_dir}/svg/")
    print(f"   ✓ Created: {output_dir}/png/")
    print()
    
    # Initialize generation system
    print("🔧 Initializing icon generation system...")
    try:
        system = IconGenerationSystem()
        print(f"   ✓ Loaded {len(system.generators)} panel generators")
        print()
    except Exception as e:
        print(f"   ✗ Error initializing system: {e}")
        sys.exit(1)
    
    # Generate all icons
    print("🎨 Generating icons...")
    print()
    
    start_time = time.time()
    
    try:
        results = system.generate_all()
    except Exception as e:
        print(f"\n✗ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    elapsed_time = time.time() - start_time
    
    # Save metadata
    print()
    print("💾 Saving metadata...")
    try:
        import json
        metadata_path = output_dir / 'metadata.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        print(f"   ✓ Saved: {metadata_path}")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not save metadata: {e}")
    
    # Generate preview HTML
    print()
    print("🌐 Generating preview HTML...")
    try:
        preview_path = output_dir / 'preview.html'
        create_preview_html(results, preview_path)
        print(f"   ✓ Saved: {preview_path}")
    except Exception as e:
        print(f"   ⚠️  Warning: Could not generate preview: {e}")
    
    # Print summary
    print_footer(results, elapsed_time)
    
    # Final instructions
    print("📌 Next Steps:")
    print("   1. Open output/preview.html in your browser to view all icons")
    print("   2. Icons are in output/svg/ and output/png/")
    print("   3. All sizes use naming: IconName_SIZE.svg/png")
    print()
    
    # Check for errors
    failed_icons = [name for name, data in results['icons'].items() 
                   if not all(data['sizes'].values())]
    
    if failed_icons:
        print("⚠️  Some icons had errors:")
        for icon_name in failed_icons[:5]:  # Show first 5
            icon_data = results['icons'][icon_name]
            failed_sizes = [str(size) for size, success in icon_data['sizes'].items() if not success]
            print(f"   • {icon_name}: Failed sizes {', '.join(failed_sizes)}")
            if icon_data.get('errors'):
                for size, error in list(icon_data['errors'].items())[:1]:  # Show first error
                    print(f"     Error: {error}")
        
        if len(failed_icons) > 5:
            print(f"   ... and {len(failed_icons) - 5} more")
        print()
    
    print("=" * 60)
    print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
