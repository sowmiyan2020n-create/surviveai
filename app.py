import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(
    page_title="SurviveAI",
    page_icon="🆘",
    layout="wide"
)

if not os.path.exists("sellers.csv"):
    pd.DataFrame(columns=[
        "Business Name", "Industry", "Location",
        "Product", "Stock (kg)", "Price (₹/kg)",
        "Crisis Reason", "Contact", "Trust Score", "Date"
    ]).to_csv("sellers.csv", index=False)

if not os.path.exists("buyers.csv"):
    pd.DataFrame(columns=[
        "Buyer Name", "Industry", "Location",
        "Product Needed", "Quantity (kg)", "Budget (₹/kg)",
        "Contact", "Date"
    ]).to_csv("buyers.csv", index=False)

st.sidebar.image("https://img.icons8.com/emoji/96/sos-button.png", width=80)
st.sidebar.title("SurviveAI")
st.sidebar.markdown("**Crisis Business Connector**")
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "🏭 Seller Portal",
    "🛍️ Buyer Portal",
    "🤖 Find Matches",
    "📊 Dashboard"
])

INDUSTRIES = [
    "🧵 Textile & Thread",
    "🌾 Agriculture & Rice",
    "👟 Footwear",
    "💎 Jewellery",
    "🐟 Fisheries",
    "🚗 Auto Parts",
    "🧴 Chemicals",
    "🪵 Furniture",
    "🍎 Food Processing",
    "⚙️ Engineering",
    "🌿 Spices & Herbs",
    "➕ Other"
]

CRISIS_REASONS = [
    "🇺🇸 US Tariff",
    "⚔️ War / Shipping Blocked",
    "🦠 Pandemic",
    "📉 Market Crash",
    "🌊 Natural Disaster",
    "📦 Export Cancelled"
]

if page == "🏠 Home":
    st.markdown("""
    <h1 style='text-align:center; color:#FF4B4B;'>
    🆘 SurviveAI
    </h1>
    <h3 style='text-align:center; color:gray;'>
    Crisis Business Connector — When Export Stops, We Find Local Buyers
    </h3>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 😔 The Problem")
        st.write("War, tariffs & global crisis stops exports. Machines idle. Workers suffer. No platform to find domestic buyers quickly.")
    with col2:
        st.markdown("### 💡 Our Solution")
        st.write("Register your stock. We find verified domestic buyers using AI matching. Connect directly. No middleman. Free forever.")
    with col3:
        st.markdown("### 🏆 Our Impact")
        st.write("Helping textile, agriculture, footwear & all industries survive any global crisis by connecting to Indian buyers.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.error("### 🏭 I Am A Seller\nMy business is in crisis — I need buyers!")
        if st.button("Go to Seller Portal →", use_container_width=True):
            st.info("Click '🏭 Seller Portal' in the sidebar!")
    with col2:
        st.success("### 🛍️ I Am A Buyer\nI need products at good prices!")
        if st.button("Go to Buyer Portal →", use_container_width=True):
            st.info("Click '🛍️ Buyer Portal' in the sidebar!")

elif page == "🏭 Seller Portal":
    st.title("🏭 Seller Registration")
    st.markdown("**Register your business — we'll find you domestic buyers!**")
    st.markdown("---")

    with st.form("seller_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("🏭 Business Name *")
            industry = st.selectbox("🏢 Industry *", INDUSTRIES)
            location = st.text_input("📍 Location (City) *")
            product = st.text_input("📦 Product Name *")
        with col2:
            stock = st.number_input("📦 Stock Available (kg) *", min_value=1)
            price = st.number_input("💰 Price per kg (₹) *", min_value=1)
            crisis = st.selectbox("🚨 Crisis Reason *", CRISIS_REASONS)
            contact = st.text_input("📞 Contact Number *")

        gst = st.text_input("📄 GST Number (for verification)")

        submitted = st.form_submit_button("✅ Register My Business", use_container_width=True)

        if submitted:
            if name and location and product and contact:
                trust = 50
                if gst: trust += 25
                if stock > 100: trust += 15
                if contact: trust += 10

                df = pd.read_csv("sellers.csv")
                new_row = {
                    "Business Name": name,
                    "Industry": industry,
                    "Location": location,
                    "Product": product,
                    "Stock (kg)": stock,
                    "Price (₹/kg)": price,
                    "Crisis Reason": crisis,
                    "Contact": contact,
                    "Trust Score": trust,
                    "Date": datetime.now().strftime("%Y-%m-%d")
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv("sellers.csv", index=False)

                st.success(f"✅ Registered Successfully!")
                st.metric("🛡️ Your Trust Score", f"{trust}/100")
                if trust >= 70:
                    st.success("🟢 VERIFIED — Your listing is visible to buyers!")
                else:
                    st.warning("🟡 Add GST number to increase trust score!")
            else:
                st.error("Please fill all required fields!")

elif page == "🛍️ Buyer Portal":
    st.title("🛍️ Buyer Portal")
    st.markdown("**Post what you need — we'll find verified sellers!**")
    st.markdown("---")

    with st.form("buyer_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("🏢 Buyer Name *")
            industry = st.selectbox("🏢 Industry *", INDUSTRIES)
            location = st.text_input("📍 Location (City) *")
        with col2:
            product = st.text_input("📦 Product Needed *")
            quantity = st.number_input("📦 Quantity Needed (kg) *", min_value=1)
            budget = st.number_input("💰 Budget per kg (₹) *", min_value=1)
            contact = st.text_input("📞 Contact Number *")

        submitted = st.form_submit_button("🔍 Find Sellers", use_container_width=True)

        if submitted:
            if name and location and product and contact:
                df = pd.read_csv("buyers.csv")
                new_row = {
                    "Buyer Name": name,
                    "Industry": industry,
                    "Location": location,
                    "Product Needed": product,
                    "Quantity (kg)": quantity,
                    "Budget (₹/kg)": budget,
                    "Contact": contact,
                    "Date": datetime.now().strftime("%Y-%m-%d")
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv("buyers.csv", index=False)
                st.success("✅ Request Posted! Check 'Find Matches' tab!")
            else:
                st.error("Please fill all required fields!")

elif page == "🤖 Find Matches":
    st.title("🤖 AI Match Finder")
    st.markdown("**Finding best matches between sellers and buyers!**")
    st.markdown("---")

    try:
        sellers = pd.read_csv("sellers.csv")
        buyers = pd.read_csv("buyers.csv")

        if len(sellers) == 0 or len(buyers) == 0:
            st.warning("⚠️ No sellers or buyers registered yet!")
        else:
            st.subheader("🎯 Best Matches Found!")
            match_found = False
            for _, buyer in buyers.iterrows():
                matched = sellers[
                    (sellers["Price (₹/kg)"] <= buyer["Budget (₹/kg)"]) &
                    (sellers["Product"].astype(str).str.lower() == str(buyer["Product Needed"]).lower())
                ].sort_values("Trust Score", ascending=False)

                if len(matched) > 0:
                    match_found = True
                    best = matched.iloc[0]
                    score = min(99, int(
                        (1 - abs(best["Price (₹/kg)"] - buyer["Budget (₹/kg)"]) /
                         buyer["Budget (₹/kg)"]) * 100
                    ))

                    with st.container():
                        st.markdown(f"""
                        <div style='background:#e8f5e9; padding:20px;
                        border-radius:10px; border-left:5px solid #2e7d32;
                        margin:10px 0; color:#1b5e20;'>
                        <h3 style='color:#1b5e20;'>🤝 Match Found!</h3>
                        <b>🛍️ Buyer:</b> {buyer['Buyer Name']} — {buyer['Location']}<br>
                        <b>🏭 Seller:</b> {best['Business Name']} — {best['Location']}<br>
                        <b>📦 Product:</b> {best['Product']}<br>
                        <b>💰 Price:</b> ₹{best['Price (₹/kg)']}/kg
                        (Budget: ₹{buyer['Budget (₹/kg)']})<br>
                        <b>📦 Stock:</b> {best['Stock (kg)']} kg available<br>
                        <b>🛡️ Trust Score:</b> {best['Trust Score']}/100<br>
                        <b>✅ Match Score:</b> {score}%<br>
                        <b>📞 Contact:</b> {best['Contact']}
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(
                            f"[📱 WhatsApp Now](https://wa.me/91{best['Contact']})",
                            unsafe_allow_html=True
                        )
                        st.markdown("---")

            if not match_found:
                st.warning("⚠️ No matches found yet! Add more sellers and buyers!")

    except:
        st.warning("⚠️ No matches found yet!")

elif page == "📊 Dashboard":
    st.title("📊 SurviveAI Dashboard")
    st.markdown("---")

    try:
        sellers = pd.read_csv("sellers.csv")
        buyers = pd.read_csv("buyers.csv")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🏭 Businesses Registered", len(sellers))
        with col2:
            st.metric("🛍️ Active Buyers", len(buyers))
        with col3:
            total_stock = sellers["Stock (kg)"].sum() if len(sellers) > 0 else 0
            st.metric("📦 Total Stock (kg)", f"{total_stock:,}")
        with col4:
            total_value = (sellers["Stock (kg)"] * sellers["Price (₹/kg)"]).sum() if len(sellers) > 0 else 0
            st.metric("💰 Total Value (₹)", f"{total_value:,.0f}")

        if len(sellers) > 0:
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                fig = px.pie(sellers, names="Industry",
                           title="Industries in Crisis")
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig2 = px.bar(sellers, x="Business Name",
                            y="Trust Score",
                            title="Seller Trust Scores",
                            color="Trust Score",
                            color_continuous_scale="RdYlGn")
                st.plotly_chart(fig2, use_container_width=True)

            st.subheader("📋 All Registered Sellers")
            st.dataframe(sellers, use_container_width=True)

    except:
        st.warning("No data yet — register sellers and buyers first!")