"""
Sistema di logging strutturato per FurnitureAI
Log formattati in italiano con emoji e livelli di severità
"""

import logging
import os
from datetime import datetime

class ColoredFormatter(logging.Formatter):
    """Formatter con emoji e colori per i log"""
    
    # Emoji per ogni livello
    EMOJI_MAP = {
        'DEBUG': 'ℹ️',
        'INFO': '✅',
        'WARNING': '⚠️',
        'ERROR': '❌',
        'CRITICAL': '🔥'
    }
    
    def format(self, record):
        """Formatta il record di log con emoji"""
        emoji = self.EMOJI_MAP.get(record.levelname, 'ℹ️')
        record.emoji = emoji
        return super().format(record)

def setup_logger(name='FurnitureAI', level=logging.INFO):
    """
    Configura un logger con formato strutturato in italiano
    
    Args:
        name: Nome del logger
        level: Livello di log minimo
    
    Returns:
        logging.Logger: Logger configurato
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Evita duplicazione degli handler
    if logger.handlers:
        return logger
    
    # Handler per console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # Formato: [EMOJI] TIMESTAMP - LIVELLO - Messaggio
    formatter = ColoredFormatter(
        '%(emoji)s %(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # Handler per file (opzionale, se la directory logs esiste)
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    if os.path.exists(logs_dir):
        log_file = os.path.join(logs_dir, f'furnitureai_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

class LogContext:
    """Context manager per logging di operazioni con timing"""
    
    def __init__(self, logger, operation_name):
        """
        Inizializza il contesto di logging
        
        Args:
            logger: Logger da utilizzare
            operation_name: Nome dell'operazione
        """
        self.logger = logger
        self.operation_name = operation_name
        self.start_time = None
    
    def __enter__(self):
        """Inizio operazione"""
        self.start_time = datetime.now()
        self.logger.info(f"🔄 Inizio operazione: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fine operazione con timing"""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(f"✅ Completato: {self.operation_name} ({elapsed:.2f}s)")
        else:
            self.logger.error(f"❌ Errore in {self.operation_name}: {exc_val} ({elapsed:.2f}s)")
        
        return False  # Non sopprime le eccezioni
