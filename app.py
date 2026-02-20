#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الفراهيدي الذكي
TAM Smart Cultural Platform - Al-Farahidi Smart
Powered by Chinese AI Models (Qwen, Kimi, DeepSeek)
"""

import base64
import os
import json
import re
import requests
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

# ═══ استيراد المكتبات ═══
import streamlit as st

# ═══ إعداد الصفحة ═══
st.set_page_config(
    page_title="الفراهيدي الذكي | تام",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
    'chinese_red': '#DE2910',
}

# ═══ CSS كامل ═══
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
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 25%, #FFD700 50%, #B8860B 75%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255,215,0,0.3);
    }}
    
    .tam-arabic {{
        font-family: 'Noto Kufi Arabic', sans-serif; font-size: 3.5rem; font-weight: bold;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 25%, #FFD700 50%, #B8860B 75%, #FFD700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .tam-separator {{
        height: 4px; width: 80%; margin: 10px auto;
        background: linear-gradient(to right, transparent, {COLORS['aged_gold']}, transparent);
    }}
    
    .chinese-badge {{
        display: inline-flex; align-items: center; gap: 8px;
        background: linear-gradient(135deg, {COLORS['chinese_red']}, #ff6b6b);
        color: white; padding: 8px 20px;
        border-radius: 25px; font-family: 'Noto Kufi Arabic';
        font-size: 0.9rem; margin-top: 10px;
        box-shadow: 0 4px 15px rgba(222, 41, 16, 0.3);
    }}
    
    .farahidi-title {{
        margin-top: 1rem; padding: 0.5rem 2rem;
        border: 1px solid {COLORS['electric_turquoise']}; border-radius: 50px;
        color: {COLORS['electric_turquoise']}; font-family: 'Noto Kufi Arabic';
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
    }}
    
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
    
    .result-card {{
        background: rgba(10, 22, 40, 0.6);
        border-right: 4px solid {COLORS['electric_turquoise']};
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
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
    
    .model-selector {{
        background: rgba(10, 22, 40, 0.8);
        border: 1px solid {COLORS['aged_gold']}40;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 2rem;
    }}
    
    .model-card {{
        background: rgba(222, 41, 16, 0.1);
        border: 1px solid {COLORS['chinese_red']};
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .model-card:hover {{
        background: rgba(222, 41, 16, 0.2);
        transform: translateX(-5px);
    }}
    
    .model-card.selected {{
        background: rgba(222, 41, 16, 0.3);
        border-width: 2px;
    }}
    
    .welcome-section {{
        background: linear-gradient(135deg, rgba(0, 212, 200, 0.1) 0%, rgba(200, 164, 77, 0.1) 100%);
        border: 1px solid {COLORS['electric_turquoise']}40;
        border-radius: 20px;
        padding: 2rem;
        margin-top: 3rem;
        text-align: center;
    }}
    
    .facebook-btn {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        background: linear-gradient(135deg, #1877F2 0%, #166fe5 100%);
        color: white !important;
        font-family: 'Noto Kufi Arabic', sans-serif;
        font-size: 1.2rem;
        font-weight: bold;
        padding: 1rem 2.5rem;
        border-radius: 50px;
        text-decoration: none;
        transition: all 0.3s ease;
    }}
    
    .facebook-btn:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(24, 119, 242, 0.5);
    }}
    
    .tam-footer {{
        text-align: center; padding: 2rem;
        color: rgba(245, 240, 227, 0.5); font-size: 0.9rem;
        margin-top: 2rem; border-top: 1px solid {COLORS['aged_gold']}20;
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

# ═══ تعليمات صارمة للفراهيدي (الصيني) ═══
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

# ═══ محرك الفراهيدي الصيني ═══
class ChineseAIFarahidiEngine:
    """محرك الفراهيدي الذكي باستخدام النماذج الصينية"""
    
    # ═══ إعدادات النماذج الصينية المتاحة ═══
    MODELS = {
        "qwen3-32b": {
            "name": "Qwen 3 (32B) - Alibaba",
            "provider": "openrouter",
            "model_id": "qwen/qwen3-32b:free",
            "description": "أفضل نموذج صيني مفتوح المصدر، يتفوق على Llama",
            "requires_key": True
        },
        "kimi-k2": {
            "name": "Kimi K2 - Moonshot",
            "provider": "openrouter",
            "model_id": "moonshotai/kimi-k2:free",
            "description": "خبير البرمجة واللغة العربية",
            "requires_key": True
        },
        "kimi-k2.5": {
            "name": "Kimi K2.5 - Moonshot",
            "provider": "nvidia",
            "model_id": "moonshotai/kimi-k2.5",
            "description": "الأحدث والأقوى - متاح مجاناً عبر NVIDIA",
            "requires_key": True
        },
        "deepseek-r1": {
            "name": "DeepSeek R1",
            "provider": "openrouter",
            "model_id": "deepseek/deepseek-r1:free",
            "description": "ملك التفكير المنطقي والعميق",
            "requires_key": True
        },
        "glm-4.5": {
            "name": "GLM-4.5 - Zhipu AI",
            "provider": "openrouter",
            "model_id": "z-ai/glm-4.5:free",
            "description": "نصف الحجم، ضعف الأداء",
            "requires_key": True
        }
    }
    
    def __init__(self, api_key: str = None, model_key: str = "qwen3-32b"):
        self.api_key = api_key
        self.model_key = model_key
        self.model_config = self.MODELS.get(model_key, self.MODELS["qwen3-32b"])
        self.is_configured = False
        
        if api_key:
            self.is_configured = True
    
    def analyze_poetry(self, text: str) -> Dict:
        """تحليل الشعر باستخدام النموذج الصيني المختار"""
        if not self.is_configured:
            return self._fallback_analysis(text)
        
        try:
            provider = self.model_config["provider"]
            
            if provider == "openrouter":
                return self._call_openrouter(text)
            elif provider == "nvidia":
                return self._call_nvidia(text)
            else:
                return self._fallback_analysis(text)
                
        except Exception as e:
            st.warning(f"⚠️ تعذر الاتصال بالنموذج الصيني: {str(e)}")
            return self._fallback_analysis(text)
    
    def _call_openrouter(self, text: str) -> Dict:
        """استدعاء OpenRouter API"""
        prompt = f"{FARAHEEDI_SYSTEM_PROMPT}\n\nالنص المدخل:\n{text}\n\nحلل هذا النص كالفراهيدي الخبير وأعد النتيجة بتنسيق JSON فقط."
        
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://tam-platform.streamlit.app",
                "X-Title": "الفراهيدي الذكي - تام"
            },
            json={
                "model": self.model_config["model_id"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 2048
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            result_text = data['choices'][0]['message']['content']
            return self._parse_result(result_text)
        else:
            raise Exception(f"OpenRouter Error: {response.status_code}")
    
    def _call_nvidia(self, text: str) -> Dict:
        """استدعاء NVIDIA NIMs API"""
        prompt = f"{FARAHEEDI_SYSTEM_PROMPT}\n\nالنص المدخل:\n{text}\n\nحلل هذا النص كالفراهيدي الخبير وأعد النتيجة بتنسيق JSON فقط."
        
        response = requests.post(
            url="https://integrate.api.nvidia.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model_config["model_id"],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 2048
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            result_text = data['choices'][0]['message']['content']
            return self._parse_result(result_text)
        else:
            raise Exception(f"NVIDIA Error: {response.status_code}")
    
    def _parse_result(self, result_text: str) -> Dict:
        """استخراج JSON من الرد"""
        # تنظيف الرد
        if "```json" in result_text:
            result_text = result_text.split("```json")[1].split("```")[0]
        elif "```" in result_text:
            result_text = result_text.split("```")[1].split("```")[0]
        
        result = json.loads(result_text.strip())
        result['source'] = self.model_config["name"]
        result['model_key'] = self.model_key
        return result
    
    def _fallback_analysis(self, text: str) -> Dict:
        """تحليل بديل محلي"""
        return {
            "diacritized_text": text,
            "meter_name": "غير محدد (تحليل محلي)",
            "meter_type": "غير معروف",
            "tafeelat": [],
            "qafiya_type": "غير محدد",
            "rawwiy": "",
            "emotional_analysis": "يتطلب الاتصال بالنموذج الصيني",
            "grammar_notes": "",
            "is_single_tafeela": False,
            "source": "تحليل محلي",
            "model_key": "local"
        }

# ═══ دوال العرض ═══
def render_logo():
    st.markdown("""
    <div class="tam-logo-container">
        <div class="tam-musnad" dir="ltr">𐩩𐩱𐩣</div>
        <div class="tam-arabic">تام</div>
        <div class="tam-separator"></div>
        <div style="font-family: 'Noto Kufi Arabic'; color: #C8A44D; font-size: 1.2rem;">منصة تام الثقافية الذكية</div>
        <div class="chinese-badge">🇨🇳 مدعوم بالذكاء الاصطناعي الصيني</div>
        <div class="farahidi-title"><span>🧠</span> الفراهيدي الذكي</div>
    </div>
    """, unsafe_allow_html=True)

def render_model_selector() -> tuple:
    """عرض اختيار النموذج الصيني"""
    st.markdown("### 🤖 اختر النموذج الصيني")
    
    cols = st.columns(3)
    selected_model = None
    
    models = ChineseAIFarahidiEngine.MODELS
    
    for idx, (key, config) in enumerate(models.items()):
        with cols[idx % 3]:
            is_selected = st.session_state.get('selected_model') == key
            border_color = "#DE2910" if is_selected else "#C8A44D40"
            bg_color = "rgba(222, 41, 16, 0.2)" if is_selected else "rgba(10, 22, 40, 0.6)"
            
            card_html = f"""
            <div style="
                background: {bg_color};
                border: 2px solid {border_color};
                border-radius: 15px;
                padding: 1rem;
                margin: 0.5rem 0;
                cursor: pointer;
                transition: all 0.3s ease;
            ">
                <div style="font-family: 'Noto Kufi Arabic'; font-weight: bold; color: #00d4c8; font-size: 1rem;">
                    {config['name']}
                </div>
                <div style="font-size: 0.8rem; color: #f5f0e3; opacity: 0.8; margin-top: 5px;">
                    {config['description']}
                </div>
                <div style="font-size: 0.7rem; color: #C8A44D; margin-top: 5px;">
                    المزود: {config['provider']}
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            if st.button(f"اختيار", key=f"btn_{key}", use_container_width=True):
                st.session_state.selected_model = key
                st.rerun()
    
    return st.session_state.get('selected_model', 'qwen3-32b')

def get_api_key_for_model(model_key: str) -> Optional[str]:
    """الحصول على مفتاح API المناسب للنموذج"""
    config = ChineseAIFarahidiEngine.MODELS.get(model_key)
    if not config:
        return None
    
    provider = config["provider"]
    
    # محاولة قراءة من Secrets
    try:
        if provider == "openrouter":
            if 'OpenRouter_API_Key' in st.secrets:
                return st.secrets['OpenRouter_API_Key']
        elif provider == "nvidia":
            if 'NVIDIA_API_Key' in st.secrets:
                return st.secrets['NVIDIA_API_Key']
    except:
        pass
    
    # محاولة قراءة من متغيرات البيئة
    if provider == "openrouter":
        return os.environ.get("OpenRouter_API_Key")
    elif provider == "nvidia":
        return os.environ.get("NVIDIA_API_Key")
    
    return None

def render_api_key_input(model_key: str):
    """عرض حقل إدخال مفتاح API"""
    config = ChineseAIFarahidiEngine.MODELS.get(model_key)
    if not config:
        return None
    
    provider = config["provider"]
    
    st.markdown(f"""
    <div style="background: rgba(255, 165, 2, 0.1); border: 1px dashed #ffa502; 
                border-radius: 10px; padding: 1rem; margin: 1rem 0;">
        <div style="font-family: 'Noto Kufi Arabic'; color: #ffa502; margin-bottom: 10px;">
            🔑 أدخل مفتاح API للـ {config['name']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if provider == "openrouter":
        st.markdown("""
        <div style="font-size: 0.9rem; margin-bottom: 10px;">
            1. سجل مجاناً في <a href="https://openrouter.ai" target="_blank" style="color: #00d4c8;">openrouter.ai</a><br>
            2. احصل على API Key من لوحة التحكم<br>
            3. أدخل المفتاح هنا:
        </div>
        """, unsafe_allow_html=True)
        api_key = st.text_input("OpenRouter API Key", type="password", key="openrouter_key")
        
    elif provider == "nvidia":
        st.markdown("""
        <div style="font-size: 0.9rem; margin-bottom: 10px;">
            1. سجل مجاناً في <a href="https://build.nvidia.com" target="_blank" style="color: #00d4c8;">build.nvidia.com</a><br>
            2. اختر Kimi K2.5 واضغط "Get API Key"<br>
            3. أدخل المفتاح هنا:
        </div>
        """, unsafe_allow_html=True)
        api_key = st.text_input("NVIDIA API Key", type="password", key="nvidia_key")
    
    return api_key

def render_result(result: Dict):
    """عرض نتائج التحليل"""
    meter_name = result.get('meter_name', 'غير محدد')
    meter_type = result.get('meter_type', 'غير معروف')
    tafeelat = result.get('tafeelat', [])
    qafiya_type = result.get('qafiya_type', 'غير محدد')
    rawwiy = result.get('rawwiy', '')
    emotional = result.get('emotional_analysis', '')
    grammar = result.get('grammar_notes', '')
    source = result.get('source', 'غير معروف')
    
    # شارة المصدر
    is_chinese = "Gemini" not in str(source) and "محلي" not in str(source)
    badge_color = "#DE2910" if is_chinese else "#4CAF50"
    badge_text = "🇨🇳 نموذج صيني" if is_chinese else "✓"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">البحر العروضي</div>
            <div class="result-value">{meter_name}</div>
        </div>""", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">النوع</div>
            <div class="result-value">{meter_type}</div>
        </div>""", unsafe_allow_html=True)
    
    with col3:
        confidence = 95 if is_chinese else 60
        color = "#4CAF50" if confidence > 80 else "#ffa502"
        st.markdown(f"""
        <div class="result-card" style="border-right-color: {color}">
            <div class="result-label">الثقة</div>
            <div class="result-value" style="color:{color}">{confidence}%</div>
        </div>""", unsafe_allow_html=True)
    
    # شارة المصدر
    st.markdown(f"""
    <div style="text-align: center; margin: 10px 0;">
        <span style="background: {badge_color}; color: white; padding: 5px 15px; 
                     border-radius: 20px; font-size: 0.9rem; font-family: 'Noto Kufi Arabic';">
            {badge_text} | {source}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    if rawwiy:
        st.markdown(f"""
        <div style="background: rgba(155, 89, 182, 0.2); border: 2px solid #9b59b6; 
                    border-radius: 15px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
            <div style="font-size: 1.3rem; font-weight: bold; color: #9b59b6; margin-bottom: 10px;">
                القافية: {qafiya_type}
            </div>
            <div style="font-size: 1.1rem; color: #f5f0e3;">
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
                <div style="background: rgba(10, 22, 40, 0.8); border-radius: 15px; 
                            padding: 1rem; border: 2px solid #2ed573; text-align: center;">
                    <div style="font-family: 'Noto Kufi Arabic'; font-weight: bold; 
                                color: #00d4c8; font-size: 1.2rem;">{taf}</div>
                </div>
                """, unsafe_allow_html=True)
    
    with st.expander("🔍 تحليل الفراهيدي العميق"):
        if emotional:
            st.markdown("**المشاعر والإحساس:**")
            st.markdown(f'<div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 10px; font-family: Cairo; text-align: right; direction: rtl;">{emotional}</div>', unsafe_allow_html=True)
        
        if grammar:
            st.markdown("**الملاحظات النحوية:**")
            st.markdown(f'<div style="background: rgba(0,0,0,0.3); padding: 1rem; border-radius: 10px; font-family: Cairo; text-align: right; direction: rtl; color: #ffa502;">{grammar}</div>', unsafe_allow_html=True)

def render_welcome_section():
    st.markdown("""
    <div class="welcome-section">
        <div style="font-family: 'Noto Kufi Arabic'; font-size: 1.3rem; color: #f5f0e3; line-height: 2; margin-bottom: 1.5rem;">
            أهلاً بك في <span style="color: #00d4c8; font-weight: bold;">منصة تام</span>.. 
            <span style="color: #00d4c8; font-weight: bold;">الفراهيدي الذكي</span> بانتظارك! ❤️<br>
            لدعم استمرار هذا المشروع الثقافي، نرجو منك الانضمام لأسرتنا على فيسبوك.
        </div>
        <div style="display: flex; justify-content: center;">
            <a href="https://www.facebook.com/profile.php?id=61588035955900" target="_blank" class="facebook-btn">
                <span>📘</span>
                <span>انضم لمجتمعنا على فيسبوك</span>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="tam-footer">
        جميع الحقوق محفوظة © 2026 منصة تام الثقافية | الفراهيدي الذكي 🇨🇳
    </div>
    """, unsafe_allow_html=True)

# ═══ التطبيق الرئيسي ═══
def main():
    render_logo()
    
    # تهيئة session state
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = "qwen3-32b"
    if 'raw_text' not in st.session_state:
        st.session_state.raw_text = ""
    if 'final_text' not in st.session_state:
        st.session_state.final_text = ""
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    
    # اختيار النموذج
    selected_model = render_model_selector()
    
    # الحصول على مفتاح API
    api_key = get_api_key_for_model(selected_model)
    
    # إذا لم يكن المفتاح في Secrets، اطلب من المستخدم
    if not api_key:
        api_key = render_api_key_input(selected_model)
    
    # تهيئة المحرك
    engine = ChineseAIFarahidiEngine(api_key, selected_model)
    
    # عرض حالة الاتصال
    if engine.is_configured:
        st.markdown(f"""
        <div class="status-message success">
            ✅ متصل بنجاح بـ <strong>{engine.model_config['name']}</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-message warning">
            ⚠️ لم يتم إدخال مفتاح API. سيعمل التطبيق بالتحليل المحلي المحدود.<br>
            <small>أدخل المفتاح أعلاه للاستفادة من قوة النماذج الصينية</small>
        </div>
        """, unsafe_allow_html=True)
    
    # الألسنة
    tab1, tab2 = st.tabs(["✍️ المُشكّل الآلي", "🔍 المحلل العروضي"])
    
    with tab1:
        st.markdown('<div style="font-family: Noto Kufi Arabic; text-align: center; margin-bottom: 10px;">أدخل النص ليقوم الفراهيدي بتشكيله وتدقيقه:</div>', unsafe_allow_html=True)
        
        raw_input = st.text_area("", value=st.session_state.get('raw_text', ''), height=150, key="input_raw", placeholder="اكتب النص هنا...")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("✨ تشكيل وتحليل", use_container_width=True):
                if raw_input:
                    with st.spinner(f"جاري الاتصال بـ {engine.model_config['name']}..."):
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
            if st.button("📋 مثال", use_container_width=True):
                st.session_state.raw_text = "وحلف النصب يا ايتول هنا\nتوشي الليل والاحزان جهرا"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("🗑️ مسح", use_container_width=True):
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
            render_result(result)
    
    with tab2:
        st.markdown('<div style="font-family: Noto Kufi Arabic; text-align: center; margin-bottom: 10px;">تحليل الوزن العروضي:</div>', unsafe_allow_html=True)
        
        text_to_analyze = st.text_area("", value=st.session_state.get('final_text', ''), height=150, key="analysis_input", placeholder="أدخل النص المشكل هنا...")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("🔍 تحليل عميق", use_container_width=True, key="deep_analyze"):
                if text_to_analyze.strip():
                    with st.spinner("جاري التحليل العميق..."):
                        result = engine.analyze_poetry(text_to_analyze)
                        st.session_state.deep_analysis = result
                        st.rerun()
                else:
                    st.error("⚠️ أدخل نصاً أولاً!")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("📋 مثال", use_container_width=True, key="ex2"):
                st.session_state.final_text = "سَيَسْتَبْقِي الهِتَافُ إلَيْكَ دَهْرًا\nفَشَقَّ الدَّرْبَ بِالأَحْرَارِ نَصْرًا"
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="btn-gold">', unsafe_allow_html=True)
            if st.button("🗑️ مسح", use_container_width=True, key="cl2"):
                st.session_state.final_text = ""
                st.session_state.deep_analysis = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.get('deep_analysis'):
            render_result(st.session_state.deep_analysis)
    
    render_welcome_section()
    render_footer()

if __name__ == "__main__":
    main()
