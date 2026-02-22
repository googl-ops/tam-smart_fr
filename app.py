#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import requests

st.set_page_config(page_title="تشخيص الاتصال", page_icon="🔧")

st.title("🔧 تشخيص الاتصال بـ OpenRouter")

# قراءة المفتاح
api_key = None
try:
    if 'OpenRouter_API_Key' in st.secrets:
        api_key = st.secrets['OpenRouter_API_Key']
        st.success(f"✅ وجدت المفتاح في Secrets!")
        st.code(f"الطول: {len(api_key)} | البداية: {api_key[:20]}...")
    else:
        st.error("❌ المفتاح غير موجود في Secrets")
        st.write("المفاتيح المتاحة:", list(st.secrets.keys()))
except Exception as e:
    st.error(f"❌ خطأ: {e}")

# اختبار الاتصال
if api_key:
    st.markdown("---")
    st.subheader("🧪 اختبار الاتصال")
    
    if st.button("🔌 اختبر الاتصال الآن"):
        with st.spinner("جاري الاتصال..."):
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "qwen/qwen3-32b:free",
                        "messages": [{"role": "user", "content": "Say hi"}],
                        "max_tokens": 10
                    },
                    timeout=30
                )
                
                st.write(f"**رمز الاستجابة:** {response.status_code}")
                
                if response.status_code == 200:
                    st.success("✅ الاتصال ناجح!")
                    st.json(response.json())
                else:
                    st.error(f"❌ فشل الاتصال: {response.status_code}")
                    st.code(response.text)
                    
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")

