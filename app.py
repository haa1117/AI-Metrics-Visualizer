import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
import time

# Page config
st.set_page_config(
    page_title="AI Metrics Visualizer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with animations
st.markdown("""
    <style>
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    .intro-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 4rem 2rem;
        margin: 2rem auto;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        max-width: 1200px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .typing-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 150px;
    }
    
    .typing-text {
        font-family: monospace;
        font-size: 5.5rem;
        font-weight: 900;
        display: inline-block;
        position: relative;
        white-space: nowrap;
        overflow: hidden;
        padding-right: 8px;
        animation: typing 1.5s steps(30, end) forwards;  /* Changed from 3.5s to 1.5s */
    }
    
    .typing-text .gradient-text {
        background: linear-gradient(
            120deg,
            #00ff88 0%,
            #00ffcc 25%,
            #ff3366 50%,
            #ff6b81 75%,
            #00ff88 100%
        );
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: gradient 8s linear infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 200% center }
        100% { background-position: -200% center }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes typeAI {
        0%, 100% { width: 0; }
        10%, 40% { width: 100%; }
        50%, 100% { width: 0; }
    }
    
    @keyframes typeMetrics {
        0%, 10% { width: 0; }
        40%, 70% { width: 100%; }
        80%, 100% { width: 0; }
    }
    
    @keyframes blink {
        50% { opacity: 0; }
    }
    
    @keyframes moveCursor {
        0%, 100% { left: 0; }
        10%, 40% { left: calc(2ch + 10px); }  /* AI width */
        50% { left: calc(2ch + 80px); }      /* AI + gap */
        70% { left: calc(2ch + 80px + 7ch); } /* AI + gap + Metrics */
        80%, 90% { left: calc(2ch + 80px); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes glowPulse {
        0% { box-shadow: 0 0 5px rgba(0,255,136,0.2); }
        50% { box-shadow: 0 0 20px rgba(0,255,136,0.4); }
        100% { box-shadow: 0 0 5px rgba(0,255,136,0.2); }
    }
    
    @keyframes gradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .stApp {
        background: linear-gradient(to bottom right, #1a1a2e, #16213e);
    }
    
    .company-name-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 2rem;
        position: relative;
    }
    
    .company-name {
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        letter-spacing: -2px;
        display: inline-block;
        position: relative;
        white-space: nowrap;
    }
    
    .company-name .ai,
    .company-name .metrics {
        display: inline-block;
        position: relative;
        overflow: hidden;
    }
    
    .company-name .ai {
        background: linear-gradient(45deg, #00ff88, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-right: 0.5rem;
        width: 0;
        animation: typeAI 8s steps(2) infinite;
    }
    
    .company-name .metrics {
        background: linear-gradient(45deg, #ff3366, #ff6b81);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        width: 0;
        animation: typeMetrics 8s steps(7) infinite;
    }
    
    .cursor {
        position: absolute;
        width: 4px;
        height: 80%;
        background-color: #00ff88;
        top: 10%;
        animation: moveCursor 8s steps(9) infinite, blink 1s step-end infinite;
        left: 0;
    }
    
    .intro-text {
        font-size: 1.3rem !important;
        color: #ffffff99 !important;
        max-width: 800px;
        margin: 2rem auto 0;
        line-height: 1.8;
        animation: fadeIn 1.5s ease-out;
        font-weight: 300;
        text-align: center;
    }
    
    .intro-container {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 20px;
        padding: 4rem 2rem;
        margin: 2rem auto;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        animation: fadeIn 1s ease-out;
        position: relative;
        overflow: hidden;
        max-width: 1200px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .company-name-wrapper {
        position: relative;
        height: 120px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    
    .company-name {
        font-size: 5.5rem !important;
        font-weight: 900 !important;
        letter-spacing: -2px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        white-space: nowrap;
        margin: 0 auto;
    }
    
    .company-name .ai,
    .company-name .metrics {
        display: inline-block;
        position: relative;
        overflow: hidden;
    }
    
    .company-name .ai {
        background: linear-gradient(45deg, #00ff88, #00ffcc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-right: 0.5rem;
        width: 0;
        animation: typeAI 8s steps(2) infinite;
    }
    
    .company-name .metrics {
        background: linear-gradient(45deg, #ff3366, #ff6b81);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        width: 0;
        animation: typeMetrics 8s steps(7) infinite;
    }
    
    .cursor {
        position: absolute;
        width: 4px;
        height: 80%;
        background-color: #00ff88;
        top: 10%;
        animation: moveCursor 8s steps(9) infinite, blink 1s step-end infinite;
        left: 0;
    }
    
    .intro-text {
        font-size: 1.3rem !important;
        color: #ffffff99 !important;
        max-width: 800px;
        margin: 2rem auto 0;
        line-height: 1.8;
        animation: fadeIn 1.5s ease-out;
        font-weight: 300;
        text-align: center;
    }
    
    .intro-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(0,255,136,0), 
            rgba(0,255,136,0.5), 
            rgba(255,51,102,0.5), 
            rgba(255,51,102,0));
        animation: gradientFlow 3s ease infinite;
        background-size: 200% 200%;
    }
    
    .highlight {
        color: #00ff88;
        font-weight: 500;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        backdrop-filter: blur(10px);
        animation: fadeIn 0.6s ease-out;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        animation: glowPulse 2s infinite;
    }
    
    .stProgress .st-bo {
        background-color: #00ff88;
    }
    
    .big-font {
        font-size: 4rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    
    .metric-value {
        font-size: 2.5rem !important;
        font-weight: bold !important;
        color: #00ff88 !important;
    }
    
    .comparison-card {
        animation: slideIn 0.5s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .comparison-card:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(0,255,136,0.2);
    }
    
    .chart-container {
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes numberCount {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# Modern Intro Section
st.markdown("""
    <div class="intro-container">
        <div class="typing-container">
            <div class="typing-text">
                <span class="gradient-text">AI Metrics</span>
            </div>
        </div>
        <p class="intro-text">
            Revolutionizing the way we visualize and understand <span class="highlight">artificial intelligence</span> performance. 
            Our cutting-edge platform transforms complex AI metrics into beautiful, intuitive visualizations, 
            making it easier than ever to track, analyze, and optimize your AI models. With <span class="highlight">real-time updates</span> 
            and stunning interactive displays, we bring your AI's performance to life.
        </p>
    </div>
""", unsafe_allow_html=True)

# Metrics Section with animated counting
st.markdown("### Real-time Performance Metrics")
col1, col2, col3 = st.columns(3)

# Simulated real-time metrics
metrics = {
    'fidelity': 0.993,
    'speed': '1M tokens/sec',
    'compression': 11.3
}

# Function to create animated number
def animated_metric(label, value, format_str="{:.3f}"):
    placeholder = st.empty()
    # Create the card immediately but start with value 0
    if isinstance(value, (int, float)):
        current = 0
        placeholder.markdown(
            f"""
            <div class="metric-card">
                <h3 style='color: #00ff88;'>{label}</h3>
                <p class="metric-value">
                    {format_str.format(current)}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        # Now animate the number
        steps = 25  # More steps for smoother animation
        for i in range(1, steps + 1):
            current = (value * i) / steps
            placeholder.markdown(
                f"""
                <div class="metric-card">
                    <h3 style='color: #00ff88;'>{label}</h3>
                    <p class="metric-value">
                        {format_str.format(current)}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            time.sleep(0.075)  # 5 seconds total duration (50 steps * 0.1s)
    else:
        # For non-numeric values, show immediately
        placeholder.markdown(
            f"""
            <div class="metric-card">
                <h3 style='color: #00ff88;'>{label}</h3>
                <p class="metric-value">
                    {value}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

with col1:
    animated_metric("Fidelity Score", metrics['fidelity'])

with col2:
    animated_metric("Processing Speed", metrics['speed'])

with col3:
    animated_metric("Compression Ratio", metrics['compression'], "{:.1f}x")

# Animated Progress Bars
st.markdown("### Performance Indicators")
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Model Efficiency")
    efficiency = st.progress(0)
    for i in range(93):
        efficiency.progress(i + 1)
        time.sleep(0.01)

with col2:
    st.markdown("#### Resource Optimization")
    optimization = st.progress(0)
    for i in range(85):
        optimization.progress(i + 1)
        time.sleep(0.01)

# Interactive Visualization with animation
st.markdown("### Performance Over Time")

# Generate sample data with more points for smoother animation
dates = pd.date_range(start='2024-01-01', end='2024-03-01', freq='D')
fidelity_trend = np.random.normal(0.993, 0.002, len(dates))
fidelity_trend = np.clip(fidelity_trend, 0.98, 1.0)

df = pd.DataFrame({
    'Date': dates,
    'Fidelity': fidelity_trend,
    'Compression': np.random.normal(11.3, 0.5, len(dates))
})

# Create interactive plot with animation
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['Fidelity'],
        name='Fidelity',
        line=dict(color='#00ff88', width=3),
        mode='lines'
    )
)

fig.add_trace(
    go.Scatter(
        x=df['Date'],
        y=df['Compression']/20,
        name='Compression Ratio',
        line=dict(color='#ff3366', width=3),
        mode='lines',
        yaxis='y2'
    )
)

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    title=dict(
        text='Model Performance Metrics',
        font=dict(color='white', size=24)
    ),
    showlegend=True,
    legend=dict(font=dict(color='white')),
    xaxis=dict(
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        tickfont=dict(color='white')
    ),
    yaxis=dict(
        title=dict(
            text='Fidelity Score',
            font=dict(color='#00ff88')
        ),
        tickfont=dict(color='#00ff88'),
        showgrid=True,
        gridcolor='rgba(255,255,255,0.1)',
        range=[0.97, 1.0]
    ),
    yaxis2=dict(
        title=dict(
            text='Compression Ratio',
            font=dict(color='#ff3366')
        ),
        tickfont=dict(color='#ff3366'),
        overlaying='y',
        side='right',
        range=[0.4, 0.65]
    ),
    # Add animation settings
    transition_duration=1000,
    transition=dict(
        duration=500,
        easing='cubic-in-out'
    )
)

# Wrap chart in container for animation
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Comparison Section with animations
st.markdown("### Side-by-Side Comparison")
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div class="metric-card comparison-card">
            <h3 style='color: #00ff88;'>Our Model</h3>
            <ul style='color: white;'>
                <li>✨ 99.3% Fidelity</li>
                <li>🚀 1M tokens/second</li>
                <li>📦 11.3x Compression</li>
                <li>💡 Real-time processing</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="metric-card comparison-card">
            <h3 style='color: #ff3366;'>Industry Standard</h3>
            <ul style='color: white;'>
                <li>⚠️ 95% Fidelity</li>
                <li>🐌 100K tokens/second</li>
                <li>📦 4x Compression</li>
                <li>⏰ Batch processing</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

# Footer
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        Powered by Advanced AI Technology | Real-time Metrics Visualization
    </div>
    """,
    unsafe_allow_html=True
) 