/* تغيير الخلفية من شفافة إلى داكنة */
.stTextArea textarea {{
    background: rgba(10, 20, 40, 0.9) !important;  /* خلفية داكنة */
    border: 2px solid {COLORS['aged_gold']}60 !important;
    color: {COLORS['sandstone_cream']} !important;  /* نص فاتح */
}}

/* إزالة الخلفية البيضاء الافتراضية */
.stTextArea > div > div {{
    background: transparent !important;
}}
