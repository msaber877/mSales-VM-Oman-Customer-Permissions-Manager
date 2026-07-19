"""
Configuration module containing constants, colors, and translations.
"""

from msales.permissions import load_permission_codes

PERMISSION_CODES = load_permission_codes()

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
