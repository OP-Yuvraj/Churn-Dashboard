import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


df = pd.read_csv('churn_user.csv')

## Executive Summary Section
st.set_page_config(page_title="Churn User Dashboard", layout="wide")

st.title("📱 Mobile User Churn Dashboard")

# KPIs
Total_users = df.shape[0]
churn_users = df[df['churn'] == 1].shape[0]
active_users = df[df['churn'] == 0].shape[0]
churn_rate = (churn_users/Total_users)*100

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total User",Total_users)
c2.metric("Churned Users",churn_users)
c3.metric("Active Users",active_users)
c4.metric("Churn Rate (%)",f'{churn_rate:.2f}%')

st.divider()
plt.style.use("dark_background")

# Churn Distribution

st.header("📊Churn Vs Non-Churn Distribution")
 
churn_count = df['churn'].value_counts().sort_index()
fig,ax = plt.subplots(figsize=(8,4))
bar=ax.bar(["Non-Churn","Churn"],churn_count)
ax.bar_label(bar,fmt="%d")
ax.set_ylabel("Number Of Users")
st.pyplot(fig)

st.subheader("📊User Section")
st.write(" ")
c6,c7 = st.columns(2)

# Active days vs Churn
with c6:
    st.markdown(" Avg Active Days by Churn vs Non-churn")

    active_day = df.groupby('churn')['active_days'].mean()
    label = ["Non-churn",'active_user']


    fig2,ax2 = plt.subplots(figsize=(4,4))
    ax2.pie(active_day,labels=label,autopct=lambda pct: f"{(pct/100)*active_day.sum():.1f}",startangle=90)
    ax2.axis("equal")
    st.pyplot(fig2)

st.write(" ")
# Avg rating vs churn
with c7:
    st.markdown("Average Rating by Churn Status")

    rating_churn = df.groupby("churn")["avg_rating"].mean()


    fig3, ax3 = plt.subplots(figsize=(4,4))
    ax3.pie(rating_churn,labels=["Non-Churn", "Churn"],autopct=lambda pct:f"{(pct/100)*rating_churn.sum():.2f}",startangle=90)
    ax3.axis("equal")
    st.pyplot(fig3)

st.write("  ")
# Rating std

st.header("📊 Rating Standard Deviation by Churn Status")
rating_std = df.groupby("churn")["rating_std"].mean()
fig4,ax4 = plt.subplots(figsize=(8,4))
bar2=ax4.barh(["Non-Churn","Churn"],rating_std)
ax4.bar_label(bar2,fmt='%.2f')
ax4.set_xlabel("Average Rating Std.")
st.pyplot(fig4)
# Sidebar filter
st.sidebar.header("🔎 Filter Users")

# Churn filter
churn_filter = st.sidebar.selectbox(
    "Select Churn Status",
    options=["All", "Non-Churn", "Churn"]
)

# Interaction filter
min_interaction = st.sidebar.slider(
    "Minimum Total Interaction",
    int(df["total_interaction"].min()),
    int(df["total_interaction"].max()),
    0
)

# Unique app filter
min_unique_app = st.sidebar.slider(
    "Minimum Unique Apps Used",
    int(df["unique_app"].min()),
    int(df["unique_app"].max()),
    0
)

# Apply Filter
filtered_df = df.copy()

# Churn filter
if churn_filter == "Non-Churn":
    filtered_df = filtered_df[filtered_df["churn"] == 0]
elif churn_filter == "Churn":
    filtered_df = filtered_df[filtered_df["churn"] == 1]

# Interaction filter
filtered_df = filtered_df[
    filtered_df["total_interaction"] >= min_interaction
]

# Unique app filter
filtered_df = filtered_df[
    filtered_df["unique_app"] >= min_unique_app
]

# User Interaction Section Table
table_df = filtered_df.copy()

# Calculate avg interaction per day
table_df["avg_interaction_per_day"] = (
    table_df["total_interaction"] / table_df["active_days"]
)

# Calculate avg interaction per app
table_df["avg_interaction_per_app"] = (
    table_df["total_interaction"] / table_df["unique_app"]
)

# Select required columns
final_table = table_df[
    [
        "uid",
        "total_interaction",
        "avg_interaction_per_day",
        "avg_interaction_per_app"
    ]
]

# Show Table
st.subheader("📋 User Interaction Report")
st.dataframe(final_table)

## Download Report Button
csv = final_table.to_csv(index=False)

st.download_button(
    label="⬇ Download Report",
    data=csv,
    file_name="user_interaction_report.csv",
    mime="text/csv"
)




