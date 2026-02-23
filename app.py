import streamlit as st
import json
import sys

# 1. فحص إصدارات المكتبات المثبتة
def check_versions():
    st.markdown("### 🛠️ فحص البيئة البرمجية")
    col1, col2 = st.columns(2)
    col1.write(f"إصدار Python: `{sys.version.split()[0]}`")
    col2.write(f"إصدار Streamlit: `{st.__version__}`")
    
    try:
        from google import genai
        import google.genai as genai_pkg
        st.success(f"✅ مكتبة `google-genai` جاهزة")
    except ImportError:
        st.error("❌ مكتبة `google-genai` غير مثبتة")

# 2. فحص الأسرار (Secrets) والمفتاح
def check_api_key():
    st.markdown("---")
    st.markdown("### 🔑 فحص مفتاح API")
    key_name = "Gemini_API_Key"
    
    if key_name in st.secrets:
        key = st.secrets[key_name]
        st.success(f"✅ المفتاح `{key_name}` موجود في الأسرار")
        st.info(f"طول المفتاح: {len(key)} رمز | البداية: `{key[:4]}...`")
    else:
        st.error(f"❌ المفتاح `{key_name}` مفقود من إعدادات Secrets!")

# 3. اختبار الاتصال الحقيقي وكشف خطأ 404
def test_model_connectivity():
    st.markdown("---")
    st.markdown("### 📡 اختبار الاتصال بالنماذج")
    
    try:
        from google import genai
        client = genai.Client(api_key=st.secrets["Gemini_API_Key"])
        
        # محاولة طلب بسيط جداً للكشف عن حالة الموديل
        # اخترنا هذا الموديل لأنه ظهر في قائمتك المتاحة
        target_model = "gemini-2.5-flash" 
        
        with st.spinner(f"جاري اختبار الموديل `{target_model}`..."):
            response = client.models.generate_content(
                model=target_model,
                contents="ping"
            )
            st.success(f"✅ تم الاتصال بنجاح بموديل {target_model}")
            
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg:
            st.error("🚨 خطأ 404: اسم الموديل غير صحيح أو غير مدعوم في منطقتك الجغرافية حالياً.")
        elif "Unterminated string" in error_msg:
            st.error("🚨 خطأ في تنسيق JSON: الرد وصل منقوصاً (غالباً بسبب جودة الاتصال).")
        else:
            st.error(f"❌ فشل الاختبار: {error_msg}")

# تشغيل الفحص
if st.button("🚀 تشغيل فحص النظام الشامل"):
    check_versions()
    check_api_key()
    test_model_connectivity()
