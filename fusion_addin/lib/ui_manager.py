"""
UI Manager - Workspace esistente + Tab personalizzata + Pannelli e comandi
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
            # Workspace: prova SOLIDO, altrimenti quello attivo
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                ws = self.ui.activeWorkspace
            if not ws:
                self.logger.error("Nessun workspace trovato.")
                return

            # Pulisci eventuale tab pre-esistente
            all_tabs = ws.toolbarTabs
            for existing_tab in all_tabs:
                if existing_tab.id == 'FurnitureAI_MainTab' or existing_tab.name == 'Furniture AI':
                    existing_tab.deleteMe()

            # Crea Tab
            self.main_tab = all_tabs.add('FurnitureAI_MainTab', 'Furniture AI')

            # Pannello 1: CREA RAPIDO (comandi nativi: schizzo + estrusione)
            p_crea = self.main_tab.toolbarPanels.add('FAI_CreaPanel', 'Crea rapido')
            self._add_native_command(p_crea, 'SketchCreateCommand')   # Crea schizzo
            self._add_native_command(p_crea, 'PressPullCommand')      # Estrusione/PressPull

            # Pannello 2: IA & WIZARD (comando custom placeholder)
            p_ia = self.main_tab.toolbarPanels.add('FAI_IAPanel', 'IA & Wizard')
            self._add_custom_button(p_ia, 'FAI_Wizard_Btn', 'Wizard Mobili', 'Avvia wizard')

            # Attiva la tab
            self.main_tab.isVisible = True
            self.main_tab.activate()

            self.app.log(f"FurnitureAI: UI creata su workspace {ws.name}")

        except Exception as e:
            if self.ui:
                self.ui.messageBox(f"Errore UI:\n{str(e)}\n\n{traceback.format_exc()}")

    def cleanup(self):
        try:
            if self.main_tab and self.main_tab.isValid:
                self.main_tab.deleteMe()
        except:
            pass

    # --- Helpers -------------------------------------------------

    def _add_native_command(self, panel, command_id):
        """
        Aggiunge un comando nativo Fusion (commandDefinition già esistente)
        al pannello indicato.
        """
        cmd_defs = self.ui.commandDefinitions
        cmd_def = cmd_defs.itemById(command_id)
        if not cmd_def:
            if self.logger:
                self.logger.error(f"Comando nativo non trovato: {command_id}")
            return
        panel.controls.addCommand(cmd_def)

    def _add_custom_button(self, panel, cmd_id, name, tooltip):
        """
        Crea un comando custom semplice (placeholder) e lo aggiunge al pannello.
        """
        cmd_defs = self.ui.commandDefinitions
        existing_cmd = cmd_defs.itemById(cmd_id)
        if existing_cmd:
            existing_cmd.deleteMe()

        btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip)
        handler = CommandCreatedHandler(name, self.logger)
        btn.commandCreated.add(handler)
        self.handlers.append(handler)
        panel.controls.addCommand(btn)

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, name, logger):
        super().__init__()
        self.name = name
        self.logger = logger
    def notify(self, args):
        on_exec = CommandExecuteHandler(self.name, self.logger)
        args.command.execute.add(on_exec)
        # setPythonOwner non è necessario qui

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, name, logger):
        super().__init__()
        self.name = name
        self.logger = logger
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        ui.messageBox(f"Esecuzione {self.name}")
