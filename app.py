import streamlit as st
import os

st.title("🔍 تشخيص نهاري للمشكلة")

# معلومات النظام
st.subheader("معلومات النظام")
st.write(f"Streamlit version: {st.__version__}")

# محاولة استيراد المكتبة
try:
    from google import genai
    st.success("✅ المكتبة google-genai مستوردة")
    
    # معلومات المكتبة
    import google.genai as genai_module
    st.write(f"إصدار المكتبة: {getattr(genai_module, '__version__', 'غير معروف')}")
except Exception as e:
    st.error(f"❌ فشل استيراد المكتبة: {e}")

# قراءة المفتاح
st.subheader("قراءة المفتاح")
api_key = None

# من Secrets
try:
    api_key = st.secrets.get("Gemini_API_Key")
    if api_key:
        st.success(f"✅ المفتاح موجود في Secrets: {api_key[:15]}...")
        st.write(f"طول المفتاح: {len(api_key)}")
    else:
        st.error("❌ المفتاح غير موجود في Secrets")
except Exception as e:
    st.error(f"❌ خطأ في قراءة Secrets: {e}")

# اختبار الاتصال
if api_key:
    st.subheader("اختبار الاتصال")
    try:
        client = genai.Client(api_key=api_key)
        
        # اختبار بسيط
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="قل: الاختبار ناجح",
            config=genai.types.GenerateContentConfig(max_output_tokens=10)
        )
        
        st.success(f"✅ الاتصال ناجح! الرد: {response.text}")
        
    except Exception as e:
        st.error(f"❌ فشل الاتصال: {e}")
        
        # تحليل الخطأ
        error_str = str(e)
        if "API key not valid" in error_str:
            st.info("""
            🔴 **المفتاح غير صالح**
            
            **الحلول:**
            1. تأكد أنك أنشأت المفتاح من: https://ai.google.dev/gemini-api/docs/api-key
            2. تأكد من تفعيل الفوترة (Billing) في Google Cloud
            3. تأكد من تفعيل Gemini API في مشروعك
            4. جرب إنشاء مفتاح جديد في مشروع جديد
            
            **رابط Google Cloud Console:**
            https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
            """)
        elif "403" in error_str:
            st.info("""
            🔴 **خطأ 403 - الوصول مرفوض**
            
            **الحل:**
            - المفتاح صحيح لكن API غير مفعل للمشروع
            - اذهب إلى Google Cloud Console → APIs & Services → Enable APIs
            - فعّل "Generative Language API"
            """)
        else:
            st.info(f"تفاصيل الخطأ: {error_str}")
