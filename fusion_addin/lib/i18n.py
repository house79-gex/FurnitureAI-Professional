"""
Sistema di internazionalizzazione (i18n) per FurnitureAI
Supporta caricamento automatico della lingua, fallback e gestione placeholder
"""

import json
import os
import re

class I18n:
    """Gestore multilingua con auto-detect e fallback"""
    
    def __init__(self, app=None, default_locale='en_US'):
        """
        Inizializza il sistema i18n
        
        Args:
            app: Istanza di adsk.core.Application (opzionale, per auto-detect)
            default_locale: Lingua di fallback (default: en_US)
        """
        self.default_locale = default_locale
        self.current_locale = default_locale
        self.translations = {}
        self.locales_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'locales'
        )
        
        # Auto-detect della lingua da Fusion 360
        if app:
            try:
                fusion_locale = app.preferences.generalPreferences.userLanguage
                self.current_locale = self._convert_fusion_locale(fusion_locale)
            except:
                pass
        
        # Carica le traduzioni
        self._load_translations()
    
    def _convert_fusion_locale(self, fusion_locale):
        """
        Converte il codice locale di Fusion in formato standard
        
        Args:
            fusion_locale: Codice lingua di Fusion (es. 'it-IT')
        
        Returns:
            str: Codice locale normalizzato (es. 'it_IT')
        """
        return fusion_locale.replace('-', '_')
    
    def _load_translations(self):
        """Carica i file di traduzione JSON"""
        # Carica la lingua corrente
        current_file = os.path.join(self.locales_path, f'{self.current_locale}.json')
        if os.path.exists(current_file):
            with open(current_file, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        
        # Carica il fallback se diverso
        if self.current_locale != self.default_locale:
            fallback_file = os.path.join(self.locales_path, f'{self.default_locale}.json')
            if os.path.exists(fallback_file):
                with open(fallback_file, 'r', encoding='utf-8') as f:
                    fallback_data = json.load(f)
                    # Merge con fallback (non sovrascrive le chiavi esistenti)
                    for key, value in fallback_data.items():
                        if key not in self.translations:
                            self.translations[key] = value
    
    def t(self, key, **kwargs):
        """
        Ottieni una traduzione con supporto placeholder
        
        Args:
            key: Chiave di traduzione (es. 'wizard.title')
            **kwargs: Variabili per i placeholder (es. width=800)
        
        Returns:
            str: Stringa tradotta con placeholder sostituiti
        """
        # Naviga la struttura ad albero usando la notazione punto
        keys = key.split('.')
        value = self.translations
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # Fallback: ritorna la chiave stessa
                return key
        
        # Sostituisci i placeholder {variable}
        if isinstance(value, str) and kwargs:
            for var_name, var_value in kwargs.items():
                placeholder = '{' + var_name + '}'
                value = value.replace(placeholder, str(var_value))
        
        return value
    
    def set_locale(self, locale):
        """
        Cambia la lingua corrente
        
        Args:
            locale: Nuovo codice locale (es. 'it_IT')
        """
        self.current_locale = locale
        self._load_translations()
    
    def get_available_locales(self):
        """
        Ottieni l'elenco delle lingue disponibili
        
        Returns:
            list: Lista di codici locale disponibili
        """
        locales = []
        if os.path.exists(self.locales_path):
            for filename in os.listdir(self.locales_path):
                if filename.endswith('.json'):
                    locales.append(filename[:-5])
        return locales

# Istanza singleton globale
_i18n_instance = None

def init_i18n(app=None, default_locale='en_US'):
    """
    Inizializza il sistema i18n globale
    
    Args:
        app: Istanza di adsk.core.Application
        default_locale: Lingua di fallback
    
    Returns:
        I18n: Istanza del gestore i18n
    """
    global _i18n_instance
    _i18n_instance = I18n(app, default_locale)
    return _i18n_instance

def t(key, **kwargs):
    """
    Funzione di convenienza per traduzioni
    
    Args:
        key: Chiave di traduzione
        **kwargs: Variabili placeholder
    
    Returns:
        str: Stringa tradotta
    """
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18n()
    return _i18n_instance.t(key, **kwargs)

def get_i18n():
    """Ottieni l'istanza globale i18n"""
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = I18n()
    return _i18n_instance
