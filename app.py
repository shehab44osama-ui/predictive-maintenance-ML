
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import os
import joblib
import plotly.graph_objects as go
import plotly.express as px

# =========================================================
# PMAI // ULTRA INDUSTRIAL CONTROL CENTER
# =========================================================
st.set_page_config(
    page_title="PMAI | Predictive Maintenance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STATE
# =========================================================
defaults = {
    "page": "Overview",
    "current_prediction": None,
    "chat_history": [],
    "last_run": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# DESIGN SYSTEM
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
 --bg:#050b14; --panel:#0a1422; --panel2:#0d1b2c;
 --line:#18304a; --line2:#224663; --text:#edf6ff; --muted:#7890a8;
 --cyan:#2dd4e5; --blue:#4d8dff; --green:#35d49a;
 --red:#ff5b70; --amber:#f2c14e;
}
*{font-family:Inter,sans-serif}
.stApp{
 background:
 radial-gradient(circle at 80% -10%,rgba(45,212,229,.12),transparent 28%),
 radial-gradient(circle at 0% 35%,rgba(77,141,255,.08),transparent 25%),
 var(--bg);
 color:var(--text);
}
.main .block-container{max-width:1600px;padding:1.1rem 2rem 3rem}
[data-testid="stSidebar"]{background:#040a12;border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:var(--text)}
[data-testid="stSidebar"] .stButton>button{
 background:#081522!important;border:1px solid #132b42!important;
 text-align:left!important;min-height:42px!important;color:#b9cada!important;
}
[data-testid="stSidebar"] .stButton>button:hover{
 border-color:var(--cyan)!important;color:white!important;
}
.brand{padding:8px 4px 22px;border-bottom:1px solid var(--line);margin-bottom:20px}
.brand-main{font-size:27px;font-weight:800;letter-spacing:-1px}
.brand-main b{color:var(--cyan)}
.brand-sub{font-size:9px;color:#5e7891;letter-spacing:2px;margin-top:4px}
.nav-label{font-size:9px;color:#5e7891;font-weight:800;letter-spacing:1.5px;margin:12px 0 8px}
.side-status{border:1px solid var(--line);border-radius:14px;padding:13px;margin-top:15px;background:#07111d}
.side-status div{font-size:11px;color:#8ea6bc;margin:7px 0}
.side-status strong{color:white}
.topbar{
 display:flex;justify-content:space-between;align-items:center;
 background:rgba(9,22,36,.78);border:1px solid var(--line);
 border-radius:15px;padding:11px 16px;margin-bottom:16px;
}
.topbar-left{font-size:10px;letter-spacing:1.5px;color:#8da6bc;font-weight:800}
.live{font-size:10px;color:#4de0a6;font-weight:800}
.hero{
 background:linear-gradient(135deg,#0d253c,#081421 58%,#0b1d30);
 border:1px solid #20415d;border-radius:25px;padding:27px 30px;
 position:relative;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.22)
}
.hero:after{
 content:"";position:absolute;right:-85px;top:-125px;width:300px;height:300px;
 border-radius:50%;border:1px solid rgba(45,212,229,.2);
 box-shadow:0 0 0 40px rgba(45,212,229,.025),0 0 0 80px rgba(45,212,229,.018)
}
.kicker{font-size:9px;color:var(--cyan);font-weight:800;letter-spacing:2px}
.hero h1{font-size:36px;line-height:1.1;margin:8px 0;color:white;letter-spacing:-1.2px}
.hero p{font-size:12px;line-height:1.7;color:#8fa7bd;max-width:760px}
.badge{display:inline-block;margin-top:10px;padding:6px 10px;border-radius:999px;
 background:rgba(53,212,154,.07);border:1px solid rgba(53,212,154,.25);
 color:#64dfae;font-size:9px;font-weight:800;letter-spacing:.8px}
.section{font-size:18px;font-weight:800;color:white;margin:23px 0 3px}
.sub{font-size:11px;color:#667f96;margin-bottom:12px}
.card{background:linear-gradient(145deg,#0c1b2c,#081522);border:1px solid var(--line);
 border-radius:17px;padding:17px;box-shadow:0 10px 30px rgba(0,0,0,.13)}
.kpi{background:linear-gradient(145deg,#0d2135,#081522);border:1px solid var(--line);
 border-radius:17px;padding:16px;min-height:112px}
.kpi-label{font-size:9px;color:#668097;font-weight:800;letter-spacing:1.1px}
.kpi-value{font-size:27px;font-weight:800;color:white;margin-top:7px}
.kpi-foot{font-size:10px;color:#526b82;margin-top:4px}
.telemetry{background:#081624;border:1px solid #17314b;border-radius:14px;padding:13px}
.telemetry .name{font-size:10px;color:#7891a7;font-weight:700}
.telemetry .value{font-size:22px;font-weight:800;color:white;margin-top:3px}
.telemetry .unit{font-size:9px;color:#5f7890}
.risk-high{background:linear-gradient(145deg,#35141f,#170d15);border:1px solid #733141}
.risk-low{background:linear-gradient(145deg,#0d3029,#091b1d);border:1px solid #1d6656}
.risk{border-radius:20px;padding:23px;min-height:205px}
.risk-label{font-size:9px;color:#7790a6;letter-spacing:1.3px;font-weight:800}
.risk-title{font-size:30px;font-weight:800;margin:7px 0}
.risk-high .risk-title{color:#ff6f81}.risk-low .risk-title{color:#55dba8}
.risk-number{font-size:46px;font-weight:800;color:white;line-height:1}
.risk-note{font-size:11px;color:#8299ad;margin-top:12px;line-height:1.6}
.ai{background:linear-gradient(145deg,#0c2035,#091521);border:1px solid #225072;
 border-radius:19px;padding:20px}
.ai-title{color:#6fe3eb;font-size:12px;font-weight:800;letter-spacing:.5px}
.ai-sub{color:#607b93;font-size:10px;margin-top:4px}
.divider{height:1px;background:var(--line);margin:17px 0}
.alert{padding:13px 15px;border-radius:13px;margin:7px 0;font-size:11px;line-height:1.55}
.alert-red{background:#251019;border:1px solid #592535;color:#ff9aaa}
.alert-green{background:#09231d;border:1px solid #1d5b4b;color:#77ddb5}
.alert-amber{background:#241d0c;border:1px solid #5c4b1d;color:#e9ca71}
.stButton>button{border-radius:11px!important;min-height:43px!important;
 background:#0b1b2c!important;border:1px solid #1c3b56!important;color:#dceaf5!important;font-weight:700!important}
.stButton>button:hover{border-color:var(--cyan)!important;color:white!important}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{
 background:#081726!important;border:1px solid #1b3853!important;border-radius:10px!important}
input,textarea{background:#081726!important;color:white!important}
label{color:#8fa6bb!important;font-size:11px!important;font-weight:700!important}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:13px}
[data-testid="stChatMessage"]{background:#091827;border:1px solid #17334c;border-radius:14px}
.footer{text-align:center;color:#3f5970;font-size:9px;padding:35px 0 5px;letter-spacing:1px}
</style>
""", unsafe_allow_html=True)

# =========================================================
# MODEL / HISTORY
# =========================================================
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

try:
    model = load_model()
except Exception as e:
    st.error("Could not load model.pkl")
    st.code(str(e))
    st.stop()

HISTORY_FILE = "prediction_history.csv"

def load_history():
    if Path(HISTORY_FILE).exists():
        try:
            return pd.read_csv(HISTORY_FILE)
        except Exception:
            pass
    return pd.DataFrame()

def save_prediction(record):
    old = load_history()
    new = pd.DataFrame([record])
    result = pd.concat([old, new], ignore_index=True) if not old.empty else new
    result.to_csv(HISTORY_FILE, index=False)

# =========================================================
# GEMINI
# =========================================================
try:
    from google import genai
except ImportError:
    genai = None

def gemini_client():
    if genai is None:
        return None, "google-genai is not installed."
    key = ""
    try:
        key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        pass
    if not key:
        key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        return None, "GEMINI_API_KEY was not found."
    try:
        return genai.Client(api_key=key), None
    except Exception as e:
        return None, str(e)

def machine_context(r):
    if not r:
        return "No current prediction."
    return str({
        "machine_type": r.get("Machine Type"),
        "operating_mode": r.get("Operating Mode"),
        "vibration_rms": r.get("Vibration RMS"),
        "motor_temperature": r.get("Motor Temperature"),
        "current": r.get("Average Phase Current"),
        "pressure": r.get("Pressure Level"),
        "rpm": r.get("RPM"),
        "hours_since_maintenance": r.get("Hours Since Maintenance"),
        "ambient_temperature": r.get("Ambient Temperature"),
        "temperature_difference": r.get("Temperature Difference"),
        "maintenance_load": r.get("Maintenance Load"),
        "prediction": r.get("Prediction"),
        "failure_probability": r.get("Failure Probability"),
    })

def ask_gemini(question):
    client, err = gemini_client()
    if client is None:
        return f"⚠️ Gemini is not connected.\n\n{err}"
    prompt = f"""
You are a professional predictive-maintenance AI assistant.
Use ONLY the supplied machine data. Do not invent measurements.
Do not override the CatBoost prediction. A prediction is not proof
that a physical failure has occurred.

MACHINE DATA:
{machine_context(st.session_state.current_prediction)}

QUESTION:
{question}

Answer professionally and concisely. Give practical maintenance guidance.
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini error: {e}"

# =========================================================
# SIDEBAR
# =========================================================
history = load_history()
total = len(history)
high = int((history["Prediction"] == "HIGH RISK").sum()) if "Prediction" in history.columns else 0

with st.sidebar:
    st.markdown("""
    <div class="brand">
      <div class="brand-main">⚙️ PM<b>AI</b></div>
      <div class="brand-sub">Industrial Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">CONTROL CENTER</div>', unsafe_allow_html=True)
    nav = ["Overview", "Predictive Monitor", "Analytics", "AI Assistant"]
    for item in nav:
        if st.button(item, key="nav_"+item, use_container_width=True):
            st.session_state.page = item
            st.rerun()

    st.markdown('<div class="nav-label">SYSTEM</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="side-status">
      <div>● Model <strong>ONLINE</strong></div>
      <div>▣ Engine <strong>CatBoost</strong></div>
      <div>◉ Window <strong>24 HOURS</strong></div>
      <div>⌁ Predictions <strong>{total}</strong></div>
      <div>⚠ Alerts <strong>{high}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("PMAI v2.0 • Predictive Maintenance")

# =========================================================
# TOP
# =========================================================
st.markdown("""
<div class="topbar">
  <div class="topbar-left">PMAI / INDUSTRIAL AI OPERATIONS CENTER</div>
  <div class="live">● LIVE SYSTEM • MODEL ONLINE</div>
</div>
<div class="hero">
  <div class="kicker">INDUSTRIAL INTELLIGENCE PLATFORM</div>
<h1>predictive maintenance</h1>
<p>AI-Powered Industrial Failure Prediction & Monitoring</p>  <p>
    An AI-assisted predictive-maintenance control center for detecting
    machine-failure risk within the next 24 hours using a trained CatBoost model.
  </p>
  <span class="badge">CATBOOST ONLINE &nbsp; • &nbsp; REAL-TIME INPUT &nbsp; • &nbsp; 24H RISK WINDOW</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# OVERVIEW
# =========================================================
if st.session_state.page == "Overview":
    avg_prob = float(history["Failure Probability"].mean()) if "Failure Probability" in history.columns and not history.empty else 0
    latest = history.iloc[-1] if not history.empty else None

    st.markdown('<div class="section">Mission Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Operational summary of the predictive-maintenance system.</div>', unsafe_allow_html=True)

    k = st.columns(5)
    vals = [
        ("MODEL", "CATBOOST", "Production model"),
        ("PREDICTIONS", total, "Analyses stored"),
        ("HIGH RISK", high, "Risk predictions"),
        ("AVG RISK", f"{avg_prob:.1f}%", "Historical average"),
        ("STATUS", "ONLINE", "Inference ready"),
    ]
    for col,(lab,val,foot) in zip(k,vals):
        with col:
            st.markdown(f"""<div class="kpi"><div class="kpi-label">{lab}</div>
            <div class="kpi-value">{val}</div><div class="kpi-foot">{foot}</div></div>""",unsafe_allow_html=True)

    st.markdown('<div class="section">Latest Machine State</div>', unsafe_allow_html=True)
    if latest is None:
        st.info("No prediction yet. Open Predictive Monitor and run the first analysis.")
    else:
        a,b = st.columns([1,1])
        with a:
            is_high = latest.get("Prediction") == "HIGH RISK"
            cls = "risk-high" if is_high else "risk-low"
            title = "HIGH RISK" if is_high else "LOW RISK"
            st.markdown(f"""
            <div class="risk {cls}">
              <div class="risk-label">LATEST PREDICTIVE STATE</div>
              <div class="risk-title">{title}</div>
              <div class="risk-number">{float(latest.get("Failure Probability",0)):.2f}%</div>
              <div class="risk-note">{latest.get("Machine Type")} • {latest.get("Operating Mode")} •
              {latest.get("Saved At")}</div>
            </div>
            """,unsafe_allow_html=True)
        with b:
            st.markdown('<div class="card"><b style="color:#72dce5;">LATEST TELEMETRY</b><div class="divider"></div>',unsafe_allow_html=True)
            cols=st.columns(3)
            data=[
                ("Temperature",latest.get("Motor Temperature"),"°C"),
                ("Vibration",latest.get("Vibration RMS"),"RMS"),
                ("Current",latest.get("Average Phase Current"),"A"),
                ("Pressure",latest.get("Pressure Level"),""),
                ("RPM",latest.get("RPM"),""),
                ("Maintenance Load",latest.get("Maintenance Load"),""),
            ]
            for col,(name,val,unit) in zip(cols,data):
                with col:
                    st.markdown(f"""<div class="telemetry"><div class="name">{name}</div>
                    <div class="value">{val}</div><div class="unit">{unit}</div></div>""",unsafe_allow_html=True)
            st.markdown('</div>',unsafe_allow_html=True)

    st.markdown('<div class="section">System Architecture</div>',unsafe_allow_html=True)
    c=st.columns(4)
    for col,title,desc in zip(c,
        ["01 / SENSOR INPUT","02 / FEATURE ENGINEERING","03 / CATBOOST INFERENCE","04 / AI INTERPRETATION"],
        ["Machine operating measurements","Derived predictive variables","Failure probability within 24h","Gemini explanation & guidance"]):
        with col:
            st.markdown(f"""<div class="card"><div class="kpi-label">{title}</div>
            <div style="color:white;font-weight:800;margin-top:9px;font-size:14px;">{desc}</div></div>""",unsafe_allow_html=True)

# =========================================================
# PREDICTIVE MONITOR
# =========================================================
if st.session_state.page == "Predictive Monitor":
    st.markdown('<div class="section">Predictive Monitor</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">Configure the machine, enter live telemetry, and execute a 24-hour failure-risk analysis.</div>',unsafe_allow_html=True)

    c1,c2,c3=st.columns(3)
    with c1: machine_type=st.selectbox("Machine Type",["CNC","Pump","Compressor","Robotic Arm"])
    with c2: operating_mode=st.selectbox("Operating Mode",["idle","normal","peak"],index=1)
    with c3: hour=st.selectbox("Operating Hour",list(range(24)),index=12,format_func=lambda x:f"{x:02d}:00")

    st.markdown('<div class="section">Live Telemetry</div>',unsafe_allow_html=True)
    r1,r2,r3,r4=st.columns(4)
    with r1: vibration_rms=st.number_input("Vibration RMS",min_value=0.0,value=1.0,step=.01)
    with r2: temperature_motor=st.number_input("Motor Temperature (°C)",value=70.0,step=.1)
    with r3: current_phase_avg=st.number_input("Average Phase Current (A)",min_value=0.0,value=10.0,step=.1)
    with r4: pressure_level=st.number_input("Pressure Level",min_value=0.0,value=5.0,step=.1)
    r5,r6,r7,r8=st.columns(4)
    with r5: rpm=st.number_input("RPM",min_value=0.0,value=1500.0,step=10.0)
    with r6: hours_since_maintenance=st.number_input("Hours Since Maintenance",min_value=0.0,value=100.0,step=1.0)
    with r7: ambient_temp=st.number_input("Ambient Temperature (°C)",value=25.0,step=.1)
    with r8: timestamp=st.date_input("Inspection Date",value=datetime.now().date())

    td=temperature_motor-ambient_temp
    vr=vibration_rms/(rpm+1)
    cr=current_phase_avg/(rpm+1)
    pr=pressure_level/(rpm+1)
    ml=hours_since_maintenance*rpm
    dow=timestamp.weekday()
    month=timestamp.month

    st.markdown('<div class="section">Derived Predictive Signals</div>',unsafe_allow_html=True)
    fcols=st.columns(5)
    for col,(name,val,unit) in zip(fcols,[
        ("Temperature Δ",f"{td:.2f}","°C"),("Vibration / RPM",f"{vr:.5f}",""),
        ("Current / RPM",f"{cr:.5f}",""),("Pressure / RPM",f"{pr:.5f}",""),
        ("Maintenance Load",f"{ml:,.0f}","")]):
        with col:
            st.markdown(f"""<div class="kpi"><div class="kpi-label">{name}</div>
            <div class="kpi-value">{val}<span style="font-size:10px;color:#607990"> {unit}</span></div>
            <div class="kpi-foot">Engineered feature</div></div>""",unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)
    if st.button("⚡ EXECUTE PREDICTIVE ANALYSIS",use_container_width=True):
        X=pd.DataFrame({
            "machine_type":[machine_type],"vibration_rms":[vibration_rms],
            "temperature_motor":[temperature_motor],"current_phase_avg":[current_phase_avg],
            "pressure_level":[pressure_level],"rpm":[rpm],"operating_mode":[operating_mode],
            "hours_since_maintenance":[hours_since_maintenance],"ambient_temp":[ambient_temp],
            "hour":[hour],"day_of_week":[dow],"month":[month],
            "temperature_difference":[td],"vibration_rpm_ratio":[vr],
            "current_rpm_ratio":[cr],"pressure_rpm_ratio":[pr],"maintenance_load":[ml]
        })
        try:
            with st.spinner("CatBoost inference in progress..."):
                pred=model.predict(X)[0]
                prob=float(model.predict_proba(X)[0][1])
        except Exception as e:
            st.error("Prediction failed.")
            st.code(str(e))
            st.stop()

        fp=prob*100
        npct=100-fp
        record={
            "Saved At":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Machine Type":machine_type,"Operating Mode":operating_mode,"Date":str(timestamp),
            "Operating Hour":hour,"Vibration RMS":vibration_rms,"Motor Temperature":temperature_motor,
            "Average Phase Current":current_phase_avg,"Pressure Level":pressure_level,"RPM":rpm,
            "Hours Since Maintenance":hours_since_maintenance,"Ambient Temperature":ambient_temp,
            "Day of Week":dow,"Month":month,"Temperature Difference":td,
            "Vibration/RPM Ratio":vr,"Current/RPM Ratio":cr,"Pressure/RPM Ratio":pr,
            "Maintenance Load":ml,"Prediction":"HIGH RISK" if pred==1 else "LOW RISK",
            "Failure Probability":round(fp,2),"Normal Probability":round(npct,2)
        }
        save_prediction(record)
        st.session_state.current_prediction=record
        st.session_state.last_run=datetime.now()

        st.markdown('<div class="section">Decision Panel</div>',unsafe_allow_html=True)
        a,b=st.columns([1.05,1])
        with a:
            cls="risk-high" if pred==1 else "risk-low"
            title="HIGH RISK" if pred==1 else "LOW RISK"
            st.markdown(f"""<div class="risk {cls}">
            <div class="risk-label">CATBOOST PREDICTION</div>
            <div class="risk-title">{title}</div>
            <div class="risk-number">{fp:.2f}%</div>
            <div class="risk-note">Estimated probability of failure within the next 24 hours.</div>
            </div>""",unsafe_allow_html=True)
        with b:
            fig=go.Figure(go.Indicator(
                mode="gauge+number",value=fp,
                number={"suffix":"%","font":{"size":30,"color":"white"}},
                gauge={"axis":{"range":[0,100],"tickcolor":"#6b8196"},
                       "bar":{"color":"#ff5b70" if pred==1 else "#35d49a"},
                       "bgcolor":"#0a1726","bordercolor":"#203b55",
                       "steps":[{"range":[0,30],"color":"#09231d"},
                                {"range":[30,70],"color":"#28220e"},
                                {"range":[70,100],"color":"#251019"}]}))
            fig.update_layout(height=230,margin=dict(l=20,r=20,t=25,b=10),
                              paper_bgcolor="rgba(0,0,0,0)",font_color="white")
            st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        st.markdown('<div class="section">Telemetry Snapshot</div>',unsafe_allow_html=True)
        tc=st.columns(6)
        for col,(name,val,unit) in zip(tc,[
            ("Vibration",vibration_rms,"RMS"),("Temperature",temperature_motor,"°C"),
            ("Current",current_phase_avg,"A"),("Pressure",pressure_level,""),
            ("RPM",rpm,""),("Maint. Load",f"{ml:,.0f}","")]):
            with col:
                st.markdown(f"""<div class="telemetry"><div class="name">{name}</div>
                <div class="value">{val}</div><div class="unit">{unit}</div></div>""",unsafe_allow_html=True)

        st.markdown('<div class="section">AI Maintenance Intelligence</div>',unsafe_allow_html=True)
        with st.spinner("Gemini is interpreting the result..."):
            ai=ask_gemini("Analyze the current prediction. Explain why the result matters, identify which supplied measurements deserve attention, and provide practical maintenance actions. Use only the supplied data.")
        st.markdown(f"""<div class="ai"><div class="ai-title">✦ GEMINI / CONTEXT-AWARE ANALYSIS</div>
        <div class="ai-sub">AI interpretation based on the current CatBoost prediction</div>
        <div class="divider"></div><div style="font-size:13px;color:#dce8f2;line-height:1.85;white-space:pre-wrap">{ai}</div></div>""",unsafe_allow_html=True)

# =========================================================
# ANALYTICS
# =========================================================
if st.session_state.page == "Analytics":
    st.markdown('<div class="section">Predictive Analytics</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">Explore historical prediction behavior and machine-risk patterns.</div>',unsafe_allow_html=True)

    if history.empty:
        st.info("No historical predictions yet.")
    else:
        c1,c2,c3,c4=st.columns(4)
        avg=float(history["Failure Probability"].mean()) if "Failure Probability" in history.columns else 0
        high_rate=(high/len(history))*100 if len(history) else 0
        metrics=[("TOTAL RUNS",len(history),"Analyses"),("HIGH-RISK RUNS",high,"Alerts"),
                 ("HIGH-RISK RATE",f"{high_rate:.1f}%","Historical share"),("AVG FAILURE RISK",f"{avg:.1f}%","All runs")]
        for col,(lab,val,foot) in zip([c1,c2,c3,c4],metrics):
            with col: st.markdown(f"""<div class="kpi"><div class="kpi-label">{lab}</div>
            <div class="kpi-value">{val}</div><div class="kpi-foot">{foot}</div></div>""",unsafe_allow_html=True)

        st.markdown('<div class="section">Failure Probability Timeline</div>',unsafe_allow_html=True)
        df=history.copy()
        df["Saved At"]=pd.to_datetime(df["Saved At"],errors="coerce")
        df=df.dropna(subset=["Saved At"]).tail(50)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=df["Saved At"],y=df["Failure Probability"],
                                 mode="lines+markers",line=dict(color="#2dd4e5",width=2),
                                 marker=dict(size=5),name="Failure Probability"))
        fig.add_hline(y=70,line_dash="dash",line_color="#ff5b70",annotation_text="High-risk reference")
        fig.update_layout(height=360,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#071321",
                          font_color="#8ea6ba",margin=dict(l=10,r=10,t=20,b=10),
                          xaxis_title="",yaxis_title="Failure Probability (%)")
        st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False})

        left,right=st.columns(2)
        with left:
            counts=history["Prediction"].value_counts()
            fig2=go.Figure(go.Pie(labels=counts.index,values=counts.values,hole=.68,
                                  marker=dict(colors=["#ff5b70" if x=="HIGH RISK" else "#35d49a" for x in counts.index])))
            fig2.update_layout(height=330,paper_bgcolor="rgba(0,0,0,0)",font_color="#b9cada",
                               showlegend=True,margin=dict(l=10,r=10,t=20,b=10))
            st.plotly_chart(fig2,use_container_width=True,config={"displayModeBar":False})
        with right:
            if "Machine Type" in history.columns and "Failure Probability" in history.columns:
                by_machine=history.groupby("Machine Type")["Failure Probability"].mean().sort_values()
                fig3=px.bar(by_machine,orientation="h",title="Average Failure Probability by Machine")
                fig3.update_traces(marker_color="#4d8dff")
                fig3.update_layout(height=330,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="#071321",
                                   font_color="#8ea6ba",margin=dict(l=10,r=10,t=45,b=10))
                st.plotly_chart(fig3,use_container_width=True,config={"displayModeBar":False})

        st.markdown('<div class="section">Prediction Records</div>',unsafe_allow_html=True)
        st.dataframe(history.iloc[::-1].reset_index(drop=True),use_container_width=True,hide_index=True)
        st.download_button("⬇ Export CSV",history.to_csv(index=False).encode("utf-8"),
                           "prediction_history.csv","text/csv")

# =========================================================
# AI ASSISTANT
# =========================================================
if st.session_state.page == "AI Assistant":
    st.markdown('<div class="section">AI Maintenance Assistant</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">Ask Gemini about the latest machine prediction and supplied telemetry.</div>',unsafe_allow_html=True)

    if st.session_state.current_prediction:
        r=st.session_state.current_prediction
        st.markdown(f"""<div class="ai"><div class="ai-title">CURRENT MACHINE CONTEXT</div>
        <div class="ai-sub">{r["Machine Type"]} • {r["Operating Mode"]} • {r["Prediction"]}</div>
        <div class="divider"></div><div style="color:#d9e6ef;font-size:12px">
        Failure Probability <b>{r["Failure Probability"]}%</b> &nbsp; | &nbsp;
        Temperature <b>{r["Motor Temperature"]}°C</b> &nbsp; | &nbsp;
        Vibration <b>{r["Vibration RMS"]}</b> &nbsp; | &nbsp;
        RPM <b>{r["RPM"]}</b></div></div>""",unsafe_allow_html=True)
    else:
        st.info("Run a prediction first to provide Gemini with machine context.")

    st.markdown("<br>",unsafe_allow_html=True)
    questions=[
        "Explain the latest prediction in simple terms.",
        "Which supplied sensor reading needs attention?",
        "What maintenance actions should be considered?",
        "Give me a short maintenance report."
    ]
    qc=st.columns(4)
    for i,q in enumerate(questions):
        if qc[i].button(q,key=f"quick_{i}",use_container_width=True):
            st.session_state.chat_history.append({"role":"user","content":q})
            st.session_state.chat_history.append({"role":"assistant","content":ask_gemini(q)})
            st.rerun()

    for m in st.session_state.chat_history:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    q=st.chat_input("Ask the maintenance AI...")
    if q:
        st.session_state.chat_history.append({"role":"user","content":q})
        st.session_state.chat_history.append({"role":"assistant","content":ask_gemini(q)})
        st.rerun()

    if st.session_state.chat_history and st.button("Clear Conversation"):
        st.session_state.chat_history=[]
        st.rerun()

# =========================================================
# FOOTER
# =========================================================
st.markdown("""<div class="footer">PMAI ULTRA • INDUSTRIAL AI OPERATIONS CENTER • CATBOOST • GEMINI • 24-HOUR FAILURE PREDICTION</div>""",unsafe_allow_html=True)
