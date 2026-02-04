"""
Analizzatore foto materiali con LLaVA
Skeleton per estrazione automatica caratteristiche materiale da foto
"""

from ..ai.vision_client import VisionClient

class PhotoAnalyzer:
    """Analizza foto materiali con AI vision"""
    
    def __init__(self):
        """Inizializza l'analizzatore"""
        self.vision_client = VisionClient()
    
    def analyze_material_photo(self, photo_path):
        """
        Analizza foto materiale
        
        Args:
            photo_path: Path foto
        
        Returns:
            dict: Caratteristiche estratte
        """
        result = self.vision_client.extract_material_info(photo_path)
        return result
