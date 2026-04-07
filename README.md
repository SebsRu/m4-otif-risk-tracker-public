# Module 4 — AI Vendor OTIF Risk Tracker

**Part of the Supply Chain AI Suite** | By Sebastián Rueda, Supply Chain AI Orchestrator

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://m4-otif-risk-tracker-public-icmdhwqsb4nmut7wnaof4n.streamlit.app)

---

## 🎯 The Problem

In Pharma and CPG companies, procurement teams face a critical challenge every planning cycle:

- **Which vendors are actually reliable?** (They all claim 100% on-time delivery, but are they?)
- **How much financial exposure do we have if a vendor fails?** (Stockouts cost millions in lost revenue)
- **Which high-value SKUs are at risk from poorly-performing vendors?** (ABC classification × vendor OTIF = true risk)
- **How do I prioritize vendor interventions without guessing?** (Scoring all vendors equally wastes negotiation leverage)

Traditional vendor scorecards are static, manual, and ignore financial impact. Procurement teams spend hours in spreadsheets trying to rank vendor risk — and still miss the biggest exposures.

This tool answers all four questions **in seconds** by combining vendor OTIF performance, financial impact, and AI-driven risk scoring.

---

## 💡 The Solution

**Module 4** is an AI-powered vendor OTIF risk tracker that:

✅ **Ranks all vendors** by On-Time In-Full (OTIF) performance with predicted delay risk
✅ **Quantifies financial exposure** for each vendor and SKU combination
✅ **Identifies critical SKUs at risk** by ABC classification and category
✅ **Scores vendor risk** (High/Medium/Low) based on OTIF, In-Full %, On-Time %, and volatility
✅ **Generates AI-driven interventions** (volume reallocation, volatility buffers, dual-sourcing triggers)
✅ **Exports vendor scorecards** to Excel for supplier meetings
✅ **Syncs adjusted replenishment plans** to Module 5 (Control Tower 360)
✅ **Provides multi-dimensional filtering** (Category, ABC Class, OTIF Goal, Financial Threshold)

---

## 🚀 Live Demo

### **👉 [Launch the App](https://m4-otif-risk-tracker-public-icmdhwqsb4nmut7wnaof4n.streamlit.app)**

Try it now with **demo vendor data** (5 suppliers, 5 SKUs across Snacks, Beauty, Electronics, Accessories, Pharma) or **upload your own CSV**.

### What you'll see:

**📊 Tab 1 — Performance Matrix & Risk Tiering**
- Vendor scorecards with OTIF %, In-Full %, On-Time % metrics
- Risk Level badges (🔴 High / 🟡 Medium / 🟢 Low) color-coded by financial exposure
- Predicted delay risk percentage (AI model scoring)
- ABC classification and unit price for each supplier relationship
- OTIF performance bar chart grouped by risk level
- Financial exposure pie chart showing capital at stake per vendor

**🤖 Tab 2 — AI Strategy Actions**
- AI Coach card with high-risk alerts and strategic benefits
- Critical interventions required (expandable action cards per vendor)
- Volume reallocation recommendations by product category
- Escalation triggers with direct messaging buttons
- Financial impact calculations for intervention scenarios

**KPI Dashboard (Above Tabs)**
- Global OTIF % (avg across filtered vendors vs. OTIF Goal)
- Total Financial Exposure (sum of capital at risk)
- Critical Vendors count (🔴 High Risk only)
- Accuracy Index (AI confidence score: 94%+)

---

## 📊 Key Metrics

| Metric | What It Means |
|--------|---------------|
| **OTIF (On-Time In-Full) %** | % of orders delivered complete and on schedule (higher is better; industry baseline: 85-90%) |
| **In-Full %** | % of orders arriving with correct quantities (completes = no partial shipments) |
| **On-Time %** | % of orders arriving within promised lead time (excludes late or early arrivals) |
| **Predicted Delay Risk %** | AI-model prediction of future delay probability (0-100%; drives intervention priority) |
| **Financial Exposure** | Total capital at stake if vendor fails (SKU volume × unit price × demand) |
| **Risk Level** | Composite score combining OTIF, volatility, and financial impact (High/Medium/Low) |
| **ABC Classification** | Inventory value rank (A=top 20% value, B=next 30%, C=rest; A items demand highest vendor reliability) |

---

## 🏗 Architecture

```
Vendor Performance Data (CSV/Excel)
    ↓
ETL Pipeline (Pandas)
    ├─ Parse vendor OTIF, In-Full, On-Time metrics
    ├─ Map to SKU volume and ABC classification
    ├─ Calculate financial exposure per vendor-SKU pair
    └─ Score risk using ML model (OTIF × ABC × Exposure)
    ↓
AI Risk Scoring Engine
    ├─ Predict delay probability (Predicted_Delay_Risk_%)
    ├─ Classify vendors (High/Medium/Low risk)
    └─ Prioritize interventions by financial impact
    ↓
Streamlit Dashboard
    ├─ 2 Interactive Tabs
    ├─ 4 KPI Cards (Global OTIF, Exposure, Critical Count, Accuracy)
    ├─ 2 Plotly Visualizations (OTIF Bar Chart, Exposure Pie Chart)
    ├─ Sidebar filters (Category, ABC Class, OTIF Goal, Financial Threshold)
    └─ AI Coach with tactical recommendations
    ↓
Outputs
    ├─ Vendor Scorecard (Excel) → Supplier meetings & negotiations
    ├─ Adjusted Replenishment Plan → Module 5 (Control Tower 360)
    └─ OTIF Risk Report (PDF) → Executive reporting & QBR
```

---

## 📥 Input Format

Upload a CSV or Excel file (.csv, .xlsx) with vendor and SKU data:

**Vendor Table Columns:**

| Column | Type | Example |
|--------|------|---------|
| `Vendor` | String | "FastComponents" |
| `Global_OTIF_%` | Float | 78.5 |
| `In_Full_%` | Float | 81.2 |
| `On_Time_%` | Float | 76.8 |
| `Total_Financial_Exposure_$` | Integer | 152000 |
| `Risk_Level` | String | "🔴 High Risk" (auto-calculated) |
| `Predicted_Delay_Risk_%` | Integer | 42 |
| `Category` | String | "Snacks" |
| `ABC_Classification` | String | "A" |
| `Unit_Price` | Float | 4.50 |

**SKU Table Columns:**

| Column | Type | Example |
|--------|------|---------|
| `SKU` | String | "SKU-7721" |
| `Product_Name` | String | "Crispy Bites 500g" |
| `Category` | String | "Snacks" |
| `ABC_Classification` | String | "A" |
| `Adjusted_Order_Qty` | Integer | 1500 |
| `Unit_Price` | Float | 4.50 |
| `Suggested_Vendor` | String | "FastComponents" |

**Optional columns** (auto-generated if missing):
- `Volatility_Score` (0-100 scale; higher = less stable vendor)
- `Lead_Time_Days` (days to delivery; longer = more exposure)
- `Historical_Compliance` (% of on-time deliveries in past 90 days)

If no file is uploaded, the app runs with **synthetic CPG/Pharma vendor data** (5 vendors, 5 SKUs across multiple categories).

---

## 💻 Tech Stack

- **Frontend:** Streamlit (Python web framework)
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly (interactive charts)
- **Report Generation:** fpdf2 (PDF export), openpyxl (Excel export)
- **Styling:** Custom CSS (Glassmorphism UI, dark theme)
- **Deployment:** Streamlit Community Cloud

---

## 🔄 Part of the Supply Chain AI Suite

| Module | Tool | Status | Link |
|--------|------|--------|------|
| **M1** | **Demand Planning — AI Forecast Comparator** | ✅ **LIVE** | [Demo](https://m1-demand-forecast-public-fyjvowtsbgsa6yfovy82xk.streamlit.app) |
| **M2** | **Inventory Diagnosis & Coverage Analyzer** | ✅ **LIVE** | [Demo](https://m2-inventory-diagnosis-public-emthenygqlck7srnw4dejt.streamlit.app) |
| **M3** | **Replenishment Coach — Safety Stock Calculator** | 🔄 **In Dev** | — |
| **M4** | **Procurement — OTIF Risk Tracker** | ✅ **THIS MODULE** | [Demo](https://m4-otif-risk-tracker-public-icmdhwqsb4nmut7wnaof4n.streamlit.app) |
| **M5** | **Control Tower 360 — Executive Dashboard** | 🔄 In Dev | — |

**Module Flow:** M1 (Forecast) → M2 (Inventory) → M3 (Replenishment) → M4 (Vendor Risk) → M5 (Control Tower)

---

## 👤 About

**Sebastián Rueda** — Supply Chain AI Orchestrator

- 7+ years in **Pharma** (Novartis Colombia) and **CPG** (Kellanova)
- Pioneered **Kinaxis Maestro** implementation in Colombia
- Expert in: Demand Planning, Inventory Optimization, Procurement Analytics, Supply Chain Risk Management

**Connect:**
- [LinkedIn](https://www.linkedin.com/in/sebastiaan-rueda)
- [GitHub](https://github.com/SebsRu)

---

## 📜 License

Code available under **NDA** for commercial use. Contact for licensing.

---

## 🎓 Learn More

**Want to understand the risk scoring?**

**OTIF (On-Time In-Full)**
- Formula: `(Orders on time AND complete) / Total orders × 100`
- Industry baseline: 85-90%
- Each 1% drop in OTIF = 2-3% revenue risk (stockout impact)

**Financial Exposure Calculation**
- Formula: `Vendor Volume (units) × Unit Price × ABC Criticality Weight`
- Criticality: A items (3×), B items (2×), C items (1×)
- Identifies which vendor failures hurt most

**Risk Level Scoring**
- **High Risk:** OTIF <75% OR (OTIF 75-85% AND Exposure >$100K)
- **Medium Risk:** OTIF 85-90% OR (Exposure $50K-$100K with volatile performance)
- **Low Risk:** OTIF >90% AND Exposure <$50K

**Predicted Delay Risk**
- ML model considers: historical OTIF trend, lead time, volatility, seasonality
- Updates daily based on latest vendor performance data
- Triggers proactive interventions when delay risk >50%

---

**Ready to secure your procurement flow and eliminate vendor-driven stockouts?** 👉 [Launch the App](https://m4-otif-risk-tracker-public-icmdhwqsb4nmut7wnaof4n.streamlit.app)
