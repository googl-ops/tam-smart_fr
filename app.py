#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الفراهيدي الذكي
TAM Smart Cultural Platform - Al-Farahidi Smart
"""

import subprocess
import sys

def install_packages():
    packages = ['streamlit']
    for package in packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

install_packages()

import streamlit as st
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# ═══ إعدادات الصفحة ═══
st.set_page_config(
    page_title="مختبر الفراهيدي الذكي | منصة تام",
    page_icon="𐩩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══ الألوان ═══
COLORS = {
    'midnight_blue': '#071A2F',
    'aged_gold': '#C8A44D',
    'electric_turquoise': '#00d4c8',
    'sandstone_cream': '#f5f0e3',
    'error_red': '#ff4757',
    'warning_orange': '#ffa502',
    'success_green': '#2ed573'
}

# ═══ CSS ═══
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
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid {COLORS['aged_gold']}40 !important; border-radius: 15px !important;
        color: {COLORS['sandstone_cream']} !important; font-family: 'Noto Naskh Arabic', serif !important;
        font-size: 1.3rem !important; line-height: 2 !important;
        text-align: center !important; direction: rtl !important; min-height: 200px !important;
    }}
    
    .stTextArea textarea:focus {{
        border-color: {COLORS['electric_turquoise']} !important;
    }}
    
    .stTextArea label {{ display: none !important; }}
    
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
</style>
""", unsafe_allow_html=True)

# ═══ نماذج البيانات ═══
@dataclass
class TafeelaResult:
    name: str
    pattern: str
    actual: str
    status: str
    position: int
    break_info: Optional[str] = None

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

# ═══ المحرك العروضي ═══
class ArudiEngine:
    TAFEELAT_COMPLETE = {
        'فعولن': '11010',
        'مفاعيلن': '1101010',
        'مفاعلن': '110110',
        'فاعلاتن': '1011010',
        'فاعلن': '10110',
        'مستفعلن': '1011010',
        'متفاعلن': '1110110',
        'مفاعلتن': '1101110',
        'فاعل': '101',
        'فعول': '1101',
        'مفاع': '110',
        'مستفعل': '10110',
    }
    
    METERS = {
        'الطويل': {'pattern': ['فعولن', 'مفاعيلن', 'فعولن', 'مفاعلن'], 'min': 3},
        'المديد': {'pattern': ['فاعلاتن', 'فاعلن', 'فاعلاتن'], 'min': 2},
        'البسيط': {'pattern': ['مستفعلن', 'فاعلن', 'مستفعلن', 'فاعلن'], 'min': 3},
        'الوافر': {'pattern': ['مفاعلتن', 'مفاعلتن', 'فعولن'], 'min': 2},
        'الكامل': {'pattern': ['متفاعلن', 'متفاعلن', 'متفاعلن'], 'min': 2},
        'الهزج': {'pattern': ['مفاعيلن', 'فاعلاتن'], 'min': 2},
        'الرجز': {'pattern': ['مستفعلن', 'مستفعلن', 'مستفعلن'], 'min': 2},
        'الرمل': {'pattern': ['فاعلاتن', 'فاعلاتن', 'فاعلاتن'], 'min': 2},
        'السريع': {'pattern': ['مستفعلن', 'مستفعلن', 'فاعلن'], 'min': 2},
        'المنسرح': {'pattern': ['مستفعلن', 'فاعلاتن', 'مستفعلن', 'فاعلن'], 'min': 3},
        'الخفيف': {'pattern': ['فاعلاتن', 'مستفعلن', 'فاعلاتن'], 'min': 2},
        'المتقارب': {'pattern': ['فعولن', 'فعولن', 'فعولن', 'فعولن'], 'min': 3},
        'المتدارك': {'pattern': ['فاعلن', 'فاعلن', 'فاعلن', 'فاعلن'], 'min': 3},
    }

    @staticmethod
    def text_to_binary(text: str) -> str:
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ؤ', 'و').replace('ئ', 'ي').replace('ء', '')
        text = text.replace('ة', 'ه')
        
        binary = []
        i = 0
        
        while i < len(text):
            char = text[i]
            
            if char == ' ':
                i += 1
                continue
            
            if char in 'ابتثجحخدذرزسشصضطظعغفقكلمنهويى':
                next_char = text[i+1] if i+1 < len(text) else None
                
                if next_char in 'َُِ':
                    binary.append('1')
                    i += 2
                elif next_char == 'ْ':
                    binary.append('0')
                    i += 2
                elif next_char == 'ّ':
                    binary.append('0')
                    binary.append('1')
                    i += 2
                elif next_char in 'ًٌٍ':
                    binary.append('1')
                    binary.append('0')
                    i += 2
                else:
                    if char in 'اويى':
                        binary.append('0')
                    else:
                        binary.append('1')
                    i += 1
            else:
                i += 1
        
        return ''.join(binary)
    
    @staticmethod
    def extract_tafeelat(binary: str) -> List[TafeelaResult]:
        results = []
        i = 0
        
        sorted_tafeelat = sorted(ArudiEngine.TAFEELAT_COMPLETE.items(), 
                                key=lambda x: len(x[1]), reverse=True)
        
        while i < len(binary):
            found = False
            
            for name, pattern in sorted_tafeelat:
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
                    
                    elif ArudiEngine._is_partial(segment, pattern):
                        status = 'incomplete' if len(segment) < len(pattern) else 'broken'
                        break_info = ArudiEngine._find_break(segment, pattern, i)
                        
                        results.append(TafeelaResult(
                            name=name, pattern=pattern, actual=segment,
                            status=status, position=i, break_info=break_info
                        ))
                        i += length
                        found = True
                        break
            
            if not found:
                i += 1
        
        return results
    
    @staticmethod
    def _is_partial(actual: str, expected: str) -> bool:
        if len(actual) != len(expected):
            return False
        diff = sum(1 for a, e in zip(actual, expected) if a != e)
        return diff <= 1
    
    @staticmethod
    def _find_break(actual: str, expected: str, position: int) -> str:
        for idx, (a, e) in enumerate(zip(actual, expected)):
            if a != e:
                return f"كسر في الموضع {idx+1}: المتوقع '{e}' والموجود '{a}'"
        return "تفعيلة ناقصة"
    
    @staticmethod
    def identify_meter(tafeelat: List[TafeelaResult]) -> Tuple[Optional[str], Optional[str], str]:
        if not tafeelat:
            return None, None, "invalid"
        
        broken_count = sum(1 for t in tafeelat if t.status == 'broken')
        
        if broken_count >= 3:
            return None, None, "invalid"
        
        detected_names = [t.name for t in tafeelat]
        best_match = None
        best_score = 0
        
        for meter_name, meter_info in ArudiEngine.METERS.items():
            score = ArudiEngine._match_score(detected_names, meter_info['pattern'])
            if score > best_score:
                best_score = score
                best_match = (meter_name, meter_info)
        
        if not best_match:
            return None, None, "invalid"
        
        meter_name, meter_info = best_match
        complete_count = sum(1 for t in tafeelat if t.status == 'complete')
        
        if complete_count == len(meter_info['pattern']):
            meter_type = "تام"
        elif complete_count == len(meter_info['pattern']) - 1:
            meter_type = "مجزوء"
        elif complete_count == len(meter_info['pattern']) - 2:
            meter_type = "مشطور"
        else:
            meter_type = "منهوك"
        
        status = "valid" if broken_count == 0 else "partial" if broken_count <= 2 else "invalid"
        
        return meter_name, meter_type, status
    
    @staticmethod
    def _match_score(detected: List[str], expected: List[str]) -> float:
        if not detected or not expected:
            return 0.0
        matches = sum(1 for i, exp in enumerate(expected) if i < len(detected) and detected[i] == exp)
        return matches / len(expected)

# ═══ دوال العرض ═══
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
    status_class = tafeela.status
    status_symbol = "✓" if tafeela.status == 'complete' else "!" if tafeela.status == 'incomplete' else "✗"
    
    st.markdown(f"""
    <div class="tafeela-card {status_class}">
        <div class="tafeela-status {status_class}">{status_symbol}</div>
        <div class="tafeela-name {status_class}">{tafeela.name}</div>
        <div class="tafeela-pattern">{tafeela.actual}</div>
        <div style="color: #888; font-size: 0.9rem; margin-top: 0.5rem;">
            النمط الصحيح: {tafeela.pattern}
        </div>
        {f'<div class="break-info"><span class="break-location">⚠️ {tafeela.break_info}</span></div>' if tafeela.break_info else ''}
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
            يوجد {result.break_count} كسر عروضي في التحليل
        </div>
        """, unsafe_allow_html=True)
        
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
    
    if result.tafeelat:
        st.markdown("#### 🧩 التفعيلات المكتشفة:")
        for idx, tafeela in enumerate(result.tafeelat):
            render_tafeela(tafeela, idx)
    
    with st.expander("🔍 النمط الثنائي"):
        st.markdown(f'<div class="technical-box">{result.binary_code}</div>', unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="tam-footer">
        جميع الحقوق محفوظة © 2026 منصة تام الثقافية
    </div>
    """, unsafe_allow_html=True)

# ═══ الصفحة الرئيسية ═══
def main():
    render_logo()
    
    poem_input = st.text_area(
        "",
        height=200,
        placeholder="أدخل أبيات القصيدة هنا...",
        key="poem_input"
    )
    
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
    
    if clear:
        st.session_state.poem_input = ""
        st.rerun()
    
    if example:
        st.session_state.poem_input = "فَلا تَظُنَّنَّ أَنَّ اللَّيثَ يَبْتَسِمُ"
        st.rerun()
    
    if analyze and poem_input.strip():
        with st.spinner("جاري التحليل..."):
            engine = ArudiEngine()
            binary = engine.text_to_binary(poem_input)
            tafeelat = engine.extract_tafeelat(binary)
            meter_name, meter_type, status = engine.identify_meter(tafeelat)
            
            break_count = sum(1 for t in tafeelat if t.status in ['broken', 'incomplete'])
            break_locations = [f"التفعيلة {i+1}: {t.break_info}" 
                             for i, t in enumerate(tafeelat) 
                             if t.break_info]
            
            result = AnalysisResult(
                original_text=poem_input,
                binary_code=binary,
                tafeelat=tafeelat,
                meter_name=meter_name,
                meter_type=meter_type,
                status=status,
                break_count=break_count,
                break_locations=break_locations
            )
            
            render_result(result)
    
    elif analyze and not poem_input.strip():
        st.error("⚠️ الرجاء إدخال نص القصيدة أولاً")
    
    render_footer()

if __name__ == "__main__":
    main()
