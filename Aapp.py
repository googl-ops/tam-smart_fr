#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
منصة تام الثقافية الذكية - الفراهيدي الذكي
TAM Smart Cultural Platform - Al-Farahidi Smart
Powered by Gemini 2.5 Flash
"""

import base64
import os
import json
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import streamlit as st

# ═══ استيراد المكتبات ═══
try:
    from google import genai
    from google.genai import types
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    st.error("❌ مكتبة google-genai غير مثبتة. نفذ: pip install google-genai")

# ═══ استرجاع المفتاح السري ═══
def get_gemini_api_key():
    try:
        if 'Gemini_API_Key' in st.secrets:
            return st.secrets['Gemini_API_Key']
    except: pass
    return os.environ.get("Gemini_API_Key")

st.set_page_config(page_title="الفراهيدي الذكي | تام", page_icon="🧠", layout="wide")

# ═══ الألوان والهوية البصرية ═══
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
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Noto+Kufi+Arabic:wght@400;700&display=swap');
    .stApp {{ background: {COLORS['midnight_blue']}; color: {COLORS['sandstone_cream']}; font-family: 'Cairo', sans-serif; }}
    .tam-musnad {{ font-size: 4rem; text-align: center; background: linear-gradient(135deg, #FFD700, #B8860B); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
    .result-card {{ background: rgba(10, 22, 40, 0.6); border-right: 4px solid {COLORS['electric_turquoise']}; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; }}
    .tafeela-card {{ background: rgba(10, 22, 40, 0.8); border: 2px solid {COLORS['aged_gold']}40; border-radius: 15px; padding: 1rem; text-align: center; }}
    .stButton>button {{ border: 2px solid {COLORS['electric_turquoise']} !important; color: {COLORS['electric_turquoise']} !important; background: transparent !important; border-radius: 50px !important; }}
    .diacritics-box {{ background: rgba(0, 0, 0, 0.2); border: 1px dashed {COLORS['electric_turquoise']}; padding: 20px; border-radius: 10px; font-size: 1.3rem; text-align: center; }}
</style>
""", unsafe_allow_html=True)

# ═══ محرك الفراهيدي الذكي ═══
class FarahidiGeminiEngine:
    def __init__(self, api_key: str = None):
        self.client = genai.Client(api_key=api_key) if api_key else None

    def analyze_poetry(self, text: str) -> Dict:
        if not self.client: return {"error": "API Key missing"}
        
        response_schema = {
            "type": "object",
            "properties": {
                "diacritized_text": {"type": "string"},
                "meter_name": {"type": "string"},
                "meter_type": {"type": "string"},
                "tafeelat": {"type": "array", "items": {"type": "string"}},
                "qafiya_type": {"type": "string"},
                "rawwiy": {"type": "string"},
                "emotional_analysis": {"type": "string"},
                "grammar_notes": {"type": "string"},
                "is_single_tafeela": {"type": "boolean"}
            },
            "required": ["diacritized_text", "meter_name", "meter_type", "tafeelat"]
        }

        try:
            response = self.client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=f"أنت الخليل بن أحمد الفراهيدي. حلل هذا النص وأعد JSON: {text}",
                config=types.GenerateContentConfig(
                    temperature=0.0,
                    response_schema=response_schema,
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            return {"error": str(e)}

# ═══ واجهة الاستخدام ═══
def main():
    st.markdown('<div class="tam-musnad">𐩩𐩱𐩣</div>', unsafe_allow_html=True)
    
    api_key = get_gemini_api_key()
    engine = FarahidiGeminiEngine(api_key)

    tab1, tab2 = st.tabs(["✍️ المُشكّل الآلي", "🔍 المحلل العروضي"])
    
    with tab1:
        raw_input = st.text_area("أدخل النص الشعري:", key="raw_input")
        if st.button("✨ تشكيل وتحليل"):
            if raw_input:
                with st.spinner("جاري التحليل..."):
                    res = engine.analyze_poetry(raw_input)
                    if "error" not in res:
                        st.markdown(f'<div class="diacritics-box">{res["diacritized_text"]}</div>', unsafe_allow_html=True)
                        st.write(f"**البحر:** {res['meter_name']} | **النوع:** {res['meter_type']}")
                        st.write(f"**التفعيلات:** {', '.join(res['tafeelat'])}")
                    else:
                        st.error(res["error"])

if __name__ == "__main__":
    main()

