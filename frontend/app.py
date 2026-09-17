import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from api_client import get_health, predict_segment, predict_forecast

st.set_page_config(page_title="Beauty E-commerce ML", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Customer Segmentation", "Sales Forecasting", "API Status"])

if page == "Customer Segmentation":
    st.title("👥 Customer Segmentation")
    st.markdown("Enter customer metrics to predict their segment.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        recency = st.number_input("Recency (days since last purchase)", min_value=0, value=30)
    with col2:
        frequency = st.number_input("Frequency (number of purchases)", min_value=1, value=5)
    with col3:
        monetary = st.number_input("Monetary (total spent $)", min_value=0.0, value=150.0, step=10.0)
        
    if st.button("Predict Segment", type="primary"):
        with st.spinner("Calling API..."):
            success, result = predict_segment(recency, frequency, monetary)
            
        if success:
            cluster_id = result.get('cluster_id')
            segment_name = result.get('segment_name')
            st.success(f"### Segment: {segment_name} (Cluster {cluster_id})")
        else:
            st.error(f"Failed to get prediction: {result.get('error')}")

elif page == "Sales Forecasting":
    st.title("📈 Sales Forecasting")
    st.markdown("Forecast future sales based on historical data.")
    
    weeks = st.slider("Number of weeks to forecast", min_value=1, max_value=52, value=4)
    
    if st.button("Generate Forecast", type="primary"):
        with st.spinner("Calling API..."):
            success, result = predict_forecast(weeks)
            
        if success:
            forecast = result.get("forecast", [])
            lower = result.get("lower_bound", [])
            upper = result.get("upper_bound", [])
            
            # Create a dataframe for plotting
            future_dates = pd.date_range(start=pd.Timestamp.today(), periods=weeks, freq='W')
            
            fig = go.Figure()
            
            # Add confidence interval
            if lower and upper:
                fig.add_trace(go.Scatter(
                    x=list(future_dates) + list(future_dates)[::-1],
                    y=upper + lower[::-1],
                    fill='toself',
                    fillcolor='rgba(0,100,80,0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    hoverinfo="skip",
                    showlegend=True,
                    name='Confidence Interval'
                ))
            
            # Add forecast line
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=forecast,
                mode='lines+markers',
                line=dict(color='rgb(0,100,80)'),
                name='Forecast'
            ))
            
            fig.update_layout(
                title=f"Sales Forecast for next {weeks} weeks",
                xaxis_title="Date",
                yaxis_title="Sales ($)",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show raw data
            st.subheader("Raw Data")
            df = pd.DataFrame({
                "Date": future_dates.strftime("%Y-%m-%d"),
                "Forecast": np.round(forecast, 2)
            })
            if lower and upper:
                df["Lower Bound"] = np.round(lower, 2)
                df["Upper Bound"] = np.round(upper, 2)
            st.dataframe(df, use_container_width=True)
            
        else:
            st.error(f"Failed to get forecast: {result.get('error')}")

elif page == "API Status":
    st.title("🔌 API Status")
    
    st.write(f"**Current API URL configured:** `{os.getenv('API_URL', 'http://localhost:8000')}`")
    
    if st.button("Check Health"):
        with st.spinner("Pinging API..."):
            is_healthy = get_health()
        
        if is_healthy:
            st.success("API is reachable and healthy!")
        else:
            st.error("API is unreachable. Is the server running?")
