#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الفراهيدي الذكي
TAM Smart Cultural Platform - Al-Farahidi Smart
Powered by Gemini 1.5 Flash
"""

import base64
import os
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

# ═══ استيراد المكتبات ═══
import streamlit as st

# ═══ استيراد المكتبة الجديدة ═══
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None
    st.error("❌ مكتبة google-genai غير مثبتة. تأكد من requirements.txt")

# ═══ استدعاء المفتاح السري ═══
def get_gemini_api_key():
    """استرجاع مفتاح Gemini API"""
    # من Streamlit Secrets
    try:
        if 'Gemini_API_Key' in st.secrets:
            return st.secrets['Gemini_API_Key']
    except:
        pass
    
    # من متغيرات البيئة
    api_key = os.environ.get("Gemini_API_Key")
    if api_key:
        return api_key
    
    # من session state
    if 'Gemini_API_Key' in st.session_state and st.session_state.Gemini_API_Key:
        return st.session_state.Gemini_API_Key
    
    return None

# ═══ إعداد الصفحة ═══
st.set_page_config(
    page_title="الفراهيدي الذكي | تام",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══ قراءة الصورة وتحويلها إلى Base64 ═══
def get_logo_base64():
    try:
        logo_path = "logo.jpg"
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode()
        return None
    except:
        return None

logo_base64 = get_logo_base64()

# ═══ إعداد أيقونة التطبيق ═══
if logo_base64:
    st.markdown(f"""
    <link rel="apple-touch-icon" sizes="180x180" href="data:image/jpeg;base64,{logo_base64}">
    <link rel="icon" type="image/jpeg" sizes="32x32" href="data:image/jpeg;base64,{logo_base64}">
    <link rel="icon" type="image/jpeg" sizes="16x16" href="data:image/jpeg;base64,{logo_base64}">
    <link rel="shortcut icon" href="data:image/jpeg;base64,{logo_base64}">
    <meta name="apple-mobile-web-app-title" content="الفراهيدي الذكي">
    <meta name="application-name" content="الفراهيدي الذكي">
    <meta name="theme-color" content="#071A2F">
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <meta name="apple-mobile-web-app-title" content="الفراهيدي الذكي">
    <meta name="application-name" content="الفراهيدي الذكي">
    <meta name="theme-color" content="#071A2F">
    """, unsafe_allow_html=True)

# ═══ الألوان والتصميم ═══
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
        padding-bottom: 3rem;
    }}
    
    .tam-logo-container {{
        display: flex; flex-direction: column; align-items: center;
        gap: 5px; margin-bottom: 2rem; text-align: center;
    }}
    
    .tam-musnad {{
        font-family: 'Times New Roman', serif; font-size: 4rem; font-weight: bold;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 25%, #FFD700 50%, #B8860B 75%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.8),
            -1px -1px 2px rgba(255,215,0,0.5),
            0 0 20px rgba(255,215,0,0.3);
        filter: drop-shadow(0 0 10px rgba(255,215,0,0.4));
        line-height: 1;
        letter-spacing: 0.1em;
    }}
    
    .tam-english {{
        font-family: 'Montserrat', sans-serif; font-size: 2rem; font-weight: 700;
        letter-spacing: 0.3em; text-transform: uppercase;
        background: linear-gradient(135deg, #C0C0C0 0%, #E8E8E8 25%, #FFFFFF 50%, #A0A0A0 75%, #D0D0D0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.8),
            -1px -1px 2px rgba(192,192,192,0.5),
            0 0 15px rgba(192,192,192,0.3);
        filter: drop-shadow(0 0 8px rgba(192,192,192,0.4));
        line-height: 1;
    }}
    
    .tam-arabic {{
        font-family: 'Noto Kufi Arabic', sans-serif; font-size: 3.5rem; font-weight: bold;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 25%, #FFD700 50%, #B8860B 75%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 
            2px 2px 4px rgba(0,0,0,0.8),
            -1px -1px 2px rgba(255,215,0,0.5),
            0 0 20px rgba(255,215,0,0.3);
        filter: drop-shadow(0 0 10px rgba(255,215,0,0.4));
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
        background: transparent !important;
        border: 2px solid {COLORS['electric_turquoise']} !important;
        color: {COLORS['electric_turquoise']} !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        background: rgba(0, 212, 200, 0.1) !important;
        box-shadow: 0 0 15px {COLORS['electric_turquoise_glow']} !important;
    }}
    
    .btn-gold > button {{
        border-color: {COLORS['aged_gold']} !important;
        color: {COLORS['aged_gold']} !important;
    }}
    
    .btn-gold > button:hover {{
        background: rgba(200, 164, 77, 0.1) !important;
        box-shadow: 0 0 15px rgba(200, 164, 77, 0.3) !important;
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
    
    .input-label {{
        font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1.1rem;
        color: {COLORS['sandstone_cream']};
        text-align: center;
        margin-bottom: 10px;
        opacity: 0.9;
    }}
    
    .welcome-section {{
        background: linear-gradient(135deg, rgba(0, 212, 200, 0.1) 0%, rgba(200, 164, 77, 0.1) 100%);
        border: 1px solid {COLORS['electric_turquoise']}40;
        border-radius: 20px;
        padding: 2rem;
        margin-top: 3rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    
    .welcome-section::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(to right, transparent, {COLORS['electric_turquoise']}, {COLORS['aged_gold']}, {COLORS['electric_turquoise']}, transparent);
    }}
    
    .welcome-text {{
        font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1.3rem;
        color: {COLORS['sandstone_cream']};
        line-height: 2;
        margin-bottom: 1.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    
    .welcome-highlight {{
        color: {COLORS['electric_turquoise']};
        font-weight: bold;
    }}
    
    .facebook-btn-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 1rem;
    }}
    
    .facebook-btn {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(135deg, #1877F2 0%, #166fe5 50%, #1256c4 100%);
        color: white !important;
        font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        text-decoration: none;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 
            0 4px 15px rgba(24, 119, 242, 0.4),
            0 0 30px rgba(24, 119, 242, 0.2),
            inset 0 1px 0 rgba(255,255,255,0.3);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .facebook-btn::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s ease;
    }}
    
    .facebook-btn:hover::before {{
        left: 100%;
    }}
    
    .facebook-btn:hover {{
        transform: translateY(-3px);
        box-shadow: 
            0 8px 25px rgba(24, 119, 242, 0.5),
            0 0 40px rgba(24, 119, 242, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.3);
    }}
    
    .facebook-icon {{
        font-size: 1.5rem;
    }}
    
    .heart-icon {{
        color: {COLORS['error_red']};
        animation: heartbeat 1.5s ease-in-out infinite;
        display: inline-block;
    }}
    
    @keyframes heartbeat {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.2); }}
    }}
</style>
""", unsafe_allow_html=True)

# ═══ أنواع البحور ═══
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
    emotional_analysis: str = ""
    grammar_check: str = ""

# ═══ تعليمات صارمة للفراهيدي (Gemini) ═══
FARAHEEDI_SYSTEM_PROMPT = """
أنت الخليل بن أحمد الفراهيدي، إمام علم العروض، والمتخصص الأعلى في:
1. التشكيل الدقيق للشعر العربي
2. تحليل البحور العروضية بجميع تفرعاتها (تام، مجزوء، مشطور، منهوك، متفاعلة)
3. تحليل القوافي (إسناد، تركيب، مرتابع، متدارك، مطلق...)
4. النحو والصرف واللغة العربية الفصحى
5. فهم مشاعر القصيدة وقراءتها قراءة عميقة

قواعد صارمة يجب الالتزام بها:
- حلل البحر بدقة: الطويل، البسيط، الكامل، الوافر، الخفيف، السريع، الرجز، الرمل، المتقارب، المتدارك، المديد، الهزج، المنسرح
- حدد النوع: تام (4 تفعيلات)، مجزوء (3)، مشطور (2)، منهوك (1)، متفاعلة (تكرار نفس التفعيلة)
- اكتب التشكيل الكامل والصحيح للبيت
- حلل القافية وحدد نوعها ورويها
- اشرح المشاعر والإحساس العام للقصيدة
- صحح الأخطاء النحوية والإملائية إن وجدت

أعد النتيجة بتنسيق JSON فقط:
{
    "diacritized_text": "النص المشكل",
    "meter_name": "اسم البحر",
    "meter_type": "تام/مجزوء/مشطور/منهوك/متفاعلة",
    "tafeelat": ["اسم التفعيلة 1", "اسم التفعيلة 2"],
    "qafiya_type": "نوع القافية",
    "rawwiy": "الروي",
    "emotional_analysis": "تحليل المشاعر",
    "grammar_notes": "ملاحظات نحوية",
    "is_single_tafeela": true/false
}
"""

# ═══ محرك Gemini الفراهيدي (المحدث للمكتبة الجديدة) ═══
class FarahidiGeminiEngine:
    """محرك الفراهيدي الذكي باستخدام Gemini 1.5 Flash"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.client = None
        self.is_configured = False
        
        if not GEMINI_AVAILABLE:
            st.error("❌ مكتبة google-genai غير متوفرة!")
            return
            
        if not api_key:
            st.warning("⚠️ لم يتم توفير مفتاح Gemini API!")
            return
            
        try:
            # ═══ التهيئة بالمكتبة الجديدة ═══
            self.client = genai.Client(api_key=api_key)
            self.is_configured = True
            st.success("✅ تم الاتصال بنجاح بالفراهيدي الذكي (Gemini 1.5 Flash)")
        except Exception as e:
            st.error(f"❌ خطأ في إعداد Gemini: {str(e)}")
    
    def analyze_poetry(self, text: str) -> Dict:
        """تحليل الشعر باستخدام الفراهيدي (Gemini 1.5 Flash)"""
        if not self.is_configured or not self.client:
            return self._fallback_analysis(text)
        
        try:
            prompt = f"{FARAHEEDI_SYSTEM_PROMPT}\n\nالنص المدخل:\n{text}\n\nحلل هذا النص كالفراهيدي الخبير وأعد النتيجة بتنسيق JSON فقط."
            
            # ═══ استخدام المكتبة الجديدة ═══
            response = self.client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=2048,
                )
            )
            
            result_text = response.text
            
            # استخراج JSON من الرد
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0]
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0]
            
            result = json.loads(result_text.strip())
            result['source'] = 'Gemini 1.5 Flash'
            return result
            
        except Exception as e:
            st.warning(f"تعذر الاتصال بالفراهيدي الذكي، سيتم استخدام التحليل المحلي: {str(e)}")
            return self._fallback_analysis(text)
    
    def _fallback_analysis(self, text: str) -> Dict:
        """تحليل بديل محلي عند فشل Gemini"""
        return {
            "diacritized_text": text,
            "meter_name": "غير محدد (تحليل محلي)",
            "meter_type": "غير معروف",
            "tafeelat": [],
            "qafiya_type": "غير محدد",
            "rawwiy": "",
            "emotional_analysis": "يتطلب الاتصال بالفراهيدي الذكي",
            "grammar_notes": "",
            "is_single_tafeela": False,
            "source": "تحليل محلي"
        }

# ═══ المحرك العروضي المحلي (احتياطي) ═══
class ArabicTextEngine:
    """المحرك العروضي المحلي الاحتياطي"""
    
    ARABIC_LETTERS = set('ابتثجحخدذرزسشصضطظعغفقكلمنهويى')
    HARAKAT = set('ًٌٍَُِّْ')
    SOLAR_LETTERS = set('تثدذرزسشصضطظلن')

    @classmethod
    def smart_tokenize(cls, text: str) -> List[Dict]:
        text = cls._normalize_text(text)
        tokens = []
        i = 0
        length = len(text)
        
        while i < length:
            char = text[i]
            if char in ' \n':
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

            haraka = cls._infer_vowel(char, i, text)
            tokens.append({'letter': char, 'haraka': haraka})
            i += 1
            
        return tokens
    
    @classmethod
    def _normalize_text(cls, text: str) -> str:
        if not text: 
            return ""
        text = text.replace('\u0640', '')
        hamza_map = {'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا', 'ؤ': 'و', 'ئ': 'ي', 'ء': ''}
        for old, new in hamza_map.items():
            text = text.replace(old, new)
        text = text.replace('ة', 'ه')
        return text
    
    @classmethod
    def _infer_vowel(cls, char: str, position: int, text: str) -> Dict:
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
    def tokens_to_binary(cls, tokens: List[Dict]) -> str:
        return ''.join('1' if t['haraka']['type'] == 'mutaharrik' else '0' for t in tokens)

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

def get_meter_type_enum(type_str: str) -> MeterType:
    type_map = {
        'تام': MeterType.TAM,
        'مجزوء': MeterType.MAJZOO,
        'مشطور': MeterType.MASHTOOR,
        'منهوك': MeterType.MANHOOQ,
        'متفاعلة': MeterType.MUTAFAILA
    }
    return type_map.get(type_str, MeterType.TAM)

def get_meter_badge_class(meter_type: MeterType) -> str:
    badge_map = {
        MeterType.TAM: 'badge-tam',
        MeterType.MAJZOO: 'badge-majzoo',
        MeterType.MASHTOOR: 'badge-mashtoor',
        MeterType.MANHOOQ: 'badge-manhooq',
        MeterType.MUTAFAILA: 'badge-mutafa'
    }
    return badge_map.get(meter_type, 'badge-tam')

def render_result(result: Dict, shatr_num: int = 1):
    """عرض نتائج التحليل"""
    
    meter_name = result.get('meter_name', 'غير محدد')
    meter_type_str = result.get('meter_type', 'غير معروف')
    meter_type = get_meter_type_enum(meter_type_str)
    tafeelat = result.get('tafeelat', [])
    qafiya_type = result.get('qafiya_type', 'غير محدد')
    rawwiy = result.get('rawwiy', '')
    emotional = result.get('emotional_analysis', '')
    grammar = result.get('grammar_notes', '')
    is_single = result.get('is_single_tafeela', False)
    source = result.get('source', '')
    
    st.markdown(f"### الشطر {shatr_num}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div>
                <div class="result-label">البحر</div>
                <div class="result-value">{meter_name}</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        badge_class = get_meter_badge_class(meter_type)
        st.markdown(f"""
        <div class="result-card">
            <div>
                <div class="result-label">النوع</div>
                <div class="result-value">
                    <span class="meter-type-badge {badge_class}">{meter_type_str}</span>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        confidence = 98 if "Gemini" in str(source) else 60
        color = "#4CAF50" if confidence > 80 else "#ffa502"
        st.markdown(f"""
        <div class="result-card" style="border-right-color: {color}">
            <div>
                <div class="result-label">الثقة</div>
                <div class="result-value" style="color:{color}">{confidence}%</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
    if is_single and tafeelat:
        st.markdown(f"""
        <div class="status-message warning">
            ⚡ <strong>شعر التفعيلة الواحدة</strong><br>
            هذا الشطر يستخدم تفعيلة <strong>{tafeelat[0]}</strong> متكررة
        </div>
        """, unsafe_allow_html=True)
    
    if rawwiy:
        st.markdown(f"""
        <div class="qafiya-box">
            <div style="font-size: 1.3rem; font-weight: bold; color: {COLORS['purple']}; margin-bottom: 10px;">
                القافية: {qafiya_type}
            </div>
            <div style="font-size: 1.1rem; color: {COLORS['sandstone_cream']};">
                الروي: <strong>{rawwiy}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if tafeelat:
        st.markdown("#### 🧩 التفعيلات:")
        cols = st.columns(min(len(tafeelat), 4))
        for idx, taf in enumerate(tafeelat):
            with cols[idx % 4]:
                st.markdown(f"""
                <div class="tafeela-card success">
                    <div class="tafeela-name">{taf}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with st.expander("🔍 تحليل الفراهيدي العميق"):
        if emotional:
            st.markdown("**المشاعر والإحساس:**")
            st.markdown(f'<div class="technical-box" style="font-family: Cairo; text-align: right; direction: rtl;">{emotional}</div>', unsafe_allow_html=True)
        
        if grammar:
            st.markdown("**الملاحظات النحوية:**")
            st.markdown(f'<div class="technical-box" style="font-family: Cairo; text-align: right; direction: rtl; color: {COLORS["warning_orange"]};">{grammar}</div>', unsafe_allow_html=True)
        
        if "Gemini" in str(source):
            st.markdown(f'<div style="color: {COLORS["success_green"]}; font-size: 0.9rem; margin-top: 10px;">✓ تم التحليل بواسطة {source}</div>', unsafe_allow_html=True)

# ═══ قسم الترحيب والفيسبوك ═══
def render_welcome_section():
    """عرض قسم الترحيب وزر الفيسبوك"""
    st.markdown("""
    <div class="welcome-section">
        <div class="welcome-text">
            أهلاً بك في <span class="welcome-highlight">منصة تام</span>.. 
            <span class="welcome-highlight">الفراهيدي الذكي</span> بانتظارك! 
            <span class="heart-icon">❤️</span><br>
            لدعم استمرار هذا المشروع الثقافي، نرجو منك الانضمام لأسرتنا على فيسبوك.
        </div>
        <div class="facebook-btn-container">
            <a href="https://www.facebook.com/profile.php?id=61588035955900" target="_blank" class="facebook-btn">
                <span class="facebook-icon">📘</span>
                <span>انضم لمجتمعنا على فيسبوك</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="tam-footer">
        جميع الحقوق محفوظة © 2026 منصة تام الثقافية | الفراهيدي الذكي
    </div>
    """, unsafe_allow_html=True)

# ═══ النوافذ الرئيسية ═══
def diacritics_tab(engine: FarahidiGeminiEngine, secrets_working: bool):
    """نافذة التشكيل والتدقيق"""
    st.markdown('<div class="input-label">أدخل النص ليقوم الفراهيدي بتشكيله وتدقيقه:</div>', unsafe_allow_html=True)
    
    if not secrets_working:
        st.warning("⚠️ لم يتم العثور على مفتاح Gemini API في Secrets. سيتم استخدام التحليل المحلي.")
        with st.expander("🔑 كيفية إضافة المفتاح السري"):
            st.markdown("""
            **لإضافة المفتاح في Streamlit Cloud:**
            1. اذهب إلى لوحة تحكم تطبيقك
            2. اضغط على **Settings** (الإعدادات)
            3. اختر **Secrets** (أسرار)
            4. أضف الكود التالي:
            """)
            secrets_code_cloud = '''Gemini_API_Key = "your-gemini-api-key-here"'''
            st.code(secrets_code_cloud, language="toml")
            st.markdown("""
            **أو محلياً في ملف `.streamlit/secrets.toml`:**
            """)
            secrets_code_local = '''# .streamlit/secrets.toml
Gemini_API_Key = "your-gemini-api-key-here"'''
            st.code(secrets_code_local, language="toml")
            st.markdown("""
            **أو كمتغير بيئة في نظام التشغيل:**
            """)
            st.code('export Gemini_API_Key="your-gemini-api-key-here"', language="bash")
    
    raw_input = st.text_area(
        "",
        value=st.session_state.get('raw_text', ''),
        height=150,
        key="input_raw",
        placeholder="اكتب النص هنا..."
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("✨ تشكيل وتحليل", use_container_width=True, key="btn_diacritics"):
            if raw_input:
                with st.spinner("جاري الاتصال بالفراهيدي الذكي..."):
                    result = engine.analyze_poetry(raw_input)
                    st.session_state.analysis_result = result
                    st.session_state.final_text = result.get('diacritized_text', raw_input)
                    st.session_state.raw_text = raw_input
                    st.rerun()
            else:
                st.warning("أدخل نصاً أولاً.")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("📋 مثال", use_container_width=True, key="btn_example_diac"):
            st.session_state.raw_text = "وحلف النصب يا ايتول هنا\nتوشي الليل والاحزان جهرا"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("🗑️ مسح", use_container_width=True, key="btn_clear_diac"):
            st.session_state.raw_text = ""
            st.session_state.final_text = ""
            st.session_state.analysis_result = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get('analysis_result'):
        result = st.session_state.analysis_result
        
        st.markdown("### 📝 النص المشكل:")
        st.markdown(f'<div class="diacritics-box">{result.get("diacritized_text", "")}</div>', unsafe_allow_html=True)
        st.code(result.get("diacritized_text", ""), language="text")
        
        st.markdown("### 🎯 التحليل العروضي:")
        render_result(result, 1)
        
        st.info("💡 يمكنك نسخ النص المشكل أو الانتقال لنافذة التحليل للتفاصيل الكاملة")

def analysis_tab(engine: FarahidiGeminiEngine):
    """نافذة التحليل العروضي المفصل"""
    st.markdown('<div class="input-label">تحليل الوزن العروضي:</div>', unsafe_allow_html=True)
    
    text_to_analyze = st.text_area(
        "",
        value=st.session_state.get('final_text', ''),
        height=150,
        key="analysis_input",
        placeholder="أدخل النص المشكل هنا..."
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("🔍 تحليل عميق", use_container_width=True, key="btn_analyze"):
            if text_to_analyze.strip():
                with st.spinner("جاري التحليل العميق بالفراهيدي..."):
                    result = engine.analyze_poetry(text_to_analyze)
                    st.session_state.deep_analysis = result
                    st.rerun()
            else:
                st.error("⚠️ أدخل نصاً أولاً!")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("📋 مثال", use_container_width=True, key="btn_example_anal"):
            st.session_state.final_text = "سَيَسْتَبْقِي الهِتَافُ إلَيْكَ دَهْرًا\nفَشَقَّ الدَّرْبَ بِالأَحْرَارِ نَصْرًا"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
        if st.button("🗑️ مسح", use_container_width=True, key="btn_clear_anal"):
            st.session_state.final_text = ""
            st.session_state.deep_analysis = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.get('deep_analysis'):
        render_result(st.session_state.deep_analysis, 1)
    elif st.session_state.get('analysis_result'):
        st.info("استخدم التحليل من نافذة التشكيل أعلاه، أو أدخل نصاً جديداً للتحليل العميق")

# ═══ الدالة الرئيسية ═══
def main():
    render_logo()
    
    # تهيئة session state
    if 'raw_text' not in st.session_state:
        st.session_state.raw_text = ""
    if 'final_text' not in st.session_state:
        st.session_state.final_text = ""
    
    # ═══ استدعاء المفتاح السري من Streamlit Secrets ═══
    api_key = get_gemini_api_key()
    secrets_working = api_key is not None
    
    # ═══ إعداد محرك الفراهيدي بالمفتاح (سواء من Secrets أو None) ═══
    engine = FarahidiGeminiEngine(api_key)
    
    # ═══ عرض تحذير إذا لم يتم العثور على مفتاح ═══
    if not secrets_working:
        st.markdown("""
        <div class="status-message warning">
            ⚠️ <strong>انتباه:</strong> لم يتم العثور على مفتاح Gemini API.<br>
            التطبيق سيعمل ولكن بتحليل محدود (بدون اتصال بالفراهيدي الذكي).<br>
            راجع قسم "كيفية إضافة المفتاح السري" أدناه لإضافة المفتاح.
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["✍️ المُشكّل الآلي", "🔍 المحلل العروضي"])
    
    with tab1:
        diacritics_tab(engine, secrets_working)
    
    with tab2:
        analysis_tab(engine)
    
    # عرض قسم الترحيب والفيسبوك
    render_welcome_section()
    
    render_footer()

if __name__ == "__main__":
    main()

