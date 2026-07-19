"""
Author: Mohamed Saber
Project: mSales Data Lounge Infrastructure (2026)
File: main.py
Description: Secure, localized application entry point embedded with global exception handling layers.
"""

import os
import sys
import traceback
from datetime import datetime

# إعداد مسار محلي صلب لتخزين ملف سجل الأخطاء داخل نفس المجلد الحاضن
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "debug_error.log")

def global_exception_logger(ex_type, ex_value, ex_traceback):
    """
    التقاط وتحويل كافة الاستثناءات غير المعالجة في النظام وحفظها في سجل محلي مع إظهار نافذة خطأ آمنة.
    """
    # منع معالجة إنهاء البرنامج الطبيعي كخطأ
    if issubclass(ex_type, KeyboardInterrupt):
        sys.__excepthook__(ex_type, ex_value, ex_traceback)
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = "".join(traceback.format_exception(ex_type, ex_value, ex_traceback))
    
    # 1. كتابة تفاصيل الاستثناء بالكامل في ملف اللوق المحلي بشكل آمن
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n{'='*60}\n")
            log_file.write(f"TIMESTAMP: {timestamp}\n")
            log_file.write(f"EXCEPTION TYPE: {ex_type.__name__}\n")
            log_file.write(f"CRITICAL ERROR DETAILS:\n{error_message}")
            log_file.write(f"{'='*60}\n")
    except Exception as io_err:
        print(f"Critical: Failed to write to log file: {io_err}", file=sys.stderr)

    # 2. محاولة عرض صندوق أخطاء للمستخدم عبر Tkinter دون التسبب في تعليق الواجهة الأساسية
    try:
        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية الفارغة
        messagebox.showerror(
            "Application Critical Error",
            f"An unhandled system exception occurred.\n\nType: {ex_type.__name__}\nDetails saved locally to:\n{LOG_FILE_PATH}"
        )
        root.destroy()
    except Exception:
        # خطة بديلة في حال كان الانهيار في نواة الجرافيكس نفسها
        print(f"[-] Native UI Crash. Log generated successfully at {LOG_FILE_PATH}", file=sys.stderr)

# إجبار نظام تشغيل بايثون على تمرير كافة الاستثناءات العامة عبر الدالة المعالجة الخاصة بنا
sys.excepthook = global_exception_logger


def start_application():
    """
    استدعاء وإقلاع الواجهة البرمجية الأساسية لتطبيق mSales بعد تأمين البيئة
    """
    print("[+] Core engine initiated. Verifying modular context paths...")
    
    # إضافة المجلد الحالي ومجلد الـ msales لـ sys.path ديناميكياً لتفادي ModuleNotFoundError
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)

    # استدعاء كلاس التطبيق الرئيسي الموزع داخل الموديل المستقر
    from msales.ui.app_core import mSalesApp
    
    # تشغيل التطبيق الفعلي داخل سياق معالجة الأخطاء المحلي
    app = mSalesApp()
    app.mainloop()


if __name__ == "__main__":
    print(f"[+] Initializing mSales Isolation Flow strictly inside: {BASE_DIR}")
    # تشغيل المحرك الرئيسي للتطبيق
    start_application()