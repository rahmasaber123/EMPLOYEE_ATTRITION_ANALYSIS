import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import base64

st.set_page_config(page_title="Kayfa HR Analytics", page_icon="favicon.png", layout="wide")

# ── THEME-AWARE HELPERS ──
PRIMARY = "#4338E0"
GREEN = "#10B981"
RED = "#EF4444"

st.markdown("""
<style>
    .insight-card {
        border-left: 4px solid #4338E0;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin: 8px 0;
        background: rgba(67, 56, 224, 0.06);
    }
    .insight-card p { margin: 0; font-size: 14px; line-height: 1.6; }
    .cta-card {
        border-left: 4px solid #10B981;
        border-radius: 0 10px 10px 0;
        padding: 14px 18px;
        margin: 4px 0 16px;
        background: rgba(16, 185, 129, 0.06);
    }
    .cta-card p { margin: 0; font-size: 14px; line-height: 1.6; }
    .metric-card {
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid rgba(0,0,0,0.08);
    }
    .metric-val { font-size: 28px; font-weight: 700; margin: 4px 0; }
    .metric-label { font-size: 12px; opacity: 0.6; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

def get_logo_b64():
    with open("logo.png", "rb") as f:
        return base64.b64encode(f.read()).decode()

def insight(text):
    st.markdown(f'<div class="insight-card"><p>💡 <strong>Insight:</strong> {text}</p></div>', unsafe_allow_html=True)

def cta(text):
    st.markdown(f'<div class="cta-card"><p>🎯 <strong>Recommended action:</strong> {text}</p></div>', unsafe_allow_html=True)

def rate_by(data, col):
    if len(data) == 0: return pd.DataFrame({col: [], "Attrition Rate (%)": []})
    r = data.groupby(col)["Attrition_flag"].mean().reset_index()
    r.columns = [col, "Attrition Rate (%)"]
    r["Attrition Rate (%)"] = (r["Attrition Rate (%)"] * 100).round(1)
    return r

def safe_rate(data, col, val):
    sub = data[data[col] == val]
    return round(sub["Attrition_flag"].mean() * 100, 1) if len(sub) > 0 else 0.0

def add_baseline_trace(fig, baseline, x_range):
    fig.add_trace(go.Scatter(
        x=x_range, y=[baseline]*len(x_range),
        mode="lines", name=f"Company average ({baseline:.1f}%)",
        line=dict(dash="dash", color="red", width=2),
        showlegend=True
    ))

def show(fig):
    st.plotly_chart(fig, use_container_width=True, theme="streamlit")

# ── DATA ──
@st.cache_data
def load_data():
    df = pd.read_csv("employees.csv")
    ordinals = {
        "Work-Life Balance": ["Poor", "Fair", "Good", "Excellent"],
        "Job Level": ["Entry", "Mid", "Senior"],
        "Job Satisfaction": ["Low", "Medium", "High", "Very High"],
        "Education Level": ["High School", "Associate Degree", "Bachelor's Degree", "Master's Degree", "PhD"],
        "Performance Rating": ["Low", "Below Average", "Average", "High"],
        "Company Reputation": ["Poor", "Fair", "Good"],
        "Company Size": ["Small", "Medium", "Large"],
    }
    for col, cats in ordinals.items():
        if col in df.columns:
            df[col] = pd.Categorical(df[col], categories=cats, ordered=True)
    df["Attrition_flag"] = (df["Attrition"] == "Left").astype(int)
    return df

df = load_data()
baseline = round(df["Attrition_flag"].mean() * 100, 1)


# ══════════════════════════════════════
# PAGES
# ══════════════════════════════════════

def page_home():
    logo_b64 = get_logo_b64()
    st.markdown(f"""
    <div style="text-align:center;padding:40px 0 20px">
        <img src="data:image/png;base64,{logo_b64}" style="height:80px;margin-bottom:16px"/>
        <h1 style="margin:0">Week #1 Task:</h1>
        <h2 style="margin:0;color:{PRIMARY}">Employee Attrition Intelligence Dashboard</h2>
        <p style="margin-top:12px;font-size:16px;opacity:0.7">{len(df):,} employees analysed</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    left_count = df["Attrition_flag"].sum()
    stayed_count = len(df) - left_count

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Total employees</div>
            <div class="metric-val" style="color:{PRIMARY}">{len(df):,}</div>
        </div>''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Overall attrition</div>
            <div class="metric-val" style="color:{RED}">{baseline}%</div>
        </div>''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Employees lost</div>
            <div class="metric-val" style="color:{RED}">{left_count:,}</div>
        </div>''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''<div class="metric-card">
            <div class="metric-label">Employees retained</div>
            <div class="metric-val" style="color:{GREEN}">{stayed_count:,}</div>
        </div>''', unsafe_allow_html=True)

    st.divider()


def page_foundations():
    tab1, tab2, tab3 = st.tabs(["The headline", "Overtime", "Remote work"])

    # ── Q1 ──
    with tab1:
        st.subheader("What share of employees left, and which role loses the most?")

        left_count = df["Attrition_flag"].sum()
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">Overall attrition</div>
                <div class="metric-val" style="color:{RED}">{baseline}%</div>
            </div>''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">Employees lost</div>
                <div class="metric-val" style="color:{RED}">{left_count:,}</div>
            </div>''', unsafe_allow_html=True)
        with c3:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">Total headcount</div>
                <div class="metric-val" style="color:{PRIMARY}">{len(df):,}</div>
            </div>''', unsafe_allow_html=True)
        
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

        jr = rate_by(df, "Job Role")
        fig = px.bar(jr.sort_values("Attrition Rate (%)"),
                     x="Attrition Rate (%)", y="Job Role", orientation="h",
                     text_auto=".1f",
                     title="Attrition rate by job role — which function leaks most?")
        fig.update_traces(marker_color=PRIMARY)
        add_baseline_trace(fig, baseline, [jr["Attrition Rate (%)"].min()-2, jr["Attrition Rate (%)"].max()+2])
        fig.update_layout(yaxis_title="", xaxis_title="Attrition Rate (%)", height=400)
        show(fig)

        highest = jr.loc[jr["Attrition Rate (%)"].idxmax()]
        lowest = jr.loc[jr["Attrition Rate (%)"].idxmin()]
        spread = round(highest["Attrition Rate (%)"] - lowest["Attrition Rate (%)"], 1)

        insight(f'The spread between the highest ({highest["Job Role"]} at {highest["Attrition Rate (%)"]:.1f}%) and lowest ({lowest["Job Role"]} at {lowest["Attrition Rate (%)"]:.1f}%) role is only {spread}pp. Attrition is a company-wide problem, not a departmental one — no single role is an outlier.')
        cta(f'Do not launch role-specific retention programs. The {spread}pp spread does not justify targeting one department over another. Instead, focus retention budget on the cross-cutting drivers identified in later sections (job level, remote work, work-life balance).')

    # ── Q2 ──
    with tab2:
        st.subheader("Are overtime employees more likely to leave?")

        ot = rate_by(df, "Overtime")
        fig = px.bar(ot, x="Overtime", y="Attrition Rate (%)", color="Overtime",
                     text_auto=".1f",
                     title="Attrition rate by overtime status",
                     color_discrete_map={"Yes": "#EF4444", "No": "#22C55E"})
        add_baseline_trace(fig, baseline, ot["Overtime"].tolist())
        fig.update_layout(xaxis_title="", height=400, showlegend=True)
        fig.update_traces(width=0.4, selector=dict(type="bar"))
        show(fig)

        ot_y = safe_rate(df, "Overtime", "Yes")
        ot_n = safe_rate(df, "Overtime", "No")
        gap = round(ot_y - ot_n, 1)
        ot_count = len(df[df["Overtime"]=="Yes"])
        ot_pct = round(ot_count / len(df) * 100, 1)

        insight(f'Overtime employees leave at {ot_y}% vs {ot_n}% — a {gap}pp increase. {ot_count:,} employees ({ot_pct}%) currently work overtime. While the gap is modest alone, overtime compounds with other risk factors (on-site work, poor balance) as shown in later sections.')
        cta(f'1) Flag employees exceeding 10+ overtime hours/week for 3 consecutive months. 2) When overtime spikes in a team, investigate staffing levels — chronic overtime usually signals understaffing. 3) Offer overtime-heavy teams priority access to remote days as an immediate pressure release.')

    # ── Q3 ──
    with tab3:
        st.subheader("Does remote work keep people?")

        rw = rate_by(df, "Remote Work")
        remote_count = len(df[df["Remote Work"]=="Yes"])
        remote_pct = round(remote_count / len(df) * 100, 1)

        fig = px.bar(rw, x="Remote Work", y="Attrition Rate (%)", color="Remote Work",
                     text_auto=".1f",
                     title="Attrition rate by remote work status",
                     color_discrete_map={"Yes": "#22C55E", "No": "#EF4444"})
        add_baseline_trace(fig, baseline, rw["Remote Work"].tolist())
        fig.update_layout(xaxis_title="", height=400)
        fig.update_traces(width=0.4, selector=dict(type="bar"))
        show(fig)

        onsite = safe_rate(df, "Remote Work", "No")
        remote = safe_rate(df, "Remote Work", "Yes")
        gap_rw = round(onsite - remote, 1)

        insight(f'On-site employees leave at {onsite}% vs {remote}% for remote workers — a {gap_rw}pp gap. However, only {remote_count:,} employees ({remote_pct}%) currently work remotely. The effect size is large, but the small sample limits confidence. We cannot conclude that moving everyone remote would halve attrition — self-selection bias is likely (remote-eligible roles may differ structurally).')
        cta(f'1) Audit which on-site roles could realistically support hybrid work. 2) Pilot a hybrid policy (3 office / 2 remote) in 2-3 high-attrition teams and measure retention over 6 months before scaling. 3) For must-be-on-site roles, offer compressed workweeks as an alternative flexibility option.')


def page_comparison():
    tab1, tab2, tab3, tab4 = st.tabs(["Pay fairness", "Retention timeline",
                                       "Engagement warning signs", "Life stage"])

    # ── Q4 ──
    with tab1:
        st.subheader("Within the same job level, does pay affect attrition?")

        df["Income Quartile"] = pd.qcut(df["Monthly Income"], q=4,
            labels=["Low Pay", "Lower-Mid Pay", "Upper-Mid Pay", "High Pay"])

        pay = df.groupby(["Job Level", "Income Quartile"])["Attrition_flag"].mean().reset_index()
        pay.columns = ["Job Level", "Income Quartile", "Attrition Rate (%)"]
        pay["Attrition Rate (%)"] = (pay["Attrition Rate (%)"] * 100).round(1)

        fig = px.line(pay, x="Income Quartile", y="Attrition Rate (%)", color="Job Level",
                      markers=True,
                      title="Attrition across pay quartiles within each job level — does more pay help?",
                      color_discrete_sequence=[PRIMARY, "#7C78EA", "#C7C5F7"])
        add_baseline_trace(fig, baseline, pay["Income Quartile"].unique().tolist())
        fig.update_layout(xaxis_title="Pay quartile (within company)", yaxis_title="Attrition Rate (%)", height=420)
        show(fig)

        # Compute flatness
        spreads = []
        for level in df["Job Level"].cat.categories:
            sub = pay[pay["Job Level"]==level]
            if len(sub) > 1:
                spreads.append({"Level": level, "Spread": round(sub["Attrition Rate (%)"].max() - sub["Attrition Rate (%)"].min(), 1)})
        spread_df = pd.DataFrame(spreads)
        max_spread = spread_df["Spread"].max()

        insight(f'The lines are nearly flat. Within each job level, the gap between lowest and highest paid employees is at most {max_spread}pp. Entry-level attrition stays around 62-65% regardless of pay. Mid-level stays around 45-46%. Senior stays around 19-21%. Job level drives attrition — pay does not.')
        cta(f'1) Do not use across-the-board salary increases as a retention tool — the data shows they will not reduce attrition. 2) Review pay bands for external competitiveness, but allocate retention budget toward career progression, mentorship, and remote access instead. 3) If Entry-level employees earn below market, fix that for fairness — but do not expect it to move the attrition needle.')

    # ── Q5 ──
    with tab2:
        st.subheader("At what tenure stage is attrition highest?")

        df["Tenure Stage"] = pd.cut(df["Years at Company"],
            bins=[0, 1, 3, 5, 10, 20, 50],
            labels=["< 1 Year", "1–3 Years", "3–5 Years", "5–10 Years", "10–20 Years", "20+ Years"],
            include_lowest=True)

        tenure = rate_by(df, "Tenure Stage")
        fig = px.line(tenure, x="Tenure Stage", y="Attrition Rate (%)", markers=True,
                      title="Attrition rate across employee tenure — when do people leave?")
        fig.update_traces(line_color=PRIMARY, line_width=3, marker_size=10)
        add_baseline_trace(fig, baseline, tenure["Tenure Stage"].tolist())
        fig.update_layout(xaxis_title="Time at company", yaxis_title="Attrition Rate (%)", height=420)
        show(fig)

        peak = tenure.loc[tenure["Attrition Rate (%)"].idxmax()]
        lowest = tenure.loc[tenure["Attrition Rate (%)"].idxmin()]

        insight(f'Attrition peaks during the {peak["Tenure Stage"]} stage at {peak["Attrition Rate (%)"]:.1f}%, then drops to {lowest["Attrition Rate (%)"]:.1f}% for {lowest["Tenure Stage"]} employees. The biggest retention challenge is not onboarding — it is employees in the mid-career window who may start questioning their growth trajectory around year 3-5.')
        cta(f'1) Launch a mid-career retention program targeting employees approaching their 3rd year — before they hit the peak risk zone. 2) Require career development discussions and promotion reviews before the 3-year mark. 3) Offer leadership tracks, skill certifications, or cross-functional projects as re-engagement hooks at the 2.5-year mark.')

    # ── Q6 ──
    with tab3:
        st.subheader("Which satisfaction × balance combination is the strongest warning sign?")

        df["Engagement Profile"] = df["Job Satisfaction"].astype(str) + " satisfaction + " + df["Work-Life Balance"].astype(str) + " balance"
        eng = rate_by(df, "Engagement Profile").sort_values("Attrition Rate (%)", ascending=False)

        fig = px.bar(eng.head(8), x="Attrition Rate (%)", y="Engagement Profile", orientation="h",
                     text_auto=".1f",
                     title="Top 8 highest-risk engagement profiles — satisfaction × work-life balance")
        fig.update_traces(marker_color=PRIMARY)
        add_baseline_trace(fig, baseline,
                          [eng["Attrition Rate (%)"].min()-5, eng["Attrition Rate (%)"].max()+5])
        fig.update_layout(yaxis_title="", xaxis_title="Attrition Rate (%)", height=450)
        show(fig)

        worst = eng.iloc[0]
        second = eng.iloc[1]

        # Check if WLB dominates
        poor_wlb_avg = rate_by(df, "Work-Life Balance")
        poor_rate = safe_rate(df, "Work-Life Balance", "Poor")

        insight(f'The highest-risk profile is "{worst["Engagement Profile"]}" at {worst["Attrition Rate (%)"]:.1f}%, followed by "{second["Engagement Profile"]}" at {second["Attrition Rate (%)"]:.1f}%. Notice that Poor balance appears in both top slots regardless of satisfaction level. Work-life balance is the dominant signal — even "Very High" satisfaction does not protect against poor balance.')
        cta(f'1) Flag any employee reporting Poor work-life balance as at-risk, regardless of their satisfaction score — satisfaction surveys alone miss these people. 2) Require managers to hold a follow-up conversation within 2 weeks when an employee reports Poor or Fair balance for two consecutive periods. 3) Monitor workload and overtime for flagged employees before attrition occurs.')

    # ── Q7 ──
    with tab4:
        st.subheader("Does life stage predict who leaves?")

        df["Age Group"] = pd.cut(df["Age"], bins=[18, 25, 35, 45, 60],
            labels=["18–25", "26–35", "36–45", "46–60"])
        df["Dependent Group"] = pd.cut(df["Number of Dependents"], bins=[-1, 0, 2, 10],
            labels=["None", "1–2", "3+"])

        df_clean = df.dropna(subset=["Age Group", "Dependent Group"])
        df_clean["Life Stage"] = (df_clean["Age Group"].astype(str) + " | "
                                  + df_clean["Marital Status"] + " | "
                                  + df_clean["Dependent Group"].astype(str))

        life = rate_by(df_clean, "Life Stage").sort_values("Attrition Rate (%)", ascending=False)
        life_counts = df_clean.groupby("Life Stage").size().reset_index(name="Count")
        life = life.merge(life_counts, on="Life Stage")
        life = life[life["Count"] >= 50]  # filter small groups

        fig = px.bar(life.head(10), x="Attrition Rate (%)", y="Life Stage", orientation="h",
                     text_auto=".1f",
                     title="Top 10 highest-risk life-stage profiles (min 50 employees)")
        fig.update_traces(marker_color=PRIMARY)
        add_baseline_trace(fig, baseline,
                          [life["Attrition Rate (%)"].min()-5, life["Attrition Rate (%)"].max()+5])
        fig.update_layout(yaxis_title="", xaxis_title="Attrition Rate (%)", height=480)
        show(fig)

        worst_ls = life.iloc[0]
        above_baseline = round(worst_ls["Attrition Rate (%)"] - baseline, 1)

        insight(f'The highest-risk life stage is "{worst_ls["Life Stage"]}" at {worst_ls["Attrition Rate (%)"]:.1f}% — {above_baseline}pp above the company average. Young, single employees with few dependents have the fewest personal anchors and the most career mobility. They are the easiest to lose and the hardest to retain through compensation alone.')
        cta(f'1) Create a retention program for employees aged 18–35 who are single — focused on career acceleration, not benefits they do not value yet. 2) Offer fast-track certifications, mentorship pairings, and visible promotion timelines within the first 2 years. 3) Conduct stay-interviews with high-performing young employees every 6 months to surface flight risk early.')


def page_synthesis():
    tab1, tab2, tab3 = st.tabs(["Career stagnation", "Highest-risk profile",
                                 "What moves the needle"])

    # ── Q8 ──
    with tab1:
        st.subheader("Does feeling 'stuck' line up with leaving?")

        df["Job Level Score"] = df["Job Level"].map({"Entry": 1, "Mid": 2, "Senior": 3}).astype(int)
        df["Leadership Score"] = df["Leadership Opportunities"].map({"No": 0, "Yes": 1}).astype(int)
        innovation_col = "Innovation Opportunities"
        df["Innovation Score"] = df[innovation_col].map({"No": 0, "Yes": 1}).astype(int) if innovation_col in df.columns else 0
        df["Growth Score"] = df["Number of Promotions"] + df["Job Level Score"] + df["Leadership Score"] + df["Innovation Score"]

        growth = rate_by(df, "Growth Score")
        fig = px.line(growth, x="Growth Score", y="Attrition Rate (%)", markers=True,
                      title="Attrition by career growth score — does opportunity retain people?")
        fig.update_traces(line_color=PRIMARY, line_width=3, marker_size=8)
        add_baseline_trace(fig, baseline, growth["Growth Score"].tolist())
        fig.update_layout(xaxis_title="Growth score (promotions + level + leadership + innovation)",
                         yaxis_title="Attrition Rate (%)", height=420)
        show(fig)

        low_growth = growth[growth["Growth Score"] <= 2]["Attrition Rate (%)"].mean()
        high_growth = growth[growth["Growth Score"] >= 5]["Attrition Rate (%)"].mean()
        gap = round(low_growth - high_growth, 1)

        insight(f'The relationship is nearly linear: employees with a growth score of 2 or below average {low_growth:.1f}% attrition, while those scoring 5+ average {high_growth:.1f}% — a {gap}pp gap. Promotions, seniority, and access to leadership/innovation opportunities all compound. Employees who feel stuck leave; employees who see growth stay.')
        cta(f'1) Establish a formal internal mobility program — employees can apply for new roles or projects after 12 months. 2) Require managers to create documented career development plans for all Entry and Mid-level employees. 3) Set a KPI: every employee should receive at least one growth opportunity (promotion, certification, leadership assignment, or cross-functional project) within 18 months.')

    # ── Q9 ──
    with tab2:
        st.subheader("What is the single highest-risk employee profile?")

        risk = df.groupby(["Job Level", "Remote Work", "Work-Life Balance"]).agg(
            Employees=("Attrition_flag", "count"),
            Attrition_Rate=("Attrition_flag", "mean")
        ).reset_index()
        risk["Attrition_Rate"] = (risk["Attrition_Rate"] * 100).round(1)
        risk["Profile"] = (risk["Job Level"].astype(str) + " | "
                          + risk["Remote Work"] + " | "
                          + risk["Work-Life Balance"].astype(str))
        risk = risk[risk["Employees"] >= 100].sort_values("Attrition_Rate", ascending=False)

        fig = px.bar(risk.head(10), x="Attrition_Rate", y="Profile", orientation="h",
                     text=risk.head(10).apply(lambda r: f'{r["Attrition_Rate"]:.1f}% ({r["Employees"]:,} emp)', axis=1),
                     title="Top 10 highest-risk profiles (min 100 employees) — attrition rate + headcount")
        fig.update_traces(marker_color=PRIMARY, textposition="outside")
        add_baseline_trace(fig, baseline, [0, risk["Attrition_Rate"].max()+10])
        fig.update_layout(yaxis_title="", xaxis_title="Attrition Rate (%)", height=480)
        show(fig)

        worst = risk.iloc[0]
        above = round(worst["Attrition_Rate"] - baseline, 1)

        insight(f'The highest-risk profile is **{worst["Profile"]}** at {worst["Attrition_Rate"]:.1f}% attrition — {above}pp above the company average of {baseline}%. This is not a niche group: {worst["Employees"]:,} employees match this profile. The pattern combines the three strongest independent drivers: job level, remote work access, and work-life balance.')
        cta(f'1) Generate a list of all employees matching this profile — {worst["Employees"]:,} people who are immediate flight risks. 2) Within 30 days, provide each with at least one intervention: hybrid eligibility, flexible scheduling, or reduced overtime targets. 3) Assign a mentor and conduct monthly check-ins for 6 months. Measure whether attrition in this group drops below {baseline}% as the success threshold.')

    # ── Q10 ──
    with tab3:
        st.subheader("If HR could fix one thing next quarter, what should it be?")

        drivers = {
            "Job Level": rate_by(df, "Job Level"),
            "Remote Work": rate_by(df, "Remote Work"),
            "Work-Life Balance": rate_by(df, "Work-Life Balance"),
            "Overtime": rate_by(df, "Overtime"),
        }
        if "Company Reputation" in df.columns:
            drivers["Company Reputation"] = rate_by(df, "Company Reputation")
        if "Employee Recognition" in df.columns:
            drivers["Employee Recognition"] = rate_by(df, "Employee Recognition")

        ranking = []
        for name, table in drivers.items():
            max_shift = abs(table["Attrition Rate (%)"] - baseline).max()
            ranking.append({"Driver": name, "Max shift from baseline (pp)": round(max_shift, 1)})
        ranking = pd.DataFrame(ranking).sort_values("Max shift from baseline (pp)", ascending=False)

        fig = px.bar(ranking, x="Max shift from baseline (pp)", y="Driver", orientation="h",
                     text_auto=".1f",
                     title="Which driver moves attrition the most? — maximum deviation from company average")
        fig.update_traces(marker_color=PRIMARY)
        fig.update_layout(yaxis_title="", xaxis_title="Percentage points from baseline", height=400)
        show(fig)

        top3 = ranking.head(3)
        r1 = top3.iloc[0]
        r2 = top3.iloc[1]
        r3 = top3.iloc[2]

        st.markdown("### Top 3 drivers ranked by impact")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">🥇 {r1['Driver']}</div>
                <div class="metric-val" style="color:{RED}">{r1['Max shift from baseline (pp)']}pp</div>
            </div>''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">🥈 {r2['Driver']}</div>
                <div class="metric-val" style="color:{PRIMARY}">{r2['Max shift from baseline (pp)']}pp</div>
            </div>''', unsafe_allow_html=True)
        with c3:
            st.markdown(f'''<div class="metric-card">
                <div class="metric-label">🥉 {r3['Driver']}</div>
                <div class="metric-val" style="color:{PRIMARY}">{r3['Max shift from baseline (pp)']}pp</div>
            </div>''', unsafe_allow_html=True)
        
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # Compute estimated impact for #1
        top_driver = r1["Driver"]
        top_table = drivers[top_driver]
        worst_cat = top_table.loc[top_table["Attrition Rate (%)"].idxmax()]
        best_cat = top_table.loc[top_table["Attrition Rate (%)"].idxmin()]
        worst_count = len(df[df[top_driver]==worst_cat[top_driver]])
        potential_saves = round(worst_count * (worst_cat["Attrition Rate (%)"] - best_cat["Attrition Rate (%)"]) / 100)

        insight(f'{r1["Driver"]} has the largest impact at {r1["Max shift from baseline (pp)"]}pp, followed by {r2["Driver"]} ({r2["Max shift from baseline (pp)"]}pp) and {r3["Driver"]} ({r3["Max shift from baseline (pp)"]}pp). The top driver separates {worst_cat[top_driver]} ({worst_cat["Attrition Rate (%)"]:.1f}%) from {best_cat[top_driver]} ({best_cat["Attrition Rate (%)"]:.1f}%). If the worst-performing group could be brought to the best group\'s rate, an estimated {potential_saves:,} additional employees could be retained.')
        cta(f'Fix {r1["Driver"]} first. For the {worst_count:,} employees in the {worst_cat[top_driver]} category: 1) Accelerate promotion pathways and career visibility within 90 days. 2) Pair with the #2 driver ({r2["Driver"]}) — employees affected by both should be the highest priority. 3) Set a quarterly attrition target for this group and track monthly. Estimated impact: up to {potential_saves:,} retained employees if the gap closes by half.')


# ══════════════════════════════════════
# NAVIGATION
# ══════════════════════════════════════
st.sidebar.image("logo.png", width=100)
st.sidebar.divider()

pg = st.navigation([
    st.Page(page_home, title="Home", icon="🏠"),
    st.Page(page_foundations, title="Foundations", icon="📊"),
    st.Page(page_comparison, title="Comparison & Segmentation", icon="🔎"),
    st.Page(page_synthesis, title="Synthesis & Decisions", icon="🎯"),
])
pg.run()
