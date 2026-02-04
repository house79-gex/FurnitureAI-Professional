"""
Script di setup repository per sviluppo FurnitureAI
Verifica struttura, dipendenze, e configurazione
"""

import os
import sys
import json

def check_structure():
    """Verifica struttura directory"""
    print("📁 Verificando struttura directory...")
    
    required_dirs = [
        'lib/core',
        'lib/joinery',
        'lib/hardware',
        'lib/doors',
        'lib/materials',
        'lib/ai',
        'lib/commands',
        'locales',
        'data',
        'docs',
        'scripts',
        'tests'
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            missing.append(dir_path)
    
    if missing:
        print(f"❌ Directory mancanti: {', '.join(missing)}")
        return False
    
    print("✅ Struttura directory OK")
    return True

def check_files():
    """Verifica file essenziali"""
    print("\n📄 Verificando file essenziali...")
    
    required_files = [
        'FurnitureAI.py',
        'FurnitureAI.manifest',
        'README.md',
        'data/config_default.json',
        'data/hardware_catalog.json',
        'locales/it_IT.json',
        'locales/en_US.json'
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print(f"❌ File mancanti: {', '.join(missing)}")
        return False
    
    print("✅ File essenziali OK")
    return True

def check_config():
    """Verifica configurazione"""
    print("\n⚙️  Verificando configurazione...")
    
    try:
        with open('data/config_default.json', 'r') as f:
            config = json.load(f)
        
        required_keys = ['ai', 'geometry', 'units']
        for key in required_keys:
            if key not in config:
                print(f"❌ Chiave mancante in config: {key}")
                return False
        
        print("✅ Configurazione OK")
        return True
    except Exception as e:
        print(f"❌ Errore lettura config: {e}")
        return False

def check_locales():
    """Verifica localizzazioni"""
    print("\n🌍 Verificando localizzazioni...")
    
    locales = ['it_IT', 'en_US']
    for locale in locales:
        file_path = f'locales/{locale}.json'
        if not os.path.exists(file_path):
            print(f"❌ Locale mancante: {locale}")
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'wizard' not in data or 'common' not in data:
                print(f"❌ Struttura locale incompleta: {locale}")
                return False
        except Exception as e:
            print(f"❌ Errore parsing {locale}: {e}")
            return False
    
    print("✅ Localizzazioni OK")
    return True

def main():
    """Main setup check"""
    print("=" * 60)
    print("FurnitureAI Professional v3.0 - Setup Verification")
    print("=" * 60)
    print()
    
    # Change to addon directory
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    checks = [
        check_structure(),
        check_files(),
        check_config(),
        check_locales()
    ]
    
    print()
    print("=" * 60)
    
    if all(checks):
        print("✅ Setup verification PASSED")
        print()
        print("Repository pronto per:")
        print("  • Sviluppo: Apri in VS Code/PyCharm")
        print("  • Testing: python -m unittest discover tests")
        print("  • Installazione: Esegui scripts/install.sh o install.bat")
        print()
        return 0
    else:
        print("❌ Setup verification FAILED")
        print()
        print("Risolvi gli errori sopra elencati.")
        print()
        return 1

if __name__ == '__main__':
    sys.exit(main())
