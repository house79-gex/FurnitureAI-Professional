"""
Gestore UI per FurnitureAI - Versione Stabile Anti-Errore Sessione
"""

import adsk.core
import adsk.fusion
import traceback

class UIManager:
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
        """Crea la scheda Furniture AI con gestione errori robusta"""
        try:
            # 1. Recupero Workspace sicuro
            workspaces = self.ui.workspaces
            self.workspace = workspaces.itemById('FusionDesignWorkspace')
            
            if not self.workspace:
                self.logger.error("Workspace Progettazione non trovato.")
                return

            # 2. Pulizia preventiva (fondamentale per evitare duplicati o blocchi)
            try:
                existing_tab = self.workspace.toolbarTabs.itemById('FurnitureAI_MainTab')
                if existing_tab:
                    existing_tab.deleteMe()
            except:
                pass

            # 3. Creazione Tab Principale
            # Usiamo un nome interno unico e un nome visibile chiaro
            self.main_tab = self.workspace.toolbarTabs.add('FurnitureAI_MainTab', 'Furniture AI')
            
            # 4. Importazione Pannelli Standard (Crea e Modifica)
            # Avvolto in try/except per non bloccare tutto se Fusion non li espone subito
            try:
                solid_tab = self.workspace.toolbarTabs.itemById('SolidTab')
                if solid_tab:
                    # Aggiungiamo CREA
                    c_panel = solid_tab.toolbarPanels.itemById('SolidCreatePanel')
                    if c_panel:
                        self.main_tab.toolbarPanels.add(c_panel)
                    # Aggiungiamo MODIFICA (molto utile per mobili)
                    m_panel = solid_tab.toolbarPanels.itemById('SolidModifyPanel')
                    if m_panel:
                        self.main_tab.toolbarPanels.add(m_panel)
            except:
                self.logger.info("Impossibile integrare i pannelli standard in questo momento.")

            # 5. Creazione Pannelli Personalizzati
            self._create_custom_panels()
            self._create_commands()
            self._populate_panels()

            # 6. Attivazione forzata
            self.main_tab.activate()
            self.logger.info("✅ Interfaccia Furniture AI caricata.")

        except Exception as e:
            # Se l'errore è pCurrentSession, il log ci avvisa ma non blocchiamo l'utente
            err_msg = str(e)
            if "pCurrentSession" in err_msg:
                self.logger.error("Sessione non ancora pronta. Riavvia l'Add-in tra qualche secondo.")
            else:
                self.ui.messageBox(f"Errore caricamento UI:\n{err_msg}")
            self.logger.error(traceback.format_exc())

    def _create_custom_panels(self):
        try:
            # Pannello IA & WIZARD
            p_ia = self.main_tab.toolbarPanels.add('FurnitureAI_IAPanel', 'IA & PROGETTAZIONE')
            self.panels.append(('FurnitureAI_IAPanel', p_ia))

            # Pannello PRODUZIONE
            p_prod = self.main_tab.toolbarPanels.add('FurnitureAI_ProdPanel', 'PRODUZIONE')
            self.panels.append(('FurnitureAI_ProdPanel', p_prod))
        except:
            pass

    def _create_commands(self):
        cmd_defs = self.ui.commandDefinitions
        # Configurazione comandi
        config = {
            'FurnitureAI_IAPanel': [
                ('FAI_Wizard', 'Wizard Mobili', 'Crea mobile'),
                ('FAI_Gen', 'Generatore IA', 'AI Design'),
            ],
            'FurnitureAI_ProdPanel': [
                ('FAI_Cut', 'Lista Taglio', 'Nesting'),
            ]
        }

        for p_id, cmds in config.items():
            for c_id, name, desc in cmds:
                try:
                    existing = cmd_defs.itemById(c_id)
                    if existing: existing.deleteMe()
                    
                    btn = cmd_defs.addButtonDefinition(c_id, name, desc)
                    handler = CommandCreatedHandler(name, self.logger)
                    btn.commandCreated.add(handler)
                    self.handlers.append(handler)
                    self.command_defs.append((p_id, btn))
                except:
                    continue

    def _populate_panels(self):
        for p_target_id, cmd_def in self.command_defs:
            for p_id, p_obj in self.panels:
                if p_id == p_target_id:
                    try:
                        p_obj.controls.addCommand(cmd_def)
                    except:
                        continue

    def cleanup(self):
        try:
            if self.main_tab and self.main_tab.isValid:
                self.main_tab.deleteMe()
            for _, cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()
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
            on_execute = CommandExecuteHandler(self.command_name, self.logger)
            args.command.execute.add(on_execute)
            # Manteniamo l'oggetto in vita
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
        ui.messageBox(f'Comando: {self.command_name}\nStatus: Pronto per logica.')
