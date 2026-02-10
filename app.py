#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الفراهيدي الذكي
TAM Smart Cultural Platform - Al-Farahidi Smart
"""

import subprocess
import sys

def install_packages():
    packages = ['streamlit', 'requests']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

install_packages()

import streamlit as st
import requests
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

st.set_page_config(
    page_title="مختبر الفراهيدي الذكي | منصة تام",
    page_icon="𐩩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

COLORS = {
    'midnight_blue': '#071A2F',
    'aged_gold': '#C8A44D',
    'electric_turquoise': '#00d4c8',
    'electric_turquoise_glow': 'rgba(0, 212, 200, 0.5)',
    'sandstone_cream': '#f5f0e3',
    'error_red': '#ff4757',
    'warning_orange': '#ffa502',
    'success_green': '#2ed573'
}

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;500;700&family=Cairo:wght@300;400;600;800&family=Noto+Kufi+Arabic:wght@400;700&family=Montserrat:wght@400;700&display=swap');
    
    .stApp {{
        background: {COLORS['midnight_blue']};
        font-family: 'Cairo', 'Noto Naskh Arabic', sans-serif;
        color: {COLORS['sandstone_cream']};
    }}
    
    header {{ background: rgba(7, 26, 47, 0.95) !important; border-bottom: 1px solid {COLORS['aged_gold']}40; }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    
    .main .block-container {{
        max-width: 900px; padding: 2rem;
        background: rgba(7, 26, 47, 0.6);
        border: 1px solid {COLORS['aged_gold']}40;
        border-radius: 30px;
        margin-top: 2rem;
    }}
    
    .tam-logo-container {{
        display: flex; flex-direction: column; align-items: center;
        gap: 5px; margin-bottom: 2rem; text-align: center;
    }}
    
    .tam-musnad {{
        font-family: 'Times New Roman', serif; font-size: 4rem; font-weight: bold;
        color: {COLORS['aged_gold']};
        text-shadow: 5px 5px 10px rgba(0,0,0,0.9);
        line-height: 1;
    }}
    
    .tam-english {{
        font-family: 'Montserrat', sans-serif; font-size: 2.5rem; font-weight: 700;
        letter-spacing: 0.25em; text-transform: uppercase;
        color: #C0C0C0;
        text-shadow: 5px 5px 10px rgba(0,0,0,0.9);
        line-height: 1;
    }}
    
    .tam-arabic {{
        font-family: 'Noto Kufi Arabic', sans-serif; font-size: 3.5rem; font-weight: bold;
        color: {COLORS['aged_gold']};
        text-shadow: 5px 5px 10px rgba(0,0,0,0.9);
        line-height: 1;
    }}
    
    .tam-separator {{
        height: 4px; width: 80%; margin: 10px auto;
        background: linear-gradient(to right, transparent, {COLORS['aged_gold']}, transparent);
    }}
    
    .tam-platform-name {{
        font-family: 'Noto Kufi Arabic', sans-serif; font-size: 1.5rem; font-weight: 700;
        color: {COLORS['aged_gold']};
        text-shadow: 4px 4px 8px rgba(0,0,0,0.9);
        margin-top: 0.5rem;
    }}
    
    .farahidi-title {{
        margin-top: 2rem; padding: 0.5rem 2rem;
        border: 1px solid {COLORS['electric_turquoise']}; border-radius: 50px;
        color: {COLORS['electric_turquoise']}; font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1.2rem; background: rgba(0, 212, 200, 0.1);
        display: inline-flex; align-items: center; gap: 0.5rem;
    }}
    
    .stTextArea textarea {{
        background: rgba(10, 20, 40, 0.9) !important;
        border: 2px solid {COLORS['aged_gold']}60 !important;
        border-radius: 15px !important;
        color: {COLORS['sandstone_cream']} !important;
        font-family: 'Noto Naskh Arabic', serif !important;
        font-size: 1.4rem !important;
        line-height: 2 !important;
        text-align: center !important;
        direction: rtl !important;
        min-height: 200px !important;
        padding: 20px !important;
    }}
    
    .stTextArea textarea:focus {{
        border-color: {COLORS['electric_turquoise']} !important;
        box-shadow: 0 0 15px {COLORS['electric_turquoise_glow']} !important;
        background: rgba(10, 25, 50, 0.95) !important;
    }}
    
    .stTextArea textarea::placeholder {{
        color: rgba(245, 240, 227, 0.5) !important;
        font-size: 1.2rem !important;
    }}
    
    .stTextArea label {{ display: none !important; }}
    
    .stTextArea > div > div {{
        background: transparent !important;
    }}
    
    .stButton > button {{
        font-family: 'Noto Kufi Arabic', sans-serif !important; font-weight: 700 !important;
        font-size: 1.1rem !important; border-radius: 50px !important;
        padding: 1rem 2.5rem !important; border: none !important;
        cursor: pointer !important;
    }}
    
    .btn-gold > button {{
        background: linear-gradient(180deg, #d4af37 0%, #C8A44D 50%, #b8941f 100%) !important;
        color: {COLORS['midnight_blue']} !important;
    }}
    
    .btn-outline > button {{
        background: transparent !important; border: 2px solid {COLORS['electric_turquoise']} !important;
        color: {COLORS['electric_turquoise']} !important;
    }}
    
    .btn-danger > button {{
        background: transparent !important; border: 2px solid #ff6b6b !important;
        color: #ff6b6b !important;
    }}
    
    .tafeela-card {{
        background: rgba(10, 22, 40, 0.8);
        border-radius: 15px; padding: 1.5rem; margin: 1rem 0;
        border: 2px solid {COLORS['aged_gold']}40;
        text-align: center; position: relative;
    }}
    
    .tafeela-card.error {{ border-color: {COLORS['error_red']}; }}
    .tafeela-card.warning {{ border-color: {COLORS['warning_orange']}; }}
    .tafeela-card.success {{ border-color: {COLORS['success_green']}; }}
    
    .tafeela-name {{
        font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 2rem; font-weight: bold;
        color: {COLORS['electric_turquoise']}; margin-bottom: 0.5rem;
    }}
    
    .tafeela-name.error {{ color: {COLORS['error_red']}; }}
    .tafeela-name.warning {{ color: {COLORS['warning_orange']}; }}
    
    .tafeela-pattern {{
        font-family: 'Courier New', monospace; font-size: 1.5rem;
        color: {COLORS['sandstone_cream']}; letter-spacing: 0.2em;
        direction: ltr; display: inline-block;
    }}
    
    .tafeela-status {{
        position: absolute; top: 10px; left: 10px;
        width: 30px; height: 30px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: bold; font-size: 1.2rem;
    }}
    
    .tafeela-status.error {{ background: {COLORS['error_red']}; color: white; }}
    .tafeela-status.warning {{ background: {COLORS['warning_orange']}; color: white; }}
    .tafeela-status.success {{ background: {COLORS['success_green']}; color: white; }}
    
    .status-message {{
        padding: 1.5rem; border-radius: 15px; margin: 1rem 0;
        font-family: 'Noto Kufi Arabic', sans-serif; text-align: center;
    }}
    
    .status-message.success {{
        background: rgba(46, 213, 115, 0.2);
        border: 2px solid {COLORS['success_green']};
        color: {COLORS['success_green']};
    }}
    
    .status-message.warning {{
        background: rgba(255, 165, 2, 0.2);
        border: 2px solid {COLORS['warning_orange']};
        color: {COLORS['warning_orange']};
    }}
    
    .status-message.error {{
        background: rgba(255, 71, 87, 0.2);
        border: 2px solid {COLORS['error_red']};
        color: {COLORS['error_red']};
    }}
    
    .break-info {{
        background: rgba(255, 71, 87, 0.1);
        border-right: 4px solid {COLORS['error_red']};
        padding: 1rem; margin: 0.5rem 0;
        border-radius: 5px; text-align: right;
    }}
    
    .break-location {{
        color: {COLORS['error_red']}; font-weight: bold;
        font-family: 'Noto Kufi Arabic', sans-serif;
    }}
    
    .technical-box {{
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px; padding: 1rem;
        font-family: 'Courier New', monospace;
        direction: ltr; text-align: left;
        font-size: 1.1rem; color: {COLORS['electric_turquoise']};
        word-break: break-all;
    }}
    
    .tam-footer {{
        text-align: center; padding: 2rem;
        color: rgba(245, 240, 227, 0.5); font-size: 0.9rem;
        margin-top: 2rem; border-top: 1px solid {COLORS['aged_gold']}20;
    }}
    
    /* تنسيقات نافذة التشكيل والتدقيق */
    .diacritics-box {{
        background: rgba(10, 20, 40, 0.9) !important;
        border: 2px solid {COLORS['electric_turquoise']}60 !important;
        border-radius: 15px !important;
        color: {COLORS['sandstone_cream']} !important;
        font-family: 'Noto Naskh Arabic', serif !important;
        font-size: 1.4rem !important;
        line-height: 2.5 !important;
        text-align: center !important;
        direction: rtl !important;
        padding: 25px !important;
        min-height: 200px !important;
        white-space: pre-wrap !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(7, 26, 47, 0.8);
        padding: 10px;
        border-radius: 15px;
        border: 1px solid {COLORS['aged_gold']}40;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: {COLORS['sandstone_cream']};
        font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1rem;
        border-radius: 10px;
        padding: 10px 20px;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {COLORS['electric_turquoise']}30 !important;
        border: 1px solid {COLORS['electric_turquoise']} !important;
    }}
    
    /* إزالة الخلفية البيضاء من جميع العناصر */
    .stMarkdown, .stTextArea, div[data-testid="stVerticalBlock"] {{
        background: transparent !important;
    }}
    
    div[data-testid="stVerticalBlock"] > div {{
        background: transparent !important;
    }}
    
    .element-container {{
        background: transparent !important;
    }}
    
    .stExpander {{
        background: rgba(10, 22, 40, 0.6) !important;
        border-radius: 15px;
        border: 1px solid {COLORS['aged_gold']}40;
    }}
</style>
""", unsafe_allow_html=True)

@dataclass
class TafeelaResult:
    name: str
    pattern: str
    actual: str
    status: str
    position: int
    break_info: Optional[str] = None
    zahaf: Optional[str] = None

@dataclass
class AnalysisResult:
    original_text: str
    binary_code: str
    tafeelat: List[TafeelaResult]
    meter_name: Optional[str]
    meter_type: Optional[str]
    status: str
    break_count: int
    break_locations: List[str]

class SmartArudiEngine:
    """محرك عروضي ذكي يتعامل مع النصوص غير المشكولة"""
    
    TAFEELAT = {
        'فعولن': {'pattern': '11010', 'variants': ['1100', '1110', '11011']},
        'مفاعيلن': {'pattern': '1101010', 'variants': ['110100', '110110', '1101011']},
        'مفاعلن': {'pattern': '110110', 'variants': ['11010', '110111']},
        'فاعلاتن': {'pattern': '1011010', 'variants': ['101100', '101110', '101111']},
        'فاعلن': {'pattern': '10110', 'variants': ['1011', '10101']},
        'مستفعلن': {'pattern': '1011010', 'variants': ['101100', '11010', '1010110']},
        'متفاعلن': {'pattern': '1110110', 'variants': ['111010', '1111110']},
        'مفاعلتن': {'pattern': '1101110', 'variants': ['110110', '110111']},
    }
    
    METERS = {
        'الطويل': {'pattern': ['فعولن', 'مفاعيلن', 'فعولن', 'مفاعلن']},
        'المديد': {'pattern': ['فاعلاتن', 'فاعلن', 'فاعلاتن']},
        'البسيط': {'pattern': ['مستفعلن', 'فاعلن', 'مستفعلن', 'فاعلن']},
        'الوافر': {'pattern': ['مفاعلتن', 'مفاعلتن', 'فعولن']},
        'الكامل': {'pattern': ['متفاعلن', 'متفاعلن', 'متفاعلن']},
        'الهزج': {'pattern': ['مفاعيلن', 'فاعلاتن']},
        'الرجز': {'pattern': ['مستفعلن', 'مستفعلن', 'مستفعلن']},
        'الرمل': {'pattern': ['فاعلاتن', 'فاعلاتن', 'فاعلاتن']},
        'السريع': {'pattern': ['مستفعلن', 'مستفعلن', 'فاعلن']},
        'المنسرح': {'pattern': ['مستفعلن', 'فاعلاتن', 'مستفعلن', 'فاعلن']},
        'الخفيف': {'pattern': ['فاعلاتن', 'مستفعلن', 'فاعلاتن']},
        'المتقارب': {'pattern': ['فعولن', 'فعولن', 'فعولن', 'فعولن']},
        'المتدارك': {'pattern': ['فاعلن', 'فاعلن', 'فاعلن', 'فاعلن']},
    }
    
    @staticmethod
    def smart_normalize(text: str) -> str:
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ؤ', 'و').replace('ئ', 'ي').replace('ء', '')
        text = text.replace('ة', 'ه')
        return text
    
    @staticmethod
    def syllable_analysis(text: str) -> List[Dict]:
        text = SmartArudiEngine.smart_normalize(text)
        syllables = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            if char == ' ':
                i += 1
                continue
            
            if char not in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويى':
                i += 1
                continue
            
            next_char = text[i+1] if i+1 < len(text) else None
            
            if char in 'اويى':
                if next_char and next_char in 'َُِ':
                    syllables.append({'type': 'short', 'char': char, 'haraka': next_char})
                    i += 2
                else:
                    syllables.append({'type': 'long', 'char': char})
                    i += 1
            
            elif char == 'ا':
                syllables.append({'type': 'long', 'char': char})
                i += 1
            
            elif char == 'ل' and i > 0 and text[i-1] == 'ا':
                i += 1
            
            else:
                if next_char in 'ًٌٍَُِّْ':
                    if next_char == 'ْ':
                        syllables.append({'type': 'closed', 'char': char})
                    elif next_char == 'ّ':
                        syllables.append({'type': 'shadda', 'char': char})
                    elif next_char in 'ًٌٍ':
                        syllables.append({'type': 'tanween', 'char': char})
                    else:
                        syllables.append({'type': 'open', 'char': char, 'haraka': next_char})
                    i += 2
                else:
                    syllables.append({'type': 'open', 'char': char, 'haraka': 'َ'})
                    i += 1
        
        return syllables
    
    @staticmethod
    def syllables_to_binary(syllables: List[Dict]) -> str:
        binary = []
        
        for syl in syllables:
            if syl['type'] == 'long':
                binary.append('0')
            elif syl['type'] == 'closed':
                binary.append('0')
            elif syl['type'] == 'shadda':
                binary.append('0')
                binary.append('1')
            elif syl['type'] == 'tanween':
                binary.append('1')
                binary.append('0')
            else:
                binary.append('1')
        
        return ''.join(binary)
    
    @staticmethod
    def extract_tafeelat(binary: str) -> List[TafeelaResult]:
        results = []
        i = 0
        
        while i < len(binary):
            found = False
            
            for name, info in sorted(SmartArudiEngine.TAFEELAT.items(), 
                                    key=lambda x: len(x[1]['pattern']), reverse=True):
                pattern = info['pattern']
                length = len(pattern)
                
                if i + length <= len(binary):
                    segment = binary[i:i+length]
                    
                    if segment == pattern:
                        results.append(TafeelaResult(
                            name=name, pattern=pattern, actual=segment,
                            status='complete', position=i
                        ))
                        i += length
                        found = True
                        break
                    
                    elif segment in info['variants']:
                        zahaf_name = SmartArudiEngine._identify_zahaf(segment, pattern)
                        results.append(TafeelaResult(
                            name=name, pattern=pattern, actual=segment,
                            status='complete', position=i, zahaf=zahaf_name
                        ))
                        i += length
                        found = True
                        break
                    
                    elif SmartArudiEngine._is_acceptable(segment, pattern):
                        results.append(TafeelaResult(
                            name=name, pattern=pattern, actual=segment,
                            status='complete', position=i, zahaf='زحاف خفيف'
                        ))
                        i += length
                        found = True
                        break
            
            if not found:
                i += 1
        
        return results
    
    @staticmethod
    def _identify_zahaf(variant: str, original: str) -> str:
        zahafat = {
            '1100': 'خبن', '1110': 'طي', '11011': 'إعلال',
            '110100': 'خبن', '110110': 'إقامة', '1101011': 'كسر',
            '101100': 'خبن', '101110': 'طي', '101111': 'إعلال',
        }
        return zahafat.get(variant, 'زحاف')
    
    @staticmethod
    def _is_acceptable(segment: str, pattern: str) -> bool:
        if len(segment) != len(pattern):
            return False
        
        diff_count = sum(1 for a, p in zip(segment, pattern) if a != p)
        
        if diff_count == 1:
            diff_pos = next(i for i, (a, p) in enumerate(zip(segment, pattern)) if a != p)
            if diff_pos in [2, 3, 4]:
                return True
        
        return diff_count == 0
    
    @staticmethod
    def identify_meter(tafeelat: List[TafeelaResult]) -> Tuple[Optional[str], Optional[str], str]:
        if not tafeelat:
            return None, None, "invalid"
        
        detected_names = [t.name for t in tafeelat]
        
        best_match = None
        best_score = 0
        
        for meter_name, meter_info in SmartArudiEngine.METERS.items():
            expected = meter_info['pattern']
            
            matches = 0
            for i, exp in enumerate(expected):
                if i < len(detected_names):
                    if detected_names[i] == exp:
                        matches += 1.0
                    elif SmartArudiEngine._are_related(detected_names[i], exp):
                        matches += 0.8
            
            score = matches / len(expected) if expected else 0
            
            if score > best_score:
                best_score = score
                best_match = (meter_name, meter_info, score)
        
        if not best_match or best_score < 0.5:
            return None, None, "invalid"
        
        meter_name, meter_info, score = best_match
        
        if len(tafeelat) >= len(meter_info['pattern']):
            meter_type = "تام"
        elif len(tafeelat) == len(meter_info['pattern']) - 1:
            meter_type = "مجزوء"
        else:
            meter_type = "مشطور"
        
        status = "valid" if score >= 0.7 else "partial" if score >= 0.5 else "invalid"
        
        return meter_name, meter_type, status
    
    @staticmethod
    def _are_related(t1: str, t2: str) -> bool:
        if t1[:3] == t2[:3]:
            return True
        
        pairs = [
            ('فعولن', 'مفاعيلن'), ('فاعلن', 'فاعلاتن'),
            ('مستفعلن', 'فاعلاتن'), ('متفاعلن', 'مفاعلتن')
        ]
        
        for a, b in pairs:
            if (t1 == a and t2 == b) or (t1 == b and t2 == a):
                return True
        
        return False

class DiacriticsEngine:
    """محرك التشكيل والتدقيق اللغوي"""
    
    @staticmethod
    def add_diacritics(text: str) -> str:
        """إضافة التشكيل للنص"""
        try:
            url = "https://qutrub.arabeyes.org/api/diacritize"
            headers = {"Content-Type": "application/json"}
            data = {"text": text}
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("diacritized_text", text)
            else:
                return DiacriticsEngine._fallback_diacritics(text)
                
        except Exception:
            return DiacriticsEngine._fallback_diacritics(text)
    
    @staticmethod
    def _fallback_diacritics(text: str) -> str:
        """تشكيل بديل بسيط"""
        lines = text.strip().split('\n')
        diacritized_lines = []
        
        for line in lines:
            words = line.split()
            diacritized_words = []
            
            for word in words:
                diacritized_word = DiacriticsEngine._apply_basic_diacritics(word)
                diacritized_words.append(diacritized_word)
            
            diacritized_lines.append(' '.join(diacritized_words))
        
        return '\n'.join(diacritized_lines)
    
    @staticmethod
    def _apply_basic_diacritics(word: str) -> str:
        """تطبيق قواعد تشكيل أساسية"""
        if not word:
            return word
        
        # قواعد بسيطة للتشكيل
        if word.endswith('ت') or word.endswith('ن') or word.endswith('ا'):
            if not any(h in word for h in 'ًٌٍَُِّْ'):
                return word + 'ُ'
        
        if len(word) <= 3:
            return word + 'َ'
        
        return word
    
    @staticmethod
    def spell_check(text: str) -> Tuple[str, List[str]]:
        """التدقيق الإملائي"""
        corrections = []
        lines = text.split('\n')
        corrected_lines = []
        
        common_errors = {
            'هذا': 'هَذَا',
            'التي': 'التِي',
            'الذي': 'الذِي',
            'في': 'فِي',
            'من': 'مِن',
            'إلى': 'إلَى',
            'على': 'عَلَى',
            'عن': 'عَن',
        }
        
        for line in lines:
            words = line.split()
            corrected_words = []
            
            for word in words:
                clean_word = re.sub(r'[^\w\s]', '', word)
                if clean_word in common_errors:
                    corrections.append(f"تصحيح: {word} ← {common_errors[clean_word]}")
                    corrected_words.append(common_errors[clean_word])
                else:
                    corrected_words.append(word)
            
            corrected_lines.append(' '.join(corrected_words))
        
        return '\n'.join(corrected_lines), corrections
    
    @staticmethod
    def grammar_check(text: str) -> List[str]:
        """التدقيق النحوي البسيط"""
        suggestions = []
        
        if 'في في' in text:
            suggestions.append("تكرار حرف الجر 'في'")
        
        if 'من من' in text:
            suggestions.append("تكرار حرف الجر 'من'")
        
        if text.strip().endswith('و'):
            suggestions.append("الجملة تنتهي بحرف العطف 'و'")
        
        return suggestions

def render_logo():
    st.markdown("""
    <div class="tam-logo-container">
        <div class="tam-musnad" dir="ltr">𐩩𐩱𐩣</div>
        <div class="tam-english" dir="ltr">TAM</div>
        <div class="tam-arabic">تام</div>
        <div class="tam-separator"></div>
        <div class="tam-platform-name">منصة تام الثقافية الذكية</div>
        <div class="farahidi-title"><span>🧠</span> الفراهيدي الذكي</div>
    </div>
    """, unsafe_allow_html=True)

def render_tafeela(tafeela: TafeelaResult, index: int):
    status_class = 'success' if tafeela.status == 'complete' else 'warning' if tafeela.zahaf else 'error'
    status_symbol = "✓" if status_class == 'success' else "!" if status_class == 'warning' else "✗"
    
    zahaf_text = f'<div style="color: #ffa502; font-size: 0.9rem;">زحاف: {tafeela.zahaf}</div>' if tafeela.zahaf else ''
    
    st.markdown(f"""
    <div class="tafeela-card {status_class}">
        <div class="tafeela-status {status_class}">{status_symbol}</div>
        <div class="tafeela-name {status_class}">{tafeela.name}</div>
        <div class="tafeela-pattern">{tafeela.actual}</div>
        {zahaf_text}
    </div>
    """, unsafe_allow_html=True)

def render_result(result: AnalysisResult):
    st.markdown("### 🎯 نتائج التحليل العروضي")
    
    if result.status == "valid":
        st.markdown(f"""
        <div class="status-message success">
            ✅ البحر المحدد: <strong>{result.meter_name} ({result.meter_type})</strong><br>
            القصيدة موزونة بشكل صحيح
        </div>
        """, unsafe_allow_html=True)
    elif result.status == "partial":
        st.markdown(f"""
        <div class="status-message warning">
            ⚠️ البحر المحتمل: <strong>{result.meter_name} ({result.meter_type})</strong><br>
            يوجد بعض الزحافات في التحليل
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-message error">
            ❌ <strong>لا يمكن تحديد البحر بدقة</strong><br>
            الرجاء التحقق من التشكيل أو إدخال نص أوضح
        </div>
        """, unsafe_allow_html=True)
    
    if result.tafeelat:
        st.markdown("#### 🧩 التفعيلات المكتشفة:")
        for idx, tafeela in enumerate(result.tafeelat):
            render_tafeela(tafeela, idx)
    
    with st.expander("🔍 النمط الصوتي"):
        st.markdown(f'<div class="technical-box">{result.binary_code}</div>', unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="tam-footer">
        جميع الحقوق محفوظة © 2026 منصة تام الثقافية
    </div>
    """, unsafe_allow_html=True)

def diacritics_tab():
    """نافذة التشكيل والتدقيق اللغوي"""
    st.markdown("### ✨ تشكيل وتدقيق القصيدة")
    
    input_text = st.text_area(
        "أدخل النص للتشكيل والتدقيق:",
        height=200,
        placeholder="أدخل أبيات القصيدة هنا للتشكيل والتدقيق الإملائي والنحوي...",
        key="diacritics_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        process = st.button("✨ تشكيل وتدقيق", use_container_width=True, key="btn_diacritics")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        example = st.button("📋 مثال", use_container_width=True, key="btn_example_diac")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        clear = st.button("🗑️ مسح", use_container_width=True, key="btn_clear_diac")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if clear:
        st.session_state.diacritics_input = ""
        st.rerun()
    
    if example:
        st.session_state.diacritics_input = "وحلف النصب يا ايتول هنا\nتوشي الليل والاحزان جهرا"
        st.rerun()
    
    if process and input_text.strip():
        with st.spinner("جاري التشكيل والتدقيق..."):
            engine = DiacriticsEngine()
            
            # التشكيل
            diacritized = engine.add_diacritics(input_text)
            
            # التدقيق الإملائي
            spell_checked, spell_corrections = engine.spell_check(diacritized)
            
            # التدقيق النحوي
            grammar_suggestions = engine.grammar_check(spell_checked)
            
            # عرض النتيجة
            st.markdown("#### 📝 النص المشكل والمدقق:")
            st.markdown(f'<div class="diacritics-box">{spell_checked}</div>', unsafe_allow_html=True)
            
            # زر النسخ
            st.code(spell_checked, language="text")
            
            # التنبيهات
            if spell_corrections or grammar_suggestions:
                with st.expander("⚠️ ملاحظات التدقيق"):
                    if spell_corrections:
                        st.markdown("**التصحيحات الإملائية:**")
                        for corr in spell_corrections:
                            st.markdown(f"- {corr}")
                    
                    if grammar_suggestions:
                        st.markdown("**الملاحظات النحوية:**")
                        for sugg in grammar_suggestions:
                            st.markdown(f"- {sugg}")
            
            st.info("💡 يمكنك نسخ النص المشكل أعلاه وإدخاله في نافذة التحليل العروضي")

def analysis_tab():
    """نافذة التحليل العروضي"""
    
    poem_input = st.text_area(
        "",
        height=200,
        placeholder="أدخل أبيات القصيدة المشكلة هنا...",
        key="poem_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        analyze = st.button("🔍 تحليل القصيدة", use_container_width=True, key="btn_analyze")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        example = st.button("📋 مثال", use_container_width=True, key="btn_example_anal")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        clear = st.button("🗑️ مسح", use_container_width=True, key="btn_clear_anal")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if clear:
        st.session_state.poem_input = ""
        st.rerun()
    
    if example:
        st.session_state.poem_input = "سَيَسْتَبْقِي الهِتَافُ إلَيْكَ دَهْرًا\nفَشَقَّ الدَّرْبَ بِالأَحْرَارِ نَصْرًا"
        st.rerun()
    
    if analyze and poem_input.strip():
        with st.spinner("جاري التحليل العروضي..."):
            engine = SmartArudiEngine()
            
            syllables = engine.syllable_analysis(poem_input)
            binary = engine.syllables_to_binary(syllables)
            tafeelat = engine.extract_tafeelat(binary)
            meter_name, meter_type, status = engine.identify_meter(tafeelat)
            
            result = AnalysisResult(
                original_text=poem_input,
                binary_code=binary,
                tafeelat=tafeelat,
                meter_name=meter_name,
                meter_type=meter_type,
                status=status,
                break_count=0,
                break_locations=[]
            )
            
            render_result(result)
    
    elif analyze and not poem_input.strip():
        st.error("⚠️ الرجاء إدخال نص القصيدة أولاً")

def main():
    render_logo()
    
    # إنشاء التبويبات
    tab1, tab2 = st.tabs(["✨ تشكيل وتدقيق", "🔍 تحليل عروضي"])
    
    with tab1:
        diacritics_tab()
    
    with tab2:
        analysis_tab()
    
    render_footer()

if __name__ == "__main__":
    main()
