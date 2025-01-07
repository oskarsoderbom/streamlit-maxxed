import streamlit as st
import hydralit_components as hc
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import yaml
import streamlit_authenticator as stauth
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add file handler
log_file = "app.log"
file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Page configuration
st.set_page_config(
    page_title="Analytics Dashboard Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "selected_date_range" not in st.session_state:
    st.session_state.selected_date_range = "7D"


# Load custom CSS
def load_css():
    try:
        css_file = Path("style/main.css")
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        logger.error(f"Error loading CSS: {str(e)}")


load_css()

# Load authentication config
with open("config.yaml") as file:
    config = yaml.safe_load(file)

# Create authentication credentials
credentials = {
    "usernames": {
        "admin": {
            "email": "admin@company.com",
            "name": "Admin User",
            "password": "$2b$12$WoNp6hULuz5AkeOpHsFY.uu7KSiHAF0BpEFRKZGHXqSsyLSTobZA6",  # admin123
        },
        "analyst": {
            "email": "analyst@company.com",
            "name": "Data Analyst",
            "password": "$2b$12$WoNp6hULuz5AkeOpHsFY.uu7KSiHAF0BpEFRKZGHXqSsyLSTobZA6",  # admin123
        },
    }
}

# Create the authenticator object
authenticator = stauth.Authenticate(
    credentials, "streamlit_auth_cookie", "random_signature_key", 30
)

# Authentication
try:
    # Create the login widget
    authenticator.login(key="login_form", location="main")

    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "sidebar")
        st.write(f'Welcome *{st.session_state["name"]}*')

        # Main application logic
        with st.sidebar:
            # Profile section
            with st.container():
                st.image("https://avatars.githubusercontent.com/u/0", width=100)
                st.markdown(f"### Welcome, {st.session_state['name']} 👋")
                st.markdown("---")

            # Rest of your sidebar code...
            selected = option_menu(
                menu_title=None,
                options=["Dashboard", "Analytics", "Performance", "Settings"],
                icons=["house-door-fill", "graph-up", "speedometer2", "gear"],
                default_index=0,
                styles={
                    "container": {
                        "padding": "0!important",
                        "background-color": "transparent",
                    },
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

        # Main content based on selection
        if selected == "Dashboard":
            st.title("Dashboard")

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

                st.plotly_chart(
                    fig, use_container_width=True, config={"displayModeBar": False}
                )

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

                st.plotly_chart(
                    fig, use_container_width=True, config={"displayModeBar": False}
                )

            # Engagement Metrics
            st.markdown("### Engagement Metrics")

            # Create columns with proper spacing
            metrics_cols = st.columns([1, 1, 1])

            with metrics_cols[0]:
                # Traffic Sources
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
                    xaxis=dict(
                        tickfont=dict(color="#D1D5DB"), showgrid=False, title=None
                    ),
                    yaxis=dict(
                        tickfont=dict(color="#D1D5DB"),
                        showgrid=True,
                        gridcolor="rgba(255,255,255,0.1)",
                        title=None,
                    ),
                    margin=dict(l=40, r=20, t=40, b=40),
                )

                st.plotly_chart(
                    fig, use_container_width=True, config={"displayModeBar": False}
                )

            with metrics_cols[1]:
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
                    legend=dict(
                        font=dict(color="#D1D5DB"),
                        yanchor="middle",
                        y=0.5,
                        xanchor="center",
                        x=0.5,
                    ),
                    margin=dict(l=20, r=20, t=40, b=20),
                )

                st.plotly_chart(
                    fig, use_container_width=True, config={"displayModeBar": False}
                )

            with metrics_cols[2]:
                # Session Duration
                times = pd.DataFrame(
                    {
                        "Time": ["0-1m", "1-3m", "3-10m", "10m+"],
                        "Sessions": [40, 30, 20, 10],
                    }
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
                    xaxis=dict(
                        tickfont=dict(color="#D1D5DB"), showgrid=False, title=None
                    ),
                    yaxis=dict(
                        tickfont=dict(color="#D1D5DB"),
                        showgrid=True,
                        gridcolor="rgba(255,255,255,0.1)",
                        title=None,
                    ),
                    margin=dict(l=40, r=20, t=40, b=40),
                )

                st.plotly_chart(
                    fig, use_container_width=True, config={"displayModeBar": False}
                )

        elif selected == "Analytics":
            st.title("Analytics")

            # Tabs for different analytics views
            tab1, tab2, tab3 = st.tabs(
                ["Traffic Analysis", "Conversion Funnel", "User Behavior"]
            )

            with tab1:
                st.markdown("### Traffic Analysis")
                # Traffic analysis content
                st.line_chart(np.random.randn(20, 3))

            with tab2:
                st.markdown("### Conversion Funnel")
                # Funnel chart
                funnel_data = pd.DataFrame(
                    {
                        "Stage": ["Visits", "Cart", "Checkout", "Purchase"],
                        "Users": [1000, 600, 250, 100],
                    }
                )
                st.bar_chart(funnel_data.set_index("Stage"))

            with tab3:
                st.markdown("### User Behavior")
                # Heatmap or user flow visualization
                st.area_chart(np.random.randn(20, 3))

        elif selected == "Performance":
            st.title("Performance")

            # System metrics
            perf_col1, perf_col2 = st.columns(2)

            with perf_col1:
                st.markdown("### System Health")
                st.metric("Server Response Time", "42ms", "-3ms")
                st.metric("CPU Usage", "24%", "5%")
                st.metric("Memory Usage", "62%", "-2%")

            with perf_col2:
                st.markdown("### Error Rates")
                st.metric("Error Rate", "0.12%", "-0.08%")
                st.metric("4xx Errors", "22", "-5")
                st.metric("5xx Errors", "1", "-2")

        elif selected == "Settings":
            st.title("Settings")

            # User Settings
            st.header("User Settings")

            # Password Change
            if st.checkbox("Change Password"):
                try:
                    if authenticator.reset_password(
                        st.session_state["username"], "Reset password"
                    ):
                        st.success("Password modified successfully")
                except Exception as e:
                    st.error(f"Error changing password: {str(e)}")

            # Theme Settings
            st.header("Theme Settings")
            theme = st.toggle("Dark Mode", value=st.session_state.dark_mode)
            if theme != st.session_state.dark_mode:
                st.session_state.dark_mode = theme
                st.experimental_rerun()

            # Notification Settings
            st.header("Notification Settings")
            email_notif = st.checkbox("Email Notifications", value=True)
            push_notif = st.checkbox("Push Notifications", value=True)

            # Data Settings
            st.header("Data Settings")
            cache_data = st.checkbox("Cache Dashboard Data", value=True)
            auto_refresh = st.select_slider(
                "Auto Refresh Interval",
                options=["Off", "30s", "1m", "5m", "15m", "30m", "1h"],
                value="5m",
            )

            # Save Settings
            if st.button("Save Settings"):
                st.success("Settings saved successfully!")

    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")

except Exception as e:
    logger.error(f"Authentication error: {str(e)}")
    st.error("An error occurred during authentication. Please try again.")
