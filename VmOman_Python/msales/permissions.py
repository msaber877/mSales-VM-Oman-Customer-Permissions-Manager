import os
import json

def load_permission_codes():
    """
    Load permission codes from the local JSON file.
    If the file does not exist, it creates one with default codes.
    
    Returns:
        dict: A dictionary mapping permission code identifiers to their descriptions.
    """
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
        except Exception:
            return default_codes
    else:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(default_codes, f, indent=4, ensure_ascii=False)
        except Exception:
            pass
        return default_codes

def save_permission_codes(codes):
    """
    Save the given permission codes dictionary to the local JSON file.
    
    Args:
        codes (dict): The dictionary of permission codes to save.
        
    Returns:
        bool: True if saving was successful, False otherwise.
    """
    filename = "permission_codes.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(codes, f, indent=4, ensure_ascii=False)
        return True
    except Exception:
        return False
