#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mSales Data Merger & Permission Codes Editor
VM-Oman Edition v3.5 - ENTERPRISE MODERN GUI
Author: IT Team - EME International
Version: 3.5.0 (Modern Dashboard, Bilingual, Drag & Drop, Searchable Views)
"""

import sys
import io
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
from datetime import datetime
import traceback
import json
from tkinterdnd2 import DND_FILES, TkinterDnD

# Fix for Windows Unicode encoding in console
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except:
        pass

# ===========================================================================================
# PERMISSION CODES DATABASE (DYNAMIC VIA JSON)
# ===========================================================================================

def load_permission_codes():
    filename = "permission_codes.json"
    default_codes = {
        "SR_PERMISSION_CODE.a": "Eload",
        "SR_PERMISSION_CODE.b": "DST Channel",
        "SR_PERMISSION_CODE.c": "Activation",
        "SR_PERMISSION_CODE.d": "SIM Replacement",
        "SR_PERMISSION_CODE.e": "Portin",
        "SR_PERMISSION_CODE.f": "Offline Activation",
        "SR_PERMISSION_CODE.g": "SIM Upgrade",
        "SR_PERMISSION_CODE.h": "Dealer Activation",
        "SR_PERMISSION_CODE.i": "Change Ownership",
        "SR_PERMISSION_CODE.j": "Update ID",
        "SR_PERMISSION_CODE.k": "Vanity Change Owner",
        "SR_PERMISSION_CODE.l": "Show Commission Amounts",
        "SR_PERMISSION_CODE.m": "Commission Structure",
        "SR_PERMISSION_CODE.n": "Dealer Migration",
        "SR_PERMISSION_CODE.o": "E-Wallet",
        "SR_PERMISSION_CODE.p": "Product Selling",
        "SR_PERMISSION_CODE.q": "Dealer Sim Replacement",
        "SR_PERMISSION_CODE.r": "ESIM",
        "SR_PERMISSION_CODE.s": "Recharge-Required Activation Exemption",
        "OpSIMPriceExemption": "Sim Price Exemption",
        "OpPortInManualApprovalOption": "Portin Manual Approval Option",
        "OpIDStatusCheck": "ID Status Check",
        "OpBulkPortIn": "Bulk PortIn"
    }
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            return default_codes
    else:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(default_codes, f, indent=4, ensure_ascii=False)
        except Exception as e:
            pass
        return default_codes

def save_permission_codes(codes):
    filename = "permission_codes.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(codes, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        return False

PERMISSION_CODES = load_permission_codes()

# ===========================================================================================
# MODERN SYSTEM COLORS & THEME
# ===========================================================================================

COLORS = {
    # Left Sidebar (Dark Slate Theme)
    'sidebar_bg': '#0F172A',
    'sidebar_hover': '#1E293B',
    'sidebar_selected': '#0EA5E9',
    'sidebar_text': '#F8FAFC',
    
    # Core Palette
    'primary': '#0EA5E9',           # Vibrant Sky Blue
    'primary_hover': '#38BDF8',
    'bg_main': '#F1F5F9',           # Cool slate light-gray
    'bg_card': '#FFFFFF',           # Pure White panels
    'border': '#E2E8F0',            # Thin borders
    
    # Text colors
    'text_primary': '#0F172A',      # Dark Slate
    'text_secondary': '#64748B',    # Muted Slate
    'text_muted': '#94A3B8',
    'text_light': '#FFFFFF',
    
    # Status colors
    'success': '#10B981',           # Emerald Green
    'success_bg': '#D1FAE5',
    'warning': '#F59E0B',           # Amber Orange
    'warning_bg': '#FEF3C7',
    'danger': '#F43F5E',            # Rose Red
    'danger_bg': '#FFE4E6',
    
    # Logs Terminal (Retro Slate-Dark)
    'console_bg': '#0B0F19',
    'console_fg': '#34D399',
}

# ===========================================================================================
# TRANSLATIONS DICTIONARY (BILINGUAL INTERFACE)
# ===========================================================================================

TRANSLATIONS = {
    'EN': {
        'app_title': "mSales Data Merger & Permission Editor",
        'home': "🏠 Home",
        'upload': "📂 Upload Files",
        'merge_results': "🔄 Merge Preview",
        'edit_permissions': "✏️ Bulk Edit",
        'export': "💾 Export Data",
        'quick_start': "🚀 Quick Start Guide",
        'quick_start_desc': "Merge customer & dealer files and update permissions in minutes:\n\n• Automatic VLOOKUP matching on Dealer Codes.\n• Add or remove permissions globally with dynamic database.\n• Exclude status column instantly for clean export.\n• Real-time log terminal and searchable results preview.",
        'start_btn': "▶ Start Processing",
        'select_files_title': "Select Input Data Files",
        'select_files_sub': "Drag & Drop or browse to load files",
        'customer_file': "📄 Customer File (CSV)",
        'dealer_file': "📊 Dealer File (Excel)",
        'drag_drop_csv': "Drag & Drop Customer CSV file here\n(or click to browse)",
        'drag_drop_excel': "Drag & Drop Dealer Excel file here\n(or click to browse)",
        'no_file': "No file loaded",
        'loaded': "✓ Loaded: {filename} ({rows} rows)",
        'error_load': "Failed to read file",
        'next': "Next Step ▶",
        'back': "◀ Back",
        'total_codes': "Total Records",
        'matched': "Matched",
        'not_found': "Not Found",
        'success_rate': "Match Success Rate",
        'dealer_code': "Dealer Code",
        'permission_codes': "Permission Codes",
        'before_permissions': "Before Modification",
        'after_permissions': "After Modification",
        'change': "Change / Diff",
        'status': "Matching Status",
        'edit_codes_btn': "✏️ Bulk Edit Permissions",
        'save_results_btn': "💾 Export Matched Data",
        'available_codes': "📋 Available Permissions",
        'selected_codes': "✓ Selected for Action",
        'search_placeholder': "Search dealer code...",
        'search_av_placeholder': "Search permissions...",
        'add_code': "➕ Add New Code",
        'delete_code': "🗑️ Delete Code",
        'operation': "⚙️ Bulk Operation Type",
        'op_add': "➕ Add selected codes to all matching rows",
        'op_remove': "➖ Remove selected codes from all matching rows",
        'apply_changes': "⚡ Apply Bulk Edit",
        'system_logs': "System Logs Terminal",
        'show_logs': "💻 Show Logs",
        'hide_logs': "💻 Hide Logs",
        'confirm_delete': "Confirm Deletion",
        'confirm_delete_msg': "Are you sure you want to delete permission code '{code}'?",
        'warning': "Warning",
        'error': "Error",
        'success': "Success",
        'fill_all': "Please fill in all fields!",
        'code_exists': "Code '{code}' already exists in DB!",
        'add_custom_title': "Add Custom Permission",
        'code_label': "Permission Code String:",
        'desc_label': "Service Description:",
        'save': "Save Code",
        'cancel': "Cancel",
        'apply_warning_no_select': "Please select at least one permission code first!",
        'apply_success': "Bulk update applied on {rows} records.\n\nVerify changes in the Preview screen.",
        'save_success': "Data saved successfully to:\n{path}\n\nTotal lines: {rows}\nColumns: CODE, PERMISSION",
        'export_title': "Export Clean Results",
        'export_sub': "Save final matched file without status markers",
        'export_card_title': "Dataset Ready for Save",
        'export_desc': "The application has matched {rows} dealer records. The 'STATUS' flag column is discarded automatically during save for seamless upload systems.",
        'export_format': "Choose Save Format",
        'save_and_export': "💾 Save & Export Dataset",
        'log_ready': "Application workspace initialized."
    },
    'AR': {
        'app_title': "مدمج بيانات mSales ومحرر الصلاحيات",
        'home': "🏠 الرئيسية",
        'upload': "📂 رفع الملفات",
        'merge_results': "🔄 معاينة النتائج",
        'edit_permissions': "✏️ تعديل جماعي",
        'export': "💾 تصدير النتائج",
        'quick_start': "🚀 دليل البدء السريع",
        'quick_start_desc': "قم بدمج ملفات العملاء والتجار ومعالجة الصلاحيات في دقائق قليلة:\n\n• مطابقة تلقائية باستخدام VLOOKUP بناءً على كود التاجر.\n• إضافة أو إزالة الصلاحيات جماعياً من خلال قاعدة بيانات مرنة.\n• استبعاد عمود الحالة تلقائياً عند الحفظ لضمان سرعة الرفع والقبول.\n• لوحة سجلات فورية وجدول معاينة متطور يدعم البحث والتصفية.",
        'start_btn': "▶ ابدأ المعالجة",
        'select_files_title': "تحديد ملفات البيانات المدخلة",
        'select_files_sub': "اسحب وأسقط الملفات أو تصفح لاختيارها",
        'customer_file': "📄 ملف العملاء (CSV)",
        'dealer_file': "📊 ملف التجار (Excel)",
        'drag_drop_csv': "اسحب وأسقط ملف العملاء CSV هنا\n(أو انقر لتصفح المجلدات)",
        'drag_drop_excel': "اسحب وأسقط ملف التجار Excel هنا\n(أو انقر لتصفح المجلدات)",
        'no_file': "لم يتم تحميل أي ملف",
        'loaded': "✓ تم التحميل: {filename} ({rows} سجل)",
        'error_load': "فشل في قراءة الملف المدخل",
        'next': "الخطوة التالية ◀",
        'back': "◀ السابق",
        'total_codes': "إجمالي السجلات",
        'matched': "المطابقة",
        'not_found': "غير الموجودة",
        'success_rate': "نسبة نجاح المطابقة",
        'dealer_code': "كود التاجر",
        'permission_codes': "أكواد الصلاحيات",
        'before_permissions': "قبل التعديل",
        'after_permissions': "بعد التعديل",
        'change': "التعديل",
        'status': "حالة المطابقة",
        'edit_codes_btn': "✏️ تعديل جماعي للصلاحيات",
        'save_results_btn': "💾 تصدير وحفظ النتائج",
        'available_codes': "📋 الصلاحيات المتاحة بالبرنامج",
        'selected_codes': "✓ الصلاحيات المحددة للتعديل",
        'search_placeholder': "بحث بكود التاجر...",
        'search_av_placeholder': "بحث في الصلاحيات...",
        'add_code': "➕ إضافة كود جديد",
        'delete_code': "🗑️ حذف الكود المحدد",
        'operation': "⚙️ نوع التعديل الجماعي",
        'op_add': "➕ إضافة الصلاحيات المحددة لكافة السجلات المطابقة",
        'op_remove': "➖ إزالة الصلاحيات المحددة من كافة السجلات المطابقة",
        'apply_changes': "⚡ تطبيق التعديل الجماعي",
        'system_logs': "لوحة سجل العمليات الفورية",
        'show_logs': "💻 عرض السجل",
        'hide_logs': "💻 إخفاء السجل",
        'confirm_delete': "تأكيد الحذف",
        'confirm_delete_msg': "هل أنت متأكد من حذف كود الصلاحية '{code}' نهائياً؟",
        'warning': "تحذير",
        'error': "خطأ",
        'success': "نجاح",
        'fill_all': "يرجى تعبئة كافة الحقول المطلوبة!",
        'code_exists': "كود الصلاحية '{code}' موجود بالفعل بقاعدة البيانات!",
        'add_custom_title': "إضافة كود صلاحية مخصص",
        'code_label': "كود الصلاحية (Permission Code):",
        'desc_label': "وصف الخدمة (Description):",
        'save': "حفظ الكود",
        'cancel': "إلغاء",
        'apply_warning_no_select': "برجاء اختيار كود صلاحية واحد على الأقل أولاً!",
        'apply_success': "تم تطبيق التحديث الجماعي بنجاح على {rows} سجل.\n\nبرجاء مراجعة التغييرات في شاشة المعاينة.",
        'save_success': "تم حفظ البيانات بنجاح إلى المسار:\n{path}\n\nإجمالي الأسطر: {rows}\nالأعمدة المحفوظة: CODE, PERMISSION",
        'export_title': "تصدير وحفظ النتائج النظيفة",
        'export_sub': "حفظ الملف النهائي بدون أعمدة الحالة لضمان التوافقية",
        'export_card_title': "البيانات جاهزة تماماً للتصدير",
        'export_desc': "تمت مطابقة {rows} من سجلات التجار. سيتم استبعاد عمود الحالة (STATUS) تلقائياً عند حفظ الملف ليكون جاهزاً للرفع على الأنظمة التشغيلية مباشرة.",
        'export_format': "اختر صيغة الملف المصدر",
        'save_and_export': "💾 حفظ وتصدير الملف",
        'log_ready': "تم تشغيل بيئة عمل برنامج mSales بنجاح."
    }
}

# ===========================================================================================
# LOGGER SYSTEM
# ===========================================================================================

class Logger:
    """Event logging system with callback dispatch"""
    def __init__(self):
        self.logs = []
        self.callbacks = []
    
    def add(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        icons = {"INFO": "ℹ", "SUCCESS": "✓", "WARNING": "⚠", "ERROR": "✗"}
        entry = f"[{timestamp}] {icons.get(level, '•')} {message}"
        self.logs.append(entry)
        try:
            print(entry)
        except:
            pass
        for callback in self.callbacks:
            try:
                callback(entry, level)
            except:
                pass
    
    def get_all(self):
        return "\n".join(self.logs)

logger = Logger()

# ===========================================================================================
# DATA PROCESSING HANDLER
# ===========================================================================================

class DataHandler:
    """Main data engine for VLOOKUP and Code manipulation"""
    
    ENCODINGS = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    @staticmethod
    def read_csv(filepath):
        """Read CSV file with multiple encoding support"""
        for encoding in DataHandler.ENCODINGS:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                logger.add(f"CSV loaded: {os.path.basename(filepath)} ({encoding})", "SUCCESS")
                return df
            except:
                continue
        raise Exception("Failed to read CSV file. Please check file formatting.")
    
    @staticmethod
    def read_excel(filepath):
        """Read Excel file"""
        try:
            df = pd.read_excel(filepath)
            logger.add(f"Excel loaded: {os.path.basename(filepath)}", "SUCCESS")
            return df
        except Exception as e:
            logger.add(f"Error reading Excel: {str(e)}", "ERROR")
            raise
    
    @staticmethod
    def normalize_separators(value):
        """Convert separators from - to , and clean spaces"""
        if pd.isna(value) or str(value).strip() == "":
            return []
        normalized = str(value).replace('-', ',').replace('#NAME?', '')
        codes = [c.strip() for c in normalized.split(',') if c.strip()]
        return codes
    
    @staticmethod
    def vlookup_merge(customers_df, dealers_df):
        """VLOOKUP operation with improved matching"""
        logger.add("Starting VLOOKUP matching algorithm...", "INFO")
        
        if 'CODE' not in customers_df.columns or 'CF_PERMISSION' not in customers_df.columns:
            raise ValueError("Customer CSV file must contain 'CODE' and 'CF_PERMISSION' columns.")
        
        dealer_col = dealers_df.columns[0]
        
        dealer_codes_raw = dealers_df[dealer_col].dropna().tolist()
        customer_codes_raw = customers_df['CODE'].tolist()
        
        dealer_codes_normalized = [str(c).strip() for c in dealer_codes_raw]
        customer_codes_normalized = [str(c).strip() for c in customer_codes_raw]
        
        dealer_codes_set = set(dealer_codes_normalized)
        customer_codes_set = set(customer_codes_normalized)
        
        intersection = dealer_codes_set & customer_codes_set
        
        logger.add(f"Customer records: {len(customer_codes_set)} unique codes", "INFO")
        logger.add(f"Dealer records: {len(dealer_codes_set)} unique codes", "INFO")
        logger.add(f"Matched intersection size: {len(intersection)} codes", "INFO")
        
        results = []
        matched_count = 0
        unmatched_count = 0
        
        for idx, dealer_code in enumerate(dealer_codes_raw, 1):
            dealer_code_str = str(dealer_code).strip()
            
            matching = customers_df[
                customers_df['CODE'].astype(str).str.strip() == dealer_code_str
            ]
            
            if len(matching) > 0:
                permission_raw = matching.iloc[0]['CF_PERMISSION']
                permission_normalized = ','.join(
                    DataHandler.normalize_separators(permission_raw)
                )
                
                results.append({
                    'CODE': dealer_code,
                    'PERMISSION': permission_normalized,
                    'ORIGINAL_PERMISSION': permission_normalized,
                    'STATUS': 'Matched'
                })
                matched_count += 1
            else:
                results.append({
                    'CODE': dealer_code,
                    'PERMISSION': '',
                    'ORIGINAL_PERMISSION': '',
                    'STATUS': 'Not Found'
                })
                unmatched_count += 1
        
        logger.add(f"VLOOKUP complete. Matched: {matched_count}, Unmatched: {unmatched_count}", "SUCCESS")
        return pd.DataFrame(results)
    
    @staticmethod
    def add_codes(current_codes_str, new_codes):
        """Add new codes without duplicates"""
        current = DataHandler.normalize_separators(current_codes_str)
        for code in new_codes:
            if code not in current:
                current.append(code)
        return ','.join(current)
    
    @staticmethod
    def remove_codes(current_codes_str, codes_to_remove):
        """Remove specified codes"""
        current = DataHandler.normalize_separators(current_codes_str)
        filtered = [c for c in current if c not in codes_to_remove]
        return ','.join(filtered)

# ===========================================================================================
# MODERN ENTERPRISE BILINGUAL GUI
# ===========================================================================================

class mSalesApp(TkinterDnD.Tk):
    """Modern Desktop Dashboard Application for VM-Oman"""
    
    def __init__(self):
        super().__init__()
        
        # Configure root properties
        self.title("mSales -VM Oman Customer Permissions Manager")
        self.geometry("1300x820")
        self.minsize(1080, 720)
        self.configure(bg=COLORS['bg_main'])
        
        # Application state
        self.current_lang = 'EN'  # Default language: English
        self.active_step = 'home'
        self.logs_visible = True
        
        self.customers_df = None
        self.dealers_df = None
        self.merged_df = None
        self.csv_path = None
        self.excel_path = None
        self.selected_codes_dict = {}
        self.data_modified = False
        
        # UI Elements pointers
        self.sidebar_frame = None
        self.nav_buttons = {}
        self.main_container = None
        
        self.header_frame = None
        self.header_title = None
        self.header_subtitle = None
        self.header_text_inner = None
        self.header_btn_inner = None
        self.lang_btn = None
        self.logs_btn = None
        
        self.workspace_frame = None
        self.console_frame = None
        self.console_text = None
        
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
        self.console_text.configure(yscroll=scrollbar.set)
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

    # ===========================================================================================
    # FRAME WORKSPACE NAVIGATION LOGIC
    # ===========================================================================================

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

    # ===========================================================================================
    # SCREEN 1: LANDING/HOME VIEW
    # ===========================================================================================

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

    # ===========================================================================================
    # SCREEN 2: FILE UPLOAD (DRAG & DROP ZONE)
    # ===========================================================================================

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
        canvas.drop_target_register(DND_FILES)
        canvas.dnd_bind('<<Drop>>', lambda e, ft=file_type: self.on_file_drop(e, ft))
        canvas.dnd_bind('<<DragEnter>>', lambda e, cv=canvas, tk_key=drag_key: self.on_drag_enter(e, cv, tk_key))
        canvas.dnd_bind('<<DragLeave>>', lambda e, cv=canvas, tk_key=drag_key: self.on_drag_leave(e, cv, tk_key))
        
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

    # ===========================================================================================
    # SCREEN 3: VLOOKUP MERGE PREVIEW & REAL-TIME SEARCHING
    # ===========================================================================================

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
        self.tree.configure(yscroll=scr.set)
        
        scr_x = ttk.Scrollbar(table_frm, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=scr_x.set)
        
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

    # ===========================================================================================
    # SCREEN 4: BULK PERMISSION EDITOR VIEW WITH DYNAMIC SEARCH
    # ===========================================================================================

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
        
        # Available code list treeview
        tree_av_frm = tk.Frame(left_panel, bg=COLORS['bg_card'], padx=15, pady=5)
        tree_av_frm.pack(fill=tk.BOTH, expand=True)
        
        cols_av = ('#', 'Code', 'Desc')
        self.av_tree = ttk.Treeview(tree_av_frm, columns=cols_av, show='headings')
        self.av_tree.heading('#', text="#")
        self.av_tree.heading('Code', text=self.t('permission_codes'))
        self.av_tree.heading('Desc', text=self.t('desc_label'))
        
        self.av_tree.column('#', width=30, anchor=tk.CENTER)
        self.av_tree.column('Code', width=160, anchor=tk.W)
        self.av_tree.column('Desc', width=180, anchor=tk.W)
        
        scr_av = ttk.Scrollbar(tree_av_frm, orient=tk.VERTICAL, command=self.av_tree.yview)
        self.av_tree.configure(yscroll=scr_av.set)
        
        self.av_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scr_av.pack(side=tk.RIGHT, fill=tk.Y)
        self.av_tree.bind("<Double-1>", self.on_available_code_double_click)
        
        # CRUD operations panel
        crud_bar = tk.Frame(left_panel, bg=COLORS['bg_card'], padx=15, pady=10)
        crud_bar.pack(fill=tk.X)
        
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
        self.sel_tree.configure(yscroll=scr_sel.set)
        
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
        dialog = tk.Toplevel(self)
        dialog.title(self.t('add_custom_title'))
        dialog.geometry("420x250")
        dialog.configure(bg=COLORS['bg_main'])
        dialog.resizable(False, False)
        dialog.transient(self)
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
        if not self.selected_codes_dict:
            messagebox.showwarning(self.t('warning'), self.t('apply_warning_no_select'))
            return
            
        codes_list = list(self.selected_codes_dict.keys())
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
            
            messagebox.showinfo(
                self.t('success'),
                self.t('apply_success').format(rows=len(self.merged_df))
            )
            self.show_merge_screen()
        except Exception as e:
            logger.add(f"Failed bulk changes execution: {str(e)}", "ERROR")
            messagebox.showerror(self.t('error'), f"Operation failure:\n{str(e)}")

    # ===========================================================================================
    # SCREEN 5: EXPORT HUB VIEW
    # ===========================================================================================

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

    # ===========================================================================================
    # CUSTOM STYLED UTILITY WIDGETS & LAYOUT BUILDERS
    # ===========================================================================================

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
            self.console_text.insert(tk.END, log_entry + "\n", tag)
            self.console_text.see(tk.END)
            self.console_text.config(state=tk.DISABLED)

# ===========================================================================================
# SYSTEM MAIN ENTRY POINT
# ===========================================================================================

if __name__ == "__main__":
    try:
        logger.add("="*75, "INFO")
        logger.add("mSales Data Merger v3.5 - MODERN ENTERPRISE EDITION", "INFO")
        logger.add("="*75, "INFO")
        
        app = mSalesApp()
        app.mainloop()
        
    except Exception as e:
        logger.add(f"Fatal system crash: {str(e)}", "ERROR")
        logger.add(traceback.format_exc(), "ERROR")