#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الإصدار الكامل مع Streamlit
TAM Smart Cultural Platform - Full Version with Streamlit

المميزات:
- دعم جميع البحور (16 بحر)
- دعم جميع الأنواع (تام، مجزوء، مشطور، منهوك، مربع، مضارع...)
- دعم جميع الزحافات (خبن، طي، إقامة، تسهيل، كسر، إعلال، إبدال)
- تقطيع صوتي دقيق
- تحليل القصيدة كاملة
- تصحيح تلقائي
- واجهة تفاعلية جميلة مع Streamlit
"""

# ═══ تثبيت المكتبات ═══
import subprocess
import sys

def install_packages():
    packages = ['streamlit', 'pandas', 'numpy', 'plotly']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            print(f"جاري تثبيت {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

install_packages()

# ═══ المكتبات ═══
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple
import re
import json
from collections import defaultdict

# ═══ إعدادات الصفحة ═══
st.set_page_config(
    page_title="منصة تام الثقافية الذكية",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══ CSS مخصص للتصميم العصري ═══
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        font-family: 'Noto Naskh Arabic', serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 15px 32px;
        font-size: 18px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 10px 0;
    }
    
    .poem-text {
        font-size: 24px;
        line-height: 2;
        text-align: center;
        color: #ffffff;
        background: rgba(0, 0, 0, 0.3);
        padding: 30px;
        border-radius: 15px;
        border-right: 5px solid #f5576c;
        margin: 20px 0;
        font-family: 'Noto Naskh Arabic', serif;
    }
    
    .analysis-result {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .tafeela-box {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        margin: 5px;
        border-radius: 25px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .fault-badge {
        display: inline-block;
        padding: 5px 15px;
        margin: 3px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
    }
    
    .fault-acceptable {
        background: #ffd93d;
        color: #333;
    }
    
    .fault-critical {
        background: #ff6b6b;
        color: white;
    }
    
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        margin: 20px 0;
    }
    
    .header-title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #ffffff;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 10px;
        font-family: 'Noto Naskh Arabic', serif;
    }
    
    .subtitle {
        font-size: 20px;
        text-align: center;
        color: rgba(255,255,255,0.9);
        margin-bottom: 30px;
    }
    
    .sidebar-title {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .info-box {
        background: rgba(255, 255, 255, 0.1);
        border-left: 4px solid #f5576c;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ═══ نماذج البيانات ═══
@dataclass
class ShatrAnalysis:
    original_text: str = ""
    arudi_text: str = ""
    binary_code: str = ""
    tafeelat: List[Dict] = field(default_factory=list)
    meter_name: Optional[str] = None
    meter_type: Optional[str] = None
    faults: List[Dict] = field(default_factory=list)
    confidence: float = 0.0
    is_valid: bool = False
    suggested_correction: Optional[str] = None

@dataclass
class PoemAnalysis:
    verses: List[ShatrAnalysis] = field(default_factory=list)
    unified_meter: Optional[str] = None
    meter_type: Optional[str] = None
    overall_confidence: float = 0.0
    is_monorhyme: bool = True

# ═══ محرك المعالجة العربية المتقدم ═══
class ArabicTextEngine:
    """محرك متقدم لمعالجة النصوص العربية"""
    
    ARABIC_LETTERS = {
        'ا': {'name': 'ألف', 'is_vowel': True, 'is_long': True},
        'ب': {'name': 'باء'}, 'ت': {'name': 'تاء'}, 'ث': {'name': 'ثاء'},
        'ج': {'name': 'جيم'}, 'ح': {'name': 'حاء'}, 'خ': {'name': 'خاء'},
        'د': {'name': 'دال'}, 'ذ': {'name': 'ذال'},
        'ر': {'name': 'راء', 'is_qalqala': True},
        'ز': {'name': 'زاي'}, 'س': {'name': 'سين'}, 'ش': {'name': 'شين'},
        'ص': {'name': 'صاد'},
        'ض': {'name': 'ضاد', 'is_qalqala': True},
        'ط': {'name': 'طاء', 'is_qalqala': True},
        'ظ': {'name': 'ظاء'}, 'ع': {'name': 'عين'}, 'غ': {'name': 'غين'},
        'ف': {'name': 'فاء'},
        'ق': {'name': 'قاف', 'is_qalqala': True},
        'ك': {'name': 'كاف'}, 'ل': {'name': 'لام'}, 'م': {'name': 'ميم'},
        'ن': {'name': 'نون'}, 'ه': {'name': 'هاء'},
        'و': {'name': 'واو', 'is_vowel': True, 'is_long': True},
        'ي': {'name': 'ياء', 'is_vowel': True, 'is_long': True},
        'ى': {'name': 'ألف مقصورة', 'is_vowel': True, 'is_long': True},
        'ة': {'name': 'تاء مربوطة'}, 'ء': {'name': 'همزة'},
        'ؤ': {'name': 'همزة على واو'}, 'ئ': {'name': 'همزة على ياء'},
        'إ': {'name': 'ألف همزة تحت', 'is_vowel': True},
        'أ': {'name': 'ألف همزة فوق', 'is_vowel': True},
        'آ': {'name': 'ألف مد', 'is_vowel': True, 'is_long': True},
    }
    
    HARAKAT = {
        'َ': {'name': 'فتحة', 'type': 'mutaharrik', 'weight': 1},
        'ُ': {'name': 'ضمة', 'type': 'mutaharrik', 'weight': 1},
        'ِ': {'name': 'كسرة', 'type': 'mutaharrik', 'weight': 1},
        'ْ': {'name': 'سكون', 'type': 'sakin', 'weight': 0},
        'ّ': {'name': 'شدة', 'type': 'shadda', 'weight': 2},
        'ً': {'name': 'تنوين فتح', 'type': 'tanween', 'weight': 2},
        'ٌ': {'name': 'تنوين ضم', 'type': 'tanween', 'weight': 2},
        'ٍ': {'name': 'تنوين كسر', 'type': 'tanween', 'weight': 2},
        'ٰ': {'name': 'ألف مد علية', 'type': 'long_vowel', 'weight': 0},
        'ٓ': {'name': 'مد', 'type': 'madd', 'weight': 0},
    }

    @classmethod
    def normalize_text(cls, text: str) -> str:
        """تطبيع شامل للنص العربي"""
        if not text:
            return ""
        
        # إزالة التطويل
        text = text.replace('\u0640', '')
        
        # توحيد الهمزات
        hamza_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا', 'ؤ': 'و', 'ئ': 'ي'}
        for old, new in hamza_map.items():
            text = text.replace(old, new)
        
        # توحيد التاءات
        text = text.replace('ة', 'ه')
        
        # إزالة الأحرف غير العربية
        allowed = set(cls.ARABIC_LETTERS.keys()) | set(cls.HARAKAT.keys()) | {' ', '\n', '\t', '،', '.', '؛', '؟'}
        text = ''.join(c for c in text if c in allowed)
        
        return ' '.join(text.split())

    @classmethod
    def tokenize_phonetic(cls, text: str) -> List[Dict]:
        """تقطيع النص إلى وحدات صوتية (حرف + حركة)"""
        text = cls.normalize_text(text)
        tokens = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            if char in ' \t\n،.؛؟':
                i += 1
                continue
            
            if char in cls.ARABIC_LETTERS:
                letter_info = cls.ARABIC_LETTERS[char].copy()
                haraka = None
                next_idx = i + 1
                
                if next_idx < len(text) and text[next_idx] in cls.HARAKAT:
                    haraka_symbol = text[next_idx]
                    haraka = cls.HARAKAT[haraka_symbol].copy()
                    haraka['symbol'] = haraka_symbol
                    
                    # معالجة الشدة = حرفان (ساكن + متحرك)
                    if haraka['type'] == 'shadda':
                        tokens.append({
                            'letter': char,
                            'letter_info': letter_info,
                            'haraka': {'name': 'سكون ضمني', 'type': 'sakin', 'symbol': 'ْ'},
                            'is_shadda_first': True
                        })
                        
                        if next_idx + 1 < len(text) and text[next_idx + 1] in cls.HARAKAT:
                            real_haraka = cls.HARAKAT[text[next_idx + 1]].copy()
                            real_haraka['symbol'] = text[next_idx + 1]
                            tokens.append({
                                'letter': char,
                                'letter_info': letter_info,
                                'haraka': real_haraka,
                                'is_shadda_second': True
                            })
                            i += 3
                        else:
                            tokens.append({
                                'letter': char,
                                'letter_info': letter_info,
                                'haraka': {'name': 'سكون', 'type': 'sakin', 'symbol': 'ْ'},
                                'is_shadda_second': True
                            })
                            i += 2
                        continue
                    
                    # معالجة التنوين = حركة + نون ساكنة
                    elif haraka['type'] == 'tanween':
                        tokens.append({
                            'letter': char,
                            'letter_info': letter_info,
                            'haraka': haraka,
                            'has_tanween': True
                        })
                        
                        noon_info = cls.ARABIC_LETTERS['ن'].copy()
                        tokens.append({
                            'letter': 'ن',
                            'letter_info': noon_info,
                            'haraka': {'name': 'سكون', 'type': 'sakin', 'symbol': 'ْ'},
                            'is_tanween_noon': True
                        })
                        i += 2
                        continue
                    
                    i += 2
                else:
                    # لا حركة = سكون افتراضي
                    haraka = {'name': 'سكون افتراضي', 'type': 'sakin', 'symbol': 'ْ'}
                    i += 1
                
                tokens.append({
                    'letter': char,
                    'letter_info': letter_info,
                    'haraka': haraka
                })
            else:
                i += 1
        
        return tokens

    @classmethod
    def tokens_to_arudi(cls, tokens: List[Dict]) -> str:
        """تحويل الوحدات الصوتية إلى نص عروضي"""
        arudi_parts = []
        
        for token in tokens:
            letter = token['letter']
            haraka_type = token['haraka']['type']
            
            if haraka_type == 'mutaharrik':
                symbol = 'م'  # متحرك
            elif haraka_type == 'sakin':
                symbol = 'س'  # ساكن
            elif haraka_type == 'long_vowel':
                symbol = 'ط'  # طويل (مد)
            else:
                symbol = 'س'  # افتراضي ساكن
            
            arudi_parts.append(f"{letter}{symbol}")
        
        return ' '.join(arudi_parts)

    @classmethod
    def tokens_to_binary(cls, tokens: List[Dict]) -> str:
        """تحويل الوحدات الصوتية إلى نمط ثنائي"""
        binary = []
        
        for token in tokens:
            haraka_type = token['haraka']['type']
            
            # قاعدة: المتحرك = 1، الساكن = 0
            if haraka_type == 'mutaharrik':
                binary.append('1')
            elif haraka_type == 'sakin':
                binary.append('0')
            elif haraka_type == 'long_vowel':
                binary.append('0')
            else:
                binary.append('1')
        
        return ''.join(binary)

# ═══ قاعدة بيانات البحور الكاملة ═══
class MetersDatabase:
    """قاعدة بيانات شاملة لجميع البحور وأنواعها"""
    
    TAFEELAT = {
        'فعولن': {'binary': '11010', 'feet': 2, 'sabab': 'خبن', 'watad': 'مجرور'},
        'مفاعيلن': {'binary': '1101010', 'feet': 3, 'sabab': 'وتر', 'watad': 'مجرور'},
        'مفاعلن': {'binary': '110110', 'feet': 2, 'sabab': 'خبن', 'watad': 'مجرور'},
        'فاعلاتن': {'binary': '1011010', 'feet': 3, 'sabab': 'وتر', 'watad': 'مجرور'},
        'فاعلن': {'binary': '10110', 'feet': 2, 'sabab': 'خبن', 'watad': 'مجرور'},
        'مستفعلن': {'binary': '1011010', 'feet': 3, 'sabab': 'وتر', 'watad': 'مجرور'},
        'متفاعلن': {'binary': '1110110', 'feet': 3, 'sabab': 'وتر', 'watad': 'مجرور'},
        'مفاعلتن': {'binary': '1101110', 'feet': 3, 'sabab': 'وتر', 'watad': 'مجرور'},
        'فعول': {'binary': '1101', 'feet': 1.5, 'sabab': 'خبن', 'incomplete': True},
        'فاعل': {'binary': '101', 'feet': 1.5, 'sabab': 'خبن', 'incomplete': True},
        'مفاع': {'binary': '110', 'feet': 1.5, 'sabab': 'خبن', 'incomplete': True},
        'مستفعل': {'binary': '10110', 'feet': 2, 'sabab': 'خبن', 'incomplete': True},
    }
    
    ZAHAFAAT = {
        'فعولن': [
            {'pattern': '11010', 'name': 'الأصل', 'valid': True},
            {'pattern': '1100', 'name': 'خبن', 'valid': True, 'fault': 'خبن', 'desc': 'حذف الساكن الخامس'},
            {'pattern': '1110', 'name': 'طي', 'valid': True, 'fault': 'طي', 'desc': 'نقل الحركة إلى الساكن'},
            {'pattern': '11011', 'name': 'إعلال', 'valid': True, 'fault': 'إعلال', 'desc': 'تغيير الحركة'},
        ],
        'مفاعيلن': [
            {'pattern': '1101010', 'name': 'الأصل', 'valid': True},
            {'pattern': '110100', 'name': 'خبن', 'valid': True, 'fault': 'خبن', 'desc': 'حذف النون الساكنة'},
            {'pattern': '110110', 'name': 'إقامة', 'valid': True, 'fault': 'إقامة', 'desc': 'قلب الوتر'},
            {'pattern': '1101011', 'name': 'كسر', 'valid': True, 'fault': 'كسر', 'desc': 'نقل الحركة في الوتر'},
        ],
        'فاعلاتن': [
            {'pattern': '1011010', 'name': 'الأصل', 'valid': True},
            {'pattern': '101100', 'name': 'خبن', 'valid': True, 'fault': 'خبن'},
            {'pattern': '101110', 'name': 'طي', 'valid': True, 'fault': 'طي'},
            {'pattern': '101111', 'name': 'إعلال', 'valid': True, 'fault': 'إعلال'},
        ],
        'مستفعلن': [
            {'pattern': '1011010', 'name': 'الأصل', 'valid': True},
            {'pattern': '101100', 'name': 'خبن', 'valid': True, 'fault': 'خبن'},
            {'pattern': '11010', 'name': 'تسهيل', 'valid': True, 'fault': 'تسهيل', 'desc': 'تخفيف المستفعلن إلى فعولن'},
            {'pattern': '1010110', 'name': 'إبدال', 'valid': True, 'fault': 'إبدال', 'desc': 'تبديل الساكنين'},
        ],
        'متفاعلن': [
            {'pattern': '1110110', 'name': 'الأصل', 'valid': True},
            {'pattern': '111010', 'name': 'خبن', 'valid': True, 'fault': 'خبن'},
            {'pattern': '1111110', 'name': 'طي', 'valid': True, 'fault': 'طي'},
        ],
    }
    
    METERS = {
        'الطويل': {
            'tafeelat': ['فعولن', 'مفاعيلن', 'فعولن', 'مفاعلن'],
            'base_pattern': '11010110101011010110101',
            'types': {
                'تام': {'tafeelat': ['فعولن', 'مفاعيلن', 'فعولن', 'مفاعلن'], 'cut': None, 'desc': 'أربع تفعيلات كاملة'},
                'مجزوء': {'tafeelat': ['فعولن', 'مفاعيلن', 'فعولن'], 'cut': 'العروض', 'desc': 'حذف آخر تفعيلة'},
                'مشطور': {'tafeelat': ['فعولن', 'مفاعيلن'], 'cut': 'الضرب', 'desc': 'حذف آخر تفعيلتين'},
                'منهوك': {'tafeelat': ['فعولن', 'مفاعيلن', 'فعول'], 'cut': 'العروض مقطوع', 'desc': 'مقطوع العروض'},
            },
            'description': 'أطول البحور، يمتاز بثقل إيقاعه',
            'origin': 'الطبيعي'
        },
        'المديد': {
            'tafeelat': ['فاعلاتن', 'فاعلن', 'فاعلاتن'],
            'base_pattern': '1011010101101011010',
            'types': {
                'تام': {'tafeelat': ['فاعلاتن', 'فاعلن', 'فاعلاتن'], 'cut': None},
                'مجزوء': {'tafeelat': ['فاعلاتن', 'فاعلن'], 'cut': 'العروض'},
                'مشطور': {'tafeelat': ['فاعلاتن', 'فاعل'], 'cut': 'الضرب'},
            },
            'description': 'بحر المديح والأغراض الطويلة',
            'origin': 'الطبيعي'
        },
        'البسيط': {
            'tafeelat': ['مستفعلن', 'فاعلن', 'مستفعلن', 'فاعلن'],
            'base_pattern': '101101010110101101010110',
            'types': {
                'تام': {'tafeelat': ['مستفعلن', 'فاعلن', 'مستفعلن', 'فاعلن'], 'cut': None},
                'مجزوء': {'tafeelat': ['مستفعلن', 'فاعلن', 'مستفعلن'], 'cut': 'العروض'},
                'مشطور': {'tafeelat': ['مستفعلن', 'فاعلن'], 'cut': 'الضرب'},
                'متدارك': {'tafeelat': ['مستفعل', 'فاعلن', 'مستفعل', 'فاعلن'], 'cut': None, 'fault': 'تدارك', 'desc': 'زحاف التدارك'},
            },
            'description': 'أكثر البحور استخداماً، يُسمى بحر الشعر العربي',
            'origin': 'الطبيعي'
        },
        'الوافر': {
            'tafeelat': ['مفاعلتن', 'مفاعلتن', 'فعولن'],
            'base_pattern': '1101110110111011010',
            'types': {
                'تام': {'tafeelat': ['مفاعلتن', 'مفاعلتن', 'فعولن'], 'cut': None},
                'مجزوء': {'tafeelat': ['مفاعلتن', 'مفاعلتن'], 'cut': 'العروض'},
            },
            'description': 'بحر الوصف والغزل',
            'origin': 'الصناعي'
        },
        'الكامل': {
            'tafeelat': ['متفاعلن', 'متفاعلن', 'متفاعلن'],
            'base_pattern': '111011011101101110110',
            'types': {
                'تام': {'tafeelat': ['متفاعلن', 'متفاعلن', 'متفاعلن'], 'cut': None},
                'مجزوء': {'tafeelat': ['متفاعلن', 'متفاعلن'], 'cut': 'العروض'},
                'مشطور': {'tafeelat': ['متفاعلن'], 'cut': 'الضرب'},
                'مضارع': {'tafeelat': ['متفاعل', 'متفاعل', 'متفاعل'], 'cut': None, 'fault': 'تضعيف', 'desc': 'تضعيف: حذف النون'},
            },
            'description': 'بحر السهولة والتجانس',
            'origin': 'الطبيعي'
        },
        'الهزج': {
            'tafeelat': ['مفاعيلن', 'فاعلاتن'],
            'base_pattern': '11010101101010',
            'types': {
                'تام': {'tafeelat': ['مفاعيلن', 'فاعلاتن'], 'cut': None},
                'مجزوء': {'tafeelat': ['مفاعيلن'], 'cut': 'العروض'},
                'مشطور': {'tafeelat': ['مفاعيل'], 'cut': 'الضرب'},
            },
            'description': 'بحر الخفة والسرعة',
            'origin': 'الطبيعي'
        },
        'الرجز': {
            'tafeelat': ['مستفعلن', 'مستفعلن', 'مستفعلن'],
            'base_pattern': '101101010110101011010',
            'types': {
                'تام': {'tafeelat': ['مستفعلن', 'مستفعلن', 'مستفعلن'], 'cut': None},
                'مجزوء': {'tafeelat': ['مستفعلن', 'مستفعلن'], 'cut': 'العروض'},
                'مشطور': {'tafeelat': ['مستفعلن'], 'cut': 'الضرب'},
                'مربع': {'tafeelat': ['مستفعلن', 'مستفعلن', 'مستفعلن', 'مستفعلن'], 'cut': None, 'desc': 'أربع تفعيلات'},
            },
            'description': 'بحر القصائد القصيرة والحكمة',
            'origin': 'الطبيعي'
        },
        'الرمل': {
            'tafeelat': ['فاعلاتن', 'فاعلاتن', 'فاعلاتن'],
            'base_pattern': '101101010110101011010',
            'types': {
                'تام': {'tafeelat': ['فاعلاتن', 'فاعلاتن', 'فاعلاتن'], 'cut': None},
                'مجزوء': {'tafeelat': ['فاعلاتن', 'فاعلاتن'], 'cut': 'العروض'},
                'مشطور': {'tafeelat': ['فاعلاتن'], 'cut': 'الضرب'},
            },
            'description': 'بحر الرثاء والحزن',
            'origin': 'الطبيعي'
        },
        'السريع': {
            'tafeelat': ['مستفعلن', 'مستفعلن', 'فاعلن'],
            'base_pattern': '1011010101101010110',
            'types': {
                'تام': {'tafeelat': ['مستفعلن', 'مستفعلن', 'فاعلن'], 'cut': None},
                'مجزوء': {'tafeelat': ['مستفعلن', 'فاعلن'], 'cut': 'العروض'},
            },
            'description': 'بحر السرعة والخفة',
            'origin': 'الطبيعي'
        },
        'المنسرح': {
            'tafeelat': ['مستفعلن', 'فاعلاتن', 'مستفعلن', 'فاعلن'],
            'base_pattern': '10110101010101011010',
            'types': {
                'تام': {'tafeelat': ['مستفعلن', 'فاعلاتن', 'مستفعلن', 'فاعلن'], 'cut': None},
                'مجزوء': {'tafeelat': ['مستفعلن', 'فاعلاتن'], 'cut': 'العروض'},
            },
            'description': 'بحر السهولة والانسيابية',
            'origin': 'الطبيعي'
        },
        'الخفيف': {
            'tafeelat': ['فاعلاتن', 'مستفعلن', 'فاعلاتن'],
            'base_pattern': '101101010110101011010',
            'types': {
                'تام': {'tafeelat': ['فاعلاتن', 'مستفعلن', 'فاعلاتن'], 'cut': None},
                'مجزوء': {'tafeelat': ['فاعلاتن', 'مستفعلن'], 'cut': 'العروض'},
            },
            'description': 'بحر الخفة والليونة',
            'origin': 'الطبيعي'
        },
        'المضارع': {
            'tafeelat': ['مفاعلتن', 'فاعلاتن'],
            'base_pattern': '11010101011010',
            'types': {
                'تام': {'tafeelat': ['مفاعلتن', 'فاعلاتن'], 'cut': None},
                'مجزوء': {'tafeelat': ['مفاعلتن'], 'cut': 'العروض'},
            },
            'description': 'بحر التضرع والدعاء',
            'origin': 'الصناعي'
        },
        'المقتضب': {
            'tafeelat': ['فاعلاتن', 'مستفعلن', 'فاعلن'],
            'base_pattern': '10101011011010',
            'types': {
                'تام': {'tafeelat': ['فاعلاتن', 'مستفعلن', 'فاعلن'], 'cut': None},
            },
            'description': 'بحر مختصر ومقتضب',
            'origin': 'الصناعي'
        },
        'المجتث': {
            'tafeelat': ['مستفعلن', 'فاعلاتن', 'فاعلن'],
            'base_pattern': '10110101011010',
            'types': {
                'تام': {'tafeelat': ['مستفعلن', 'فاعلاتن', 'فاعلن'], 'cut': None},
            },
            'description': 'بحر المجتثات',
            'origin': 'الصناعي'
        },
        'المتقارب': {
            'tafeelat': ['فعولن', 'فعولن', 'فعولن', 'فعولن'],
            'base_pattern': '11010110101101011010',
            'types': {
                'تام': {'tafeelat': ['فعولن', 'فعولن', 'فعولن', 'فعولن'], 'cut': None},
                'مجزوء': {'tafeelat': ['فعولن', 'فعولن', 'فعولن'], 'cut': 'العروض'},
                'مشطور': {'tafeelat': ['فعولن', 'فعولن'], 'cut': 'الضرب'},
            },
            'description': 'بحر التقارب والتجانس',
            'origin': 'الطبيعي'
        },
        'المتدارك': {
            'tafeelat': ['فاعلن', 'فاعلن', 'فاعلن', 'فاعلن'],
            'base_pattern': '10110101101011010110',
            'types': {
                'تام': {'tafeelat': ['فاعلن', 'فاعلن', 'فاعلن', 'فاعلن'], 'cut': None},
                'مجزوء': {'tafeelat': ['فاعلن', 'فاعلن', 'فاعلن'], 'cut': 'العروض'},
            },
            'description': 'بحر التدارك والسرعة الفائقة',
            'origin': 'الطبيعي'
        },
    }

# ═══ محلل العلل العروضية ═══
class FaultsAnalyzer:
    """محلل العلل العروضية: الزحافات والعلل"""
    
    @classmethod
    def detect_faults(cls, binary: str, expected_pattern: str, tafeela_name: str) -> List[Dict]:
        """كشف العلل في التفعيلة"""
        faults = []
        
        if len(binary) != len(expected_pattern):
            faults.append({
                'type': 'length_mismatch',
                'expected': len(expected_pattern),
                'actual': len(binary),
                'severity': 'critical'
            })
            return faults
        
        for i, (exp, act) in enumerate(zip(expected_pattern, binary)):
            if exp != act:
                fault_type = cls._classify_fault(i, exp, act, tafeela_name)
                faults.append({
                    'position': i,
                    'expected': exp,
                    'actual': act,
                    'type': fault_type['name'],
                    'description': fault_type['desc'],
                    'severity': fault_type.get('severity', 'minor'),
                    'can_correct': fault_type.get('can_correct', True)
                })
        
        return faults
    
    @classmethod
    def _classify_fault(cls, position: int, expected: str, actual: str, tafeela: str) -> Dict:
        """تصنيف نوع الخلل"""
        
        if position == 4 and expected == '0' and actual == '1':
            return {
                'name': 'خبن',
                'desc': 'حذف الساكن الخامس (الخبن)',
                'severity': 'acceptable',
                'can_correct': True
            }
        
        if expected == '0' and actual == '1':
            return {
                'name': 'طي',
                'desc': 'نقل الحركة إلى الساكن (الطي)',
                'severity': 'acceptable',
                'can_correct': True
            }
        
        if tafeela == 'مفاعيلن' and position in [4, 5]:
            return {
                'name': 'إقامة',
                'desc': 'قلب الوتر في مفاعيلن',
                'severity': 'acceptable',
                'can_correct': True
            }
        
        if tafeela == 'مستفعلن' and len(expected) > len(actual):
            return {
                'name': 'تسهيل',
                'desc': 'تخفيف المستفعلن إلى فعولن',
                'severity': 'acceptable',
                'can_correct': True
            }
        
        return {
            'name': 'خلل',
            'desc': 'زحاف غير مسموح به في هذا الموضع',
            'severity': 'critical',
            'can_correct': False
        }
    
    @classmethod
    def validate_with_faults(cls, binary: str, tafeela_name: str) -> Dict:
        """التحقق من صحة التفعيلة مع السماح بالعلل المشروعة"""
        tafeela_info = MetersDatabase.TAFEELAT.get(tafeela_name, {})
        expected = tafeela_info.get('binary', '')
        
        if not expected:
            return {'valid': False, 'reason': 'تفعيلة غير معروفة'}
        
        if binary == expected:
            return {
                'valid': True,
                'has_faults': False,
                'faults': [],
                'original_pattern': expected
            }
        
        allowed_patterns = MetersDatabase.ZAHAFAAT.get(tafeela_name, [])
        
        for variant in allowed_patterns:
            if binary == variant['pattern']:
                return {
                    'valid': True,
                    'has_faults': True,
                    'fault_name': variant['name'],
                    'fault_type': variant.get('fault'),
                    'fault_desc': variant.get('desc'),
                    'faults': [{
                        'type': variant.get('fault', 'زحاف'),
                        'name': variant['name'],
                        'description': variant.get('desc', ''),
                        'acceptable': variant['valid']
                    }],
                    'original_pattern': expected,
                    'actual_pattern': binary
                }
        
        faults = cls.detect_faults(binary, expected, tafeela_name)
        
        return {
            'valid': False,
            'has_faults': True,
            'faults': faults,
            'original_pattern': expected,
            'actual_pattern': binary
        }

# ═══ الفراهيدي الذكي المتقدم Pro ═══
class FarahidiPro:
    """الفراهيدي الذكي المتقدم"""
    
    def __init__(self):
        self.text_engine = ArabicTextEngine()
        self.faults_analyzer = FaultsAnalyzer()
        self.meters_db = MetersDatabase()
    
    def analyze_shatr(self, text: str) -> ShatrAnalysis:
        """تحليل شطر واحد (صدر أو عجز)"""
        
        # ١. المعالجة الصوتية
        tokens = self.text_engine.tokenize_phonetic(text)
        
        if not tokens:
            return ShatrAnalysis(
                original_text=text,
                is_valid=False,
                confidence=0.0
            )
        
        # ٢. التحويل إلى عروضي وثنائي
        arudi_text = self.text_engine.tokens_to_arudi(tokens)
        binary_code = self.text_engine.tokens_to_binary(tokens)
        
        # ٣. استخراج التفعيلات مع الزحافات
        detected_tafeelat = self._extract_tafeelat(binary_code, tokens)
        
        # ٤. مطابقة جميع أنواع البحور
        meter_match = self._match_meter(binary_code, detected_tafeelat)
        
        # ٥. التحقق من العلل
        faults = []
        for taf in detected_tafeelat:
            if taf.get('expected_name'):
                validation = self.faults_analyzer.validate_with_faults(
                    taf['binary'], taf['expected_name']
                )
                if validation.get('has_faults'):
                    faults.extend(validation.get('faults', []))
        
        # ٦. حساب الثقة
        confidence = self._calculate_confidence(detected_tafeelat, meter_match, faults)
        
        # ٧. التصحيح المقترح
        suggested_correction = None
        if faults and not all(f.get('severity') == 'critical' for f in faults):
            suggested_correction = self._generate_correction(text, faults)
        
        return ShatrAnalysis(
            original_text=text,
            arudi_text=arudi_text,
            binary_code=binary_code,
            tafeelat=detected_tafeelat,
            meter_name=meter_match.get('meter_name'),
            meter_type=meter_match.get('meter_type'),
            faults=faults,
            confidence=confidence,
            is_valid=meter_match.get('is_valid', False),
            suggested_correction=suggested_correction
        )
    
    def _extract_tafeelat(self, binary: str, tokens: List[Dict]) -> List[Dict]:
        """استخراج التفعيلات من النمط الثنائي مع دعم الزحافات"""
        detected = []
        i = 0
        
        while i < len(binary):
            matched = False
            
            sorted_tafeelat = sorted(
                self.meters_db.TAFEELAT.items(),
                key=lambda x: len(x[1]['binary']),
                reverse=True
            )
            
            for tafeela_name, tafeela_info in sorted_tafeelat:
                pattern = tafeela_info['binary']
                pattern_len = len(pattern)
                
                if i + pattern_len <= len(binary):
                    segment = binary[i:i + pattern_len]
                    
                    if segment == pattern or self._is_valid_variation(segment, tafeela_name):
                        letter_count = self._count_letters_in_binary_segment(tokens, i, pattern_len)
                        
                        detected.append({
                            'name': tafeela_name,
                            'binary': segment,
                            'position': i,
                            'length': pattern_len,
                            'letters': letter_count,
                            'is_complete': not tafeela_info.get('incomplete', False),
                            'expected_name': tafeela_name
                        })
                        
                        i += pattern_len
                        matched = True
                        break
            
            if not matched:
                i += 1
        
        return detected
    
    def _is_valid_variation(self, binary: str, tafeela_name: str) -> bool:
        """التحقق مما إذا كان النمط متغيراً صحيحاً للتفعيلة"""
        allowed = self.meters_db.ZAHAFAAT.get(tafeela_name, [])
        return any(variant['pattern'] == binary for variant in allowed)
    
    def _count_letters_in_binary_segment(self, tokens: List[Dict], start: int, length: int) -> List[str]:
        """حساب الحروف المقابلة لجزء من النمط الثنائي"""
        letters = []
        current_pos = 0
        
        for token in tokens:
            if current_pos >= start and current_pos < start + length:
                letters.append(token['letter'])
            current_pos += 1
            
            if current_pos >= start + length:
                break
        
        return letters
    
    def _match_meter(self, binary: str, detected_tafeelat: List[Dict]) -> Dict:
        """مطابقة النمط مع قاعدة بيانات البحور (جميع الأنواع)"""
        if not detected_tafeelat:
            return {'is_valid': False, 'meter_name': None, 'meter_type': None}
        
        detected_names = [t['name'] for t in detected_tafeelat]
        
        best_match = None
        best_score = 0
        
        for meter_name, meter_info in self.meters_db.METERS.items():
            for meter_type, type_info in meter_info.get('types', {}).items():
                expected_tafeelat = type_info['tafeelat']
                
                score = self._calculate_match_score(detected_names, expected_tafeelat)
                
                if score > best_score:
                    best_score = score
                    best_match = {
                        'meter_name': meter_name,
                        'meter_type': meter_type,
                        'score': score,
                        'is_valid': score >= 0.7,
                        'expected_tafeelat': expected_tafeelat,
                        'cut': type_info.get('cut')
                    }
        
        return best_match or {'is_valid': False, 'meter_name': None, 'meter_type': None}
    
    def _calculate_match_score(self, detected: List[str], expected: List[str]) -> float:
        """حساب درجة تطابق التفعيلات"""
        if not expected:
            return 0.0
        
        matches = 0
        total = max(len(detected), len(expected))
        
        for i, exp in enumerate(expected):
            if i < len(detected):
                if detected[i] == exp:
                    matches += 1
                elif self._is_valid_variation(detected[i], exp):
                    matches += 0.8
        
        return matches / total if total > 0 else 0.0
    
    def _calculate_confidence(self, tafeelat: List[Dict], meter_match: Dict, faults: List[Dict]) -> float:
        """حساب نسبة الثقة في التحليل"""
        base_confidence = meter_match.get('score', 0.0) * 100
        
        if faults:
            critical_count = sum(1 for f in faults if f.get('severity') == 'critical')
            acceptable_count = sum(1 for f in faults if f.get('severity') == 'acceptable')
            
            penalty = (critical_count * 20) + (acceptable_count * 5)
            base_confidence = max(0, base_confidence - penalty)
        
        return round(base_confidence, 2)
    
    def _generate_correction(self, text: str, faults: List[Dict]) -> Optional[str]:
        """توليد تصحيح مقترح للنص"""
        if not faults:
            return None
        
        corrections = []
        for fault in faults:
            if fault.get('can_correct') and fault.get('severity') != 'critical':
                corrections.append(f"تصحيح: {fault.get('description', '')}")
        
        return " | ".join(corrections) if corrections else None
    
    def analyze_full_poem(self, text: str) -> PoemAnalysis:
        """تحليل قصيدة كاملة"""
        verses = text.strip().split('\n')
        analyses = []
        
        for verse in verses:
            if '،' in verse or ' ' in verse:
                parts = verse.replace('،', ' ').split()
                mid = len(parts) // 2
                
                sadr = ' '.join(parts[:mid])
                ajuz = ' '.join(parts[mid:])
                
                sadr_analysis = self.analyze_shatr(sadr)
                ajuz_analysis = self.analyze_shatr(ajuz)
                
                analyses.extend([sadr_analysis, ajuz_analysis])
        
        unified_meter = self._determine_unified_meter(analyses)
        
        return PoemAnalysis(
            verses=analyses,
            unified_meter=unified_meter.get('name'),
            meter_type=unified_meter.get('type'),
            overall_confidence=unified_meter.get('confidence', 0.0)
        )
    
    def _determine_unified_meter(self, analyses: List[ShatrAnalysis]) -> Dict:
        """تحديد البحر الموحد للقصيدة"""
        meter_votes = defaultdict(int)
        
        for analysis in analyses:
            if analysis.meter_name:
                key = f"{analysis.meter_name}_{analysis.meter_type}"
                meter_votes[key] += analysis.confidence
        
        if meter_votes:
            best_meter = max(meter_votes.items(), key=lambda x: x[1])
            meter_name, meter_type = best_meter[0].split('_')
            total_confidence = sum(a.confidence for a in analyses) / len(analyses) if analyses else 0
            
            return {
                'name': meter_name,
                'type': meter_type,
                'confidence': round(total_confidence, 2)
            }
        
        return {'name': None, 'type': None, 'confidence': 0.0}

# ═══ واجهة المستخدم Streamlit ═══
def render_header():
    """عرض رأس الصفحة"""
    st.markdown('<h1 class="header-title">📜 منصة تام الثقافية الذكية</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">نظام متقدم لتحليل الشعر العربي العروضي (الفراهيدي)</p>', unsafe_allow_html=True)

def render_sidebar():
    """عرض الشريط الجانبي"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">⚙️ الإعدادات والمعلومات</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # اختيار نوع التحليل
        analysis_mode = st.radio(
            "نوع التحليل:",
            ["شطر واحد", "بيت كامل", "قصيدة كاملة"],
            index=0
        )
        
        st.markdown("---")
        
        # معلومات عن البحور
        with st.expander("📚 البحور الشعرية (16)"):
            for meter_name, info in MetersDatabase.METERS.items():
                st.markdown(f"""
                <div class="info-box">
                    <strong>{meter_name}</strong><br>
                    <small>{info['description']}</small><br>
                    <small>الأصل: {info['origin']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # معلومات عن الزحافات
        with st.expander("🔧 الزحافات المسموحة"):
            zahafat_info = """
            - **خبن**: حذف الساكن الخامس
            - **طي**: نقل الحركة إلى الساكن
            - **إقامة**: قلب الوتر (تبديل الساكنين)
            - **تسهيل**: تخفيف المستفعلن إلى فعولن
            - **كسر**: نقل الحركة في الوتر
            - **إعلال**: تغيير الحركة
            - **إبدال**: تبديل الساكنين
            """
            st.markdown(zahafat_info)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.7); font-size: 12px;">
            منصة تام الثقافية الذكية © 2025<br>
            الإصدار 2.0 - Streamlit Edition
        </div>
        """, unsafe_allow_html=True)
        
        return analysis_mode

def render_analysis_input(analysis_mode: str):
    """عرض منطقة إدخال النص"""
    st.markdown("### ✍️ أدخل النص الشعري")
    
    if analysis_mode == "شطر واحد":
        text = st.text_area(
            "أدخل الشطر (الصدر أو العجز):",
            height=100,
            placeholder="مثال: فَلا تَظُنَّنَّ أَنَّ اللَّيثَ يَبْتَسِمُ",
            help="أدخل شطراً واحداً من البيت الشعري مع التشكيل الكامل"
        )
    elif analysis_mode == "بيت كامل":
        text = st.text_area(
            "أدخل البيت الكامل:",
            height=100,
            placeholder="مثال: فَلا تَظُنَّنَّ أَنَّ اللَّيثَ يَبْتَسِمُ ، وَما بَرَدُ الغَيثِ بِالمَرْتَعِ النَّمِلِ",
            help="أدخل البيت الشعري كاملاً مع علامة الترقيم بين الصدر والعجز"
        )
    else:  # قصيدة كاملة
        text = st.text_area(
            "أدخل القصيدة:",
            height=300,
            placeholder="أدخل الأبيات الشعرية كل بيت في سطر...",
            help="أدخل عدة أبيات، كل بيت في سطر منفصل"
        )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        analyze_btn = st.button("🔍 تحليل النص", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑️ مسح", use_container_width=True)
    with col3:
        example_btn = st.button("📋 مثال", use_container_width=True)
    
    return text, analyze_btn, clear_btn, example_btn

def render_shatr_analysis(analysis: ShatrAnalysis, index: int):
    """عرض نتائج تحليل الشطر"""
    with st.container():
        st.markdown(f'<div class="analysis-result">', unsafe_allow_html=True)
        
        # رأس التحليل
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if analysis.is_valid:
                st.success(f"✅ شطر {index + 1}: {analysis.meter_name} ({analysis.meter_type})")
            else:
                st.error(f"❌ شطر {index + 1}: لم يتم التعرف على البحر")
        
        with col2:
            st.metric("نسبة الثقة", f"{analysis.confidence}%")
        
        with col3:
            status = "صحيح" if analysis.is_valid else "به أخطاء"
            st.metric("الحالة", status)
        
        # النص الأصلي
        st.markdown(f'<div class="poem-text">{analysis.original_text}</div>', unsafe_allow_html=True)
        
        # التفعيلات
        if analysis.tafeelat:
            st.markdown("#### 🎯 التفعيلات المكتشفة:")
            tafeelat_cols = st.columns(len(analysis.tafeelat))
            
            for idx, (col, taf) in enumerate(zip(tafeelat_cols, analysis.tafeelat)):
                with col:
                    completeness = "✓" if taf['is_complete'] else "✗"
                    st.markdown(f"""
                    <div style="text-align: center; background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px;">
                        <div style="font-size: 20px; font-weight: bold; color: #f5576c;">{taf['name']}</div>
                        <div style="font-size: 12px; color: rgba(255,255,255,0.8);">{taf['binary']}</div>
                        <div style="font-size: 14px;">{completeness}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # الأكواد العروضية
        with st.expander("🔍 التفاصيل التقنية"):
            col1, col2 = st.columns(2)
            with col1:
                st.code(f"النمط الثنائي: {analysis.binary_code}", language="text")
            with col2:
                st.code(f"الكتابة العروضية: {analysis.arudi_text}", language="text")
        
        # العلل والأخطاء
        if analysis.faults:
            st.markdown("#### ⚠️ العلل المكتشفة:")
            for fault in analysis.faults:
                severity_class = "fault-acceptable" if fault.get('severity') == 'acceptable' else "fault-critical"
                st.markdown(f"""
                <span class="fault-badge {severity_class}">
                    {fault.get('type', 'غير معروف')}: {fault.get('description', '')}
                </span>
                """, unsafe_allow_html=True)
        
        # التصحيح المقترح
        if analysis.suggested_correction:
            st.info(f"💡 **تصحيح مقترح:** {analysis.suggested_correction}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_visualizations(analysis: ShatrAnalysis):
    """عرض التصورات البيانية"""
    if not analysis.tafeelat:
        return
    
    # رسم بياني للتفعيلات
    tafeela_data = []
    for idx, taf in enumerate(analysis.tafeelat):
        tafeela_data.append({
            'التفعيلة': taf['name'],
            'الموقع': idx + 1,
            'الطول': len(taf['binary']),
            'مكتملة': taf['is_complete']
        })
    
    if tafeela_data:
        df = pd.DataFrame(tafeela_data)
        
        fig = px.bar(
            df, 
            x='الموقع', 
            y='الطول',
            color='مكتملة',
            text='التفعيلة',
            title='توزيع التفعيلات في الشطر',
            color_discrete_map={True: '#11998e', False: '#f5576c'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # رسم بياني دائري للنمط الثنائي
        binary_counts = {'متحرك (1)': analysis.binary_code.count('1'), 
                      'ساكن (0)': analysis.binary_code.count('0')}
        
        fig2 = px.pie(
            values=list(binary_counts.values()),
            names=list(binary_counts.keys()),
            title='توزيع الحركات والسكون',
            color_discrete_sequence=['#f5576c', '#11998e']
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            title_font_color='white'
        )
        st.plotly_chart(fig2, use_container_width=True)

def render_full_poem_analysis(poem_analysis: PoemAnalysis):
    """عرض تحليل القصيدة الكاملة"""
    st.markdown("---")
    st.markdown("## 📊 تحليل القصيدة الكاملة")
    
    # ملخص عام
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("البحر الموحد", poem_analysis.unified_meter or "غير محدد")
    with col2:
        st.metric("النوع", poem_analysis.meter_type or "غير محدد")
    with col3:
        st.metric("عدد الأشطر", len(poem_analysis.verses))
    with col4:
        st.metric("الثقة العامة", f"{poem_analysis.overall_confidence}%")
    
    # تحليل كل شطر
    for idx, verse in enumerate(poem_analysis.verses):
        render_shatr_analysis(verse, idx)
        if idx < len(poem_analysis.verses) - 1:
            st.markdown("---")

def main():
    """الدالة الرئيسية"""
    render_header()
    analysis_mode = render_sidebar()
    
    # تهيئة المحلل
    farahidi = FarahidiPro()
    
    # حالة الجلسة
    if 'last_analysis' not in st.session_state:
        st.session_state.last_analysis = None
    
    # منطقة الإدخال
    text, analyze_btn, clear_btn, example_btn = render_analysis_input(analysis_mode)
    
    # أزرار التحكم
    if clear_btn:
        st.session_state.last_analysis = None
        st.rerun()
    
    if example_btn:
        if analysis_mode == "شطر واحد":
            text = "فَلا تَظُنَّنَّ أَنَّ اللَّيثَ يَبْتَسِمُ"
        elif analysis_mode == "بيت كامل":
            text = "فَلا تَظُنَّنَّ أَنَّ اللَّيثَ يَبْتَسِمُ ، وَما بَرَدُ الغَيثِ بِالمَرْتَعِ النَّمِلِ"
        else:
            text = """فَلا تَظُنَّنَّ أَنَّ اللَّيثَ يَبْتَسِمُ
            وَما بَرَدُ الغَيثِ بِالمَرْتَعِ النَّمِلِ
            وَلا الرِّيحُ مِن بَينِ الأَيْئِمِ تَنَسَّمُ"""
        st.rerun()
    
    # التحليل
    if analyze_btn and text:
        with st.spinner("جاري التحليل العروضي..."):
            if analysis_mode == "قصيدة كاملة":
                result = farahidi.analyze_full_poem(text)
                st.session_state.last_analysis = result
                render_full_poem_analysis(result)
            elif analysis_mode == "بيت كامل":
                # تقسيم البيت وتحليله
                parts = text.replace('،', ' ').split()
                mid = len(parts) // 2
                sadr = ' '.join(parts[:mid])
                ajuz = ' '.join(parts[mid:])
                
                sadr_result = farahidi.analyze_shatr(sadr)
                ajuz_result = farahidi.analyze_shatr(ajuz)
                
                st.markdown("### 📜 الصدر")
                render_shatr_analysis(sadr_result, 0)
                render_visualizations(sadr_result)
                
                st.markdown("### 📜 العجز")
                render_shatr_analysis(ajuz_result, 1)
                render_visualizations(ajuz_result)
            else:
                # شطر واحد
                result = farahidi.analyze_shatr(text)
                render_shatr_analysis(result, 0)
                render_visualizations(result)

if __name__ == "__main__":
    main()
