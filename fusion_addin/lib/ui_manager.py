"""
Gestore UI per FurnitureAI - Versione ad attivazione garantita
"""
import adsk.core
import adsk.fusion
import traceback

class UIManager:
    def __init__(self, logger, ui):
        self.logger = logger
        self.ui = ui
        self.app = adsk.core.Application.get()
        self.main_tab = None
        self.handlers = []
        self.command_defs = []

    def create_ui(self):
        try:
            # 1. Trova il workspace corretto (solido)
            # Proviamo prima l'ID standard, poi quello attivo
            ws = self.ui.workspaces.itemById('FusionDesignWorkspace')
            if not ws:
                ws = self.ui.activeWorkspace
            
            if not ws:
                self.logger.error("Nessun workspace trovato.")
                return

            # 2. Pulizia totale (rimuoviamo tab se esiste per ID o per Nome)
            all_tabs = ws.toolbarTabs
            for existing_tab in all_tabs:
                if existing_tab.id == 'FurnitureAI_MainTab' or existing_tab.name == 'Furniture AI':
                    existing_tab.deleteMe()

            # 3. Creazione Tab
            self.main_tab = all_tabs.add('FurnitureAI_MainTab', 'Furniture AI')
            
            # 4. Inserimento Pannello CREA (metodo infallibile)
            # Cerchiamo il pannello 'Crea' ovunque nella barra Solid
            solid_tab = all_tabs.itemById('SolidTab')
            if solid_tab:
                # Proviamo a clonare il pannello 'Crea' (SolidCreatePanel)
                try:
                    target_p = solid_tab.toolbarPanels.itemById('SolidCreatePanel')
                    if target_p:
                        self.main_tab.toolbarPanels.add(target_p)
                except: pass

            # 5. Creazione Pannello Custom 'IA & WIZARD'
            p_ia = self.main_tab.toolbarPanels.add('FAI_IAPanel', 'IA & WIZARD')
            
            # 6. Creazione Comando Wizard
            cmd_defs = self.ui.commandDefinitions
            c_id = 'FAI_Wizard_Btn'
            existing_cmd = cmd_defs.itemById(c_id)
            if existing_cmd: existing_cmd.deleteMe()
            
            btn_wizard = cmd_defs.addButtonDefinition(c_id, 'Wizard Mobili', 'Avvia wizard')
            
            # Handler
            handler = CommandCreatedHandler('Wizard', self.logger)
            btn_wizard.commandCreated.add(handler)
            self.handlers.append(handler)
            
            # Aggiungi al pannello
            p_ia.controls.addCommand(btn_wizard)

            # 7. FORZA VISIBILITÀ
            self.main_tab.isVisible = True
            self.main_tab.activate()
            
            # Messaggio di conferma nel log di Fusion (Text Commands)
            self.app.log("FurnitureAI: UI creata con successo su workspace " + ws.name)

        except Exception as e:
            self.ui.messageBox(f"Errore UI:\n{str(e)}")

    def cleanup(self):
        try:
            if self.main_tab and self.main_tab.isValid:
                self.main_tab.deleteMe()
        except: pass

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, name, logger):
        super().__init__()
        self.name = name
        self.logger = logger
    def notify(self, args):
        on_exec = CommandExecuteHandler(self.name)
        args.command.execute.add(on_exec)
        args.command.setPythonOwner(on_exec)

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, name):
        super().__init__()
        self.name = name
    def notify(self, args):
        adsk.core.Application.get().userInterface.messageBox(f"Esecuzione {self.name}")
