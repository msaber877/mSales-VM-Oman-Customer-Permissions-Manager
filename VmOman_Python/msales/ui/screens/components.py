"""
Mixin for components screen logic.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from tkinterdnd2 import DND_FILES
from msales.config import COLORS
from typing import Any


class ComponentsMixin:
    clear_workspace: Any
    update_sidebar_active_state: Any
    refresh_header_info: Any
    workspace_frame: Any
    t: Any
    current_lang: Any
    create_custom_btn: Any
    show_file_selection_screen: Any
    on_file_drop: Any
    on_drag_enter: Any
    on_drag_leave: Any
    load_csv: Any
    load_excel: Any
    csv_path: Any
    excel_path: Any
    customers_df: Any
    dealers_df: Any
    clear_loaded_file: Any

    def draw_upload_card(self, parent, file_type):
        """Constructs modern card container with drag/drop area and status representation"""
        is_csv = (file_type == 'csv')
        title_key = 'customer_file' if is_csv else 'dealer_file'
        drag_key = 'drag_drop_csv' if is_csv else 'drag_drop_excel'
        
        card = tk.Frame(parent, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
        
        content = tk.Frame(card, bg=COLORS['bg_card'], padx=25, pady=25)
        content.pack(fill=tk.BOTH, expand=True)
        
        lbl_title = tk.Label(
            content,
            text=self.t(title_key),
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        )
        lbl_title.pack(fill=tk.X, pady=(0, 10))
        
        # Interactive Drag Zone Canvas
        canvas = tk.Canvas(
            content,
            bg=COLORS['bg_main'],
            height=145,
            highlightthickness=0,
            cursor="hand2"
        )
        canvas.pack(fill=tk.X, pady=10)
        
        # Connect drop listeners
        canvas_dnd: Any = canvas
        canvas_dnd.drop_target_register(DND_FILES)
        canvas_dnd.dnd_bind('<<Drop>>', lambda e, ft=file_type: self.on_file_drop(e, ft))
        canvas_dnd.dnd_bind('<<DragEnter>>', lambda e, cv=canvas, tk_key=drag_key: self.on_drag_enter(e, cv, tk_key))
        canvas_dnd.dnd_bind('<<DragLeave>>', lambda e, cv=canvas, tk_key=drag_key: self.on_drag_leave(e, cv, tk_key))
        
        # Bind manual click dialog
        manual_load = self.load_csv if is_csv else self.load_excel
        canvas.bind("<Button-1>", lambda e: manual_load())
        
        # Bind resize configure
        canvas.bind("<Configure>", lambda e, cv=canvas, tk_key=drag_key: self.draw_canvas_content(cv, tk_key, highlight=False))
        self.draw_canvas_content(canvas, drag_key, highlight=False)
        
        # File loaded card visual response
        status_box = tk.Frame(content, bg=COLORS['bg_card'])
        status_box.pack(fill=tk.X, pady=(15, 0))
        
        path_str = self.csv_path if is_csv else self.excel_path
        df_target = self.customers_df if is_csv else self.dealers_df
        
        if path_str and df_target is not None:
            # Active green info status panel
            indicator_card = tk.Frame(status_box, bg=COLORS['success_bg'], bd=0, padx=12, pady=12)
            indicator_card.pack(fill=tk.X)
            
            green_bar = tk.Frame(indicator_card, bg=COLORS['success'], width=4)
            green_bar.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT, fill=tk.Y)
            
            meta_area = tk.Frame(indicator_card, bg=COLORS['success_bg'], padx=10)
            meta_area.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT, fill=tk.BOTH, expand=True)
            
            filename = os.path.basename(path_str)
            tk.Label(
                meta_area,
                text="✓ " + filename,
                font=("Segoe UI", 9, "bold"),
                bg=COLORS['success_bg'],
                fg='#065F46',
                anchor=tk.W if self.current_lang == 'EN' else tk.E
            ).pack(fill=tk.X)
            
            row_count_lbl = tk.Label(
                meta_area,
                text=f"{len(df_target)} rows",
                font=("Segoe UI", 8),
                bg=COLORS['success_bg'],
                fg='#047857',
                anchor=tk.W if self.current_lang == 'EN' else tk.E
            )
            row_count_lbl.pack(fill=tk.X, pady=(3, 0))
            
            # Dismiss button
            clear_btn = tk.Button(
                indicator_card,
                text="✕",
                font=("Segoe UI", 9, "bold"),
                bg=COLORS['success_bg'],
                fg=COLORS['danger'],
                activebackground=COLORS['danger_bg'],
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda ft=file_type: self.clear_loaded_file(ft)
            )
            clear_btn.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT, padx=5)
        else:
            # Muted warning panel
            tk.Label(
                status_box,
                text="⚠️ " + self.t('no_file'),
                font=("Segoe UI", 9, "italic"),
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary'],
                anchor=tk.W if self.current_lang == 'EN' else tk.E
            ).pack(fill=tk.X, padx=10)
            
        return card

    def draw_canvas_content(self, canvas, text_key, highlight=False):
        """Draw flat vector indicators on drag zones"""
        canvas.delete("all")
        
        width = canvas.winfo_width()
        if width <= 1:
            width = 400
        height = 145
        
        bg_col = '#EFF6FF' if highlight else COLORS['bg_main']
        border_col = COLORS['primary'] if highlight else COLORS['border']
        canvas.configure(bg=bg_col)
        
        # Dotted rectangle outline
        canvas.create_rectangle(
            6, 6, width-6, height-6,
            outline=border_col,
            width=2,
            dash=(5, 5)
        )
        
        # Vector Emoji Icon
        icon = "📤" if highlight else "📁"
        canvas.create_text(
            width // 2, 45,
            text=icon,
            font=("Segoe UI", 26),
            fill=COLORS['primary'] if highlight else COLORS['text_muted']
        )
        
        # Prompt details
        canvas.create_text(
            width // 2, 95,
            text=self.t(text_key),
            font=("Segoe UI", 9, "bold" if highlight else "normal"),
            fill=COLORS['text_primary'],
            justify=tk.CENTER
        )

    def create_custom_btn(self, parent, text, command, style_type='primary', width=None, height=None, font_size=10):
        """Unified custom button factory wrapping hover styles"""
        bg_configs = {
            'primary': COLORS['primary'],
            'success': COLORS['success'],
            'danger': COLORS['danger'],
            'warning': COLORS['warning'],
            'secondary': COLORS['sidebar_hover']
        }
        fg_configs = {
            'primary': COLORS['text_light'],
            'success': COLORS['text_light'],
            'danger': COLORS['text_light'],
            'warning': COLORS['text_light'],
            'secondary': COLORS['sidebar_text']
        }
        hover_configs = {
            'primary': COLORS['primary_hover'],
            'success': '#059669',
            'danger': '#E11D48',
            'warning': '#D97706',
            'secondary': COLORS['sidebar_selected']
        }
        
        bg = bg_configs.get(style_type, COLORS['primary'])
        fg = fg_configs.get(style_type, COLORS['text_light'])
        hover_bg = hover_configs.get(style_type, COLORS['primary_hover'])
        
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", font_size, "bold" if style_type in ['primary', 'success', 'danger'] else "normal"),
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            cursor="hand2",
            padx=12,
            pady=7
        )
        
        if width:
            btn.config(width=width)
        if height:
            btn.config(height=height)
            
        def on_enter(e):
            if btn['state'] != tk.DISABLED:
                btn.config(bg=hover_bg)
        def on_leave(e):
            if btn['state'] != tk.DISABLED:
                btn.config(bg=bg)
            
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        return btn
