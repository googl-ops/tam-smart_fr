#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Testing imports...")

# Test Python built-in
import base64, os, json, re
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
print("✅ Python built-in libraries: OK")

# Test Streamlit
try:
    import streamlit as st
    print(f"✅ Streamlit: OK (version {st.__version__})")
except ImportError:
    print("❌ Streamlit: NOT INSTALLED")

# Test Google GenAI
try:
    from google import genai
    from google.genai import types
    print("✅ Google GenAI: OK")
    print(f"   Client available: {hasattr(genai, 'Client')}")
    print(f"   Types available: {hasattr(types, 'GenerateContentConfig')}")
except ImportError:
    print("❌ Google GenAI: NOT INSTALLED")

print("\nAll tests completed!")
