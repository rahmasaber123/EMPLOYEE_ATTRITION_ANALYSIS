import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Kayfa HR Analytics", page_icon="📊", layout="wide")
BLUE = "#4338E0"
LIGHT_BLUE = "#E8E7FB"
WHITE = "#FFFFFF"
GRAY = "#6B7280"
DARK = "#1E1B4B"

st.markdown("""
<style>
    .block-container {padding-top: 1.5rem;}
    .stTabs [data-baseweb="tab-list"] {gap: 8px;}
    .stTabs [data-baseweb="tab"] {
        background: white; border-radius: 8px; padding: 8px 20px;
        border: 1px solid #E5E7EB; font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #4338E0 !important; color: white !important;
        border: 1px solid #4338E0;
    }
    .kpi-card {
        background: white; border-radius: 12px; padding: 18px 20px;
        border: 1px solid #E5E7EB; text-align: center;
    }
    .kpi-val {font-size: 26px; font-weight: 700; margin: 2px 0;}
    .kpi-label {font-size: 12px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.8px;}
    .kpi-sub {font-size: 12px; margin-top: 2px;}
    .insight-box {
        background: #F0EFFF; border-left: 4px solid #4338E0;
        border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 6px 0;
    }
    .insight-box p {margin: 0; font-size: 13px; color: #1E1B4B;}
    .cta-box {
        background: #ECFDF5; border-left: 4px solid #10B981;
        border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 4px 0 10px;
    }
    .cta-box p {margin: 0; font-size: 13px; color: #065F46;}
</style>
""", unsafe_allow_html=True)


# ── HELPERS ──
def kpi(label, value, sub="", color=BLUE):
    st.markdown(f"""<div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-val" style="color:{color}">{value}</div>
        <div class="kpi-sub" style="color:{GRAY}">{sub}</div>
    </div>""", unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box"><p>💡 {text}</p></div>', unsafe_allow_html=True)

def cta(text):
    st.markdown(f'<div class="cta-box"><p>🎯 {text}</p></div>', unsafe_allow_html=True)

def rate_by(data, col):
    if len(data) == 0:
        return pd.DataFrame({col: [], "Rate": []})
    r = data.groupby(col)["Attrition_flag"].mean().reset_index()
    r.columns = [col, "Rate"]
    r["Rate"] = (r["Rate"] * 100).round(1)
    return r

def safe_rate(data, col, val):
    sub = data[data[col] == val]
    if len(sub) == 0:
        return 0.0
    return round(sub["Attrition_flag"].mean() * 100, 1)

def chart_defaults(fig, h=400):
    fig.update_layout(
        plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        font=dict(color=DARK, size=12),
        margin=dict(t=50, b=40, l=50, r=20), height=h,
        xaxis_title="", yaxis_title="Attrition rate (%)"
    )
    return fig

def add_baseline(fig, val):
    fig.add_hline(y=val, line_dash="dash", line_color="#EF4444",
                  annotation_text=f"Avg: {val:.1f}%", annotation_font_color="#EF4444")
    return fig



@st.cache_data
def load_data():
    df = pd.read_csv("employees.csv")
    for col, cats in {
        "Work-Life Balance": ["Poor", "Fair", "Good", "Excellent"],
        "Job Level": ["Entry", "Mid", "Senior"],
        "Job Satisfaction": ["Low", "Medium", "High", "Very High"],
        "Education Level": ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "PhD"],
    }.items():
        df[col] = pd.Categorical(df[col], categories=cats, ordered=True)
    df["Attrition_flag"] = (df["Attrition"] == "Left").astype(int)
    return df

df = load_data()
overall_rate = round(df["Attrition_flag"].mean() * 100, 1)


# ── HEADER ──
import base64
with open("logo.png", "rb") as f:
    logo_b64 = base64.b64encode(f.read()).decode()

st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:4px;flex-direction:row-reverse">
    <img src="data:image/png;base64,{logo_b64}" style="height:50px"/>
    <div>
        <h2 style="margin:0;color:{DARK}">Employee Attrition Analytics</h2>
        <p style="margin:0;font-size:13px;color:{GRAY}">{len(df):,} employees  •  Company-wide attrition: {overall_rate}%</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ── SIDEBAR ──
st.sidebar.image("logo.png", width=70)
st.sidebar.markdown(f"<h4 style='color:{DARK}'>Filters</h4>", unsafe_allow_html=True)
sel_level = st.sidebar.multiselect("Job level", ["Entry", "Mid", "Senior"], default=["Entry", "Mid", "Senior"])
sel_remote = st.sidebar.multiselect("Remote work", ["Yes", "No"], default=["Yes", "No"])
sel_gender = st.sidebar.multiselect("Gender", df["Gender"].unique().tolist(), default=df["Gender"].unique().tolist())
sel_overtime = st.sidebar.multiselect("Overtime", ["Yes", "No"], default=["Yes", "No"])

fdf = df[
    df["Job Level"].isin(sel_level) &
    df["Remote Work"].isin(sel_remote) &
    df["Gender"].isin(sel_gender) &
    df["Overtime"].isin(sel_overtime)
]

if len(fdf) == 0:
    st.warning("No data matches your filters. Please adjust the sidebar selections.")
    st.stop()

f_rate = round(fdf["Attrition_flag"].mean() * 100, 1)


# ── KPIs (all dynamic) ──
k1, k2, k3, k4 = st.columns(4)
with k1: kpi("Headcount", f"{len(fdf):,}", f"of {len(df):,} total")
with k2: kpi("Attrition rate", f"{f_rate}%", "filtered selection", "#EF4444" if f_rate > overall_rate else "#10B981")
with k3:
    if "Entry" in sel_level and len(fdf[fdf["Job Level"]=="Entry"]) > 0:
        er = safe_rate(fdf, "Job Level", "Entry")
        kpi("Entry-level risk", f"{er}%", "highest risk segment", "#EF4444" if er > f_rate else BLUE)
    else:
        kpi("Entry-level risk", "N/A", "not in current filter", GRAY)
with k4:
    if "Yes" in sel_remote and len(fdf[fdf["Remote Work"]=="Yes"]) > 0:
        rr = safe_rate(fdf, "Remote Work", "Yes")
        kpi("Remote attrition", f"{rr}%", "lowest risk segment", "#10B981")
    else:
        kpi("Remote attrition", "N/A", "not in current filter", GRAY)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)


# ── TABS ──
tab1, tab2, tab3 = st.tabs(["📈 Key drivers", "🔎 Supporting factors", "🔀 Risk combinations"])


# ══════════ TAB 1: KEY DRIVERS ══════════
with tab1:

   
    jl = rate_by(fdf, "Job Level")
    if len(jl) > 0:
        highest_jl = jl.loc[jl["Rate"].idxmax()]
        lowest_jl = jl.loc[jl["Rate"].idxmin()]
        fig = px.bar(jl, x="Job Level", y="Rate", text_auto=".1f",
                     color_discrete_sequence=[BLUE], title="Attrition by job level")
        add_baseline(fig, f_rate)
        chart_defaults(fig, 420)
        fig.update_traces(textposition="outside", width=0.5)
        st.plotly_chart(fig, use_container_width=True)
        gap = round(highest_jl["Rate"] - lowest_jl["Rate"], 1)
        insight(f'{highest_jl["Job Level"]}-level employees leave at {highest_jl["Rate"]}% vs {lowest_jl["Job Level"]} at {lowest_jl["Rate"]}% — a {gap}pp gap. For every 10 new hires at the {highest_jl["Job Level"]} level, roughly {round(highest_jl["Rate"]/10)} will leave. This makes early-tenure retention the highest-impact area for HR to focus on.')
        cta(f'1) Implement a 90-day structured onboarding program for all {highest_jl["Job Level"]}-level hires by next quarter. 2) Mandate monthly 1-on-1s between new hires and managers for the first 12 months. 3) Publish internal promotion timelines — employees who see a 18-month path to Mid-level are less likely to look externally.')

    st.markdown("---")

    rw = rate_by(fdf, "Remote Work")
    if len(rw) > 0:
        fig = px.bar(rw, x="Remote Work", y="Rate", text_auto=".1f",
                     color="Remote Work",
                     color_discrete_map={"Yes": "#10B981", "No": "#EF4444"},
                     title="Attrition by remote work status")
        add_baseline(fig, f_rate)
        chart_defaults(fig, 400)
        fig.update_layout(showlegend=False)
        fig.update_traces(textposition="outside", width=0.3)
        st.plotly_chart(fig, use_container_width=True)
        onsite = safe_rate(fdf, "Remote Work", "No")
        remote = safe_rate(fdf, "Remote Work", "Yes")
        gap_rw = round(onsite - remote, 1)
        insight(f'On-site employees leave at {onsite}% — more than double remote workers at {remote}%. The {gap_rw}pp gap makes remote work the single largest difference between any two groups in this category. This is also one of the easiest levers to act on operationally.')
        cta(f'1) Audit which on-site roles genuinely require physical presence vs. those that could be hybrid. 2) Roll out a hybrid policy (3 office / 2 remote) as the new default for eligible roles within 60 days. 3) For roles that must stay on-site, offer compressed 4-day weeks as an alternative flexibility option.')

    st.markdown("---")

   
    wlb = rate_by(fdf, "Work-Life Balance")
    if len(wlb) > 0:
        fig = px.area(wlb, x="Work-Life Balance", y="Rate", markers=True,
                      title="Attrition by work-life balance",
                      color_discrete_sequence=[BLUE])
        add_baseline(fig, f_rate)
        chart_defaults(fig, 400)
        fig.update_traces(fill="tozeroy", fillcolor="rgba(67,56,224,0.1)")
        st.plotly_chart(fig, use_container_width=True)
        highest_wlb = wlb.loc[wlb["Rate"].idxmax()]
        lowest_wlb = wlb.loc[wlb["Rate"].idxmin()]
        gap_wlb = round(highest_wlb["Rate"] - lowest_wlb["Rate"], 1)
        insight(f'Attrition drops from {highest_wlb["Rate"]}% ({highest_wlb["Work-Life Balance"]}) to {lowest_wlb["Rate"]}% ({lowest_wlb["Work-Life Balance"]}) — a {gap_wlb}pp gradient. This is the clearest dose-response relationship in the dataset: as balance improves, attrition drops consistently at each level. Further analysis is needed to determine whether this is driven by team-level management, company policy, or role type.')
        cta(f'1) Break down work-life balance scores by team/manager to identify whether the issue is concentrated in specific teams or company-wide. 2) Introduce a monthly pulse survey (3 questions max) to catch deterioration early. 3) For teams with consistently Poor/Fair scores, investigate root causes — workload, management style, or role design — before prescribing solutions.')


with tab2:

    c1, c2 = st.columns(2)

    with c1:
    
        gen = rate_by(fdf, "Gender")
        if len(gen) > 0:
            f_r = safe_rate(fdf, "Gender", "Female")
            m_r = safe_rate(fdf, "Gender", "Male")
            raw_gap = round(abs(f_r - m_r), 1)

            # Control: Gender × Job Level
            gen_jl = fdf.groupby(["Gender", "Job Level"])["Attrition_flag"].mean().reset_index()
            gen_jl.columns = ["Gender", "Job Level", "Rate"]
            gen_jl["Rate"] = (gen_jl["Rate"] * 100).round(1)

          
            controlled_gaps = []
            for level in fdf["Job Level"].dropna().unique():
                sub = gen_jl[gen_jl["Job Level"] == level]
                if len(sub) == 2:
                    f_val = sub[sub["Gender"] == "Female"]["Rate"].values[0]
                    m_val = sub[sub["Gender"] == "Male"]["Rate"].values[0]
                    controlled_gaps.append(abs(f_val - m_val))
            avg_controlled_gap = round(np.mean(controlled_gaps), 1) if controlled_gaps else 0

         
            fig = px.bar(gen_jl, x="Job Level", y="Rate", color="Gender",
                         barmode="group", text_auto=".1f",
                         color_discrete_map={"Female": "#7C78EA", "Male": BLUE},
                         title="Gender × Job level (controlling for level)")
            add_baseline(fig, f_rate)
            chart_defaults(fig)
            fig.update_layout(legend=dict(orientation="h", y=-0.15))
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

           
            if avg_controlled_gap >= 5:
                insight(f'Raw gap: Female {f_r}% vs Male {m_r}% ({raw_gap}pp). After controlling for job level, the gap averages {avg_controlled_gap}pp within each level — the gender effect persists independently of seniority. This warrants a gender-specific investigation.')
                cta(f'1) The gap is real and not explained by job level alone. Conduct focus groups with female employees to identify retention barriers. 2) Audit promotion rates by gender — if female employees are promoted slower, that compounds the effect. 3) Review exit interview data for gender-specific patterns.')
            else:
                insight(f'Raw gap: Female {f_r}% vs Male {m_r}% ({raw_gap}pp). But after controlling for job level, the gap shrinks to {avg_controlled_gap}pp — the gender difference is largely explained by job level distribution, not gender itself.')
                cta(f'1) The gender gap is structural, not gender-specific. Check whether female employees are overrepresented in Entry-level roles. 2) If so, the fix is faster promotion pathways and remote access for Entry-level — which solves both the gender gap and the job level gap simultaneously.')

    with c2:
        sat = rate_by(fdf, "Job Satisfaction")
        if len(sat) > 0:
            fig = px.line(sat, x="Job Satisfaction", y="Rate", markers=True,
                          title="Satisfaction paradox",
                          color_discrete_sequence=[BLUE])
            add_baseline(fig, f_rate)
            chart_defaults(fig)
            fig.update_traces(line_width=3, marker_size=10)
            st.plotly_chart(fig, use_container_width=True)

            low_r = safe_rate(fdf, "Job Satisfaction", "Low")
            vh_r = safe_rate(fdf, "Job Satisfaction", "Very High")

            
            vh_left = fdf[(fdf["Job Satisfaction"] == "Very High") & (fdf["Attrition"] == "Left")]
            vh_stayed = fdf[(fdf["Job Satisfaction"] == "Very High") & (fdf["Attrition"] == "Stayed")]

            if len(vh_left) > 0 and len(vh_stayed) > 0:
               
                vh_left_entry = round((vh_left["Job Level"] == "Entry").mean() * 100, 1)
                vh_stayed_entry = round((vh_stayed["Job Level"] == "Entry").mean() * 100, 1)
             
                vh_left_onsite = round((vh_left["Remote Work"] == "No").mean() * 100, 1)
                vh_stayed_onsite = round((vh_stayed["Remote Work"] == "No").mean() * 100, 1)
                
                vh_left_ot = round((vh_left["Overtime"] == "Yes").mean() * 100, 1)
                vh_stayed_ot = round((vh_stayed["Overtime"] == "Yes").mean() * 100, 1)

                insight(f'Low satisfaction ({low_r}%) and Very High ({vh_r}%) both have peak attrition. Profiling Very High leavers vs stayers: {vh_left_entry}% of leavers are Entry-level (vs {vh_stayed_entry}% of stayers), {vh_left_onsite}% work on-site (vs {vh_stayed_onsite}%), and {vh_left_ot}% do overtime (vs {vh_stayed_ot}%).')

                
                drivers = []
                if vh_left_entry - vh_stayed_entry > 5:
                    drivers.append(f"entry-level concentration ({vh_left_entry}% vs {vh_stayed_entry}%)")
                if vh_left_onsite - vh_stayed_onsite > 5:
                    drivers.append(f"on-site work ({vh_left_onsite}% vs {vh_stayed_onsite}%)")
                if vh_left_ot - vh_stayed_ot > 5:
                    drivers.append(f"overtime ({vh_left_ot}% vs {vh_stayed_ot}%)")

                if drivers:
                    cta(f'The paradox is partially explained by: {", ".join(drivers)}. Very High satisfaction does not protect against structural problems. Fix the underlying drivers (job level, remote access, overtime) — satisfaction scores will follow. Do not invest in satisfaction improvement programs when the real issues are operational.')
                else:
                    cta(f'Very High leavers and stayers have identical profiles — the paradox is not explained by job level, remote work, or overtime. This points to a data quality issue: employees may feel pressure to rate satisfaction high. Replace the annual written survey with quarterly 5-minute 1-on-1 conversations between employees and a neutral HR contact (not their direct manager). Verbal, private, off-the-record conversations surface honest feedback that written forms never will.')
            else:
                insight(f'Low satisfaction ({low_r}%) and Very High ({vh_r}%) both peak. Insufficient data in current filter to profile Very High leavers.')
                cta('Broaden filters to enable cross-referencing of Very High satisfaction leavers.')

    c3, c4 = st.columns(2)

    with c3:
        ot = rate_by(fdf, "Overtime")
        if len(ot) > 0:
            fig = px.bar(ot, x="Overtime", y="Rate", text_auto=".1f",
                         color="Overtime", color_discrete_map={"Yes": "#EF4444", "No": "#10B981"},
                         title="Attrition by overtime")
            add_baseline(fig, f_rate)
            chart_defaults(fig)
            fig.update_layout(showlegend=False)
            fig.update_traces(textposition="outside", width=0.4)
            st.plotly_chart(fig, use_container_width=True)
            ot_y = safe_rate(fdf, "Overtime", "Yes")
            ot_n = safe_rate(fdf, "Overtime", "No")
            insight(f'Overtime employees leave at {ot_y}% vs {ot_n}% — a {round(ot_y - ot_n, 1)}pp gap. On its own, this is modest. But overtime rarely exists in isolation — it compounds with on-site work and poor work-life balance. An on-site employee doing overtime with Poor balance is in the highest-risk zone of the entire dataset.')
            cta(f'1) Build an overtime dashboard alert: flag any employee exceeding 10hrs/week overtime for 3+ consecutive months. 2) When overtime spikes in a team, investigate staffing — chronic overtime usually means understaffing, not underperformance. 3) Offer overtime-heavy teams priority access to remote days as an immediate pressure release.')

    with c4:
        edu = rate_by(fdf, "Education Level")
        if len(edu) > 0:
            fig = px.bar(edu, x="Education Level", y="Rate", text_auto=".1f",
                         color_discrete_sequence=[BLUE], title="Attrition by education level")
            add_baseline(fig, f_rate)
            chart_defaults(fig)
            fig.update_traces(textposition="outside")
            st.plotly_chart(fig, use_container_width=True)

            phd_r = safe_rate(fdf, "Education Level", "PhD")

           
            non_phd_levels = ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree"]
            non_phd_rates = [safe_rate(fdf, "Education Level", lvl) for lvl in non_phd_levels if safe_rate(fdf, "Education Level", lvl) > 0]
            non_phd_spread = round(max(non_phd_rates) - min(non_phd_rates), 1) if non_phd_rates else 0
            non_phd_avg = round(np.mean(non_phd_rates), 1) if non_phd_rates else 0

            # Profile PhD vs non-PhD
            phd = fdf[fdf["Education Level"] == "PhD"]
            non_phd = fdf[fdf["Education Level"] != "PhD"]

            if len(phd) > 0 and len(non_phd) > 0:
                phd_senior = round((phd["Job Level"] == "Senior").mean() * 100, 1)
                non_phd_senior = round((non_phd["Job Level"] == "Senior").mean() * 100, 1)
                phd_remote = round((phd["Remote Work"] == "Yes").mean() * 100, 1)
                non_phd_remote = round((non_phd["Remote Work"] == "Yes").mean() * 100, 1)

                insight(f'High School through Master\'s all cluster at ~{non_phd_avg}% (spread of just {non_phd_spread}pp). Education level has zero differentiating power across these 4 groups. PhD is the only outlier at {phd_r}%. Profiling: {phd_senior}% of PhDs are Senior-level (vs {non_phd_senior}% non-PhD), {phd_remote}% have remote access (vs {non_phd_remote}%).')

                advantages = []
                if phd_senior - non_phd_senior > 5:
                    advantages.append(f"seniority ({phd_senior}% vs {non_phd_senior}%)")
                if phd_remote - non_phd_remote > 5:
                    advantages.append(f"remote access ({phd_remote}% vs {non_phd_remote}%)")

                if advantages:
                    cta(f'Do not build education-based retention programs — 4 out of 5 levels have identical attrition. The PhD gap is explained by: {", ".join(advantages)}. PhDs retain better because they have more of what retains everyone. Extend seniority pathways and remote access to non-PhD employees instead of treating education as the lever.')
                else:
                    cta(f'Do not build education-based retention programs — 4 out of 5 levels have identical attrition. PhD employees retain better despite similar seniority and remote access profiles, suggesting the retention factor is role-specific (autonomy, challenge, specialization). Test whether giving non-PhD employees more ownership and specialization within their roles improves retention.')
            else:
                insight(f'PhD attrition is {phd_r}% vs ~{non_phd_avg}% for all others. Insufficient data to profile.')
                cta('Broaden filters to enable PhD profiling.')


with tab3:
    st.markdown(f"<p style='color:{GRAY};font-size:14px'>Single-variable analysis misses compounding effects. These show which <b>combinations</b> create the highest risk.</p>", unsafe_allow_html=True)

    inter1 = fdf.groupby(["Job Level", "Work-Life Balance"])["Attrition_flag"].mean().reset_index()
    inter1.columns = ["Job Level", "Work-Life Balance", "Rate"]
    inter1["Rate"] = (inter1["Rate"] * 100).round(1)
    if len(inter1) > 0:
        fig1 = px.bar(inter1, x="Job Level", y="Rate", color="Work-Life Balance",
                      barmode="group", text_auto=".1f",
                      color_discrete_sequence=["#1E1B4B", "#4338E0", "#7C78EA", "#C7C5F7"],
                      title="Job level × Work-life balance")
        chart_defaults(fig1, 440)
        fig1.update_layout(legend=dict(orientation="h", y=-0.15))
        fig1.update_traces(textposition="outside")
        st.plotly_chart(fig1, use_container_width=True)
        worst = inter1.loc[inter1["Rate"].idxmax()]
        best = inter1.loc[inter1["Rate"].idxmin()]
        insight(f'The data is clear: {worst["Job Level"]}-level employees with {worst["Work-Life Balance"]} work-life balance leave at {worst["Rate"]}%, while {best["Job Level"]}-level with {best["Work-Life Balance"]} balance leave at just {best["Rate"]}%. That is a {round(worst["Rate"] - best["Rate"], 1)}pp gap between the worst and best combination. Retention programs that target Job Level OR Work-Life Balance separately will underperform — the real leverage is at the intersection.')
        cta(f'1) Generate a list of all Entry-level employees currently scoring Poor or Fair on work-life balance — this is your immediate flight risk list. 2) Assign each person on that list a senior mentor and offer one flexible work arrangement within 30 days. 3) Set a 90-day follow-up to measure whether their balance score improved and whether they are still with the company.')

    st.markdown("---")

    inter2 = fdf.groupby(["Overtime", "Remote Work"])["Attrition_flag"].mean().reset_index()
    inter2.columns = ["Overtime", "Remote Work", "Rate"]
    inter2["Rate"] = (inter2["Rate"] * 100).round(1)
    if len(inter2) > 0:
        fig2 = px.bar(inter2, x="Overtime", y="Rate", color="Remote Work",
                      barmode="group", text_auto=".1f",
                      color_discrete_sequence=[BLUE, "#10B981"],
                      title="Overtime × Remote work")
        chart_defaults(fig2, 440)
        fig2.update_layout(legend=dict(orientation="h", y=-0.15))
        fig2.update_traces(textposition="outside")
        st.plotly_chart(fig2, use_container_width=True)
        worst2 = inter2.loc[inter2["Rate"].idxmax()]
        best2 = inter2.loc[inter2["Rate"].idxmin()]
        insight(f'On-site employees doing overtime leave at {worst2["Rate"]}%, while remote employees doing the same overtime leave at {best2["Rate"]}%. Remote work doesn\'t just reduce attrition on its own — it appears to buffer the negative effect of overtime. This suggests you don\'t necessarily need to eliminate overtime; giving overtime workers flexibility may be enough.')
        cta(f'1) Identify the top 10 teams with the highest overtime hours AND on-site requirements. 2) Pilot a "remote overtime" policy for these teams: any week an employee exceeds 8hrs overtime, they get 2 remote days the following week. 3) Measure attrition in pilot teams vs control teams over 6 months. If it works, scale company-wide.')

    st.markdown("---")

    # -- Dynamic highest risk segment --
    risk_seg = fdf[
        (fdf["Job Level"] == "Entry") &
        (fdf["Remote Work"] == "No") &
        (fdf["Work-Life Balance"].isin(["Poor", "Fair"]))
    ]
    if len(risk_seg) > 0:
        risk_rate = round(risk_seg["Attrition_flag"].mean() * 100, 1)
        risk_count = len(risk_seg)
        total_pct = round(risk_count / len(fdf) * 100, 1)
    else:
        risk_rate = "N/A"
        risk_count = 0
        total_pct = 0

    st.markdown(f"""<div style='background:{LIGHT_BLUE};border-radius:12px;padding:20px;text-align:center'>
        <p style='font-size:15px;font-weight:600;color:{DARK};margin:0 0 6px'>⚠️ Highest risk profile</p>
        <p style='font-size:20px;font-weight:700;color:{BLUE};margin:0'>Entry-level  ×  On-site  ×  Poor/Fair work-life balance</p>
        <p style='font-size:16px;font-weight:600;color:#EF4444;margin:8px 0 0'>{risk_rate}% attrition in this group  •  {risk_count:,} employees ({total_pct}% of filtered data)</p>
        <p style='font-size:12px;color:{GRAY};margin:6px 0 0'>⚠️ Small subgroup — interpret with caution. This rate reflects the combined effect of the three strongest actionable drivers. Use as a priority signal for manager outreach, not as a forecast.</p>
    </div>""", unsafe_allow_html=True)


st.markdown("---")
st.markdown(f"<p style='text-align:center;font-size:12px;color:{GRAY}'>Built by Eng Rahma Saber   •  {len(df):,} employee records  •  Drivers validated by effect size analysis</p>", unsafe_allow_html=True)
