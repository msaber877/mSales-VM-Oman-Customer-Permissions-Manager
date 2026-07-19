"""
Data handler module for processing CSV/Excel and executing the VLOOKUP logic.
Optimized to prevent DtypeWarning through strict memory parsing.
"""

import os
import sys
import pandas as pd
from .logger import logger

class DataHandler:
    """Main data engine for VLOOKUP and Code manipulation"""
    
    # قائمة الترميزات المعتمدة لدعم كافة أنظمة تصدير البيانات دون تشويه النصوص العربية
    ENCODINGS = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    
    @staticmethod
    def read_csv(filepath):
        """Read CSV file with multiple encoding support and full data type preservation"""
        for encoding in DataHandler.ENCODINGS:
            try:
                # الفحص الفني: إضافة low_memory=False لإجبار بايثون على تحليل الملف كاملاً 
                # دفعة واحدة قبل اتخاذ قرار التنميط، مما يقضي تماماً على تداخل الأنواع والـ DtypeWarning.
                df = pd.read_csv(filepath, encoding=encoding, low_memory=False)
                logger.add(f"CSV loaded: {os.path.basename(filepath)} ({encoding})", "SUCCESS")
                return df
            except Exception as e:
                # استمرار المحاولة مع الترميزات البديلة في حال فشل الترميز الحالي
                continue
                
        raise Exception("Failed to read CSV file. Please check file formatting or permissions.")
    
    @staticmethod
    def read_excel(filepath):
        """Read Excel file using explicit structural loaders"""
        try:
            df = pd.read_excel(filepath)
            logger.add(f"Excel loaded: {os.path.basename(filepath)}", "SUCCESS")
            return df
        except Exception as e:
            logger.add(f"Error reading Excel: {str(e)}", "ERROR")
            raise
    
    @staticmethod
    def normalize_separators(value):
        """Convert separators from - to , and clean structural spaces"""
        if pd.isna(value) or str(value).strip() == "":
            return []
        normalized = str(value).replace('-', ',').replace('#NAME?', '')
        codes = [c.strip() for c in normalized.split(',') if c.strip()]
        return codes
    
    @staticmethod
    def vlookup_merge(customers_df, dealers_df):
        """VLOOKUP operation with improved matching and defensive column validation"""
        logger.add("Starting VLOOKUP matching algorithm...", "INFO")
        
        # حماية دفاعية لضمان سلامة الهيكل البرمجي قبل معالجة مصفوفة البيانات
        if 'CODE' not in customers_df.columns or 'CF_PERMISSION' not in customers_df.columns:
            raise ValueError("Customer CSV file must contain 'CODE' and 'CF_PERMISSION' columns.")
        
        dealer_col = dealers_df.columns[0]
        
        dealer_codes_raw = dealers_df[dealer_col].dropna().tolist()
        customer_codes_raw = customers_df['CODE'].tolist()
        
        # توحيد كافة المعرفات إلى نصوص نظيفة ومجردة من الفراغات لضمان نجاح عملية الربط (Matching)
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
            
            # فحص المطابقة الهيكلية عبر مقارنة النصوص الموحدة
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
        """Add new codes safely without introducing structural duplicates"""
        current = DataHandler.normalize_separators(current_codes_str)
        for code in new_codes:
            if code not in current:
                current.append(code)
        return ','.join(current)
    
    @staticmethod
    def remove_codes(current_codes_str, codes_to_remove):
        """Remove specified codes from the permission string"""
        current = DataHandler.normalize_separators(current_codes_str)
        filtered = [c for c in current if c not in codes_to_remove]
        return ','.join(filtered)

# ===========================================================================================
# MODERN ENTERPRISE BILINGUAL GUI
# ===========================================================================================