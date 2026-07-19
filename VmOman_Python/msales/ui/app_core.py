"""
Core mSales application class tying all Mixins together.
"""
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD
from typing import Optional, Dict, Any, List
import pandas as pd

from msales.config import COLORS, TRANSLATIONS
from msales.core.logger import logger
from msales.ui.screens.components import ComponentsMixin
from msales.ui.screens.home import HomeScreenMixin
from msales.ui.screens.upload import UploadScreenMixin
from msales.ui.screens.merge import MergeScreenMixin
from msales.ui.screens.editor import EditorScreenMixin
from msales.ui.screens.export import ExportScreenMixin
from datetime import datetime

class mSalesApp(
    TkinterDnD.Tk,
    ComponentsMixin,
    HomeScreenMixin,
    UploadScreenMixin,
    MergeScreenMixin,
    EditorScreenMixin,
    ExportScreenMixin
):
    def __init__(self):
        super().__init__()
        
        # Configure root properties
        self.title("mSales -VM Oman Customer Permissions Manager")
        self.geometry("1300x820")
        self.minsize(1080, 720)
        self.configure(bg=COLORS['bg_main'])
        
        # Application state
        self.current_lang: str = 'EN'  # Default language: English
        self.active_step: str = 'home'
        self.logs_visible: bool = True
        
        self.customers_df: Any = None
        self.dealers_df: Any = None
        self.merged_df: Any = None
        self.csv_path: Any = None
        self.excel_path: Any = None
        self.selected_codes_dict: Dict[str, str] = {}
        self.data_modified: bool = False
        
        # UI Elements pointers
        self.sidebar_frame: Any = None
        self.nav_buttons: Dict[str, tk.Button] = {}
        self.main_container: Any = None
        
        self.header_frame: Any = None
        self.header_title: Any = None
        self.header_subtitle: Any = None
        self.header_text_inner: Any = None
        self.header_btn_inner: Any = None
        self.lang_btn: Any = None
        self.logs_btn: Any = None
        
        self.workspace_frame: Any = None
        self.console_frame: Any = None
        self.console_text: Any = None
        
        # Initialization
        self.setup_styles()
        self.build_window_skeleton()
        
        # Bind log callback
        logger.callbacks.append(self.dispatch_log_to_terminal)
        logger.add(self.t('log_ready'), "SUCCESS")
        
        # Render initial view
        self.show_home_screen()

    def t(self, key):
        """Translate key to current language"""
        return TRANSLATIONS[self.current_lang].get(key, key)

    def change_language(self):
        """Toggle system language and refresh current view"""
        self.current_lang = 'EN' if self.current_lang == 'AR' else 'AR'
        logger.add(f"Language changed to: {self.current_lang}", "INFO")
        
        # Redraw persistent frames labels
        self.refresh_sidebar_menu()
        self.refresh_header_info()
        self.logs_btn.config(text=self.t('hide_logs') if self.logs_visible else self.t('show_logs'))
        
        # Redraw dynamic workspace content
        if self.active_step == 'home':
            self.show_home_screen()
        elif self.active_step == 'upload':
            self.show_file_selection_screen()
        elif self.active_step == 'merge':
            self.show_merge_screen()
        elif self.active_step == 'edit':
            self.show_editor_screen()
        elif self.active_step == 'export':
            self.show_export_screen()

    def setup_styles(self):
        """Configure modern widgets appearance"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Clean custom Treeview styling
        self.style.configure(
            'Treeview',
            font=('Segoe UI', 9),
            rowheight=26,
            background=COLORS['bg_card'],
            foreground=COLORS['text_primary'],
            fieldbackground=COLORS['bg_card'],
            borderwidth=0
        )
        self.style.configure(
            'Treeview.Heading',
            font=('Segoe UI', 9, 'bold'),
            background=COLORS['sidebar_bg'],
            foreground=COLORS['text_light'],
            relief=tk.FLAT,
            borderwidth=0
        )
        self.style.map(
            'Treeview',
            background=[('selected', COLORS['primary']), ('active', '#F1F5F9')],
            foreground=[('selected', COLORS['text_light']), ('active', COLORS['text_primary'])]
        )
        
        # Remove dotted line on tree cell focus
        self.style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])

    def build_window_skeleton(self):
        """Design persistent sidebar, header, workspace, and collapsible terminal"""
        
        # Prevent scaling blurs on High-DPI
        try:
            self.tk.call('tk', 'scaling', 1.3)
        except:
            pass
            
        # 1. Left Sidebar
        self.sidebar_frame = tk.Frame(self, bg=COLORS['sidebar_bg'], width=230)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar_frame.pack_propagate(False)
        
        logo_area = tk.Frame(self.sidebar_frame, bg=COLORS['sidebar_bg'], pady=25)
        logo_area.pack(fill=tk.X)
        
        self.logo_lbl = tk.Label(
            logo_area,
            text="📊 mSales Merger",
            font=("Segoe UI", 15, "bold"),
            bg=COLORS['sidebar_bg'],
            fg=COLORS['primary']
        )
        self.logo_lbl.pack()
        
        self.logo_sub = tk.Label(
            logo_area,
            text="EME INTERNATIONAL",
            font=("Segoe UI", 8, "bold"),
            bg=COLORS['sidebar_bg'],
            fg=COLORS['text_muted']
        )
        self.logo_sub.pack(pady=(3, 0))
        
        # Divider line
        div = tk.Frame(self.sidebar_frame, bg=COLORS['sidebar_hover'], height=1)
        div.pack(fill=tk.X, padx=20, pady=(5, 15))
        
        # Sidebar Menu Container
        self.menu_container = tk.Frame(self.sidebar_frame, bg=COLORS['sidebar_bg'])
        self.menu_container.pack(fill=tk.BOTH, expand=True, padx=12)
        
        # Build Navigation items
        self.steps = [
            ('home', 'home', self.show_home_screen),
            ('upload', 'upload', self.show_file_selection_screen),
            ('merge', 'merge_results', self.show_merge_screen),
            ('edit', 'edit_permissions', self.show_editor_screen),
            ('export', 'export', self.show_export_screen)
        ]
        
        for key, trans_key, cmd in self.steps:
            btn = tk.Button(
                self.menu_container,
                text=self.t(trans_key),
                command=cmd,
                font=("Segoe UI", 10),
                bg=COLORS['sidebar_bg'],
                fg=COLORS['sidebar_text'],
                anchor='w',
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                padx=15,
                pady=10,
                activebackground=COLORS['sidebar_hover'],
                activeforeground=COLORS['primary']
            )
            btn.pack(fill=tk.X, pady=3)
            
            # Hover bindings
            def bind_enter(b=btn, k=key):
                return lambda e: b.config(bg=COLORS['sidebar_hover']) if self.active_step != k else None
            def bind_leave(b=btn, k=key):
                return lambda e: b.config(bg=COLORS['sidebar_bg']) if self.active_step != k else None
                
            btn.bind("<Enter>", bind_enter())
            btn.bind("<Leave>", bind_leave())
            self.nav_buttons[key] = btn
            
        # Support info at bottom
        support_text = f"Enterprise VM-Oman v3.5\nDeveloper: Mohamed Saber\nmohamed.saber@emeint.net\nDate: {datetime.now().strftime('%Y-%m-%d')}"
        support_lbl = tk.Label(
            self.sidebar_frame,
            text=support_text,
            font=("Segoe UI", 8),
            bg=COLORS['sidebar_bg'],
            fg=COLORS['text_muted'],
            justify=tk.CENTER,
            pady=15
        )
        support_lbl.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 2. Main Workspace Container
        self.main_container = tk.Frame(self, bg=COLORS['bg_main'])
        self.main_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 3. Top Header
        self.header_frame = tk.Frame(self.main_container, bg=COLORS['bg_card'], height=75)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)
        self.header_frame.pack_propagate(False)
        
        h_border = tk.Frame(self.header_frame, bg=COLORS['border'], height=1)
        h_border.pack(fill=tk.X, side=tk.BOTTOM)
        
        # Header Inner Packs (Dynamic RTL/LTR)
        self.header_text_inner = tk.Frame(self.header_frame, bg=COLORS['bg_card'])
        self.header_btn_inner = tk.Frame(self.header_frame, bg=COLORS['bg_card'])
        
        self.header_title = tk.Label(
            self.header_text_inner,
            text="",
            font=("Segoe UI", 15, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary']
        )
        self.header_title.pack(anchor=tk.W)
        
        self.header_subtitle = tk.Label(
            self.header_text_inner,
            text="",
            font=("Segoe UI", 9),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary']
        )
        self.header_subtitle.pack(anchor=tk.W, pady=(2, 0))
        
        # Header Controls
        self.logs_btn = self.create_custom_btn(
            self.header_btn_inner,
            text=self.t('hide_logs'),
            command=self.toggle_logs_console,
            style_type='secondary',
            font_size=9
        )
        self.logs_btn.pack(side=tk.LEFT, padx=5, pady=18)
        
        self.lang_btn = self.create_custom_btn(
            self.header_btn_inner,
            text="English 🇺🇸" if self.current_lang == 'AR' else "العربية 🇸🇦",
            command=self.change_language,
            style_type='primary',
            font_size=9
        )
        self.lang_btn.pack(side=tk.LEFT, padx=5, pady=18)
        
        # 4. Collapsible Log Terminal (Bottom)
        self.console_frame = tk.Frame(self.main_container, bg=COLORS['console_bg'], height=150)
        self.console_frame.pack(side=tk.BOTTOM, fill=tk.X)
        self.console_frame.pack_propagate(False)
        
        console_bar = tk.Frame(self.console_frame, bg='#111827', height=28)
        console_bar.pack(fill=tk.X)
        
        self.console_title = tk.Label(
            console_bar,
            text=self.t('system_logs'),
            font=("Segoe UI", 9, "bold"),
            bg='#111827',
            fg=COLORS['success']
        )
        self.console_title.pack(side=tk.LEFT, padx=15)
        
        close_console = tk.Button(
            console_bar,
            text="✕",
            font=("Segoe UI", 8, "bold"),
            bg='#111827',
            fg=COLORS['text_muted'],
            activebackground='#1F2937',
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            padx=8,
            command=self.toggle_logs_console
        )
        close_console.pack(side=tk.RIGHT, padx=10, pady=2)
        
        self.console_text = tk.Text(
            self.console_frame,
            bg=COLORS['console_bg'],
            fg=COLORS['console_fg'],
            font=("Consolas", 9),
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=8,
            state=tk.DISABLED
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(self.console_text, orient=tk.VERTICAL, command=self.console_text.yview)
        self.console_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Format tag levels
        self.console_text.tag_configure('info', foreground='#F8FAFC')
        self.console_text.tag_configure('success', foreground='#34D399')
        self.console_text.tag_configure('warning', foreground='#FBBF24')
        self.console_text.tag_configure('error', foreground='#F87171')
        
        # 5. Middle Dynamic Content Area
        self.workspace_frame = tk.Frame(self.main_container, bg=COLORS['bg_main'])
        self.workspace_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=20)
        
        # Setup initial header layout alignment
        self.refresh_header_info()

    def update_sidebar_active_state(self, step_key):
        """Highlights current step in menu sidebar and manages disable statuses"""
        self.active_step = step_key
        
        # Enable steps only if data is loaded
        files_loaded = (self.customers_df is not None and self.dealers_df is not None)
        
        for key, btn in self.nav_buttons.items():
            if key == step_key:
                btn.config(bg=COLORS['sidebar_selected'], fg=COLORS['text_light'])
            else:
                btn.config(bg=COLORS['sidebar_bg'], fg=COLORS['sidebar_text'])
                
            # Disable steps that require data
            if key in ['merge', 'edit', 'export']:
                if files_loaded:
                    btn.config(state=tk.NORMAL)
                else:
                    btn.config(state=tk.DISABLED, fg=COLORS['text_muted'])
            else:
                btn.config(state=tk.NORMAL)

    def refresh_sidebar_menu(self):
        """Update text on all sidebar navigation elements"""
        for key, trans_key, _ in self.steps:
            if key in self.nav_buttons:
                self.nav_buttons[key].config(text=self.t(trans_key))
        self.update_sidebar_active_state(self.active_step)

    def refresh_header_info(self):
        """Align header layout according to selected language (RTL/LTR)"""
        self.header_text_inner.pack_forget()
        self.header_btn_inner.pack_forget()
        
        # Repack based on language direction
        if self.current_lang == 'AR':
            self.header_text_inner.pack(side=tk.RIGHT, padx=25, fill=tk.Y)
            self.header_btn_inner.pack(side=tk.LEFT, padx=20, fill=tk.Y)
            align = tk.E
        else:
            self.header_text_inner.pack(side=tk.LEFT, padx=25, fill=tk.Y)
            self.header_btn_inner.pack(side=tk.RIGHT, padx=20, fill=tk.Y)
            align = tk.W
            
        self.header_title.config(anchor=align)
        self.header_subtitle.config(anchor=align)
        self.lang_btn.config(text="English 🇺🇸" if self.current_lang == 'AR' else "العربية 🇸🇦")
        
        # Load localized titles for current screen
        titles = {
            'home': (self.t('app_title'), self.t('quick_start')),
            'upload': (self.t('select_files_title'), self.t('select_files_sub')),
            'merge': (self.t('merge_results'), self.t('search_placeholder')),
            'edit': (self.t('edit_permissions'), self.t('available_codes')),
            'export': (self.t('export_title'), self.t('export_sub'))
        }
        main_t, sub_t = titles.get(self.active_step, ("", ""))
        self.header_title.config(text=main_t)
        self.header_subtitle.config(text=sub_t)
        
        # Refresh console titles
        self.console_title.config(text=self.t('system_logs'))

    def clear_workspace(self):
        """Remove all active workspace frames"""
        for child in self.workspace_frame.winfo_children():
            child.destroy()

    def toggle_logs_console(self):
        """Collapse or expand bottom developer log terminal"""
        if self.logs_visible:
            self.console_frame.pack_forget()
            self.logs_visible = False
            self.logs_btn.config(text=self.t('show_logs'))
        else:
            self.console_frame.pack(side=tk.BOTTOM, fill=tk.X)
            self.logs_visible = True
            self.logs_btn.config(text=self.t('hide_logs'))
            # Auto scroll to bottom
            self.console_text.see(tk.END)

    def dispatch_log_to_terminal(self, log_entry, log_level):
        """Append log line to text widget with colored levels tags"""
        if hasattr(self, 'console_text') and self.console_text.winfo_exists():
            self.console_text.config(state=tk.NORMAL)
            
            tag = log_level.lower()
            log_str = f"[{log_entry['time']}] {log_entry['message']}"
            self.console_text.insert(tk.END, log_str + "\n", tag)
            self.console_text.see(tk.END)
            self.console_text.config(state=tk.DISABLED)
