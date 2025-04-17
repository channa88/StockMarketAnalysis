import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Seaborn style
sns.set(style="whitegrid")

# Streamlit UI
st.title("Stock Data Analysis App")

# File Upload
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Read the CSV file
    df = pd.read_csv(uploaded_file, parse_dates=["Date"], index_col="Date")
    
    # Display the first few rows
    st.subheader("Raw Data Preview")
    st.write(df.head())

    # Creating tabs
    tab1, tab2, tab3, tab4 = st.tabs(["High Prices Over Time", "Monthly Resampled High Prices", 
                                      "Moving Average", "High Prices Differencing"])

    # Plot High Prices Over Time
    with tab1:
        st.subheader("High Prices Over Time")
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['High'], label='High Price', color='blue')
        plt.xlabel("Date")
        plt.ylabel("High Price")
        plt.title("Stock High Prices Over Time")
        plt.legend()
        st.pyplot(plt)
    
    # Resampling to Monthly Average
    df_resampled = df.resample('ME').mean(numeric_only=True)

    with tab2:
        st.subheader("Monthly Resampled High Prices")
        plt.figure(figsize=(12, 6))
        plt.plot(df_resampled.index, df_resampled['High'], label='Monthly Avg High Price', color='orange')
        plt.xlabel("Date (Monthly)")
        plt.ylabel("High Price")
        plt.title("Monthly Resampling of High Prices")
        plt.legend()
        st.pyplot(plt)
    
    # Moving Average Calculation
    with tab3:
        window_size = st.slider("Select Moving Average Window Size", min_value=10, max_value=200, value=50, step=10)
        df['high_smoothed'] = df['High'].rolling(window=window_size).mean()
        
        st.subheader("Moving Average of High Prices")
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['High'], label='Original High', color='blue')
        plt.plot(df.index, df['high_smoothed'], label=f'Moving Average ({window_size})', linestyle='--', color='red')
        plt.xlabel("Date")
        plt.ylabel("High Price")
        plt.title("Original vs Moving Average")
        plt.legend()
        st.pyplot(plt)
    
    # Differencing for Stationarity
    with tab4:
        df['high_diff'] = df['High'].diff()
        
        st.subheader("High Prices Differencing")
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['High'], label='Original High', color='blue')
        plt.plot(df.index, df['high_diff'], label='Differenced High', linestyle='--', color='green')
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.title("Original vs Differenced High")
        plt.legend()
        st.pyplot(plt)
