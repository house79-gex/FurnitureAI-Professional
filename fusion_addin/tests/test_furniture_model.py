"""
Test per furniture_types e furniture_model
Test semplici senza dipendenze Fusion 360
"""

import sys
import os

# Aggiungi path per import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib', 'core'))

def test_furniture_types():
    """Test modulo furniture_types"""
    from furniture_types import (
        FURNITURE_TYPES,
        FURNITURE_CATEGORIES,
        get_types_by_category,
        get_all_categories,
        get_type_info
    )
    
    print("Test furniture_types:")
    
    # Test 1: Verifica numero tipi
    assert len(FURNITURE_TYPES) == 15, f"Expected 15 types, got {len(FURNITURE_TYPES)}"
    print("  ✅ 15 tipi di mobile definiti")
    
    # Test 2: Verifica numero categorie
    assert len(FURNITURE_CATEGORIES) == 6, f"Expected 6 categories, got {len(FURNITURE_CATEGORIES)}"
    print("  ✅ 6 categorie definite")
    
    # Test 3: Verifica struttura base_cucina
    base_cucina = FURNITURE_TYPES['base_cucina']
    assert 'nome' in base_cucina
    assert 'dimensioni_default' in base_cucina
    assert 'dimensioni_min' in base_cucina
    assert 'dimensioni_max' in base_cucina
    print("  ✅ Struttura base_cucina valida")
    
    # Test 4: Verifica get_types_by_category
    cucina_types = get_types_by_category('cucina')
    assert len(cucina_types) == 3, f"Expected 3 kitchen types, got {len(cucina_types)}"
    print(f"  ✅ get_types_by_category('cucina') = {len(cucina_types)} tipi")
    
    # Test 5: Verifica get_all_categories
    categories = get_all_categories()
    assert len(categories) == 6
    # Verifica ordinamento
    assert categories[0][0] == 'cucina'  # Prima categoria
    print("  ✅ get_all_categories() ordinato correttamente")
    
    # Test 6: Verifica get_type_info
    info = get_type_info('base_cucina')
    assert info is not None
    assert info['nome'] == 'Base Cucina'
    print("  ✅ get_type_info() funziona")
    
    print("✅ Tutti i test furniture_types passati!\n")


def test_furniture_model():
    """Test modulo furniture_model (con mock di furniture_types)"""
    # Importa e configura manualmente il modulo per evitare relative imports
    import importlib.util
    
    # Carica furniture_types
    spec_types = importlib.util.spec_from_file_location(
        "furniture_types",
        os.path.join(os.path.dirname(__file__), '..', 'lib', 'core', 'furniture_types.py')
    )
    furniture_types = importlib.util.module_from_spec(spec_types)
    spec_types.loader.exec_module(furniture_types)
    
    # Carica furniture_model modificando gli import
    spec_model = importlib.util.spec_from_file_location(
        "furniture_model",
        os.path.join(os.path.dirname(__file__), '..', 'lib', 'core', 'furniture_model.py')
    )
    furniture_model = importlib.util.module_from_spec(spec_model)
    
    # Inject furniture_types nel namespace di furniture_model
    sys.modules['fusion_addin.lib.core.furniture_types'] = furniture_types
    
    # Ora carica furniture_model
    spec_model.loader.exec_module(furniture_model)
    
    print("Test furniture_model:")
    
    # Test 1: Creazione FurniturePiece base
    piece = furniture_model.FurniturePiece(tipo='base_cucina')
    assert piece.tipo == 'base_cucina'
    assert piece.dimensioni['larghezza'] == 600
    print("  ✅ FurniturePiece creato correttamente")
    
    # Test 2: Validazione
    is_valid, errors = piece.validate()
    assert is_valid, f"Validation failed: {errors}"
    print("  ✅ Validazione OK")
    
    # Test 3: apply_defaults
    piece.apply_defaults('base_cucina')
    assert hasattr(piece, 'zoccolo')
    assert piece.zoccolo['presente'] == True
    print("  ✅ apply_defaults() funziona")
    
    # Test 4: suggest_hardware
    hardware = piece.suggest_hardware()
    assert 'cerniere' in hardware
    assert 'guide_cassetti' in hardware
    assert 'piedini' in hardware
    print("  ✅ suggest_hardware() funziona")
    
    # Test 5: suggest_drilling
    drilling = piece.suggest_drilling()
    assert 'system32_consigliato' in drilling
    assert 'motivo' in drilling
    print("  ✅ suggest_drilling() funziona")
    
    # Test 6: calculate_door_dimensions
    door_dims = piece.calculate_door_dimensions('copertura_totale', gioco=2)
    assert door_dims is not None
    assert 'larghezza' in door_dims
    assert 'altezza' in door_dims
    print(f"  ✅ calculate_door_dimensions() = {door_dims['larghezza']}x{door_dims['altezza']} mm")
    
    # Test 7: Serializzazione
    data_dict = piece.to_dict()
    assert 'tipo' in data_dict
    assert 'dimensioni' in data_dict
    assert 'elementi' in data_dict
    print("  ✅ to_dict() funziona")
    
    # Test 8: Deserializzazione
    piece2 = furniture_model.FurniturePiece.from_dict(data_dict)
    assert piece2.tipo == piece.tipo
    assert piece2.nome == piece.nome
    print("  ✅ from_dict() funziona")
    
    # Test 9: get_default_for_type
    defaults = furniture_model.FurniturePiece.get_default_for_type('pensile_cucina')
    assert defaults is not None
    assert 'dimensioni' in defaults
    print("  ✅ get_default_for_type() funziona")
    
    print("✅ Tutti i test furniture_model passati!\n")


if __name__ == '__main__':
    try:
        test_furniture_types()
        test_furniture_model()
        print("=" * 60)
        print("🎉 TUTTI I TEST PASSATI!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n❌ TEST FALLITO: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
