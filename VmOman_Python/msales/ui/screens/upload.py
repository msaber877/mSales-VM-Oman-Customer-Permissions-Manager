"""
Mixin for upload screen logic.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from tkinterdnd2 import DND_FILES
from msales.core.data_handler import DataHandler
from msales.core.logger import logger
from msales.config import COLORS
from typing import Any

class UploadScreenMixin:
    clear_workspace: Any
    update_sidebar_active_state: Any
    refresh_header_info: Any
    workspace_frame: Any
    t: Any
    current_lang: Any
    create_custom_btn: Any
    show_home_screen: Any
    show_merge_screen: Any
    customers_df: Any
    dealers_df: Any
    csv_path: Any
    excel_path: Any
    draw_upload_card: Any
    draw_canvas_content: Any
    def show_file_selection_screen(self):
        self.clear_workspace()
        self.update_sidebar_active_state('upload')
        self.refresh_header_info()
        
        # Footer Action flow (packed first at bottom)
        footer_nav = tk.Frame(self.workspace_frame, bg=COLORS['bg_main'], pady=15)
        footer_nav.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Grid frame split columns (fills remaining space)
        grid_container = tk.Frame(self.workspace_frame, bg=COLORS['bg_main'])
        grid_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        grid_container.columnconfigure(0, weight=1, uniform="group1")
        grid_container.columnconfigure(1, weight=1, uniform="group1")
        grid_container.rowconfigure(0, weight=1)
        
        # Left card (CSV File)
        csv_card = self.draw_upload_card(grid_container, 'csv')
        csv_card.grid(row=0, column=0, padx=(0, 15), sticky="nswe")
        
        # Right card (Excel File)
        excel_card = self.draw_upload_card(grid_container, 'excel')
        excel_card.grid(row=0, column=1, padx=(15, 0), sticky="nswe")
        
        btn_back = self.create_custom_btn(
            footer_nav,
            text=self.t('back'),
            command=self.show_home_screen,
            style_type='secondary',
            width=12
        )
        btn_back.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT)
        
        btn_next = self.create_custom_btn(
            footer_nav,
            text=self.t('next'),
            command=self.show_merge_screen,
            style_type='success' if (self.customers_df is not None and self.dealers_df is not None) else 'secondary',
            width=15
        )
        btn_next.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT)
        
        if self.customers_df is None or self.dealers_df is None:
            btn_next.config(state=tk.DISABLED)

    def on_drag_enter(self, event, canvas, text_key):
        self.draw_canvas_content(canvas, text_key, highlight=True)

    def on_drag_leave(self, event, canvas, text_key):
        self.draw_canvas_content(canvas, text_key, highlight=False)

    def on_file_drop(self, event, file_type):
        path = event.data
        if path.startswith('{') and path.endswith('}'):
            path = path[1:-1]
        path = os.path.normpath(path)
        
        logger.add(f"File drag-dropped: {os.path.basename(path)}", "INFO")
        
        if file_type == 'csv':
            if not path.lower().endswith('.csv'):
                messagebox.showwarning(self.t('warning'), "Invalid extension. Drop a .csv file!")
                return
            self.load_csv(path)
        else:
            if not path.lower().endswith(('.xlsx', '.xls')):
                messagebox.showwarning(self.t('warning'), "Invalid extension. Drop an Excel (.xlsx/.xls) file!")
                return
            self.load_excel(path)

    def load_csv(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(
                title=self.t('customer_file'),
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
        if filepath:
            try:
                self.customers_df = DataHandler.read_csv(filepath)
                self.csv_path = filepath
                logger.add(f"Customer file loaded successfully: {os.path.basename(filepath)}", "SUCCESS")
                self.show_file_selection_screen()
            except Exception as e:
                logger.add(f"Customer file loading failed: {str(e)}", "ERROR")
                messagebox.showerror(self.t('error'), f"{self.t('error_load')}:\n{str(e)}")
                self.show_file_selection_screen()

    def load_excel(self, filepath=None):
        if not filepath:
            filepath = filedialog.askopenfilename(
                title=self.t('dealer_file'),
                filetypes=[("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*")]
            )
        if filepath:
            try:
                self.dealers_df = DataHandler.read_excel(filepath)
                self.excel_path = filepath
                logger.add(f"Dealer file loaded successfully: {os.path.basename(filepath)}", "SUCCESS")
                self.show_file_selection_screen()
            except Exception as e:
                logger.add(f"Dealer file loading failed: {str(e)}", "ERROR")
                messagebox.showerror(self.t('error'), f"{self.t('error_load')}:\n{str(e)}")
                self.show_file_selection_screen()

    def clear_loaded_file(self, file_type):
        if file_type == 'csv':
            self.customers_df = None
            self.csv_path = None
            logger.add("Customer file context discarded.", "INFO")
        else:
            self.dealers_df = None
            self.excel_path = None
            logger.add("Dealer file context discarded.", "INFO")
        self.merged_df = None
        self.data_modified = False
        self.show_file_selection_screen()
