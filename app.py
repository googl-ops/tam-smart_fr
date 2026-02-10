#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الفراهيدي الذكي المتقدم
TAM Smart Cultural Platform - Advanced Al-Farahidi
"""

import subprocess
import sys

def install_packages():
    packages = ['streamlit', 'requests', 'pandas', 'numpy', 'plotly']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

install_packages()

import streamlit as st
import pandas as pd
import numpy as np
import requests
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum

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
    'success_green': '#2ed573',
    'purple': '#9b59b6',
    'cyan': '#00cec9',
    'gradient_gold': 'linear-gradient(180deg, #d4af37 0%, #C8A44D 50%, #b8941f 100%)',
    'silver_gradient': 'linear-gradient(145deg, #E8E8E8 0%, #C0C0C0 30%, #A0A0A0 60%, #D0D0D0 100%)'
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
        max-width: 1000px; padding: 2rem;
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
        background: linear-gradient(145deg, #FFF5C3, #C8A44D 40%, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }}
    
    .tam-english {{
        font-family: 'Montserrat', sans-serif; font-size: 2rem; font-weight: 700;
        letter-spacing: 0.2em; text-transform: uppercase;
        background: {COLORS['silver_gradient']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
        background: rgba(255, 255, 255, 0.03) !important;
        border: 2px solid {COLORS['aged_gold']}60 !important;
        border-radius: 15px !important;
        color: {COLORS['sandstone_cream']} !important;
        font-family: 'Noto Naskh Arabic', serif !important;
        font-size: 1.2rem !important;
        line-height: 2 !important;
        text-align: center !important;
        direction: rtl !important;
        min-height: 150px !important;
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
    .stTextArea > div > div {{ background: transparent !important; }}
    
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
    .tafeela-card.purple {{ border-color: {COLORS['purple']}; }}
    .tafeela-card.cyan {{ border-color: {COLORS['cyan']}; }}
    
    .tafeela-name {{
        font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1.8rem; font-weight: bold;
        color: {COLORS['electric_turquoise']}; margin-bottom: 0.5rem;
    }}
    
    .tafeela-pattern {{
        font-family: 'Courier New', monospace; font-size: 1.3rem;
        color: {COLORS['sandstone_cream']}; letter-spacing: 0.2em;
        direction: ltr; display: inline-block;
    }}
    
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
    
    .result-card {{
        background: rgba(10, 22, 40, 0.6);
        border-right: 4px solid {COLORS['electric_turquoise']};
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }}
    
    .result-label {{
        color: {COLORS['aged_gold']};
        font-weight: bold;
        font-size: 0.9rem;
    }}
    
    .result-value {{
        font-size: 1.4rem;
        color: {COLORS['sandstone_cream']};
    }}
    
    .technical-box {{
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px; padding: 1rem;
        font-family: 'Courier New', monospace;
        direction: ltr; text-align: left;
        font-size: 1.1rem; color: {COLORS['electric_turquoise']};
        word-break: break-all;
    }}
    
    .diacritics-box {{
        background: rgba(0, 0, 0, 0.2);
        border: 1px dashed {COLORS['electric_turquoise']};
        padding: 20px;
        border-radius: 10px;
        font-family: 'Noto Naskh Arabic';
        font-size: 1.3rem;
        line-height: 2.5;
        text-align: center;
        color: #fff;
        margin-top: 20px;
    }}
    
    .qafiya-box {{
        background: rgba(155, 89, 182, 0.2);
        border: 2px solid {COLORS['purple']};
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }}
    
    .meter-type-badge {{
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        font-family: 'Noto Kufi Arabic';
        margin: 0.5rem;
    }}
    
    .badge-tam {{ background: {COLORS['success_green']}; color: white; }}
    .badge-majzoo {{ background: {COLORS['warning_orange']}; color: white; }}
    .badge-mashtoor {{ background: {COLORS['purple']}; color: white; }}
    .badge-manhooq {{ background: {COLORS['error_red']}; color: white; }}
    .badge-mutafa {{ background: {COLORS['cyan']}; color: white; }}
    
    .tam-footer {{
        text-align: center; padding: 2rem;
        color: rgba(245, 240, 227, 0.5); font-size: 0.9rem;
        margin-top: 2rem; border-top: 1px solid {COLORS['aged_gold']}20;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 20px;
        background-color: rgba(10, 22, 40, 0.5);
        padding: 10px;
        border-radius: 15px;
        border: 1px solid {COLORS['aged_gold']}40;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px;
        color: {COLORS['sandstone_cream']};
        font-family: 'Noto Kufi Arabic';
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {COLORS['electric_turquoise']} !important;
        color: {COLORS['midnight_blue']} !important;
        font-weight: bold;
    }}
    
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

class MeterType(Enum):
    TAM = "تام"
    MAJZOO = "مجزوء"
    MASHTOOR = "مشطور"
    MANHOOQ = "منهوك"
    MUTAFAILA = "متفاعلة"

class QafiyaType(Enum):
    ISNAD = "إسناد"
    TARKEEB = "تركيب"
    TAM = "تم"
    MURABA = "مرتابع"
    MUTLAQ = "مطلق"
    MUTADARIK = "متدارك"
    MUKARRAM = "مكرر"
    MUTAWAZI = "متوازٍ"
    MUTAMAN = "متماثل"
    MUTAJANIS = "متجانس"

@dataclass
class TafeelaResult:
    name: str
    pattern: str
    actual: str
    status: str
    position: int
    zahaf: Optional[str] = None
    is_complete: bool = True

@dataclass
class QafiyaAnalysis:
    rawwiy: str
    type: QafiyaType
    pattern: str
    is_valid: bool
    details: str

@dataclass
class ShatrAnalysis:
    original_text: str = ""
    arudi_text: str = ""
    binary_code: str = ""
    tafeelat: List[TafeelaResult] = field(default_factory=list)
    meter_name: Optional[str] = None
    meter_type: MeterType = None
    meter_subtype: str = ""
    confidence: float = 0.0
    is_valid: bool = False
    qafiya: Optional[QafiyaAnalysis] = None
    is_single_tafeela: bool = False

class DiacriticsEngine:
    """محرك التشكيل والتدقيق اللغوي"""
    
    @staticmethod
    def add_diacritics(text: str) -> str:
        try:
            url = "https://qutrub.arabeyes.org/api/diacritize"
            response = requests.post(url, json={"text": text}, timeout=5)
            if response.status_code == 200:
                return response.json().get("diacritized_text", text)
        except:
            pass
        return DiacriticsEngine._fallback_diacritics(text)
    
    @staticmethod
    def _fallback_diacritics(text: str) -> str:
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
        if not word:
            return word
        
        if word.endswith('ت') or word.endswith('ن') or word.endswith('ا'):
            if not any(h in word for h in 'ًٌٍَُِّْ'):
                return word + 'ُ'
        
        if len(word) <= 3:
            return word + 'َ'
        
        return word

class ArabicTextEngine:
    """المحرك العروضي الذكي"""
    
    ARABIC_LETTERS = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويى')
    HARAKAT = set('ًٌٍَُِّْ')
    SOLAR_LETTERS = set('تثدذرزسشصضطظلن')

    @classmethod
    def normalize_text(cls, text: str) -> str:
        if not text: 
            return ""
        text = text.replace('\u0640', '')
        hamza_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا', 'ؤ': 'و', 'ئ': 'ي', 'ء': ''}
        for old, new in hamza_map.items():
            text = text.replace(old, new)
        text = text.replace('ة', 'ه')
        allowed = cls.ARABIC_LETTERS | cls.HARAKAT | {' ', '\n'}
        return ''.join(c for c in text if c in allowed)

    @classmethod
    def _infer_vowel(cls, char: str, position: int, text: str, previous_tokens: List[Dict]) -> Dict:
        if position == len(text) - 1 or (position + 1 < len(text) and text[position + 1] == ' '):
            if char in 'دذرزسوي':
                return {'type': 'sakin', 'symbol': 'ْ', 'source': 'rule_waqf'}
        
        if char == 'ي': 
            return {'type': 'mutaharrik', 'symbol': 'ِ', 'source': 'rule_ya'}
        elif char == 'و': 
            return {'type': 'mutaharrik', 'symbol': 'ُ', 'source': 'rule_waw'}
        elif char == 'ا': 
            return {'type': 'sakin', 'symbol': 'ْ', 'source': 'rule_alif'}
        
        return {'type': 'mutaharrik', 'symbol': 'َ', 'source': 'default'}

    @classmethod
    def smart_tokenize(cls, text: str) -> List[Dict]:
        text = cls.normalize_text(text)
        tokens = []
        i = 0
        length = len(text)
        
        while i < length:
            char = text[i]
            if char == ' ' or char == '\n':
                i += 1
                continue
            if char not in cls.ARABIC_LETTERS:
                i += 1
                continue
            
            next_char = text[i+1] if i+1 < length else None
            
            if char == 'ا' and next_char == 'ل':
                after_lam = text[i+2] if i+2 < length else None
                if after_lam and after_lam in cls.SOLAR_LETTERS:
                    tokens.append({'letter': 'ا', 'haraka': {'type': 'mutaharrik', 'symbol': 'َ'}})
                    i += 2
                    continue
                else:
                    tokens.append({'letter': 'ا', 'haraka': {'type': 'mutaharrik', 'symbol': 'َ'}})
                    tokens.append({'letter': 'ل', 'haraka': {'type': 'sakin', 'symbol': 'ْ'}})
                    i += 2
                    continue

            if next_char in cls.HARAKAT:
                if next_char == 'ّ':
                    tokens.append({'letter': char, 'haraka': {'type': 'sakin', 'symbol': 'ْ'}})
                    tokens.append({'letter': char, 'haraka': {'type': 'mutaharrik', 'symbol': 'َ'}})
                    i += 2
                elif next_char == 'ْ':
                    tokens.append({'letter': char, 'haraka': {'type': 'sakin', 'symbol': 'ْ'}})
                    i += 2
                else:
                    tokens.append({'letter': char, 'haraka': {'type': 'mutaharrik', 'symbol': next_char}})
                    i += 2
                continue

            haraka = cls._infer_vowel(char, i, text, tokens)
            tokens.append({'letter': char, 'haraka': haraka})
            i += 1
            
        return tokens

    @classmethod
    def tokens_to_binary(cls, tokens: List[Dict]) -> str:
        return ''.join('1' if t['haraka']['type'] == 'mutaharrik' else '0' for t in tokens)

    @classmethod
    def tokens_to_arudi(cls, tokens: List[Dict]) -> str:
        return ' '.join(f"{t['letter']}{'م' if t['haraka']['type'] == 'mutaharrik' else 'س'}" for t in tokens)

class MetersDatabase:
    """قاعدة بيانات البحور العروضية الكاملة"""
    
    TAFEELAT = {
        'فعولن': '11010',
        'مفاعيلن': '1101010',
        'مفاعلن': '110110',
        'فاعلاتن': '1011010',
        'فاعلن': '10110',
        'مستفعلن': '1011010',
        'متفاعلن': '1110110',
        'مفاعلتن': '1101110',
        'فَعُولُن': '11010',
        'مَفَاعِيلُن': '1101010',
        'مَفَاعِلُن': '110110',
        'فَاعِلَاتُن': '1011010',
        'فَاعِلُن': '10110',
        'مُسْتَفْعِلُن': '1011010',
        'مُتَفَاعِلُن': '1110110',
        'مَفَاعِلَتُن': '1101110'
    }
    
    # أنواع البحور: تام، مجزوء، مشطور، منهوك، متفاعلة
    METERS = {
        'الطويل': {
            'تام': ['فعولن', 'مفاعيلن', 'فعولن', 'مفاعلن'],
            'مجزوء': ['فعولن', 'مفاعيلن', 'فعولن'],
            'مشطور': ['فعولن', 'مفاعيلن'],
            'منهوك': ['فعولن'],
            'متفاعلة': ['فعولن']
        },
        'المديد': {
            'تام': ['فاعلاتن', 'فاعلن', 'فاعلاتن'],
            'مجزوء': ['فاعلاتن', 'فاعلن'],
            'مشطور': ['فاعلاتن'],
            'منهوك': ['فاعلن']
        },
        'البسيط': {
            'تام': ['مستفعلن', 'فاعلن', 'مستفعلن', 'فاعلن'],
            'مجزوء': ['مستفعلن', 'فاعلن', 'مستفعلن'],
            'مشطور': ['مستفعلن', 'فاعلن'],
            'منهوك': ['مستفعلن']
        },
        'الوافر': {
            'تام': ['مفاعلتن', 'مفاعلتن', 'فعولن'],
            'مجزوء': ['مفاعلتن', 'مفاعلتن'],
            'مشطور': ['مفاعلتن'],
            'منهوك': ['فعولن']
        },
        'الكامل': {
            'تام': ['متفاعلن', 'متفاعلن', 'متفاعلن'],
            'مجزوء': ['متفاعلن', 'متفاعلن'],
            'مشطور': ['متفاعلن'],
            'منهوك': ['متفاعلن']
        },
        'الهزج': {
            'تام': ['مفاعيلن', 'فاعلاتن'],
            'مجزوء': ['مفاعيلن'],
            'مشطور': ['فاعلاتن'],
            'منهوك': ['مفاعيلن']
        },
        'الرجز': {
            'تام': ['مستفعلن', 'مستفعلن', 'مستفعلن'],
            'مجزوء': ['مستفعلن', 'مستفعلن'],
            'مشطور': ['مستفعلن'],
            'منهوك': ['مستفعلن']
        },
        'الرمل': {
            'تام': ['فاعلاتن', 'فاعلاتن', 'فاعلاتن'],
            'مجزوء': ['فاعلاتن', 'فاعلاتن'],
            'مشطور': ['فاعلاتن'],
            'منهوك': ['فاعلاتن']
        },
        'السريع': {
            'تام': ['مستفعلن', 'مستفعلن', 'فاعلن'],
            'مجزوء': ['مستفعلن', 'مستفعلن'],
            'مشطور': ['مستفعلن'],
            'منهوك': ['فاعلن']
        },
        'المنسرح': {
            'تام': ['مستفعلن', 'فاعلاتن', 'مستفعلن', 'فاعلن'],
            'مجزوء': ['مستفعلن', 'فاعلاتن', 'مستفعلن'],
            'مشطور': ['مستفعلن', 'فاعلاتن'],
            'منهوك': ['مستفعلن']
        },
        'الخفيف': {
            'تام': ['فاعلاتن', 'مستفعلن', 'فاعلاتن'],
            'مجزوء': ['فاعلاتن', 'مستفعلن'],
            'مشطور': ['فاعلاتن'],
            'منهوك': ['مستفعلن']
        },
        'المتقارب': {
            'تام': ['فعولن', 'فعولن', 'فعولن', 'فعولن'],
            'مجزوء': ['فعولن', 'فعولن', 'فعولن'],
            'مشطور': ['فعولن', 'فعولن'],
            'منهوك': ['فعولن']
        },
        'المتدارك': {
            'تام': ['فاعلن', 'فاعلن', 'فاعلن', 'فاعلن'],
            'مجزوء': ['فاعلن', 'فاعلن', 'فاعلن'],
            'مشطور': ['فاعلن', 'فاعلن'],
            'منهوك': ['فاعلن']
        }
    }

class QafiyaAnalyzer:
    """محلل القوافي"""
    
    HARAKAT_END = {'َ': 'فتحة', 'ُ': 'ضمة', 'ِ': 'كسرة', 'ً': 'تنوين فتح', 'ٌ': 'تنوين ضم', 'ٍ': 'تنوين كسر'}
    
    @staticmethod
    def extract_rawwiy(text: str) -> str:
        """استخراج الروي من آخر كلمة في البيت"""
        words = text.strip().split()
        if not words:
            return ""
        last_word = words[-1]
        
        # إزالة علامات الترقيم
        last_word = re.sub(r'[^\w\s]', '', last_word)
        
        # استخراج الحرف الأخير المتحرك
        for char in reversed(last_word):
            if char in QafiyaAnalyzer.HARAKAT_END:
                return char
            elif char in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويى':
                return char + 'ْ'
        
        return last_word[-1] if last_word else ""
    
    @staticmethod
    def analyze_qafiya(text: str, previous_lines: List[str] = None) -> QafiyaAnalysis:
        """تحليل نوع القافية"""
        rawwiy = QafiyaAnalyzer.extract_rawwiy(text)
        
        if not rawwiy:
            return QafiyaAnalysis("", QafiyaType.MUTLAQ, "", False, "لم يتم التعرف على الروي")
        
        # تحديد نوع القافية بناءً على الروي
        if 'ً' in rawwiy or 'ٌ' in rawwiy or 'ٍ' in rawwiy:
            qafiya_type = QafiyaType.TARKEEB
            pattern = "تنوين"
        elif rawwiy.endswith('َ'):
            qafiya_type = QafiyaType.ISNAD
            pattern = "فتحة"
        elif rawwiy.endswith('ُ'):
            qafiya_type = QafiyaType.MURABA
            pattern = "ضمة"
        elif rawwiy.endswith('ِ'):
            qafiya_type = QafiyaType.MUTADARIK
            pattern = "كسرة"
        elif rawwiy.endswith('ْ'):
            qafiya_type = QafiyaType.MUTLAQ
            pattern = "سكون"
        else:
            qafiya_type = QafiyaType.MUTLAQ
            pattern = "غير محدد"
        
        # التحقق من تطابق القافية مع الأبيات السابقة
        is_valid = True
        details = f"الروي: {rawwiy} ({pattern})"
        
        if previous_lines:
            prev_rawwiyat = [QafiyaAnalyzer.extract_rawwiy(line) for line in previous_lines if line.strip()]
            if prev_rawwiyat and rawwiy != prev_rawwiyat[-1]:
                is_valid = False
                details += " - ⚠️ الروي لا يتطابق مع البيت السابق"
            else:
                details += " - ✅ الروي متطابق"
        
        return QafiyaAnalysis(rawwiy, qafiya_type, pattern, is_valid, details)

class FarahidiAnalyzer:
    """المحلل العروضي المتكامل المتقدم"""
    
    def __init__(self):
        self.engine = ArabicTextEngine()
        self.db = MetersDatabase()
        self.qafiya_analyzer = QafiyaAnalyzer()
    
    def analyze(self, text: str, previous_lines: List[str] = None) -> ShatrAnalysis:
        tokens = self.engine.smart_tokenize(text)
        if not tokens: 
            return ShatrAnalysis()
        
        binary = self.engine.tokens_to_binary(tokens)
        arudi = self.engine.tokens_to_arudi(tokens)
        tafeelat = self._extract_tafeelat(binary)
        meter_match = self._match_meter(tafeelat)
        confidence = self._calculate_confidence(tafeelat, meter_match, binary)
        
        # تحليل القافية
        qafiya = self.qafiya_analyzer.analyze_qafiya(text, previous_lines)
        
        # التحقق من شعر التفعيلة الواحدة
        is_single_tafeela = self._check_single_tafeela(tafeelat)
        
        return ShatrAnalysis(
            original_text=text,
            arudi_text=arudi,
            binary_code=binary,
            tafeelat=tafeelat,
            meter_name=meter_match.get('meter_name'),
            meter_type=meter_match.get('meter_type'),
            meter_subtype=meter_match.get('meter_subtype', ''),
            confidence=confidence,
            is_valid=confidence >= 50,
            qafiya=qafiya,
            is_single_tafeela=is_single_tafeela
        )
    
    def _extract_tafeelat(self, binary: str) -> List[TafeelaResult]:
        detected = []
        i = 0
        sorted_taf = sorted(self.db.TAFEELAT.items(), key=lambda x: len(x[1]), reverse=True)
        
        while i < len(binary):
            matched = False
            for name, pattern in sorted_taf:
                if i + len(pattern) <= len(binary):
                    segment = binary[i:i+len(pattern)]
                    diff = sum(1 for a, b in zip(segment, pattern) if a != b)
                    if diff <= 1:
                        zahaf = None
                        if diff == 1:
                            zahaf = self._identify_zahaf(segment, pattern)
                        
                        detected.append(TafeelaResult(
                            name=name,
                            pattern=pattern,
                            actual=segment,
                            status='complete',
                            position=i,
                            zahaf=zahaf,
                            is_complete=(diff == 0)
                        ))
                        i += len(pattern)
                        matched = True
                        break
            if not matched:
                i += 1
        
        return detected
    
    def _identify_zahaf(self, variant: str, original: str) -> str:
        """تحديد نوع الزحاف"""
        zahafat_map = {
            ('11010', '1100'): 'خبن',
            ('11010', '1110'): 'طي',
            ('1101010', '110100'): 'خبن',
            ('1101010', '110110'): 'إقامة',
            ('1011010', '101100'): 'خبن',
            ('1011010', '101110'): 'طي'
        }
        return zahafat_map.get((original, variant), 'زحاف')
    
    def _match_meter(self, tafeelat: List[TafeelaResult]) -> Dict:
        if not tafeelat: 
            return {}
        
        detected_names = [t.name for t in tafeelat]
        best_match = {}
        max_score = 0
        
        for m_name, types in self.db.METERS.items():
            for m_type, expected in types.items():
                score = 0
                matched_count = 0
                
                for k, exp in enumerate(expected):
                    if k < len(detected_names):
                        if detected_names[k] == exp:
                            score += 1.0
                            matched_count += 1
                        elif self._are_related(detected_names[k], exp):
                            score += 0.7
                
                if expected:
                    final_score = score / len(expected)
                    coverage = matched_count / len(expected)
                    
                    if final_score > max_score and coverage >= 0.5:
                        max_score = final_score
                        meter_type_enum = self._get_meter_type_enum(m_type)
                        best_match = {
                            'meter_name': m_name,
                            'meter_type': meter_type_enum,
                            'meter_subtype': m_type,
                            'score': final_score
                        }
        
        return best_match
    
    def _get_meter_type_enum(self, type_str: str) -> MeterType:
        type_map = {
            'تام': MeterType.TAM,
            'مجزوء': MeterType.MAJZOO,
            'مشطور': MeterType.MASHTOOR,
            'منهوك': MeterType.MANHOOQ,
            'متفاعلة': MeterType.MUTAFAILA
        }
        return type_map.get(type_str, MeterType.TAM)
    
    def _are_related(self, t1: str, t2: str) -> bool:
        if t1[:3] == t2[:3]:
            return True
        
        related_pairs = [
            ('فعولن', 'مفاعيلن'), ('فاعلن', 'فاعلاتن'),
            ('مستفعلن', 'فاعلاتن'), ('متفاعلن', 'مفاعلتن'),
            ('مفاعلتن', 'مفاعلن'), ('فعولن', 'مفاعلتن')
        ]
        
        return (t1, t2) in related_pairs or (t2, t1) in related_pairs
    
    def _calculate_confidence(self, tafeelat, match, binary):
        if not match or not tafeelat: 
            return 0.0
        
        base_confidence = min(100, (len(tafeelat) / (len(binary)/6)) * 100)
        meter_score = match.get('score', 0) * 100
        
        return (base_confidence + meter_score) / 2
    
    def _check_single_tafeela(self, tafeelat: List[TafeelaResult]) -> bool:
        """التحقق مما إذا كان الشعر من التفعيلة الواحدة"""
        if not tafeelat:
            return False
        
        first_name = tafeelat[0].name
        return all(t.name == first_name for t in tafeelat)

def render_logo():
    st.markdown("""
    <div class="tam-logo-container">
        <div class="tam-musnad" dir="ltr">𐩩𐩱𐩣</div>
        <div class="tam-english" dir="ltr">TAM PLATFORM</div>
        <div class="tam-arabic">تام</div>
        <div class="tam-separator"></div>
        <div class="tam-platform-name">منصة تام الثقافية الذكية</div>
        <div class="farahidi-title"><span>🧠</span> الفراهيدي الذكي المتقدم</div>
    </div>
    """, unsafe_allow_html=True)

def get_meter_badge_class(meter_type: MeterType) -> str:
    badge_map = {
        MeterType.TAM: 'badge-tam',
        MeterType.MAJZOO: 'badge-majzoo',
        MeterType.MASHTOOR: 'badge-mashtoor',
        MeterType.MANHOOQ: 'badge-manhooq',
        MeterType.MUTAFAILA: 'badge-mutafa'
    }
    return badge_map.get(meter_type, 'badge-tam')

def render_tafeela(tafeela: TafeelaResult, index: int):
    status_class = 'success' if tafeela.is_complete else 'warning' if tafeela.zahaf else 'error'
    status_symbol = "✓" if status_class == 'success' else "!" if status_class == 'warning' else "✗"
    
    zahaf_text = f'<div style="color: #ffa502; font-size: 0.9rem; margin-top: 5px;">زحاف: {tafeela.zahaf}</div>' if tafeela.zahaf else ''
    
    st.markdown(f"""
    <div class="tafeela-card {status_class}">
        <div class="tafeela-status {status_class}">{status_symbol}</div>
        <div class="tafeela-name {status_class}">{tafeela.name}</div>
        <div class="tafeela-pattern">{tafeela.actual}</div>
        {zahaf_text}
    </div>
    """, unsafe_allow_html=True)

def render_qafiya(qafiya: QafiyaAnalysis):
    if not qafiya:
        return
    
    status_color = COLORS['success_green'] if qafiya.is_valid else COLORS['error_red']
    status_icon = "✅" if qafiya.is_valid else "⚠️"
    
    st.markdown(f"""
    <div class="qafiya-box">
        <div style="font-size: 1.5rem; font-weight: bold; color: {COLORS['purple']}; margin-bottom: 10px;">
            القافية: {qafiya.type.value}
        </div>
        <div style="font-size: 1.2rem; color: {COLORS['sandstone_cream']};">
            الروي: <strong>{qafiya.rawwiy}</strong> ({qafiya.pattern})
        </div>
        <div style="color: {status_color}; margin-top: 10px;">
            {status_icon} {qafiya.details}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_result(res: ShatrAnalysis, shatr_num: int = 1):
    st.markdown(f"### الشطر {shatr_num}: {res.original_text}")
    
    # عرض نوع البحر والنوع (تام/مجزوء/...)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        meter = res.meter_name if res.meter_name else "غير محدد"
        st.markdown(f"""
        <div class="result-card">
            <div>
                <div class="result-label">البحر</div>
                <div class="result-value">{meter}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        if res.meter_type:
            badge_class = get_meter_badge_class(res.meter_type)
            type_name = res.meter_type.value
        else:
            badge_class = 'badge-tam'
            type_name = "غير معروف"
        
        st.markdown(f"""
        <div class="result-card">
            <div>
                <div class="result-label">النوع</div>
                <div class="result-value">
                    <span class="meter-type-badge {badge_class}">{type_name}</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        color = "#4CAF50" if res.confidence > 80 else "#F44336" if res.confidence < 50 else "#ffa502"
        st.markdown(f"""
        <div class="result-card" style="border-right-color: {color}">
            <div>
                <div class="result-label">الثقة</div>
                <div class="result-value" style="color:{color}">{int(res.confidence)}%</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    # تنبيه شعر التفعيلة الواحدة
    if res.is_single_tafeela and res.tafeelat:
        st.markdown(f"""
        <div class="status-message warning">
            ⚡ <strong>شعر التفعيلة الواحدة</strong><br>
            هذا الشطر يستخدم تفعيلة واحدة متكررة: <strong>{res.tafeelat[0].name}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # عرض القافية
    if res.qafiya:
        render_qafiya(res.qafiya)
    
    # عرض التفعيلات
    if res.tafeelat:
        st.markdown("#### 🧩 التفعيلات المكتشفة:")
        cols = st.columns(min(len(res.tafeelat), 4))
        for idx, tafeela in enumerate(res.tafeelat):
            with cols[idx % 4]:
                render_tafeela(tafeela, idx)
    
    # التفاصيل التقنية
    with st.expander("🔍 التفاصيل التقنية"):
        st.markdown("**النمط الصوتي (Binary):**")
        st.markdown(f'<div class="technical-box">{res.binary_code}</div>', unsafe_allow_html=True)
        st.markdown("**النص العروضي:**")
        st.markdown(f'<div class="technical-box">{res.arudi_text}</div>', unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="tam-footer">
        جميع الحقوق محفوظة © 2026 منصة تام الثقافية | الفراهيدي الذكي المتقدم
    </div>
    """, unsafe_allow_html=True)

def diacritics_tab():
    """نافذة التشكيل والتدقيق اللغوي"""
    st.markdown("### ✨ أدخل النص ليقوم الفراهيدي بتشكيله وتدقيقه:")
    
    raw_input = st.text_area(
        "النص الخام",
        value=st.session_state.get('raw_text', ''),
        height=150,
        key="input_raw",
        placeholder="اكتب النص هنا..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("✨ تشكيل النص", use_container_width=True, key="btn_diacritics"):
            if raw_input:
                with st.spinner("جاري الاتصال بالمشكّل الذكي..."):
                    suggested_tashkeel = DiacriticsEngine.add_diacritics(raw_input)
                    st.session_state.final_text = suggested_tashkeel
                    st.session_state.raw_text = raw_input
            else:
                st.warning("أدخل نصاً أولاً.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        if st.button("📋 مثال", use_container_width=True, key="btn_example_diac"):
            st.session_state.raw_text = "وحلف النصب يا ايتول هنا\nتوشي الليل والاحزان جهرا"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("🗑️ مسح", use_container_width=True, key="btn_clear_diac"):
            st.session_state.raw_text = ""
            st.session_state.final_text = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get('final_text'):
        st.markdown("### 📝 النتيجة (يمكنك التعديل عليها):")
        
        final_input = st.text_area(
            "النص الجاهز",
            value=st.session_state.final_text,
            height=150,
            key="editor_final"
        )
        
        if final_input != st.session_state.final_text:
            st.session_state.final_text = final_input
        
        st.markdown(f'<div class="diacritics-box">{st.session_state.final_text}</div>', unsafe_allow_html=True)
        st.code(st.session_state.final_text, language="text")
        st.info("💡 انسخ هذا النص وانتقل للنافذة الثانية، أو اضغط زر التحليل هناك مباشرة.")

def analysis_tab():
    """نافذة التحليل العروضي المتقدم"""
    st.markdown("### 🔍 تحليل الوزن العروضي المتقدم")
    
    text_to_analyze = st.text_area(
        "",
        value=st.session_state.get('final_text', ''),
        height=150,
        key="analysis_input",
        placeholder="أدخل النص المشكل هنا..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        analyze = st.button("🔍 تحليل القصيدة", use_container_width=True, key="btn_analyze", type="primary")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        if st.button("📋 مثال", use_container_width=True, key="btn_example_anal"):
            st.session_state.final_text = "سَيَسْتَبْقِي الهِتَافُ إلَيْكَ دَهْرًا\nفَشَقَّ الدَّرْبَ بِالأَحْرَارِ نَصْرًا"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        if st.button("🗑️ مسح", use_container_width=True, key="btn_clear_anal"):
            st.session_state.final_text = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if analyze:
        if not text_to_analyze.strip():
            st.error("⚠️ الرجاء إدخال نص وتشكيله في النافذة الأولى أولاً!")
        else:
            analyzer = FarahidiAnalyzer()
            
            # تقسيم النص إلى أبيات
            lines = [s.strip() for s in re.split(r'[\n]', text_to_analyze) if s.strip()]
            previous_lines = []
            
            for idx, line in enumerate(lines):
                # تقسيم البيت إلى شطرين إذا وجد علامة تقسيم
                shatrs = re.split(r'[،,]', line)
                
                for shatr_idx, shatr in enumerate(shatrs):
                    if shatr.strip():
                        res = analyzer.analyze(shatr.strip(), previous_lines)
                        render_result(res, idx + 1)
                        previous_lines.append(shatr.strip())
                        st.divider()

def main():
    render_logo()
    
    if 'raw_text' not in st.session_state:
        st.session_state.raw_text = ""
    if 'final_text' not in st.session_state:
        st.session_state.final_text = ""
    
    tab1, tab2 = st.tabs(["✍️ المُشكّل الآلي", "🔍 المحلل العروضي المتقدم"])
    
    with tab1:
        diacritics_tab()
    
    with tab2:
        analysis_tab()
    
    render_footer()

if __name__ == "__main__":
    main()
