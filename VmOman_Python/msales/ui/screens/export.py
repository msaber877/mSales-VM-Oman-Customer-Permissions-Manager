"""
Mixin for export screen logic.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd
from msales.core.logger import logger
from msales.config import COLORS
from typing import Any

class ExportScreenMixin:
    clear_workspace: Any
    update_sidebar_active_state: Any
    refresh_header_info: Any
    workspace_frame: Any
    t: Any
    current_lang: Any
    create_custom_btn: Any
    show_merge_screen: Any
    merged_df: Any

    def show_export_screen(self):
        self.clear_workspace()
        self.update_sidebar_active_state('export')
        self.refresh_header_info()
        
        card = tk.Frame(self.workspace_frame, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        inner = tk.Frame(card, bg=COLORS['bg_card'], padx=30, pady=30)
        inner.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            inner,
            text=self.t('export_card_title'),
            font=("Segoe UI", 12, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        ).pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            inner,
            text=self.t('export_desc').format(rows=len(self.merged_df)),
            font=("Segoe UI", 10),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            justify=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT,
            wraplength=650
        ).pack(fill=tk.X, pady=10)
        
        # Info Alert bar
        alert = tk.Frame(inner, bg=COLORS['warning_bg'], bd=0, padx=12, pady=12)
        alert.pack(fill=tk.X, pady=15)
        
        tk.Label(
            alert,
            text="⚠️ " + self.t('status_column_info'),
            font=("Segoe UI", 9, "bold"),
            bg=COLORS['warning_bg'],
            fg='#92400E',
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        ).pack(fill=tk.X)
        
        # Format Choose Card
        format_card = tk.LabelFrame(
            inner,
            text=self.t('export_format'),
            font=("Segoe UI", 10, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            padx=15,
            pady=15,
            bd=1,
            relief=tk.SOLID
        )
        format_card.pack(fill=tk.X, pady=15)
        
        self.export_format_var = tk.StringVar(value="csv")
        
        r1 = tk.Radiobutton(
            format_card,
            text="CSV Format (Comma Separated Values - *.csv)",
            variable=self.export_format_var,
            value="csv",
            font=("Segoe UI", 9),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            cursor="hand2"
        )
        r1.pack(anchor=tk.W, pady=4)
        
        r2 = tk.Radiobutton(
            format_card,
            text="Excel File (Microsoft Excel Workbook - *.xlsx)",
            variable=self.export_format_var,
            value="excel",
            font=("Segoe UI", 9),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            cursor="hand2"
        )
        r2.pack(anchor=tk.W, pady=4)
        
        # Action Buttons
        footer = tk.Frame(inner, bg=COLORS['bg_card'], pady=15)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        
        btn_back = self.create_custom_btn(
            footer,
            text=self.t('back'),
            command=self.show_merge_screen,
            style_type='secondary',
            width=12
        )
        btn_back.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT)
        
        btn_save = self.create_custom_btn(
            footer,
            text=self.t('save_and_export'),
            command=self.save_export_results,
            style_type='success',
            width=25
        )
        btn_save.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT)

    def save_export_results(self):
        """Export dataset excluding STATUS column"""
        ext = ".csv" if self.export_format_var.get() == "csv" else ".xlsx"
        filename_default = "Result_Merged_Permissions" + ext
        file_types = [("CSV File", "*.csv")] if ext == ".csv" else [("Excel File", "*.xlsx")]
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=file_types,
            initialfile=filename_default
        )
        
        if filepath:
            try:
                # Exclude STATUS Column on Export
                export_df = self.merged_df[['CODE', 'PERMISSION']].copy()
                
                if filepath.endswith('.csv'):
                    export_df.to_csv(filepath, index=False, encoding='utf-8-sig')
                else:
                    export_df.to_excel(filepath, index=False)
                    
                logger.add(f"Matched dataset saved successfully: {filepath}", "SUCCESS")
                messagebox.showinfo(
                    self.t('success'),
                    self.t('save_success').format(path=filepath, rows=len(export_df))
                )
            except Exception as e:
                logger.add(f"Failed exporting file: {str(e)}", "ERROR")
                messagebox.showerror(self.t('error'), f"Writing operation failed:\n{str(e)}")
