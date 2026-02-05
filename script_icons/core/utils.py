"""
Utility functions for icon generation
COMPLETE VERSION with all functions
"""

from pathlib import Path
from typing import Dict

def calculate_contrast_ratio(color1: str, color2: str) -> float:
    """
    Calculate WCAG contrast ratio between two colors
    
    Args:
        color1: First color (hex format like '#FFFFFF')
        color2: Second color (hex format like '#000000')
        
    Returns:
        Contrast ratio (1.0 to 21.0)
    """
    def hex_to_rgb(hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def relative_luminance(rgb):
        """Calculate relative luminance"""
        r, g, b = rgb
        
        def adjust(channel):
            if channel <= 0.03928:
                return channel / 12.92
            return ((channel + 0.055) / 1.055) ** 2.4
        
        r = adjust(r)
        g = adjust(g)
        b = adjust(b)
        
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    
    # Convert colors
    rgb1 = hex_to_rgb(color1)
    rgb2 = hex_to_rgb(color2)
    
    # Calculate luminance
    l1 = relative_luminance(rgb1)
    l2 = relative_luminance(rgb2)
    
    # Calculate contrast ratio
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def create_preview_html(results: Dict, output_path: Path):
    """
    Create HTML preview of all generated icons
    
    Args:
        results: Generation results dictionary
        output_path: Path to save HTML file
    """
    html = """<!DOCTYPE html>
<html lang="en">
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #0696D7 0%, #0566A7 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: #0696D7;
        }
        
        .stat-label {
            color: #6c757d;
            margin-top: 5px;
            font-size: 0.9em;
        }
        
        .controls {
            padding: 20px 40px;
            background: white;
            border-bottom: 2px solid #e9ecef;
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .size-selector {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        
        .size-btn {
            padding: 8px 16px;
            border: 2px solid #0696D7;
            background: white;
            color: #0696D7;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .size-btn:hover {
            background: #0696D7;
            color: white;
        }
        
        .size-btn.active {
            background: #0696D7;
            color: white;
        }
        
        .search-box {
            flex: 1;
            min-width: 250px;
        }
        
        .search-box input {
            width: 100%;
            padding: 10px 15px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            font-size: 1em;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #0696D7;
        }
        
        .panel {
            padding: 40px;
        }
        
        .panel-title {
            font-size: 1.8em;
            color: #0696D7;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #0696D7;
            font-weight: 700;
        }
        
        .icon-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .icon-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .icon-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-color: #0696D7;
        }
        
        .icon-preview {
            width: 100%;
            height: 128px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            border-radius: 8px;
            margin-bottom: 15px;
            position: relative;
        }
        
        .icon-preview img {
            max-width: 100%;
            max-height: 100%;
            transition: all 0.3s;
        }
        
        .icon-name {
            font-weight: 600;
            color: #495057;
            margin-bottom: 5px;
            font-size: 0.9em;
        }
        
        .icon-info {
            font-size: 0.8em;
            color: #6c757d;
        }
        
        .status-badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.75em;
            font-weight: 600;
            margin-top: 5px;
        }
        
        .status-success {
            background: #d4edda;
            color: #155724;
        }
        
        .status-partial {
            background: #fff3cd;
            color: #856404;
        }
        
        .status-error {
            background: #f8d7da;
            color: #721c24;
        }
        
        footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #6c757d;
            border-top: 2px solid #e9ecef;
        }
        
        @media (max-width: 768px) {
            .icon-grid {
                grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎨 FurnitureAI Icons</h1>
            <p>Professional Multi-Resolution Icon Set</p>
        </header>
        
        <div class="stats">
"""
    
    # Add statistics
    total_icons = len(results['icons'])
    successful = sum(1 for icon in results['icons'].values() if all(icon['sizes'].values()))
    total_files = sum(sum(1 for s in icon['sizes'].values() if s) for icon in results['icons'].values())
    
    html += f"""
            <div class="stat">
                <div class="stat-value">{total_icons}</div>
                <div class="stat-label">Total Icons</div>
            </div>
            <div class="stat">
                <div class="stat-value">{successful}</div>
                <div class="stat-label">Complete</div>
            </div>
            <div class="stat">
                <div class="stat-value">{total_files}</div>
                <div class="stat-label">Total Files</div>
            </div>
            <div class="stat">
                <div class="stat-value">4</div>
                <div class="stat-label">Resolutions</div>
            </div>
        </div>
        
        <div class="controls">
            <div class="size-selector">
                <span style="font-weight: 600; color: #495057;">Size:</span>
                <button class="size-btn active" data-size="128">128×128</button>
                <button class="size-btn" data-size="64">64×64</button>
                <button class="size-btn" data-size="32">32×32</button>
                <button class="size-btn" data-size="16">16×16</button>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="🔍 Search icons...">
            </div>
        </div>
"""
    
    # Group icons by panel
    for panel_name in results.get('panels', {}).keys():
        icons_in_panel = [(name, data) for name, data in results['icons'].items() 
                         if name in results['panels'][panel_name]['icons']]
        
        if not icons_in_panel:
            continue
            
        html += f"""
        <div class="panel">
            <h2 class="panel-title">{panel_name}</h2>
            <div class="icon-grid">
"""
        
        for icon_name, icon_data in icons_in_panel:
            # Determine status
            sizes_ok = sum(1 for s in icon_data['sizes'].values() if s)
            if sizes_ok == 4:
                status = 'success'
                status_text = 'Complete'
            elif sizes_ok > 0:
                status = 'partial'
                status_text = f'{sizes_ok}/4 sizes'
            else:
                status = 'error'
                status_text = 'Failed'
            
            html += f"""
                <div class="icon-card" data-name="{icon_name}">
                    <div class="icon-preview">
"""
            
            # Add images for all available sizes
            for size in [16, 32, 64, 128]:
                if icon_data['sizes'].get(size):
                    display = 'block' if size == 128 else 'none'
                    html += f'                        <img src="svg/{icon_name}_{size}.svg" data-size="{size}" style="display: {display};" alt="{icon_name} {size}px">\n'
            
            html += f"""
                    </div>
                    <div class="icon-name">{icon_name}</div>
                    <div class="icon-info">
                        <span class="status-badge status-{status}">{status_text}</span>
                    </div>
                </div>
"""
        
        html += """
            </div>
        </div>
"""
    
    # Add footer and scripts
    html += """
        <footer>
            <p><strong>FurnitureAI Professional</strong> - Icon Generation System</p>
            <p style="margin-top: 10px; font-size: 0.9em;">
                Generated with ❤️ by GitHub Copilot
            </p>
        </footer>
    </div>
    
    <script>
        // Size selector
        const sizeButtons = document.querySelectorAll('.size-btn');
        const iconImages = document.querySelectorAll('.icon-preview img');
        
        sizeButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                sizeButtons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const selectedSize = btn.dataset.size;
                iconImages.forEach(img => {
                    img.style.display = img.dataset.size === selectedSize ? 'block' : 'none';
                });
            });
        });
        
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        const iconCards = document.querySelectorAll('.icon-card');
        
        searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase();
            
            iconCards.forEach(card => {
                const iconName = card.dataset.name.toLowerCase();
                if (iconName.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>
"""
    
    # Write HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"
