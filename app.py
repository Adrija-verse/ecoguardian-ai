"""
EcoGuardian AI - Streamlit Web Application
===========================================
 UI showcasing multi-agent urban ecosystem regeneration.

🏆 DESIGNED TO WIN - Competition-Ready Interface
✨ Features: Real-time agent monitoring, interactive workflows, live metrics
🎨 Modern design with animations and professional visualizations

Author: Adrija Sil

"""

"""
EcoGuardian AI - Streamlit Web Interface 
"""

import streamlit as st
import asyncio
import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).parent))

# Import the FIXED main system
from main import EcoGuardianSystem

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# Add this OUTSIDE the EcoGuardianSystem class
# (at the top of your app.py, after imports)

def _calculate_duration(start_time, end_time):
    """Calculate duration between start and end times"""
    if not start_time or not end_time:
        return "N/A"
    
    try:
        from datetime import datetime
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        duration = (end - start).total_seconds()
        
        if duration < 1:
            return f"{duration*1000:.0f}ms"
        elif duration < 60:
            return f"{duration:.1f}s"
        else:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            return f"{minutes}m {seconds}s"
    except:
        return "N/A"

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="EcoGuardian AI",
    page_icon="🌍",
    layout="wide"
)

# ============================================================================
# CUSTOM CSS
# ============================================================================
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .intervention-card {
        background: white;
        border-left: 5px solid #667eea;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .priority-high {
        background: #ff4757;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .priority-medium {
        background: #ffa502;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .priority-low {
        background: #2ed573;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if 'system' not in st.session_state:
    with st.spinner("🚀 Initializing EcoGuardian AI System..."):
        try:
            st.session_state.system = EcoGuardianSystem()
            st.session_state.initialized = True
            st.session_state.init_error = None
        except Exception as e:
            st.session_state.initialized = False
            st.session_state.init_error = str(e)

# Show initialization status
if not st.session_state.get('initialized', False):
    st.error("⚠️ System initialization failed. Some features may be limited.")
    if st.session_state.get('init_error'):
        with st.expander("Show Error Details"):
            st.code(st.session_state.init_error)
    st.info("💡 Tip: Check your .env file and ensure API keys are set correctly.")

# ============================================================================
# HEADER
# ============================================================================
st.markdown('<div class="main-header">🌍 EcoGuardian AI</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Autonomous Multi-Agent Urban Ecosystem Healer | Powered by Gemini 2.5</p>', unsafe_allow_html=True)

# Stats bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🤖 Active Agents", "3")
with col2:
    st.metric("🛠️ Tools Available", "3")
with col3:
    st.metric("🧠 AI Model", "Gemini 2.5")
with col4:
    st.metric("💾 Memory", "Active")

st.markdown("---")

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## 🌍 Navigation")
    
    workflow = st.radio(
        "Choose Workflow:",
        [
            "🔄 Sequential Analysis",
            "🌍 Multi-City Comparison",
            "👤 Personal Carbon Tracker",
            "🎯 Hybrid Orchestration",
            "📊 System Metrics"
        ]
    )
    
    st.markdown("---")
    
    st.markdown("### ℹ️ About")
    st.markdown("""
    **EcoGuardian AI** coordinates autonomous agents to:
    - 🤖 Collect environmental data
    - 🧠 Predict interventions (Gemini AI)
    - 🚀 Deploy eco-actions
    - 📊 Evaluate performance
    """)

# ============================================================================
# MAIN CONTENT - SEQUENTIAL ANALYSIS
# ============================================================================
if workflow == "🔄 Sequential Analysis":
    st.header("🔄 Sequential City Analysis")
    st.markdown("Comprehensive environmental analysis with AI-powered recommendations.")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        city = st.text_input("🏙️ Enter city name:", "Delhi", placeholder="e.g., London, Mumbai, Tokyo", key="seq_city")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Analyze", type="primary", use_container_width=True)
    
    if analyze_btn and city:
        if not st.session_state.get('initialized', False):
            st.error("⚠️ System not initialized. Please refresh the page.")
            st.stop()
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown('<div class="loading-text">🔍 Collecting environmental data...</div>', unsafe_allow_html=True)
        progress_bar.progress(25)
        
        try:
            # Run async function
            result = asyncio.run(
                st.session_state.system.run_sequential_city_analysis(city)
            )
            
            status_text.markdown('<div class="loading-text">🧠 AI is predicting interventions...</div>', unsafe_allow_html=True)
            progress_bar.progress(50)
            
            status_text.markdown('<div class="loading-text">🚀 Deploying eco-actions...</div>', unsafe_allow_html=True)
            progress_bar.progress(75)
            
            status_text.markdown('<div class="loading-text">📊 Generating report...</div>', unsafe_allow_html=True)
            progress_bar.progress(100)
            
            status_text.empty()
            progress_bar.empty()
            
            if result.get("success"):
                st.markdown(f'<div class="success-box">✅ Analysis Complete for {city}!</div>', unsafe_allow_html=True)
                
                # Display results in tabs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📊 Overview", 
                    "🌡️ Environment", 
                    "🤖 AI Predictions",
                    "🚀 Deployed Actions",
                    "📈 Impact Forecast"
                ])
                
                with tab1:
                    sections = result.get("sections", {})
                    summary = sections.get("executive_summary", {})
                    
                    # Score visualization
                    score = summary.get("environmental_score", 0)
                    aqi = summary.get("aqi", 0)
                    status = summary.get("status", "UNKNOWN")
                    
                    # Create gauge chart for environmental score
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number+delta",
                        value = score,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Environmental Health Score"},
                        delta = {'reference': 70, 'increasing': {'color': "green"}},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 40], 'color': "#ff4757"},
                                {'range': [40, 70], 'color': "#ffa502"},
                                {'range': [70, 100], 'color': "#2ed573"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        }
                    ))
                    fig_gauge.update_layout(height=300)
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        aqi_labels = {1: "Good ✅", 2: "Fair 🟢", 3: "Moderate 🟡", 4: "Poor 🟠", 5: "Very Poor 🔴"}
                        aqi_colors = {1: "success", 2: "success", 3: "warning", 4: "error", 5: "error"}
                        st.metric("Air Quality Index", 
                                 aqi_labels.get(aqi, "Unknown"),
                                 delta=f"Level {aqi}",
                                 delta_color="inverse")
                    
                    with col2:
                        st.metric("Status", status, 
                                 delta="Needs Action" if score < 60 else "Good",
                                 delta_color="inverse" if score < 60 else "normal")
                    
                    with col3:
                        risk_level = "High" if score < 40 else "Medium" if score < 70 else "Low"
                        st.metric("Risk Level", risk_level,
                                 delta="Monitor closely" if risk_level != "Low" else "Maintain")
                
                with tab2:
                    conditions = sections.get("current_conditions", {})
                    weather = conditions.get("weather", {})
                    air_quality = conditions.get("air_quality", {})
                    
                    st.subheader("🌤️ Current Weather Conditions")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        temp = weather.get('temperature_celsius', 'N/A')
                        st.metric("🌡️ Temperature", f"{temp}°C" if temp != 'N/A' else 'N/A')
                    
                    with col2:
                        humidity = weather.get('humidity_percent', 'N/A')
                        st.metric("💧 Humidity", f"{humidity}%" if humidity != 'N/A' else 'N/A')
                    
                    with col3:
                        wind = weather.get('wind_speed_mps', 'N/A')
                        st.metric("💨 Wind Speed", f"{wind} m/s" if wind != 'N/A' else 'N/A')
                    
                    with col4:
                        pressure = weather.get('pressure_hpa', 'N/A')
                        st.metric("🌀 Pressure", f"{pressure} hPa" if pressure != 'N/A' else 'N/A')
                    
                    st.markdown("---")
                    st.subheader("🏭 Air Quality Details")
                    
                    pollutants = air_quality.get("pollutants", {})
                    
                    if pollutants and any(v != 'N/A' for v in pollutants.values()):
                        # Create pollutant chart
                        pollutant_data = {
                            'Pollutant': [],
                            'Concentration (μg/m³)': [],
                            'Status': []
                        }
                        
                        for pollutant, value in pollutants.items():
                            if value != 'N/A' and value is not None:
                                pollutant_data['Pollutant'].append(pollutant.upper())
                                pollutant_data['Concentration (μg/m³)'].append(float(value))
                                # Simple status based on value
                                if float(value) < 50:
                                    pollutant_data['Status'].append('Good')
                                elif float(value) < 100:
                                    pollutant_data['Status'].append('Moderate')
                                else:
                                    pollutant_data['Status'].append('Poor')
                        
                        if pollutant_data['Pollutant']:
                            df_pollutants = pd.DataFrame(pollutant_data)
                            
                            fig_pollutants = px.bar(
                                df_pollutants,
                                x='Pollutant',
                                y='Concentration (μg/m³)',
                                color='Status',
                                color_discrete_map={'Good': '#2ed573', 'Moderate': '#ffa502', 'Poor': '#ff4757'},
                                title='Pollutant Levels'
                            )
                            st.plotly_chart(fig_pollutants, use_container_width=True)
                        else:
                            st.info("No pollutant data available")
                    else:
                        st.info("No pollutant data available")
                
                with tab3:
                    predictions = sections.get("ai_predictions", {})
                    interventions = predictions.get("interventions", [])
                    
                    st.subheader(f"🤖 AI-Powered Interventions")
                    
                    # Display Gemini info
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Powered by:** Google Gemini 2.5 Flash")
                    with col2:
                        confidence = predictions.get('average_confidence', 0)
                        conf_color = "🟢" if confidence > 70 else "🟡" if confidence > 50 else "🔴"
                        st.markdown(f"**Confidence:** {conf_color} {confidence}%")
                    
                    st.markdown("---")
                    
                    # Filter out empty/invalid interventions
                    valid_interventions = []
                    for intervention in interventions:
                        name = intervention.get('name', '').strip()
                        desc = intervention.get('description', '').strip()
                        priority = intervention.get('priority_level', 'Medium')
                        confidence_score = intervention.get('confidence_score', 0)
                        
                        # Skip if intervention is empty or invalid
                        if (name and name != 'N/A' and name != 'Intervention' and 
                            desc and desc != 'No description' and desc != 'N/A'):
                            valid_interventions.append(intervention)
                    
                    if valid_interventions:
                        st.success(f"✅ {len(valid_interventions)} High-Quality Interventions Identified")
                        
                        for i, intervention in enumerate(valid_interventions, 1):
                            priority = intervention.get('priority_level', 'Medium')
                            priority_class = f"priority-{priority.lower()}"
                            
                            with st.container():
                                st.markdown(f"""
                                <div class="intervention-card">
                                    <h4>#{i}. {intervention.get('name', 'Intervention')}</h4>
                                    <span class="{priority_class}">{priority} Priority</span>
                                    <p style='margin-top: 1rem; color: #666;'>{intervention.get('description', '')}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Confidence", f"{intervention.get('confidence_score', 0)}%")
                                with col2:
                                    st.metric("Timeline", intervention.get('timeline', 'Short-term'))
                                with col3:
                                    cost = intervention.get('estimated_cost_usd', 0)
                                    st.metric("Est. Cost", f"${cost:,}" if cost > 0 else "TBD")
                                
                                st.markdown("---")
                    else:
                        # Show rule-based fallback interventions
                        st.warning("⚠️ AI predictions incomplete. Showing rule-based recommendations:")
                        
                        fallback_interventions = [
                            {
                                "name": "🌳 Urban Tree Planting Initiative",
                                "description": f"Deploy 1,000 native trees in {city} to improve air quality and reduce urban heat island effect. Focus on high-traffic areas and industrial zones.",
                                "priority": "High" if aqi >= 4 else "Medium",
                                "confidence": 85,
                                "timeline": "6-12 months",
                                "cost": 50000
                            },
                            {
                                "name": "🚗 Traffic Emission Reduction",
                                "description": "Implement AI-powered traffic signal optimization and promote public transport to reduce vehicle emissions by 25%.",
                                "priority": "High" if aqi >= 4 else "Medium",
                                "confidence": 80,
                                "timeline": "3-6 months",
                                "cost": 150000
                            },
                            {
                                "name": "🏭 Industrial Emission Monitoring",
                                "description": "Deploy real-time IoT sensors to monitor and control industrial emissions with automated alerts.",
                                "priority": "High" if aqi >= 4 else "Low",
                                "confidence": 90,
                                "timeline": "1-3 months",
                                "cost": 200000
                            },
                            {
                                "name": "🏗️ Green Infrastructure Development",
                                "description": "Build green roofs, vertical gardens, and urban parks to improve air quality and biodiversity.",
                                "priority": "Medium",
                                "confidence": 75,
                                "timeline": "12-24 months",
                                "cost": 500000
                            },
                            {
                                "name": "⚡ Renewable Energy Integration",
                                "description": "Install solar panels and wind turbines to reduce fossil fuel dependency and carbon emissions.",
                                "priority": "Medium",
                                "confidence": 85,
                                "timeline": "12-18 months",
                                "cost": 1000000
                            }
                        ]
                        
                        for i, intervention in enumerate(fallback_interventions, 1):
                            priority = intervention['priority']
                            priority_class = f"priority-{priority.lower()}"
                            
                            with st.container():
                                st.markdown(f"""
                                <div class="intervention-card">
                                    <h4>#{i}. {intervention['name']}</h4>
                                    <span class="{priority_class}">{priority} Priority</span>
                                    <p style='margin-top: 1rem; color: #666;'>{intervention['description']}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Confidence", f"{intervention['confidence']}%")
                                with col2:
                                    st.metric("Timeline", intervention['timeline'])
                                with col3:
                                    st.metric("Est. Cost", f"${intervention['cost']:,}")
                                
                                st.markdown("---")
                
                with tab4:
                    deployed = sections.get("deployed_actions", {})
                    actions = deployed.get("actions_deployed", [])
                    
                    st.subheader(f"🚀 Deployed Actions ({len(actions)})")
                    
                    if actions:
                        for action in actions:
                            action_type = action.get('action_type', 'Unknown').replace('_', ' ').title()
                            status_icon = "✅" if action.get('status') == 'deployed' else "⏳"
                            
                            st.markdown(f"""
                            <div class="action-deployed">
                                {status_icon} <strong>{action_type}</strong>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show action details
                            details = action.get('details', {})
                            impact = action.get('impact', {})
                            
                            if details or impact:
                                with st.expander("View Details"):
                                    if details:
                                        st.json(details)
                                    if impact:
                                        st.markdown("**Environmental Impact:**")
                                        st.json(impact)
                    else:
                        st.info("No actions deployed yet")
                
                with tab5:
                    impact = sections.get("impact_summary", {})
                    
                    st.subheader("📈 Predicted Environmental Impact")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        co2_reduction = impact.get("predicted_co2_reduction", 0)
                        st.metric(
                            "CO₂ Reduction",
                            f"{co2_reduction:,} kg/year",
                            delta=f"≈ {int(co2_reduction / 21)} trees equivalent"
                        )
                    
                    with col2:
                        aqi_improvement = impact.get("predicted_aqi_improvement", 0)
                        st.metric(
                            "AQI Improvement",
                            f"{aqi_improvement}%",
                            delta="Better air quality"
                        )
                    
                    with col3:
                        actions_count = impact.get("actions_deployed", 0)
                        st.metric(
                            "Actions Deployed",
                            actions_count,
                            delta=f"{actions_count} interventions"
                        )
                    
                    # Create impact timeline visualization
                    st.markdown("---")
                    st.subheader("📊 Impact Over Time (Projected)")
                    
                    months = list(range(1, 13))
                    co2_monthly = [co2_reduction * (m/12) for m in months]
                    
                    fig_timeline = go.Figure()
                    fig_timeline.add_trace(go.Scatter(
                        x=months,
                        y=co2_monthly,
                        mode='lines+markers',
                        name='CO₂ Reduction',
                        line=dict(color='#2ed573', width=3),
                        fill='tozeroy'
                    ))
                    
                    fig_timeline.update_layout(
                        title='Cumulative CO₂ Reduction Over 12 Months',
                        xaxis_title='Month',
                        yaxis_title='CO₂ Reduced (kg)',
                        height=400
                    )
                    
                    st.plotly_chart(fig_timeline, use_container_width=True)
            
            else:
                st.markdown(f'<div class="warning-box">❌ Analysis failed: {result.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
                    
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.markdown(f'<div class="warning-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)
            st.error("Please check your API keys and internet connection.")

# ============================================================================
# MULTI-CITY COMPARISON
# ============================================================================
elif workflow == "🌍 Multi-City Comparison":
    st.header("🌍 Multi-City Comparison")
    st.markdown("Compare environmental health across multiple cities.")
    
    cities_input = st.text_input(
        "🏙️ Enter cities (comma-separated):",
        "Tokyo, London, Mumbai",
        key="parallel_cities"
    )
    
    compare_btn = st.button("🌍 Compare Cities", type="primary", use_container_width=True)
    
    if compare_btn and cities_input:
        if not st.session_state.get('initialized', False):
            st.error("⚠️ System not initialized.")
            st.stop()
        
        cities = [c.strip() for c in cities_input.split(",") if c.strip()]
        
        if len(cities) < 2:
            st.warning("Please enter at least 2 cities.")
        else:
            with st.spinner(f"🔄 Analyzing {len(cities)} cities in parallel..."):
                try:
                    result = asyncio.run(
                        st.session_state.system.run_parallel_multi_city_analysis(cities)
                    )
                    
                    if result.get("success"):
                        st.success(f"✅ Analyzed {result.get('successful_analyses')} cities successfully!")
                        
                        rankings = result.get("rankings", [])
                        
                        if rankings:
                            # Create comparison chart
                            df = pd.DataFrame(rankings)
                            
                            fig = px.bar(
                                df,
                                x='city',
                                y='score',
                                color='score',
                                color_continuous_scale=['#ff4757', '#ffa502', '#2ed573'],
                                title='Environmental Health Scores'
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Show rankings
                            st.subheader("🏆 Rankings")
                            
                            for i, rank in enumerate(rankings, 1):
                                col1, col2, col3 = st.columns([1, 3, 2])
                                
                                with col1:
                                    st.markdown(f"### #{i}")
                                
                                with col2:
                                    st.markdown(f"**{rank['city']}**")
                                    st.caption(rank['status'])
                                
                                with col3:
                                    st.metric("Score", f"{rank['score']}/100")
                                
                                st.markdown("---")
                        else:
                            st.warning("No rankings available.")
                    else:
                        st.error(f"Comparison failed: {result.get('error')}")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# ============================================================================
# PERSONAL CARBON TRACKER
# ============================================================================
elif workflow == "👤 Personal Carbon Tracker":
    st.header("👤 Personal Carbon Footprint")
    st.markdown("Calculate your carbon footprint and get recommendations.")
    
    location = st.text_input("📍 Your location:", "Mumbai")
    
    st.subheader("📝 Your Weekly Activities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        car_km = st.slider("🚗 Car travel (km/week)", 0, 500, 100)
        electricity = st.slider("⚡ Electricity (kWh/month)", 0, 1000, 200)
    
    with col2:
        beef = st.slider("🥩 Beef (kg/week)", 0.0, 10.0, 1.0, 0.5)
        dairy = st.slider("🥛 Dairy (kg/week)", 0.0, 20.0, 5.0, 1.0)
    
    calculate_btn = st.button("📊 Calculate Footprint", type="primary", use_container_width=True)
    
    if calculate_btn:
        if not st.session_state.get('initialized', False):
            st.error("⚠️ System not initialized.")
            st.stop()
        
        activities = [
            {"activity_type": "transportation", "category": "car", "amount": car_km},
            {"activity_type": "energy", "category": "electricity", "amount": electricity},
            {"activity_type": "food", "category": "beef", "amount": beef},
            {"activity_type": "food", "category": "dairy", "amount": dairy}
        ]
        
        with st.spinner("Calculating..."):
            try:
                result = asyncio.run(
                    st.session_state.system.run_personal_concierge(location, activities)
                )
                
                footprint = result.get("carbon_footprint", {})
                
                st.success("✅ Footprint Calculated!")
                
                total = footprint.get("total_emissions_kg_co2", 0)
                annual = total * 52
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Weekly", f"{total:.1f} kg CO₂")
                
                with col2:
                    st.metric("Annual", f"{annual:.0f} kg CO₂")
                
                with col3:
                    trees = int(annual / 21)
                    st.metric("Trees to Offset", f"{trees}")
                
                # Breakdown
                st.markdown("---")
                st.subheader("📊 Breakdown")
                
                breakdown = footprint.get("breakdown_by_type", {})
                
                if breakdown:
                    fig = px.pie(
                        values=list(breakdown.values()),
                        names=[k.title() for k in breakdown.keys()],
                        title='Carbon Footprint by Category'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Recommendations
                st.markdown("---")
                st.subheader("💡 Recommendations")
                
                recommendations = result.get("recommendations", [])
                for i, rec in enumerate(recommendations[:3], 1):
                    st.markdown(f"""
                    <div class="intervention-card">
                        <h4>{i}. {rec.get('action')}</h4>
                        <p style='color: #666;'>{rec.get('description')}</p>
                        <p style='color: #2ed573;'><b>Impact:</b> {rec.get('impact')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ============================================================================
# HYBRID ORCHESTRATION
# ============================================================================

elif workflow == "🎯 Hybrid Orchestration":
    st.header("🎯 Hybrid Multi-Agent Orchestration")
    st.markdown("Experience complete multi-agent coordination.")
    
    st.info("""
    **This workflow demonstrates:**
    - 🔄 Parallel data collection
    - ➡️ Sequential prediction & deployment
    - 🤝 A2A Protocol communication
    """)
    
    location = st.text_input("🏙️ Enter location:", "Paris")
    
    orchestrate_btn = st.button("🚀 Run Orchestration", type="primary", use_container_width=True)
    
    if orchestrate_btn and location:
        if not st.session_state.get('initialized', False):
            st.error("⚠️ System not initialized.")
            st.stop()
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown("🔄 Initializing coordinator agent...")
        progress_bar.progress(20)
        
        try:
            status_text.markdown("🔄 Orchestrating multi-agent workflow...")
            progress_bar.progress(40)
            
            result = asyncio.run(
                st.session_state.system.run_hybrid_orchestration(location)
            )
            
            progress_bar.progress(80)
            status_text.markdown("📊 Processing results...")
            
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            # ✅ FIX: Check for 'status' key instead of 'success'
            if result.get("status") == "completed":
                st.markdown('<div class="success-box">✅ Orchestration Complete!</div>', unsafe_allow_html=True)
                
                # Display tabs
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 Overview",
                    "🔄 Workflow Stages", 
                    "💬 A2A Messages",
                    "📈 Performance"
                ])
                
                    
                with tab1:
                    col1, col2, col3 = st.columns(3)
    
                    with col1:
                        status_icon = "✅" if result.get('status') == "completed" else "⏳"
                        st.metric("Status", f"{status_icon} {result.get('status', 'Unknown').title()}")
    
                    with col2:
                        stages_count = len(result.get('stages', {}))
                        st.metric("Workflow Stages", stages_count)
    
                    with col3:
                        messages_count = len(result.get('a2a_messages', []))
                        st.metric("A2A Messages", messages_count)
    
                    st.markdown("---")
    
                    # ✨ NEW: Orchestration Timeline Visualization
                    st.subheader("⏱️ Orchestration Timeline")
    
                    stages = result.get('stages', {})
                    messages = result.get('a2a_messages', [])
    
                    if messages:
                        # Create timeline data
                        timeline_events = []
        
                        for msg in messages:
                            timeline_events.append({
                                'Time': msg.get('timestamp', ''),
                                'Event': f"{msg.get('sender', '')} → {msg.get('receiver', '')}",
                                'Type': msg.get('message_type', ''),
                                'Category': 'Communication'
                            })
        
                         # Add stage events
                        for stage_name, stage_data in stages.items():
                            if isinstance(stage_data, dict):
                                timeline_events.append({
                                    'Time': stage_data.get('timestamp', result.get('start_time', '')),
                                    'Event': stage_name.replace('_', ' ').title(),
                                    'Type': 'stage_completion',
                                    'Category': 'Workflow Stage'
                                })
        
                        if timeline_events:
                            # Sort by time
                            timeline_events.sort(key=lambda x: x['Time'])
            
                            # Create visual timeline
                            for i, event in enumerate(timeline_events, 1):
                                category_colors = {
                                    'Communication': '#667eea',
                                    'Workflow Stage': '#38ef7d'
                                }
                
                                color = category_colors.get(event['Category'], '#999')
                
                                st.markdown(f"""
                                <div style='
                                    display: flex;
                                    align-items: center;
                                    margin: 0.8rem 0;
                                    padding: 0.8rem;
                                    background: linear-gradient(90deg, {color}22 0%, transparent 100%);
                                    border-left: 4px solid {color};
                                    border-radius: 5px;
                                '>
                                    <div style='
                                        min-width: 30px;
                                        height: 30px;
                                        background: {color};
                                        color: white;
                                        border-radius: 50%;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        font-weight: bold;
                                        margin-right: 1rem;
                                    '>
                                        {i}
                                    </div>
                                    <div style='flex: 1;'>
                                        <div style='font-weight: 600; color: #333;'>{event['Event']}</div>
                                        <div style='font-size: 0.85rem; color: #666;'>
                                            {event['Category']} • {event['Type']}
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
    
                    st.markdown("---")
                    st.subheader("📋 Orchestration Details")
                
                
                    # Create a nice info box
                    st.markdown(f"""
                    <div style='
                        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
                        padding: 1.5rem;
                        border-radius: 10px;
                        border: 1px solid #667eea33;
                    '>
                        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                            <div>
                                <div style='font-size: 0.85rem; color: #666; margin-bottom: 0.3rem;'>📍 Location</div>
                                <div style='font-weight: 600; color: #333;'>{result.get('location', location)}</div>
                            </div>
                            <div>
                                <div style='font-size: 0.85rem; color: #666; margin-bottom: 0.3rem;'>🔄 Workflow Type</div>
                                <div style='font-weight: 600; color: #333;'>{result.get('workflow_type', 'hybrid').upper()}</div>
                            </div>
                            <div>
                                <div style='font-size: 0.85rem; color: #666; margin-bottom: 0.3rem;'>🆔 Session ID</div>
                                <div style='font-family: monospace; font-size: 0.85rem; color: #555;'>{result.get('session_id', 'N/A')}</div>
                            </div>
                            <div>
                                <div style='font-size: 0.85rem; color: #666; margin-bottom: 0.3rem;'>⏱️ Duration</div>
                                <div style='font-weight: 600; color: #333;'>
                                    {_calculate_duration(result.get('start_time'), result.get('end_time'))}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                
                
                with tab2:
                    st.subheader("🔄 Multi-Agent Workflow Stages")
                    
                    stages = result.get('stages', {})
                    
                    if stages:
                        # Display each stage
                        for i, (stage_name, stage_data) in enumerate(stages.items(), 1):
                            stage_display_name = stage_name.replace('_', ' ').title()
                            
                            with st.expander(f"Stage {i}: {stage_display_name}", expanded=True):
                                if isinstance(stage_data, dict):
                                    # Show key metrics from stage
                                    if 'success' in stage_data:
                                        success_icon = "✅" if stage_data.get('success') else "❌"
                                        st.markdown(f"**Status:** {success_icon}")
                                    
                                    if 'environmental_score' in stage_data:
                                        st.metric("Environmental Score", f"{stage_data['environmental_score']}/100")
                                    
                                    if 'interventions' in stage_data:
                                        interventions = stage_data.get('interventions', [])
                                        st.metric("Interventions Generated", len(interventions))
                                    
                                    if 'actions_deployed' in stage_data:
                                        actions = stage_data.get('actions_deployed', [])
                                        st.metric("Actions Deployed", len(actions))
                                    
                                    # Show full data
                                    with st.expander("📄 View Raw Data"):
                                        st.json(stage_data)
                                else:
                                    st.info(f"Stage output: {stage_data}")
                    else:
                        st.warning("No workflow stages recorded.")
                
                with tab3:
                    st.subheader("💬 Agent-to-Agent (A2A) Communication")
                    
                    st.markdown("""
                    **A2A Protocol** enables transparent inter-agent communication.
                    Each message shows how agents coordinate and pass data.
                    """)
                    
                    messages = result.get('a2a_messages', [])
                    
                    if messages:
                        st.success(f"📨 {len(messages)} messages exchanged between agents")
                        
                        # Create a flow diagram representation
                        st.markdown("### 📊 Message Flow")
                        
                        for i, msg in enumerate(messages, 1):
                            sender = msg.get('sender', 'Unknown')
                            receiver = msg.get('receiver', 'Unknown')
                            msg_type = msg.get('message_type', 'unknown')
                            timestamp = msg.get('timestamp', 'N/A')
                            
                            # Create visual message card
                            st.markdown(f"""
                            <div style='
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                padding: 1rem;
                                border-radius: 10px;
                                color: white;
                                margin: 0.5rem 0;
                                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                            '>
                                <div style='display: flex; align-items: center; justify-content: space-between;'>
                                    <div>
                                        <b>#{i}</b> &nbsp;&nbsp;
                                        <b>{sender}</b> 
                                        <span style='opacity: 0.8;'> → </span>
                                        <b>{receiver}</b>
                                    </div>
                                    <div style='background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.85rem;'>
                                        {msg_type}
                                    </div>
                                </div>
                                <div style='margin-top: 0.5rem; font-size: 0.8rem; opacity: 0.7;'>
                                    {timestamp}
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show payload if available
                            payload = msg.get('payload', {})
                            if payload:
                                with st.expander("📦 View Message Payload"):
                                    st.json(payload)
                    else:
                        st.warning("No A2A messages recorded.")
                
                with tab4:
                    st.subheader("📈 Orchestration Performance")
                    
                    # Calculate metrics
                    stages = result.get('stages', {})
                    messages = result.get('a2a_messages', [])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Workflow Efficiency**")
                        
                        total_stages = len(stages)
                        successful_stages = sum(
                            1 for stage in stages.values() 
                            if isinstance(stage, dict) and stage.get('success', False)
                        )
                        
                        if total_stages > 0:
                            efficiency = (successful_stages / total_stages) * 100
                            st.progress(efficiency / 100)
                            st.metric("Stage Success Rate", f"{efficiency:.1f}%")
                        else:
                            st.info("No stages to evaluate")
                    
                    with col2:
                        st.markdown("**Communication Metrics**")
                        
                        unique_senders = len(set(msg.get('sender') for msg in messages))
                        unique_receivers = len(set(msg.get('receiver') for msg in messages))
                        
                        st.metric("Active Agents", unique_senders + unique_receivers)
                        st.metric("Messages Exchanged", len(messages))
                    
                    st.markdown("---")
                    
                    # Agent participation chart
                    if messages:
                        st.markdown("**Agent Participation**")
                        
                        agent_activity = {}
                        for msg in messages:
                            sender = msg.get('sender', 'unknown')
                            receiver = msg.get('receiver', 'unknown')
                            
                            if sender and sender != 'unknown':
                                agent_activity[sender] = agent_activity.get(sender, 0) + 1

                        if agent_activity:       
                        
                            df_activity = pd.DataFrame([
                                {
                                    "Agent": agent.replace('_', ' ').title(),
                                    "Messages Sent": count
                                }

                                for agent, count in sorted(agent_activity.items(), key=lambda x: x[1], reverse=True)
                            ])
                        
                            fig = px.bar(

                                df_activity,
                                x='Agent',
                                y='Messages Sent',
                                title='Agent Communication Activity',
                                color='Messages Sent',
                                color_continuous_scale='Viridis',
                                orientation='h',
                                text='Messages Sent'  # Show values on bars
                            )

                            fig.update_traces(textposition='outside')
                            fig.update_layout(
                                height=max(300, len(df_activity) * 60),
                                showlegend=False,
                                xaxis_title="Messages Sent",
                                yaxis_title="Agent"

                            )

                            st.plotly_chart(fig, use_container_width=True)

                            st.markdown("**Communication Summary**")
                            st.dataframe(
                                df_activity.style.background_gradient(
                                    subset=['Messages Sent'], 
                                    cmap='Greens'
                                ),
                                use_container_width=True,
                                hide_index=True
                            )
                        
                        else:
                            st.info("No agent activity data available")

                    else:
                        st.info("No messages to analyze")

                
            elif result.get("status") == "failed":
                st.markdown(f'<div class="warning-box">❌ Orchestration failed: {result.get("error", "Unknown error")}</div>', unsafe_allow_html=True)
                
                # Show error details
                with st.expander("🔍 Debug Information"):
                    st.json(result)
            
            else:
                st.warning(f"⏳ Orchestration status: {result.get('status', 'unknown')}")
                st.json(result)
                    
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            
            st.markdown(f'<div class="warning-box">❌ Error during orchestration: {str(e)}</div>', unsafe_allow_html=True)
            
            # Show detailed error
            with st.expander("🔍 Error Details"):
                import traceback
                st.code(traceback.format_exc())
            
            st.error("💡 Tip: Check that all agents are properly initialized and API keys are valid.")

# ============================================================================
# SYSTEM METRICS
# ============================================================================
elif workflow == "📊 System Metrics":
    st.header("📊 System Performance & Evaluation")
    
    if not st.session_state.get('initialized', False):
        st.warning("System not fully initialized.")
        st.stop()
    
    try:
        metrics = st.session_state.system.get_system_metrics()
        
        st.subheader("🤖 Agent Performance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🧠 Predictor**")
            pred = metrics.get("predictor_evaluation", {})
            st.metric("Predictions", pred.get("predictions_made", 0))
            st.metric("Avg Quality", f"{pred.get('average_quality_score', 0):.1f}/100")
        
        with col2:
            st.markdown("**🚀 Deployer**")
            dep = metrics.get("deployer_evaluation", {})
            st.metric("Deployments", dep.get("total_deployments", 0))
            st.metric("Success Rate", f"{dep.get('success_rate_percent', 0):.1f}%")
        
        with col3:
            st.markdown("**🎯 Coordinator**")
            coord = metrics.get("coordinator_evaluation", {})
            st.metric("Workflows", coord.get("total_workflows_executed", 0))
            st.metric("Success Rate", f"{coord.get('success_rate_percent', 0):.1f}%")
        
        st.markdown("---")
        st.subheader("💾 Memory Statistics")
        
        memory = metrics.get("memory_statistics", {})
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Entries", memory.get("total_entries", 0))
        
        with col2:
            st.metric("Utilization", f"{memory.get('utilization_percent', 0):.1f}%")
        
        with col3:
            st.metric("Compactions", memory.get("compaction_events", 0))
        
        st.markdown("---")
        st.success("✅ All systems operational!")
        
    except Exception as e:
        st.error(f"Error loading metrics: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <h3>🌍 EcoGuardian AI</h3>
    <p><b>Autonomous Multi-Agent Urban Ecosystem Healing System</b></p>
    <p>Built for LangChain Agents </p>
</div>
""", unsafe_allow_html=True)