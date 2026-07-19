"""
Mixin for home screen logic.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from msales.config import COLORS
from typing import Any


class HomeScreenMixin:
    clear_workspace: Any
    update_sidebar_active_state: Any
    refresh_header_info: Any
    workspace_frame: Any
    t: Any
    current_lang: Any
    create_custom_btn: Any
    show_file_selection_screen: Any

    def show_home_screen(self):
        self.clear_workspace()
        self.update_sidebar_active_state('home')
        self.refresh_header_info()
        
        card = tk.Frame(self.workspace_frame, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
        card.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        inner = tk.Frame(card, bg=COLORS['bg_card'], padx=40, pady=45)
        inner.pack(fill=tk.BOTH, expand=True)
        
        # Graphic representation
        graphic_lbl = tk.Label(
            inner,
            text="🔄",
            font=("Segoe UI", 56),
            bg=COLORS['bg_card'],
            fg=COLORS['primary']
        )
        graphic_lbl.pack(pady=(0, 20))
        
        title_lbl = tk.Label(
            inner,
            text=self.t('quick_start'),
            font=("Segoe UI", 16, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        )
        title_lbl.pack(anchor=tk.CENTER)
        
        desc_lbl = tk.Label(
            inner,
            text=self.t('quick_start_desc'),
            font=("Segoe UI", 10),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            justify=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT,
            wraplength=600,
            pady=20
        )
        desc_lbl.pack(anchor=tk.CENTER)
        
        btn_start = self.create_custom_btn(
            inner,
            text=self.t('start_btn'),
            command=self.show_file_selection_screen,
            style_type='primary',
            width=25,
            font_size=11
        )
        btn_start.pack(pady=20)
