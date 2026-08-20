import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="Enterprise MLOps ROI Inventory Predictor",
    page_icon="📈",
    layout="wide"
)

st.title("🔮 Enterprise Demand-Sensing & ROI Engine")
st.markdown("Optimize warehouse stock levels, mitigate stock-out revenue risks, and balance holding costs via secure microservices.")

# Sidebar for Environment & Core Inputs
st.sidebar.header("⚙️ System & Environment")
env_choice = st.sidebar.radio("Connect To:", ["Local Gateway (Port 8000)", "Production Render"])
API_URL = "http://127.0.0.1:8000/predict/" if env_choice == "Local Gateway (Port 8000)" else "https://ecom-mlops.onrender.com/predict/"

st.sidebar.header("📊 SKU & Operational Parameters")

sku_options = ["SKU-PROMO-01", "SKU-ENTERPRISE-02", "SKU-BULK-03", "Custom SKU..."]
selected_sku_option = st.sidebar.selectbox("Select SKU Profile", sku_options)

if selected_sku_option == "Custom SKU...":
    sku = st.sidebar.text_input("Enter Custom SKU Identifier", value="SKU-CUSTOM-99")
else:
    sku = selected_sku_option

current_stock = st.sidebar.number_input("Current Stock (Units)", min_value=0, value=120, step=10)
base_daily_sales = st.sidebar.number_input("Base Daily Sales", min_value=0.0, value=15.0, step=1.0)
supplier_lead_time = st.sidebar.slider("Supplier Lead Time (Days)", min_value=1, max_value=30, value=10)
return_rate = st.sidebar.slider("Return Rate (%)", min_value=0.0, max_value=50.0, value=8.0) / 100.0

st.sidebar.subheader("Market Volatility & Shifts")
seasonality_index = st.sidebar.slider("Seasonality Index (Multiplier)", min_value=0.5, max_value=3.0, value=1.4, step=0.1)
marketing_delta = st.sidebar.slider("Marketing Spend Delta (%)", min_value=-50.0, max_value=100.0, value=20.0, step=5.0) / 100.0
competitor_ratio = st.sidebar.slider("Competitor Price Ratio", min_value=0.5, max_value=1.5, value=0.95, step=0.05)

with st.sidebar.popover("💰 Financial & Monetization Settings"):
    st.markdown("### ROI Calculation Parameters")
    unit_price = st.number_input("Unit Selling Price ($)", value=45.0, step=5.0)
    holding_cost_unit = st.number_input("Daily Holding Cost per Unit ($)", value=0.05, step=0.01)
    st.caption("Mapped for future financial microservices.")

if st.button("Run Analysis", type="primary"):
    payload = {
        "sku": sku,
        "current_stock": current_stock,
        "base_daily_sales": base_daily_sales,
        "supplier_lead_time_days": supplier_lead_time,
        "return_rate": return_rate,
        "seasonality_index": seasonality_index,
        "marketing_spend_delta": marketing_delta,
        "competitor_price_ratio": competitor_ratio
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            data = response.json()
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Adjusted Daily Velocity", f"{data.get('adjusted_projected_daily_sales', 0)} units/day")
            col2.metric("Days Until Stockout", f"{data.get('estimated_days_until_stockout', 0)} days")
            
            risk_level = data.get('risk_level', 'Stable')
            if risk_level == "Critical":
                col3.metric("Risk Status", risk_level, delta="Action Required", delta_color="inverse")
            else:
                col3.metric("Risk Status", risk_level, delta="Healthy", delta_color="normal")
                
            st.divider()
            if data.get('action_required'):
                st.warning(f"🚨 **Alert for {sku}:** Stock will deplete before restock ({supplier_lead_time} days lead time)! Immediate reorder recommended.")
            else:
                st.info(f"✅ **Status for {sku}:** Current inventory comfortably covers the supplier lead-time window.")
                
        elif response.status_code == 429:
            st.error("⚠️ **Rate Limit Exceeded:** Too many requests sent rapidly. Please wait a moment before trying again.")
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
            
    except Exception as e:
        st.error(f"Could not connect to gateway service at `{API_URL}`: {e}")