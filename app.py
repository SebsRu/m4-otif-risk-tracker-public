# ============================================================
# © 2026 Sebastián Rueda — Supply Chain AI Orchestrator
# All rights reserved. Unauthorized copying, modification,
# redistribution or commercial use of this code is prohibited.
# Contact: sebastiaan.r@gmail.com | github.com/SebsRu
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
import os
import textwrap
from fpdf import FPDF

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Vendor OTIF Risk Tracker | Module 4",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# PREMIUM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #f8f9fa;
}

/* ── Header ── */
.mod-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 32px 40px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 8px 32px rgba(15,52,96,0.25);
}
.mod-badge {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 8px;
    padding: 6px 14px;
    color: #a8d8f0;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.mod-title {
    color: #ffffff;
    font-size: 1.9rem;
    font-weight: 800;
    margin: 8px 0 4px 0;
    line-height: 1.2;
}
.mod-subtitle {
    color: #8bb8d4;
    font-size: 0.92rem;
    font-weight: 400;
}
.mod-tag {
    background: rgba(99,179,237,0.15);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    color: #63b3ed;
    font-size: 0.75rem;
    font-weight: 500;
    margin-top: 10px;
    display: inline-block;
}

/* ── KPI Cards ── */
.kpi-card {
    background: #ffffff;
    border-radius: 14px;
    padding: 22px 20px 18px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #e9ecef;
    border-top: 4px solid #0f3460;
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.10); }
.kpi-card.blue { border-top-color: #3182ce; }
.kpi-card.gold { border-top-color: #d69e2e; }
.kpi-card.red  { border-top-color: #e53e3e; }
.kpi-card.green{ border-top-color: #38a169; }

.kpi-label { font-size: 0.75rem; font-weight: 600; color: #718096; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }
.kpi-value { font-size: 1.8rem; font-weight: 800; color: #1a202c; line-height: 1; margin-bottom: 6px; }
.kpi-delta { font-size: 0.78rem; font-weight: 500; padding: 3px 8px; border-radius: 12px; display: inline-block; }
.kpi-delta.blue { background: #ebf8ff; color: #2b6cb0; }
.kpi-delta.red  { background: #fff5f5; color: #e53e3e; }
.kpi-delta.gold { background: #fffff0; color: #b7791f; }
.kpi-delta.green{ background: #f0fff4; color: #38a169; }

/* ── AI Coach Card ── */
.ai-coach-card {
    background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
    border-radius: 14px;
    padding: 28px 32px;
    margin: 24px 0;
    box-shadow: 0 8px 24px rgba(15,52,96,0.2);
}
.ai-coach-title { color: #ffffff; font-size: 1.05rem; font-weight: 700; margin-bottom: 18px; }
.ai-rec {
    background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
    border-left: 3px solid #63b3ed; border-radius: 8px;
    padding: 14px 16px; margin-bottom: 10px; color: #e2e8f0; font-size: 0.88rem; line-height: 1.55;
}
.ai-rec strong { color: #90cdf4; }
.ai-rec.gold-border { border-left-color: #f6e05e; }
.ai-rec.red-border  { border-left-color: #fc8181; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #1a1a2e !important; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1) !important; }

.stTabs [data-baseweb="tab-list"] { background: #ffffff; border-radius: 12px; padding: 6px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.stTabs [aria-selected="true"] { background: #0f3460 !important; color: white !important; border-radius: 8px; }
.section-header { font-size: 1.1rem; font-weight: 700; color: #1a202c; border-left: 4px solid #0f3460; padding-left: 12px; margin: 28px 0 18px 0; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA LOGIC & ENRICHMENT
# ─────────────────────────────────────────────
@st.cache_data
def load_full_vendor_data():
    vendors = ["FastComponents", "Global Electronics", "NexusHardware", "ReliableParts", "TechSupply Co"]
    df_v = pd.DataFrame({
        'Vendor': vendors,
        'Global_OTIF_%': [78.5, 89.2, 72.4, 94.1, 81.5],
        'In_Full_%': [81.2, 92.8, 70.1, 95.5, 83.2],
        'On_Time_%': [76.8, 86.4, 74.8, 92.7, 79.9],
        'Total_Financial_Exposure_$': [152000, 48000, 215000, 12000, 64000],
        'Risk_Level': ['🔴 High Risk', '🟡 Medium Risk', '🔴 High Risk', '🟢 Low Risk', '🟡 Medium Risk'],
        'Predicted_Delay_Risk_%': [42, 12, 65, 4, 28],
        'Category': ["Snacks", "Beauty", "Electronics", "Accessories", "Pharma"],
        'ABC_Classification': ["A", "B", "A", "C", "B"],
        'Unit_Price': [4.50, 32.00, 299.00, 15.20, 9.80]
    })
    
    df_s = pd.DataFrame({
        "SKU": ["SKU-7721", "SKU-8842", "SKU-1120", "SKU-4409", "SKU-9951"],
        "Product_Name": ["Crispy Bites 500g", "Premium SkinCare Pro", "Switch-V3 Console", "Wrist-Strap Sport", "Cold Relief Pharma"],
        "Category": ["Snacks", "Beauty", "Electronics", "Accessories", "Pharma"],
        "ABC_Classification": ["A", "B", "A", "C", "B"],
        "Adjusted_Order_Qty": [1500, 400, 250, 800, 310],
        "Unit_Price": [4.50, 32.00, 299.00, 15.20, 9.80],
        "Suggested_Vendor": ["FastComponents", "Global Electronics", "NexusHardware", "ReliableParts", "TechSupply Co"]
    })
    return df_v, df_s

df_v, df_s = load_full_vendor_data()

# ── SIDEBAR FILTERS ──
with st.sidebar:
    st.markdown("<div style='text-align:center;'><h2>🔍 Module 4</h2><p>Vendor OTIF Risk</p></div>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("<div style='color:#a0aec0;font-size:0.75rem;font-weight:600;letter-spacing:1px;text-transform:uppercase;margin-bottom:10px;'>🎯 Global Intelligence Filters</div>", unsafe_allow_html=True)
    sel_cat = st.multiselect("Category", sorted(df_v['Category'].unique()), default=df_v['Category'].unique())
    sel_abc = st.multiselect("ABC Classification", sorted(df_v['ABC_Classification'].unique()), default=df_v['ABC_Classification'].unique())
    
    df_v = df_v[df_v['Category'].isin(sel_cat) & df_v['ABC_Classification'].isin(sel_abc)]
    
    st.divider()
    otif_goal = st.slider("OTIF Goal (%)", 70, 100, 85)
    financial_threshold = st.slider("Alert Threshold ($)", 10000, 100000, 50000)
    
    st.divider()
    # Direct Template Download (Mod 1/2 style)
    template_cols = ["SKU", "Product_Name", "Category", "ABC", "Vendor", "OTIF_Goal"]
    template_df = pd.DataFrame(columns=template_cols)
    csv_tmp = template_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download OTIF Template", csv_tmp, "AI_Vendor_Template.csv", use_container_width=True)

# ── HEADER ──
st.markdown("""
<div class="mod-header">
    <div>
        <div class="mod-badge">MODULE 4 · PROCUREMENT INTELLIGENCE</div>
        <div class="mod-title">🔍 AI Vendor OTIF Risk Tracker</div>
        <div class="mod-subtitle">Identify fulfillment gaps, quantify financial exposure, and secure procurement flow</div>
        <span class="mod-tag">⚡ Connected to Module 3 Replenishment Plan</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ──
c1, c2, c3, c4 = st.columns(4)
def kpi_html(label, value, delta, d_class, card_class="neutral"):
    return f"""<div class="kpi-card {card_class}"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><span class="kpi-delta {d_class}">{delta}</span></div>"""

with c1: st.markdown(kpi_html("Global OTIF %", f"{df_v['Global_OTIF_%'].mean():.1f}%", f"{df_v['Global_OTIF_%'].mean()-otif_goal:.1f}% vs Goal", "blue", "blue"), unsafe_allow_html=True)
with c2: st.markdown(kpi_html("Financial Exposure", f"${df_v['Total_Financial_Exposure_$'].sum():,.0f}", "Risk at stake", "red", "red"), unsafe_allow_html=True)
with c3: st.markdown(kpi_html("Critical Vendors", len(df_v[df_v['Risk_Level'].str.contains('🔴')]), f"{len(df_v)} Total Active", "gold", "gold"), unsafe_allow_html=True)
with c4: st.markdown(kpi_html("Accuracy Index", "94%+", "↑ AI Confirmed", "green", "neutral"), unsafe_allow_html=True)

st.divider()
tab1, tab2 = st.tabs(["📊 Performance Matrix", "🤖 AI Strategy Actions"])

with tab1:
    st.markdown('<div class="section-header">📊 Vendor Performance Matrix & Risk Tiering</div>', unsafe_allow_html=True)
    v_display_cols = ['Vendor', 'Global_OTIF_%', 'In_Full_%', 'On_Time_%', 'Total_Financial_Exposure_$', 'Risk_Level', 'Predicted_Delay_Risk_%', 'Category', 'ABC_Classification', 'Unit_Price']
    
    def style_risk(val):
        if '🔴' in str(val): return 'background-color: #f8d7da'
        elif '🟡' in str(val): return 'background-color: #fff3cd'
        return 'background-color: #d4edda'
    
    st.dataframe(df_v[v_display_cols].style.map(style_risk, subset=['Risk_Level']).format({"Global_OTIF_%": "{:.1f}%", "Total_Financial_Exposure_$": "${:,.0f}", "Unit_Price": "${:,.2f}"}), use_container_width=True, hide_index=True)
    
    st.divider()
    cp1, cp2 = st.columns(2)
    with cp1:
        fig_bar = px.bar(df_v, x='Vendor', y='Global_OTIF_%', color='Risk_Level', color_discrete_map={'🔴 High Risk':'#e53e3e', '🟡 Medium Risk':'#d69e2e', '🟢 Low Risk':'#38a169'}, title="OTIF Performance by Vendor")
        st.plotly_chart(fig_bar, use_container_width=True)
    with cp2:
        fig_pie = px.pie(df_v, values='Total_Financial_Exposure_$', names='Vendor', title="Share of Financial Exposure ($)")
        st.plotly_chart(fig_pie, use_container_width=True)

with tab2:
    nexus_otif = df_v[df_v['Vendor'].str.contains('NexusHardware')]['Global_OTIF_%'].iloc[0] if len(df_v[df_v['Vendor'].str.contains('NexusHardware')]) > 0 else 0
    st.markdown(f"""
    <div class="ai-coach-card">
        <div class="ai-coach-title">🤖 AI Strategy Coach - Procurement Interventions</div>
        <div class="ai-rec red-border">
            <strong>🚨 High Risk Alert - Electronics:</strong> Vendor <strong>NexusHardware</strong> shows <strong>{nexus_otif}% OTIF</strong>. 
            Financial exposure is <strong>$215,000</strong>. Action: Immediately shift 25% volume or trigger Volatility Buffer (+15%).
        </div>
        <div class="ai-rec">
            <strong>💡 Strategic Benefit:</strong> Re-routing Class A volume mitigates systemic risk of <strong>${df_v['Total_Financial_Exposure_$'].sum():,.0f}</strong>.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">🔥 Critical Interventions Required</div>', unsafe_allow_html=True)
    hr_list = df_v[df_v['Risk_Level'].str.contains('🔴')]
    for _, r in hr_list.iterrows():
        with st.expander(f"⚠️ Action Required: {r['Vendor']} (${r['Total_Financial_Exposure_$']:,.0f} Impact)", expanded=True):
            st.warning(f"Strategy: Volume Reallocation for {r['Category']} (ABC: {r['ABC_Classification']}). Delay probability: {r['Predicted_Delay_Risk_%']}% for next cycle.")
            st.button(f"📧 Escalate to {r['Vendor']} Quality Manager", key=f"esc_{r['Vendor']}")

# ─────────────────────────────────────────────
# PROFESSIONAL EXPORTS & CONTROL TOWER SYNC (EXACT USER STRUCTURE)
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">📤 Professional Exports & Control Tower Sync</div>', unsafe_allow_html=True)

# Function defined before usage
def generate_otif_pdf_function():
    pdf = FPDF()
    pdf.add_page(); pdf.set_fill_color(26, 26, 46); pdf.rect(0, 0, 210, 35, 'F')
    pdf.set_font("Helvetica", "B", 16); pdf.set_text_color(255, 255, 255); pdf.set_xy(10, 10)
    pdf.cell(0, 10, "Vendor OTIF Risk Report", ln=True)
    pdf.set_font("Helvetica", "", 10); pdf.set_text_color(160, 160, 160)
    pdf.cell(0, 8, f"Supply Chain AI Suite | {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(15); pdf.set_text_color(0,0,0); pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "1. Executive Summary", ln=True); pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 7, f"- Global OTIF Rate: {df_v['Global_OTIF_%'].mean():.1f}%", ln=True)
    pdf.cell(0, 7, f"- Total Financial Risk: ${df_v['Total_Financial_Exposure_$'].sum():,.2f}", ln=True)
    pdf_out = pdf.output(dest='S')
    if isinstance(pdf_out, str): return pdf_out.encode('latin1')
    return bytes(pdf_out)

df_adjusted = df_s.merge(df_v[['Vendor', 'Global_OTIF_%', 'Risk_Level', 'Category', 'ABC_Classification', 'Unit_Price']], left_on='Suggested_Vendor', right_on='Vendor', suffixes=('', '_v'))

c1, c2, c3 = st.columns(3)

# 1. Export Vendor Scorecard
with c1:
    if st.button("📊 Prepare Vendor Scorecard (Excel)", use_container_width=True, type="secondary", key="btn_prep_vs"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_v[v_display_cols].to_excel(writer, index=False, sheet_name='Vendor_Scorecard')
        output.seek(0)
        
        st.download_button(
            label="⬇️ Download Scorecard.xlsx",
            data=output,
            file_name=f"Vendor_Scorecard_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_vs_file"
        )

# 2. Send Plan to Control Tower (Mod 5)
with c2:
    if st.button("🚀 SEND PLAN TO CONTROL TOWER (MOD 5)", use_container_width=True, type="primary", key="btn_prep_mod5"):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_adjusted.to_excel(writer, index=False, sheet_name='Adjusted_Replenishment_Plan')
        output.seek(0)
        
        st.download_button(
            label="⬇️ Download Adjusted Plan for Mod 5",
            data=output,
            file_name=f"Adjusted_Plan_Control_Tower_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            key="dl_mod5_file"
        )
        st.success("✅ Plan ready for Control Tower")

# 3. Generate OTIF Report (PDF)
with c3:
    if st.button("📄 Generate OTIF Report (PDF)", use_container_width=True, key="btn_prep_pdf"):
        pdf_bytes = generate_otif_pdf_function()
        st.download_button(
            label="⬇️ Download OTIF Report.pdf",
            data=pdf_bytes,
            file_name=f"OTIF_Report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="dl_pdf_file"
        )

st.divider()
st.caption("Module 4: AI Vendor OTIF Risk Tracker | v2.9 Platinum Edition · Complete Feature Restoration")
