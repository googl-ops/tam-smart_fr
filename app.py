#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الفراهيدي الذكي Pro Max
TAM Smart Cultural Platform - Al-Farahidi Smart Pro Max
"""

import subprocess
import sys

def install_packages():
    packages = ['streamlit', 'pandas', 'numpy', 'plotly']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

install_packages()

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import re
import json
from collections import defaultdict

# ═══ إعدادات الصفحة ═══
st.set_page_config(
    page_title="مختبر الفراهيدي الذكي | منصة تام",
    page_icon="𐩩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══ الألوان الأصلية لتام ═══
COLORS = {
    'sabaean_blue': '#0a1628',
    'sabaean_blue_light': '#1a3a5c',
    'midnight_blue': '#071A2F',
    'aged_gold': '#C8A44D',
    'aged_gold_glow': 'rgba(200, 164, 77, 0.4)',
    'electric_turquoise': '#00d4c8',
    'electric_turquoise_glow': 'rgba(0, 212, 200, 0.3)',
    'sandstone_cream': '#f5f0e3',
    'error_red': '#ff4757',
    'warning_orange': '#ffa502',
    'success_green': '#2ed573'
}

# ═══ CSS مخصص ═══
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
    
    .stApp::before {{
        content: ""; position: fixed; top: -20%; left: -20%; width: 140%; height: 140%;
        background: radial-gradient(circle at center, rgba(11,240,255,0.08) 1px, transparent 1px) repeat;
        background-size: 50px 50px; z-index: -1; filter: blur(1px); pointer-events: none;
    }}
    
    .main .block-container {{
        max-width: 1000px; padding: 2rem;
        background: rgba(7, 26, 47, 0.6);
        border: 1px solid {COLORS['aged_gold']}40;
        border-radius: 30px; backdrop-filter: blur(20px);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5); margin-top: 2rem;
    }}
    
    .tam-logo-container {{
        display: flex; flex-direction: column; align-items: center;
        gap: 5px; margin-bottom: 2rem; text-align: center;
    }}
    
    .tam-musnad {{
        font-family: 'Times New Roman', serif; font-size: 4rem; font-weight: bold;
        letter-spacing: 0.05em;
        background: linear-gradient(145deg, #FFF5C3, #C8A44D 40%, #A67C2B 70%, #FFD700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 5px 5px 10px rgba(0,0,0,0.9); line-height: 1;
    }}
    
    .tam-english {{
        font-family: 'Montserrat', sans-serif; font-size: 2.5rem; font-weight: 700;
        letter-spacing: 0.25em; text-transform: uppercase;
        background: {COLORS['silver_gradient']};
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 5px 5px 10px rgba(0,0,0,0.9); line-height: 1;
    }}
    
    .tam-arabic {{
        font-family: 'Noto Kufi Arabic', sans-serif; font-size: 3.5rem; font-weight: bold;
        background: linear-gradient(145deg, #FFF5C3, #C8A44D 40%, #A67C2B 70%, #FFD700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 5px 5px 10px rgba(0,0,0,0.9); line-height: 1;
    }}
    
    .tam-separator {{
        height: 4px; width: 80%; margin: 10px auto;
        background: linear-gradient(to right, transparent, {COLORS['aged_gold']}, transparent);
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);
    }}
    
    .tam-platform-name {{
        font-family: 'Noto Kufi Arabic', sans-serif; font-size: 1.5rem; font-weight: 700;
        background: linear-gradient(145deg, #FFF5C3, #C8A44D 40%, #A67C2B 70%, #FFD700);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.9); margin-top: 0.5rem;
    }}
    
    .farahidi-title {{
        margin-top: 2rem; padding: 0.5rem 2rem;
        border: 1px solid {COLORS['electric_turquoise']}; border-radius: 50px;
        color: {COLORS['electric_turquoise']}; font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1.2rem; background: rgba(0, 212, 200, 0.1);
        box-shadow: 0 0 15px {COLORS['electric_turquoise_glow']};
        display: inline-flex; align-items: center; gap: 0.5rem;
    }}
    
    .stTextArea textarea {{
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid {COLORS['aged_gold']}40 !important; border-radius: 15px !important;
        color: {COLORS['sandstone_cream']} !important; font-family: 'Noto Naskh Arabic', serif !important;
        font-size: 1.3rem !important; line-height: 2 !important;
        text-align: center !important; direction: rtl !important; min-height: 200px !important;
    }}
    
    .stTextArea textarea:focus {{
        border-color: {COLORS['electric_turquoise']} !important;
        box-shadow: 0 0 20px {COLORS['electric_turquoise_glow']} !important;
    }}
    
    .stTextArea label {{ display: none !important; }}
    
    .stButton > button {{
        font-family: 'Noto Kufi Arabic', sans-serif !important; font-weight: 700 !important;
        font-size: 1.1rem !important; border-radius: 50px !important;
        padding: 1rem 2.5rem !important; border: none !important;
        cursor: pointer !important; transition: all 0.3s ease !important;
        display: inline-flex !important; align-items: center !important; gap: 0.5rem !important;
    }}
    
    .btn-gold > button {{
        background: {COLORS['gradient_gold']} !important; color: {COLORS['midnight_blue']} !important;
        box-shadow: 0 0 20px {COLORS['aged_gold_glow']} !important;
    }}
    
    .btn-outline > button {{
        background: transparent !important; border: 2px solid {COLORS['electric_turquoise']} !important;
        color: {COLORS['electric_turquoise']} !important;
    }}
    
    .btn-danger > button {{
        background: transparent !important; border: 2px solid #ff6b6b !important;
        color: #ff6b6b !important;
    }}
    
    /* بطاقات التفعيلات */
    .tafeela-card {{
        background: rgba(10, 22, 40, 0.8);
        border-radius: 15px; padding: 1.5rem; margin: 1rem 0;
        border: 2px solid {COLORS['aged_gold']}40;
        text-align: center; position: relative;
    }}
    
    .tafeela-card.error {{
        border-color: {COLORS['error_red']};
        background: rgba(255, 71, 87, 0.1);
    }}
    
    .tafeela-card.warning {{
        border-color: {COLORS['warning_orange']};
        background: rgba(255, 165, 2, 0.1);
    }}
    
    .tafeela-card.success {{
        border-color: {COLORS['success_green']};
        background: rgba(46, 213, 115, 0.1);
    }}
    
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
    
    .tafeela-status.error {{
        background: {COLORS['error_red']}; color: white;
    }}
    
    .tafeela-status.warning {{
        background: {COLORS['warning_orange']}; color: white;
    }}
    
    .tafeela-status.success {{
        background: {COLORS['success_green']}; color: white;
    }}
    
    /* قسم التفاصيل التقنية */
    .technical-details {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px; padding: 1rem; margin-top: 1rem;
        font-family: 'Courier New', monospace;
        direction: ltr; text-align: left;
    }}
    
    .binary-code {{
        font-size: 1.2rem; color: {COLORS['electric_turquoise']};
        word-break: break-all; letter-spacing: 0.1em;
    }}
    
    /* رسائل الحالة */
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
    
    /* معلومات الكسر */
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
    
    .tam-footer {{
        text-align: center; padding: 2rem;
        color: rgba(245, 240, 227, 0.5); font-size: 0.9rem;
        margin-top: 2rem; border-top: 1px solid {COLORS['aged_gold']}20;
    }}
</style>
""", unsafe_allow_html=True)

# ═══ نماذج البيانات ═══
@dataclass
class TafeelaResult:
    name: str
    pattern: str
    actual: str
    status: str  # 'complete', 'incomplete', 'broken'
    position: int
    break_info: Optional[str] = None

@dataclass
class AnalysisResult:
    original_text: str
    binary_code: str
    tafeelat: List[TafeelaResult]
    meter_name: Optional[str]
    meter_type: Optional[str]
    status: str  # 'valid', 'partial', 'invalid'
    break_count: int
    break_locations: List[str]
    confidence: float

# ═══ المحرك العروضي المتقدم ═══
class ArudiEngine:
    """محرك التحليل العروضي الدقيق"""
    
    # التفعيلات الكاملة وأنماطها
    TAFEELAT_COMPLETE = {
        'فعولن': '11010',
        'مفاعيلن': '1101010',
        'مفاعلن': '110110',
        'فاعلاتن': '1011010',
        'فاعلن': '10110',
        'مستفعلن': '1011010',
        'متفاعلن': '1110110',
        'مفاعلتن': '1101110',
        'فاعل': '101',  # ناقصة
        'فعول': '1101',  # ناقصة
        'مفاع': '110',  # ناقصة
        'مستفعل': '10110',  # ناقصة
    }
    
    # البحور ومتطلباتها
    METERS = {
        'الطويل': {
            'pattern': ['فعولن', 'مفاعيلن', 'فعولن', 'مفاعلن'],
            'min_tafeelat': 3,
            'desc': 'أطول البحور'
        },
        'المديد': {
            'pattern': ['فاعلاتن', 'فاعلن', 'فاعلاتن'],
            'min_tafeelat': 2,
            'desc': 'بحر المديح'
        },
        'البسيط': {
            'pattern': ['مستفعلن', 'فاعلن', 'مستفعلن', 'فاعلن'],
            'min_tafeelat': 3,
            'desc': 'أكثر البحور استخداماً'
        },
        'الوافر': {
            'pattern': ['مفاعلتن', 'مفاعلتن', 'فعولن'],
            'min_tafeelat': 2,
            'desc': 'بحر الوصف'
        },
        'الكامل': {
            'pattern': ['متفاعلن', 'متفاعلن', 'متفاعلن'],
            'min_tafeelat': 2,
            'desc': 'بحر السهولة'
        },
        'الهزج': {
            'pattern': ['مفاعيلن', 'فاعلاتن'],
            'min_tafeelat': 2,
            'desc': 'بحر الخفة'
        },
        'الرجز': {
            'pattern': ['مستفعلن', 'مستفعلن', 'مستفعلن'],
            'min_tafeelat': 2,
            'desc': 'بحر الحكمة'
        },
        'الرمل': {
            'pattern': ['فاعلاتن', 'فاعلاتن', 'فاعلاتن'],
            'min_tafeelat': 2,
            'desc': 'بحر الرثاء'
        },
        'السريع': {
            'pattern': ['مستفعلن', 'مستفعلن', 'فاعلن'],
            'min_tafeelat': 2,
            'desc': 'بحر السرعة'
        },
        'المنسرح': {
            'pattern': ['مستفعلن', 'فاعلاتن', 'مستفعلن', 'فاعلن'],
            'min_tafeelat': 3,
            'desc': 'بحر الانسيابية'
        },
        'الخفيف': {
            'pattern': ['فاعلاتن', 'مستفعلن', 'فاعلاتن'],
            'min_tafeelat': 2,
            'desc': 'بحر الليونة'
        },
        'المتقارب': {
            'pattern': ['فعولن', 'فعولن', 'فعولن', 'فعولن'],
            'min_tafeelat': 3,
            'desc': 'بحر التقارب'
        },
        'المتدارك': {
            'pattern': ['فاعلن', 'فاعلن', 'فاعلن', 'فاعلن'],
            'min_tafeelat': 3,
            'desc': 'بحر التدارك'
        },
    }

    @staticmethod
    def text_to_binary(text: str) -> str:
        """تحويل النص العربي إلى نمط ثنائي عروضي"""
        # تبسيط: نفترض أن النص مشكول
        binary = []
        i = 0
        text = ArudiEngine._normalize(text)
        
        while i < len(text):
            char = text[i]
            
            # تخطى المسافات
            if char == ' ':
                i += 1
                continue
            
            # الحروف العربية
            if char in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويى':
                next_char = text[i+1] if i+1 < len(text) else None
                
                # إذا كان هناك حركة صريحة
                if next_char in 'َُِ':
                    binary.append('1')  # متحرك
                    i += 2
                elif next_char == 'ْ':
                    binary.append('0')  # ساكن
                    i += 2
                elif next_char == 'ّ':
                    # الشدة = ساكن + متحرك
                    binary.append('0')
                    binary.append('1')
                    i += 2
                elif next_char in 'ًٌٍ':
                    # التنوين = متحرك + نون ساكنة
                    binary.append('1')
                    binary.append('0')
                    i += 2
                else:
                    # تخمين ذكي
                    if char in 'اويى':
                        binary.append('0')  # حروف العلة ساكنة عادة
                    else:
                        binary.append('1')  # الحروف متحركة افتراضياً
                    i += 1
            else:
                i += 1
        
        return ''.join(binary)
    
    @staticmethod
    def _normalize(text: str) -> str:
        """تطبيع النص"""
        # توحيد الهمزات
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ؤ', 'و').replace('ئ', 'ي').replace('ء', '')
        text = text.replace('ة', 'ه')
        return text
    
    @staticmethod
    def extract_tafeelat(binary: str) -> List[TafeelaResult]:
        """استخراج التفعيلات مع تحديد الكسور"""
        results = []
        i = 0
        
        while i < len(binary):
            found = False
            
            # البحث عن أطول تفعيلة ممكنة
            for name, pattern in sorted(ArudiEngine.TAFEELAT_COMPLETE.items(), 
                                       key=lambda x: len(x[1]), reverse=True):
                length = len(pattern)
                if i + length <= len(binary):
                    segment = binary[i:i+length]
                    
                    # مطابقة تامة
                    if segment == pattern:
                        results.append(TafeelaResult(
                            name=name, pattern=pattern, actual=segment,
                            status='complete', position=i
                        ))
                        i += length
                        found = True
                        break
                    
                    # مطابقة جزئية (كسر عروضي)
                    elif ArudiEngine._is_partial_match(segment, pattern):
                        status = 'incomplete' if len(segment) < len(pattern) else 'broken'
                        break_info = ArudiEngine._analyze_break(segment, pattern, i)
                        
                        results.append(TafeelaResult(
                            name=name, pattern=pattern, actual=segment,
                            status=status, position=i, break_info=break_info
                        ))
                        i += length
                        found = True
                        break
            
            if not found:
                # حرف غير معروف - تخطي
                i += 1
        
        return results
    
    @staticmethod
    def _is_partial_match(actual: str, expected: str) -> bool:
        """التحقق إذا كان النمط مطابقاً جزئياً"""
        if len(actual) != len(expected):
            return False
        
        # السماح باختلاف واحد فقط
        diff = sum(1 for a, e in zip(actual, expected) if a != e)
        return diff <= 1
    
    @staticmethod
    def _analyze_break(actual: str, expected: str, position: int) -> str:
        """تحليل مكان الكسر العروضي"""
        for idx, (a, e) in enumerate(zip(actual, expected)):
            if a != e:
                return f"كسر في الموضع {idx+1}: المتوقع '{e}' والموجود '{a}'"
        return "تفعيلة ناقصة"
    
    @staticmethod
    def identify_meter(tafeelat: List[TafeelaResult]) -> Tuple[Optional[str], Optional[str], str]:
        """تحديد البحر مع مراعاة الكسور"""
        if not tafeelat:
            return None, None, "invalid"
        
        # حساب الكسور
        complete_count = sum(1 for t in tafeelat if t.status == 'complete')
        broken_count = sum(1 for t in tafeelat if t.status == 'broken')
        incomplete_count = sum(1 for t in tafeelat if t.status == 'incomplete')
        
        # إذا كان هناك أكثر من 3 كسور - لا يمكن التحديد
        if broken_count >= 3:
            return None, None, "invalid"
        
        # مطابقة الأنماط
        detected_names = [t.name for t in tafeelat]
        best_match = None
        best_score = 0
        
        for meter_name, meter_info in ArudiEngine.METERS.items():
            score = ArudiEngine._calculate_meter_match(detected_names, meter_info['pattern'])
            if score > best_score:
                best_score = score
                best_match = (meter_name, meter_info)
        
        if not best_match:
            return None, None, "invalid"
        
        meter_name, meter_info = best_match
        
        # تحديد النوع بناءً على عدد التفعيلات
        if complete_count == len(meter_info['pattern']):
            meter_type = "تام"
        elif complete_count == len(meter_info['pattern']) - 1:
            meter_type = "مجزوء"
        elif complete_count == len(meter_info['pattern']) - 2:
            meter_type = "مشطور"
        else:
            meter_type = "منهوك"
        
        # تحديد الحالة العامة
        if broken_count == 0 and incomplete_count == 0:
            status = "valid"
        elif broken_count <= 2:
            status = "partial"
        else:
            status = "invalid"
        
        return meter_name, meter_type, status

    @staticmethod
    def _calculate_meter_match(detected: List[str], expected: List[str]) -> float:
        """حساب درجة مطابقة البحر"""
        if not detected or not expected:
            return 0.0
        
        matches = 0
        for i, exp in enumerate(expected):
            if i < len(detected):
                if detected[i] == exp:
                    matches += 1.0
                elif detected[i] in exp or exp in detected[i]:
                    matches += 0.5
        
        return matches / len(expected)

# ═══ دوال العرض ═══
def render_logo():
    """عرض الشعار"""
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

def render_tafeela_card(tafeela: TafeelaResult, index: int):
    """عرض بطاقة التفعيلة"""
    status_class = tafeela.status
    status_symbol = "✓" if tafeela.status == 'complete' else "!" if tafeela.status == 'incomplete' else "✗"
    
    st.markdown(f"""
    <div class="tafeela-card {status_class}">
        <div class="tafeela-status {status_class}">{status_symbol}</div>
        <div class="tafeela-name {status_class}">{tafeela.name}</div>
        <div class="tafeela-pattern">{tafeela.actual}</div>
        <div style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">
            المتوقع: {tafeela.pattern}
        </div>
        {f'<div class="break-info"><span class="break-location">⚠️ {tafeela.break_info}</span></div>' if tafeela.break_info else ''}
    </div>
    """, unsafe_allow_html=True)

def render_analysis(result: AnalysisResult):
    """عرض نتائج التحليل"""
    
    # عنوان النتائج
    st.markdown("### 🎯 نتائج التحليل العروضي")
    
    # حالة التحليل
    if result.status == "valid":
        st.markdown(f"""
        <div class="status-message success">
            ✅ البحر المحدد: <strong>{result.meter_name} ({result.meter_type})</strong><br>
            نسبة الثقة: {result.confidence:.0f}%
        </div>
        """, unsafe_allow_html=True)
    elif result.status == "partial":
        st.markdown(f"""
        <div class="status-message warning">
            ⚠️ البحر المحتمل: <strong>{result.meter_name} ({result.meter_type})</strong><br>
            يوجد {result.break_count} كسر عروضي في التحليل
        </div>
        """, unsafe_allow_html=True)
        
        # عرض مواقع الكسور
        if result.break_locations:
            st.markdown("#### 📍 مواقع الكسور:")
            for loc in result.break_locations:
                st.markdown(f'<div class="break-info"><span class="break-location">{loc}</span></div>', 
                          unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-message error">
            ❌ <strong>لا يمكن تحديد البحر</strong><br>
            يوجد أكثر من 3 كسور عروضية في النص
        </div>
        """, unsafe_allow_html=True)
        
        if result.break_locations:
            st.markdown("#### 📍 مواقع الأخطاء:")
            for loc in result.break_locations:
                st.markdown(f'<div class="break-info"><span class="break-location">{loc}</span></div>', 
                          unsafe_allow_html=True)
    
    # عرض التفعيلات
    if result.tafeelat:
        st.markdown("#### 🧩 التفعيلات المكتشفة:")
        for idx, tafeela in enumerate(result.tafeelat):
            render_tafeela_card(tafeela, idx)
    
    # التفاصيل التقنية (الرمز الثنائي فقط)
    with st.expander("🔍 التفاصيل التقنية"):
        st.markdown(f"""
        <div class="technical-details">
            <div class="binary-code">{result.binary_code}</div>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    """عرض الفوتر"""
    st.markdown("""
    <div class="tam-footer">
        جميع الحقوق محفوظة © 2026 منصة تام الثقافية
    </div>
    """, unsafe_allow_html=True)

# ═══ الصفحة الرئيسية ═══
def main():
    st.session_state.setdefault('poem_input', '')
    
    render_logo()
    
    # منطقة الإدخال
    poem_input = st.text_area(
        "",
        value=st.session_state.poem_input,
        height=200,
        placeholder="أدخل أبيات القصيدة هنا...",
        key="poem_input_widget"
    )
    
    # أزرار التحكم
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        analyze = st.button("🔍 تحليل القصيدة", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-outline">', unsafe_allow_html=True)
        example = st.button("📋 مثال", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
        clear = st.button("🗑️ مسح", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # معالجة الأحداث
    if clear:
        st.session_state.poem_input = ""
        st.rerun()
    
    if example:
        st.session_state.poem_input = "فَلا تَظُنَّنَّ أَنَّ اللَّيثَ يَبْتَسِمُ"
        st.rerun()
    
    if analyze and poem_input.strip():
        with st.spinner("جاري التحليل العروضي..."):
            # التحليل
            engine = ArudiEngine()
            binary = engine.text_to_binary(poem_input)
            tafeelat = engine.extract_tafeelat(binary)
            meter_name, meter_type, status = engine.identify_meter(tafeelat)
            
            # حساب الكسور
            break_count = sum(1 for t in tafeelat if t.status in ['broken', 'incomplete'])
            break_locations = [f"التفعيلة {i+1}: {t.break_info}" 
                             for i, t in enumerate(tafeelat) 
                             if t.break_info]
            
            # حساب الثقة
            confidence = 100.0 if status == "valid" else (60.0 if status == "partial" else 0.0)
            
            result = AnalysisResult(
                original_text=poem_input,
                binary_code=binary,
                tafeelat=tafeelat,
                meter_name=meter_name,
                meter_type=meter_type,
                status=status,
                break_count=break_count,
                break_locations=break_locations,
                confidence=confidence
            )
            
            render_analysis(result)
    
    elif analyze and not poem_input.strip():
        st.error("⚠️ الرجاء إدخال نص القصيدة أولاً")
    
    render_footer()

if __name__ == "__main__":
    main()
