from tkinter import ttk, messagebox
import pandas as pd
from msales.core.data_handler import DataHandler
from msales.config import COLORS, PERMISSION_CODES
from msales.permissions import save_permission_codes
from msales.core.logger import logger
from typing import Any
import tkinter as tk

class EditorScreenMixin:
    clear_workspace: Any
    update_sidebar_active_state: Any
    refresh_header_info: Any
    workspace_frame: Any
    t: Any
    current_lang: Any
    create_custom_btn: Any
    show_merge_screen: Any
    merged_df: Any
    selected_codes_dict: Any
    data_modified: Any
    av_tree: Any
    sel_tree: Any
    op_type_var: Any
    winfo_x: Any
    winfo_y: Any
    
    def show_editor_screen(self):
        self.clear_workspace()
        self.update_sidebar_active_state('edit')
        self.refresh_header_info()
        self.selected_codes_dict = {}
        
        # 1. Save Row (packed first at bottom)
        footer_frm = tk.Frame(self.workspace_frame, bg=COLORS['bg_main'])
        footer_frm.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))
        
        btn_back = self.create_custom_btn(
            footer_frm,
            text=self.t('back'),
            command=self.show_merge_screen,
            style_type='secondary',
            width=12
        )
        btn_back.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT)
        
        btn_apply = self.create_custom_btn(
            footer_frm,
            text=self.t('apply_changes'),
            command=self.execute_bulk_permission_edit,
            style_type='primary',
            width=22
        )
        btn_apply.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT)
        
        # 2. Operation Control Frame (packed above footer)
        op_card = tk.Frame(self.workspace_frame, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
        op_card.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        op_lbl = tk.Label(
            op_card,
            text=self.t('operation'),
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        )
        op_lbl.pack(fill=tk.X, padx=15, pady=(10, 5))
        
        self.op_type_var = tk.StringVar(value="add")
        
        def _update_sel_tree_colors(*args):
            if hasattr(self, 'sel_tree') and self.sel_tree.winfo_exists():
                color = '#137333' if self.op_type_var.get() == 'add' else '#C5221F'
                self.sel_tree.tag_configure('sel_tag', foreground=color)
                for item in self.sel_tree.get_children():
                    self.sel_tree.item(item, tags=('sel_tag',))
                    
        self.op_type_var.trace_add("write", _update_sel_tree_colors)
        
        r1 = tk.Radiobutton(
            op_card,
            text=self.t('op_add'),
            variable=self.op_type_var,
            value="add",
            font=("Segoe UI", 9),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['bg_card'],
            cursor="hand2"
        )
        r1.pack(anchor=tk.W if self.current_lang == 'EN' else tk.E, padx=25, pady=4)
        
        r2 = tk.Radiobutton(
            op_card,
            text=self.t('op_remove'),
            variable=self.op_type_var,
            value="remove",
            font=("Segoe UI", 9),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            activebackground=COLORS['bg_card'],
            cursor="hand2"
        )
        r2.pack(anchor=tk.W if self.current_lang == 'EN' else tk.E, padx=25, pady=4)
        
        # 3. Dual list box workspace (fills remaining space)
        panels_container = tk.Frame(self.workspace_frame, bg=COLORS['bg_main'])
        panels_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        panels_container.columnconfigure(0, weight=1, uniform="group2")
        panels_container.columnconfigure(1, weight=1, uniform="group2")
        panels_container.rowconfigure(0, weight=1)
        
        # Left Panel (Available Codes)
        left_panel = tk.Frame(panels_container, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
        left_panel.grid(row=0, column=0, padx=(0, 10), sticky="nswe")
        
        left_title = tk.Label(
            left_panel,
            text=self.t('available_codes'),
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        )
        left_title.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # Search entry
        search_av_frame = tk.Frame(left_panel, bg=COLORS['bg_card'], padx=15, pady=5)
        search_av_frame.pack(fill=tk.X)
        self.search_av_entry = tk.Entry(
            search_av_frame,
            font=("Segoe UI", 9),
            bg=COLORS['bg_main'],
            bd=0,
            highlightthickness=1,
            highlightbackground=COLORS['border'],
            highlightcolor=COLORS['primary']
        )
        self.search_av_entry.pack(fill=tk.X, ipady=3)
        self.search_av_entry.insert(0, self.t('search_av_placeholder'))
        self.search_av_entry.bind("<KeyRelease>", self.filter_available_codes_tree)
        
        def focus_in_av(e):
            if self.search_av_entry.get() == self.t('search_av_placeholder'):
                self.search_av_entry.delete(0, tk.END)
        def focus_out_av(e):
            if not self.search_av_entry.get():
                self.search_av_entry.insert(0, self.t('search_av_placeholder'))
                
        self.search_av_entry.bind("<FocusIn>", focus_in_av)
        self.search_av_entry.bind("<FocusOut>", focus_out_av)
        
        # CRUD operations panel (pack first at bottom)
        crud_bar = tk.Frame(left_panel, bg=COLORS['bg_card'], padx=15, pady=10)
        crud_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        btn_add_code = self.create_custom_btn(
            crud_bar,
            text=self.t('add_code'),
            command=self.show_add_code_dialog,
            style_type='success',
            font_size=9
        )
        btn_add_code.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT, padx=3)
        
        btn_del_code = self.create_custom_btn(
            crud_bar,
            text=self.t('delete_code'),
            command=self.delete_selected_code_db,
            style_type='danger',
            font_size=9
        )
        btn_del_code.pack(side=tk.LEFT if self.current_lang == 'EN' else tk.RIGHT, padx=3)

        # Available code list treeview (fills remaining space)
        tree_av_frm = tk.Frame(left_panel, bg=COLORS['bg_card'], padx=15, pady=5)
        tree_av_frm.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        cols_av = ('#', 'Code', 'Desc')
        self.av_tree = ttk.Treeview(tree_av_frm, columns=cols_av, show='headings')
        self.av_tree.heading('#', text="#")
        self.av_tree.heading('Code', text=self.t('permission_codes'))
        self.av_tree.heading('Desc', text=self.t('desc_label'))
        
        self.av_tree.column('#', width=30, anchor=tk.CENTER)
        self.av_tree.column('Code', width=160, anchor=tk.W)
        self.av_tree.column('Desc', width=180, anchor=tk.W)
        
        scr_av = ttk.Scrollbar(tree_av_frm, orient=tk.VERTICAL, command=self.av_tree.yview)
        self.av_tree.configure(yscrollcommand=scr_av.set)
        
        self.av_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scr_av.pack(side=tk.RIGHT, fill=tk.Y)
        self.av_tree.bind("<Double-1>", self.on_available_code_double_click)
        
        # (CRUD bar moved above to fix layout clipping)
        
        # Right Panel (Selected Codes)
        right_panel = tk.Frame(panels_container, bg=COLORS['bg_card'], bd=0, highlightbackground=COLORS['border'], highlightthickness=1)
        right_panel.grid(row=0, column=1, padx=(10, 0), sticky="nswe")
        
        right_title = tk.Label(
            right_panel,
            text=self.t('selected_codes'),
            font=("Segoe UI", 11, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        )
        right_title.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        # Selection treeview
        tree_sel_frm = tk.Frame(right_panel, bg=COLORS['bg_card'], padx=15, pady=5)
        tree_sel_frm.pack(fill=tk.BOTH, expand=True)
        
        self.sel_tree = ttk.Treeview(tree_sel_frm, columns=cols_av, show='headings')
        self.sel_tree.heading('#', text="#")
        self.sel_tree.heading('Code', text=self.t('permission_codes'))
        self.sel_tree.heading('Desc', text=self.t('desc_label'))
        
        self.sel_tree.column('#', width=30, anchor=tk.CENTER)
        self.sel_tree.column('Code', width=160, anchor=tk.W)
        self.sel_tree.column('Desc', width=180, anchor=tk.W)
        
        scr_sel = ttk.Scrollbar(tree_sel_frm, orient=tk.VERTICAL, command=self.sel_tree.yview)
        self.sel_tree.configure(yscrollcommand=scr_sel.set)
        
        self.sel_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scr_sel.pack(side=tk.RIGHT, fill=tk.Y)
        self.sel_tree.bind("<Double-1>", self.on_selected_code_double_click)
        
        # Populate codes
        self.filter_available_codes_tree()

    def filter_available_codes_tree(self, event=None):
        query = self.search_av_entry.get().strip().lower()
        if query == self.t('search_av_placeholder').lower():
            query = ""
            
        for item in self.av_tree.get_children():
            self.av_tree.delete(item)
            
        seq = 1
        for code, desc in PERMISSION_CODES.items():
            if not query or query in code.lower() or query in desc.lower():
                self.av_tree.insert('', tk.END, values=(seq, code, desc))
                seq += 1

    def on_available_code_double_click(self, event):
        selection = self.av_tree.selection()
        if selection:
            values = self.av_tree.item(selection[0])['values']
            code, desc = values[1], values[2]
            
            if code not in self.selected_codes_dict:
                seq = len(self.selected_codes_dict) + 1
                self.selected_codes_dict[code] = desc
                self.sel_tree.insert('', tk.END, values=(seq, code, desc), tags=('sel_tag',))
                self.op_type_var.set(self.op_type_var.get())

    def on_selected_code_double_click(self, event):
        selection = self.sel_tree.selection()
        if selection:
            values = self.sel_tree.item(selection[0])['values']
            code = values[1]
            
            if code in self.selected_codes_dict:
                del self.selected_codes_dict[code]
                self.sel_tree.delete(selection[0])
                
                # Re-index items inside selection treeview
                for idx, item_id in enumerate(self.sel_tree.get_children(), 1):
                    row_vals = self.sel_tree.item(item_id)['values']
                    self.sel_tree.item(item_id, values=(idx, row_vals[1], row_vals[2]))

    def show_add_code_dialog(self):
        """Centered custom dialog to add permission code metadata"""
        self_app: Any = self
        dialog = tk.Toplevel(self_app)
        dialog.title(self.t('add_custom_title'))
        dialog.geometry("420x250")
        dialog.configure(bg=COLORS['bg_main'])
        dialog.resizable(False, False)
        dialog.transient(self_app)
        dialog.grab_set()
        
        # Center coordinates
        parent_x = self.winfo_x()
        parent_y = self.winfo_y()
        dialog.geometry(f"+{parent_x + 150}+{parent_y + 150}")
        
        inner = tk.Frame(dialog, bg=COLORS['bg_card'], padx=20, pady=20)
        inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        lbl_code = tk.Label(
            inner,
            text=self.t('code_label'),
            font=("Segoe UI", 9, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        )
        lbl_code.pack(fill=tk.X, pady=(0, 3))
        
        code_entry = tk.Entry(inner, font=("Segoe UI", 10), bg=COLORS['bg_main'], bd=1, relief=tk.SOLID)
        code_entry.pack(fill=tk.X, ipady=3, pady=(0, 12))
        
        lbl_desc = tk.Label(
            inner,
            text=self.t('desc_label'),
            font=("Segoe UI", 9, "bold"),
            bg=COLORS['bg_card'],
            fg=COLORS['text_primary'],
            anchor=tk.W if self.current_lang == 'EN' else tk.E
        )
        lbl_desc.pack(fill=tk.X, pady=(0, 3))
        
        desc_entry = tk.Entry(inner, font=("Segoe UI", 10), bg=COLORS['bg_main'], bd=1, relief=tk.SOLID)
        desc_entry.pack(fill=tk.X, ipady=3, pady=(0, 18))
        
        def save():
            code_str = code_entry.get().strip()
            desc_str = desc_entry.get().strip()
            if not code_str or not desc_str:
                messagebox.showwarning(self.t('warning'), self.t('fill_all'), parent=dialog)
                return
            
            global PERMISSION_CODES
            if code_str in PERMISSION_CODES:
                messagebox.showerror(self.t('error'), self.t('code_exists').format(code=code_str), parent=dialog)
                return
                
            PERMISSION_CODES[code_str] = desc_str
            if save_permission_codes(PERMISSION_CODES):
                logger.add(f"Code added to DB: {code_str} ({desc_str})", "SUCCESS")
                messagebox.showinfo(self.t('success'), self.t('success'), parent=dialog)
                self.filter_available_codes_tree()
                dialog.destroy()
            else:
                messagebox.showerror(self.t('error'), "Failed writing database file!", parent=dialog)
                
        btn_bar = tk.Frame(inner, bg=COLORS['bg_card'])
        btn_bar.pack(fill=tk.X)
        
        btn_save = self.create_custom_btn(btn_bar, text=self.t('save'), command=save, style_type='success', font_size=9)
        btn_save.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT, padx=3)
        
        btn_cancel = self.create_custom_btn(btn_bar, text=self.t('cancel'), command=dialog.destroy, style_type='secondary', font_size=9)
        btn_cancel.pack(side=tk.RIGHT if self.current_lang == 'EN' else tk.LEFT, padx=3)

    def delete_selected_code_db(self):
        selection = self.av_tree.selection()
        if not selection:
            messagebox.showwarning(self.t('warning'), "Select code in available list first!")
            return
            
        values = self.av_tree.item(selection[0])['values']
        code = values[1]
        
        confirm = messagebox.askyesno(
            self.t('confirm_delete'),
            self.t('confirm_delete_msg').format(code=code)
        )
        if confirm:
            global PERMISSION_CODES
            if code in PERMISSION_CODES:
                del PERMISSION_CODES[code]
                if save_permission_codes(PERMISSION_CODES):
                    logger.add(f"Code deleted from DB: {code}", "SUCCESS")
                    self.filter_available_codes_tree()
                else:
                    messagebox.showerror(self.t('error'), "Failed modifying database configuration file.")

    def execute_bulk_permission_edit(self):
        """Apply modification loop on dataframe values"""
        codes_list = list(self.selected_codes_dict.keys())
        
        # Fallback: if user didn't move codes to the right list, check if they selected any in the left list
        if not codes_list and hasattr(self, 'av_tree') and self.av_tree.selection():
            for item in self.av_tree.selection():
                values = self.av_tree.item(item).get('values')
                if values and len(values) >= 2:
                    codes_list.append(values[1])
                    
        if not codes_list:
            messagebox.showwarning(self.t('warning'), self.t('apply_warning_no_select'))
            return
        op = self.op_type_var.get()
        
        try:
            for idx in range(len(self.merged_df)):
                current = str(self.merged_df.at[idx, 'PERMISSION'])
                if op == "add":
                    updated = DataHandler.add_codes(current, codes_list)
                else:
                    updated = DataHandler.remove_codes(current, codes_list)
                self.merged_df.loc[idx, 'PERMISSION'] = updated
                
            self.data_modified = True
            logger.add(f"Bulk permission editing applied: {op} {codes_list}", "SUCCESS")
            
            # Navigate back to merge screen directly to see modifications
            self.show_merge_screen()
        except Exception as e:
            logger.add(f"Failed bulk changes execution: {str(e)}", "ERROR")
            messagebox.showerror(self.t('error'), f"Operation failure:\n{str(e)}")
