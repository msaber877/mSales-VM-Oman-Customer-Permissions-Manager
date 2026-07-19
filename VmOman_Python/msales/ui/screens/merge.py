"""
Mixin for merge screen logic.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from msales.core.data_handler import DataHandler
from msales.core.logger import logger
from msales.config import COLORS
from typing import Any

class MergeScreenMixin:
    clear_workspace: Any
    update_sidebar_active_state: Any
    refresh_header_info: Any
    workspace_frame: Any
    t: Any
    current_lang: Any
    create_custom_btn: Any
    show_file_selection_screen: Any
    show_export_screen: Any
    show_editor_screen: Any
    customers_df: Any
    dealers_df: Any
    merged_df: Any
    data_modified: Any
    search_field: Any
    tree: Any
    filter_preview_table: Any
    def show_merge_screen(self):
        self.clear_workspace()
        self.update_sidebar_active_state('merge')
        
        # Run merge calculations if not performed
        if self.merged_df is None:
            try:
                self.merged_df = DataHandler.vlookup_merge(self.customers_df, self.dealers_df)
                self.data_modified = False
            except Exception as e:
                logger.add(f"Data merge engine failed: {str(e)}", "ERROR")
                messagebox.showerror(self.t('error'), f"Merge operation failed:\n{str(e)}")
                self.show_file_selection_screen()
                return

        self.refresh_header_info()
        
        # 1. Statistics Cards Row
        stats_bar = tk.Frame(self.workspace_frame, bg=COLORS['bg_main'])
        stats_bar.pack(fill=tk.X, pady=(0, 15))
        
        matched_count = len(self.merged_df[self.merged_df['STATUS'] == 'Matched'])
        unmatched_count = len(self.merged_df[self.merged_df['STATUS'] == 'Not Found'])
        total_count = len(self.merged_df)
        success_rate = (matched_count / total_count * 100) if total_count > 0 else 0.0
        
        metrics = [
            ('total_codes', str(total_count), COLORS['primary']),
            ('matched', str(matched_count), COLORS['success']),
            ('not_found', str(unmatched_count), COLORS['danger']),
            ('success_rate', f"{success_rate:.1f}%", COLORS['warning'])
        ]
        
        for key, value, color in metrics:
            card = tk.Frame(stats_bar, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            # Left colored stripe accent
            stripe = tk.Frame(card, bg=color, width=4)
            stripe.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT, fill=tk.Y)
            
            inner_panel = tk.Frame(card, bg=COLORS['bg_card'], padx=12, pady=10)
            inner_panel.pack(fill=tk.BOTH, expand=True)
            
            lbl_name = tk.Label(
                inner_panel,
                text=self.t(key),
                font=("Segoe UI", 9, "bold"),
                bg=COLORS['bg_card'],
                fg=COLORS['text_secondary'],
                anchor=tk.W if self.current_lang == 'EN' else tk.E
            )
            lbl_name.pack(fill=tk.X)
            
            lbl_value = tk.Label(
                inner_panel,
                text=value,
                font=("Segoe UI", 15, "bold"),
                bg=COLORS['bg_card'],
                fg=color,
                anchor=tk.W if self.current_lang == 'EN' else tk.E
            )
            lbl_value.pack(fill=tk.X, pady=(2, 0))
            
        # 3. Actions Row (packed first at bottom)
        actions_bar = tk.Frame(self.workspace_frame, bg=COLORS['bg_main'])
        actions_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        # 2. Search box card & table (fills remaining space)
        table_card = tk.Frame(self.workspace_frame, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
        table_card.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        
        search_area = tk.Frame(table_card, bg=COLORS['bg_card'], padx=15, pady=12)
        search_area.pack(fill=tk.X)
        
        self.search_field = tk.Entry(
            search_area,
            font=("Segoe UI", 10),
            bg=COLORS['bg_main'],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['primary']
        )
        self.search_field.pack(fill=tk.X, ipady=4)
        
        # Real-time binding
        self.search_field.bind("<KeyRelease>", self.filter_preview_table)
        
        # Placeholder injection
        self.search_field.insert(0, self.t('search_placeholder'))
        
        def focus_in(e):
            if self.search_field.get() == self.t('search_placeholder'):
                self.search_field.delete(0, tk.END)
        def focus_out(e):
            if not self.search_field.get():
                self.search_field.insert(0, self.t('search_placeholder'))
                
        self.search_field.bind("<FocusIn>", focus_in)
        self.search_field.bind("<FocusOut>", focus_out)
        
        # Results table
        table_frm = tk.Frame(table_card, bg=COLORS['bg_card'], padx=15)
        table_frm.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        cols = ('CODE', 'BEFORE', 'AFTER', 'CHANGE', 'STATUS')
        self.tree = ttk.Treeview(table_frm, columns=cols, show='headings')
        
        self.tree.heading('CODE', text=self.t('dealer_code'))
        self.tree.heading('BEFORE', text=self.t('before_permissions'))
        self.tree.heading('AFTER', text=self.t('after_permissions'))
        self.tree.heading('CHANGE', text=self.t('change'))
        self.tree.heading('STATUS', text=self.t('status'))
        
        self.tree.column('CODE', width=120, anchor=tk.CENTER, stretch=False)
        self.tree.column('BEFORE', width=450, anchor=tk.W, stretch=False)
        self.tree.column('AFTER', width=450, anchor=tk.W, stretch=False)
        self.tree.column('CHANGE', width=250, anchor=tk.CENTER, stretch=False)
        self.tree.column('STATUS', width=120, anchor=tk.CENTER, stretch=False)
        
        # Highlighting rules configuration
        self.tree.tag_configure('matched', foreground='#047857', background='#ECFDF5')
        self.tree.tag_configure('unmatched', foreground='#E11D48', background='#FFF1F2')
        self.tree.tag_configure('added_row', foreground='#137333', background='#E6F4EA') # Soft green highlight for added
        self.tree.tag_configure('removed_row', foreground='#C5221F', background='#FCE8E6') # Soft red highlight for removed
        
        scr = ttk.Scrollbar(table_frm, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scr.set)
        
        scr_x = ttk.Scrollbar(table_frm, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=scr_x.set)
        
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        scr_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Initial populate
        self.filter_preview_table()
        
        # Filtering count status
        self.records_lbl = tk.Label(
            table_card,
            text="",
            font=("Segoe UI", 9, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_secondary'],
            padx=15,
            pady=8
        )
        self.records_lbl.pack(anchor=tk.W if self.current_lang == 'EN' else tk.E)
        self.refresh_records_label(len(self.merged_df), len(self.merged_df))
        
        btn_back = self.create_custom_btn(
            actions_bar,
            text=self.t('back'),
            command=self.show_file_selection_screen,
            style_type='secondary',
            width=12
        )
        btn_back.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT)
        
        btn_export = self.create_custom_btn(
            actions_bar,
            text=self.t('save_results_btn'),
            command=self.show_export_screen,
            style_type='success',
            width=22
        )
        btn_export.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT, padx=5)
        
        if not self.data_modified:
            btn_export.config(state=tk.DISABLED, bg=COLORS['text_muted'])
        
        
        btn_edit = self.create_custom_btn(
            actions_bar,
            text=self.t('edit_codes_btn'),
            command=self.show_editor_screen,
            style_type='primary',
            width=22
        )
        btn_edit.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT, padx=5)

    def filter_preview_table(self, event=None):
        raw_val = self.search_field.get().strip()
        # Robust placeholder check
        placeholder_en = "search dealer code..."
        placeholder_ar = "بحث بكود التاجر..."
        if (not raw_val or 
            raw_val.lower() == placeholder_en or 
            raw_val == placeholder_ar or 
            placeholder_ar in raw_val or 
            raw_val in placeholder_ar):
            query = ""
        else:
            query = raw_val.lower()
            
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        visible_count = 0
        for _, row in self.merged_df.iterrows():
            code_str = str(row['CODE']).strip()
            before_str = str(row.get('ORIGINAL_PERMISSION', row['PERMISSION'])).strip()
            after_str = str(row['PERMISSION']).strip()
            status = row['STATUS']
            
            # Match query against code, original permission, or current permission
            if (not query or 
                query in code_str.lower() or 
                query in before_str.lower() or 
                query in after_str.lower()):
                
                # Determine changes (diff)
                before_list = DataHandler.normalize_separators(before_str)
                after_list = DataHandler.normalize_separators(after_str)
                
                added_codes = [c for c in after_list if c not in before_list]
                removed_codes = [c for c in before_list if c not in after_list]
                
                change_str = "-"
                tag = 'matched' if status == 'Matched' else 'unmatched'
                
                if added_codes:
                    change_str = "+ " + ",".join(added_codes)
                    tag = 'added_row'
                elif removed_codes:
                    change_str = "- " + ",".join(removed_codes)
                    tag = 'removed_row'
                    
                self.tree.insert('', tk.END, values=(
                    row['CODE'],
                    before_str,
                    after_str,
                    change_str,
                    status
                ), tags=(tag,))
                visible_count += 1
                
        self.refresh_records_label(visible_count, len(self.merged_df))

    def refresh_records_label(self, visible, total):
        if self.current_lang == 'AR':
            txt = f"المعاينة: يعرض {visible} سجل من إجمالي {total}"
        else:
            txt = f"Preview: Showing {visible} of {total} records"
        if hasattr(self, 'records_lbl') and self.records_lbl.winfo_exists():
            self.records_lbl.config(text=txt)
