"""
Gestore UI per FurnitureAI - Scheda Unica con Strumenti Fusion Integrati
"""

import adsk.core
import adsk.fusion
import traceback

class UIManager:
    """Gestore dell'interfaccia utente per FurnitureAI"""

    def __init__(self, logger, ui):
        self.logger = logger
        self.ui = ui
        self.app = adsk.core.Application.get()
        self.workspace = None
        self.main_tab = None
        self.panels = []
        self.command_defs = []
        self.handlers = []

    def create_ui(self):
        """Crea la scheda unica 'Furniture AI'"""
        try:
            workspaces = self.ui.workspaces
            # Si aggancia al workspace attivo (Progettazione)
            self.workspace = self.ui.activeWorkspace or workspaces.itemById('FusionDesignWorkspace')

            if not self.workspace:
                self.logger.error("Impossibile trovare il workspace attivo")
                return

            # 1. Pulizia preventiva
            existing_tab = self.workspace.toolbarTabs.itemById('FurnitureAI_MainTab')
            if existing_tab:
                existing_tab.deleteMe()

            # 2. Crea l'UNICA scheda principale
            self.main_tab = self.workspace.toolbarTabs.add('FurnitureAI_MainTab', 'Furniture AI')
            
            # 3. Importa il pannello CREA originale di Fusion
            design_tab = self.workspace.toolbarTabs.itemById('SolidTab')
            if design_tab:
                create_panel = design_tab.toolbarPanels.itemById('SolidCreatePanel')
                if create_panel:
                    self.main_tab.toolbarPanels.add(create_panel)

            # 4. Crea i tuoi pannelli personalizzati
            self._create_custom_panels()

            # 5. Crea e aggiungi i tuoi comandi
            self._create_commands()
            self._populate_panels()

            # Attiva la scheda
            self.main_tab.activate()
            self.logger.info("✅ Scheda 'Furniture AI' caricata con successo")

        except Exception as e:
            self.logger.error(f"❌ Errore create_ui: {str(e)}")

    def _create_custom_panels(self):
        """Crea i pannelli specifici per i tuoi strumenti"""
        try:
            # Pannello 1: IA & Progettazione
            p_ia = self.main_tab.toolbarPanels.add('FurnitureAI_IAPanel', 'IA & PROGETTAZIONE')
            self.panels.append(('FurnitureAI_IAPanel', p_ia))

            # Pannello 2: Produzione
            p_prod = self.main_tab.toolbarPanels.add('FurnitureAI_ProdPanel', 'PRODUZIONE')
            self.panels.append(('FurnitureAI_ProdPanel', p_prod))
            
            # Pannello 3: Impostazioni
            p_set = self.main_tab.toolbarPanels.add('FurnitureAI_SettingsPanel', 'IMPOSTAZIONI')
            self.panels.append(('FurnitureAI_SettingsPanel', p_set))

        except Exception as e:
            self.logger.error(f"Errore creazione pannelli: {str(e)}")

    def _create_commands(self):
        """Definisce i comandi per ogni pannello"""
        try:
            cmd_defs = self.ui.commandDefinitions
            
            # Mappa dei comandi: ID Pannello -> [ (ID, Nome, Descrizione) ]
            config = {
                'FurnitureAI_IAPanel': [
                    ('FAI_Wizard', 'Wizard Mobili', 'Crea mobile assistito'),
                    ('FAI_Gen', 'Generatore IA', 'AI Design'),
                ],
                'FurnitureAI_ProdPanel': [
                    ('FAI_Cut', 'Lista Taglio', 'Genera nesting'),
                    ('FAI_Label', 'Etichette', 'Stampa etichette'),
                ],
                'FurnitureAI_SettingsPanel': [
                    ('FAI_Config', 'Configura', 'Impostazioni globali'),
                ]
            }

            for p_id, cmds in config.items():
                for c_id, name, desc in cmds:
                    # Rimuovi se esiste già
                    existing = cmd_defs.itemById(c_id)
                    if existing: existing.deleteMe()
                    
                    # Crea nuova definizione
                    btn = cmd_defs.addButtonDefinition(c_id, name, desc)
                    
                    # Collega l'handler per il click
                    handler = CommandCreatedHandler(name, self.logger)
                    btn.commandCreated.add(handler)
                    self.handlers.append(handler)
                    
                    # Salva il riferimento per popolare i pannelli
                    self.command_defs.append((p_id, btn))

        except Exception as e:
            self.logger.error(f"Errore creazione comandi: {str(e)}")

    def _populate_panels(self):
        """Distribuisce i comandi nei rispettivi pannelli"""
        try:
            for panel_target_id, cmd_def in self.command_defs:
                for panel_id, panel_obj in self.panels:
                    if panel_id == panel_target_id:
                        panel_obj.controls.addCommand(cmd_def)
        except Exception as e:
            self.logger.error(f"Errore popolazione: {str(e)}")

    def cleanup(self):
        """Rimuove tutto all'arresto dell'Add-in"""
        try:
            if self.main_tab and self.main_tab.isValid:
                self.main_tab.deleteMe()
            
            for _, cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()
            self.logger.info("✅ UI FurnitureAI rimossa")
        except:
            pass

# --- EVENT HANDLERS ---

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        try:
            cmd = args.command
            on_execute = CommandExecuteHandler(self.command_name, self.logger)
            cmd.execute.add(on_execute)
            # Trucco per mantenere l'handler in memoria
            args.command.setPythonOwner(on_execute) 
        except:
            pass

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        ui.messageBox(f'Azione: {self.command_name}\nStatus: In sviluppo', 'FurnitureAI')
