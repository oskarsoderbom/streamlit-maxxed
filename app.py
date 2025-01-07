import streamlit as st
import hydralit_components as hc
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import json
import time

# Page configuration
st.set_page_config(
    page_title="Analytics Dashboard Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load custom CSS
def load_css():
    css_file = Path("style/main.css")
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css()

# Initialize session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "selected_date_range" not in st.session_state:
    st.session_state.selected_date_range = "7D"

# Sidebar
with st.sidebar:
    # Profile section
    with st.container():
        st.image("https://avatars.githubusercontent.com/u/0", width=100)
        st.markdown("### Welcome, Admin 👋")
        st.markdown("---")

    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Analytics", "Performance", "Settings"],
        icons=["house-door-fill", "graph-up", "speedometer2", "gear"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "var(--primary-color)", "font-size": "1rem"},
            "nav-link": {
                "font-size": "0.9rem",
                "text-align": "left",
                "padding": "0.75rem",
                "border-radius": "0.5rem",
                "--hover-color": "rgba(124,58,237,0.1)",
            },
            "nav-link-selected": {
                "background-color": "var(--primary-color)",
                "color": "white",
            },
        },
    )

    st.markdown("---")

    # Date Range Selector
    date_ranges = {
        "24H": "Last 24 Hours",
        "7D": "Last 7 Days",
        "30D": "Last 30 Days",
        "3M": "Last 3 Months",
        "YTD": "Year to Date",
    }
    selected_range = st.selectbox(
        "Date Range",
        options=list(date_ranges.keys()),
        format_func=lambda x: date_ranges[x],
        index=1,
    )
    st.session_state.selected_date_range = selected_range

# Main Content
if selected == "Dashboard":
    # Header
    st.markdown("# Dashboard Overview")

    # Quick Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            "Active Users",
            "2,847",
            "12.5%",
            help="Total number of active users in the selected period",
        )
    with col2:
        st.metric(
            "Revenue",
            "$94.2K",
            "8.1%",
            help="Total revenue generated in the selected period",
        )
    with col3:
        st.metric(
            "Conversion Rate",
            "3.24%",
            "-0.5%",
            help="Percentage of visitors who completed a desired action",
        )
    with col4:
        st.metric(
            "Avg. Session",
            "4m 12s",
            "15.3%",
            help="Average time spent by users in a session",
        )

    # Create two columns for the charts
    left_col, right_col = st.columns([2, 1])

    with left_col:
        # User Activity Chart
        st.markdown("### User Activity")

        # Generate sample data
        dates = pd.date_range(end=datetime.now(), periods=30, freq="D")
        activity_data = pd.DataFrame(
            {
                "Date": dates,
                "Active Users": np.random.randint(1000, 3000, size=30),
                "Page Views": np.random.randint(5000, 15000, size=30),
                "Sessions": np.random.randint(2000, 6000, size=30),
            }
        )

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=activity_data["Date"],
                y=activity_data["Active Users"],
                name="Active Users",
                line=dict(color="#7C3AED", width=3),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=activity_data["Date"],
                y=activity_data["Sessions"],
                name="Sessions",
                line=dict(color="#EC4899", width=3),
            )
        )

        fig.update_layout(
            height=400,
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="#D1D5DB"),
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#D1D5DB"),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
                tickfont=dict(color="#D1D5DB"),
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with right_col:
        # User Demographics
        st.markdown("### Demographics")

        # Sample demographics data
        demographics = pd.DataFrame(
            {
                "Age Group": ["18-24", "25-34", "35-44", "45-54", "55+"],
                "Users": [15, 30, 25, 20, 10],
            }
        )

        fig = px.pie(
            demographics,
            values="Users",
            names="Age Group",
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.update_layout(
            height=400,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.1,
                xanchor="center",
                x=0.5,
                font=dict(color="#D1D5DB"),
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Engagement Metrics
    st.markdown("### Engagement Metrics")

    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)

    with metrics_col1:
        # Engagement by Channel
        data = pd.DataFrame(
            {
                "Channel": ["Organic", "Social", "Email", "Referral", "Direct"],
                "Users": [45, 25, 15, 10, 5],
            }
        )

        fig = px.bar(
            data,
            x="Channel",
            y="Users",
            color="Users",
            color_continuous_scale="Agsunset",
        )

        fig.update_layout(
            title=dict(text="Traffic Sources", font=dict(color="#D1D5DB")),
            height=300,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            xaxis=dict(tickfont=dict(color="#D1D5DB"), showgrid=False),
            yaxis=dict(
                tickfont=dict(color="#D1D5DB"),
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with metrics_col2:
        # Device Distribution
        devices = pd.DataFrame(
            {"Device": ["Mobile", "Desktop", "Tablet"], "Sessions": [60, 35, 5]}
        )

        fig = px.pie(
            devices,
            values="Sessions",
            names="Device",
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.update_layout(
            title=dict(text="Device Distribution", font=dict(color="#D1D5DB")),
            height=300,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(color="#D1D5DB")),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with metrics_col3:
        # Engagement Time
        times = pd.DataFrame(
            {"Time": ["0-1m", "1-3m", "3-10m", "10m+"], "Sessions": [40, 30, 20, 10]}
        )

        fig = px.bar(
            times,
            x="Time",
            y="Sessions",
            color="Sessions",
            color_continuous_scale="Agsunset",
        )

        fig.update_layout(
            title=dict(text="Session Duration", font=dict(color="#D1D5DB")),
            height=300,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            xaxis=dict(tickfont=dict(color="#D1D5DB"), showgrid=False),
            yaxis=dict(
                tickfont=dict(color="#D1D5DB"),
                showgrid=True,
                gridcolor="rgba(255,255,255,0.1)",
            ),
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

elif selected == "Analytics":
    st.markdown("# Detailed Analytics")

    # Tabs for different analytics views
    tab1, tab2, tab3 = st.tabs(
        ["Traffic Analysis", "Conversion Funnel", "User Behavior"]
    )

    with tab1:
        st.markdown("### Traffic Analysis")
        # Add traffic analysis content here

    with tab2:
        st.markdown("### Conversion Funnel")
        # Add conversion funnel content here

    with tab3:
        st.markdown("### User Behavior")
        # Add user behavior content here

elif selected == "Performance":
    st.markdown("# Performance Metrics")
    # Add performance metrics content here

elif selected == "Settings":
    st.markdown("# Settings")

    # Settings sections
    st.markdown("### General Settings")

    # Theme Toggle
    theme = st.toggle("Dark Mode", value=st.session_state.dark_mode)
    if theme != st.session_state.dark_mode:
        st.session_state.dark_mode = theme
        st.experimental_rerun()

    # Notification Settings
    st.markdown("### Notification Preferences")
    email_notif = st.checkbox("Email Notifications", value=True)
    push_notif = st.checkbox("Push Notifications", value=True)

    # API Configuration
    st.markdown("### API Configuration")
    api_key = st.text_input("API Key", type="password")

    # Save Settings Button
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")
