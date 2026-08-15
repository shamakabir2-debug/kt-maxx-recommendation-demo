"""
KT Maxx — Release 1 Demo: FP-Growth Product Recommendation Engine
Run with:  streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="KT Maxx | Recommendation Engine Demo", layout="wide")

# ---------- Load real, precomputed data ----------
rules = pd.read_csv("app_rules.csv")
rfm_summary = pd.read_csv("app_rfm_summary.csv")

# ---------- Header ----------
st.title("KT Maxx — AI Product Recommendation Engine")

tab_customer, tab_analyst = st.tabs(["Customer view", "Analyst dashboard"])

# ============================================================
# CUSTOMER VIEW
# ============================================================
with tab_customer:
    st.subheader("Product page simulation")

    products = sorted(rules["antecedent"].unique())
    default_ix = products.index("ALARM CLOCK BAKELIKE RED") if "ALARM CLOCK BAKELIKE RED" in products else 0
    selected = st.selectbox("Pick a product a customer is viewing:", products, index=default_ix)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            f"""
            <div style="border:1px solid #ddd;border-radius:10px;padding:20px;">
            <div style="width:100%;height:90px;background:#f0f0f0;border-radius:6px;
            display:flex;align-items:center;justify-content:center;
            color:#aaa;font-size:11px;letter-spacing:.05em;text-transform:uppercase;">Product image</div>
            <div style="font-weight:700;font-size:16px;margin-top:12px;">{selected.title()}</div>
            <div style="color:#888;font-size:13px;margin-top:4px;">KT Maxx product page</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("**Predicted purchase probability**")
        recs = rules[rules["antecedent"] == selected].sort_values("confidence", ascending=False).head(3)
        if recs.empty:
            st.info("No strong association rule found for this product at the current support threshold.")
        else:
            for _, r in recs.iterrows():
                prob = r["confidence"] * 100
                st.markdown(
                    f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                    background:#f7f5f2;border-radius:8px;padding:12px 16px;margin-bottom:8px;">
                    <div>
                    <b>{r['consequent'].title()}</b><br>
                    <span style="color:#888;font-size:12px;">
                    {r['lift']:.1f}× more likely than a random customer
                    </span>
                    </div>
                    <div style="text-align:right;">
                    <div style="font-size:22px;font-weight:700;">{prob:.0f}%</div>
                    <div style="color:#888;font-size:11px;">predicted likelihood</div>
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# ============================================================
# ANALYST DASHBOARD
# ============================================================
with tab_analyst:
    c1, c2, c3 = st.columns(3)
    c1.metric("Association rules found", len(rules))
    c2.metric("Products with a recommendation", rules["antecedent"].nunique())
    c3.metric("Top rule lift", f"{rules['lift'].max():.1f}×")

    st.markdown(f"### Rules for your selected product: {selected.title()}")
    selected_rules = rules[
        (rules["antecedent"] == selected) | (rules["consequent"] == selected)
    ].sort_values("lift", ascending=False)
    if selected_rules.empty:
        st.info("No rules involve this product at the current threshold.")
    else:
        st.dataframe(
            selected_rules[["antecedent", "consequent", "confidence", "lift"]]
            .assign(confidence=lambda d: (d["confidence"] * 100).round(1))
            .rename(columns={
                "antecedent": "If a customer buys",
                "consequent": "...they also tend to buy",
                "confidence": "% of the time this pairing happens",
                "lift": "Strength of connection (×)",
            })
            .reset_index(drop=True),
            use_container_width=True,
        )

    st.divider()
    st.markdown("### Top product pairs by lift (catalog-wide)")
    top15 = rules.sort_values("lift", ascending=False).head(15).copy()
    top15["pair"] = top15["antecedent"].str.title() + " ↔ " + top15["consequent"].str.title()
    fig1 = px.bar(
        top15.sort_values("lift"),
        x="lift",
        y="pair",
        orientation="h",
        labels={"lift": "Lift (× more likely than chance)", "pair": ""},
    )
    fig1.update_traces(marker_color="#8a7a63")
    fig1.update_layout(height=450, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Customer segments (RFM, 4,338 real customers)")
    seg_order = rfm_summary.sort_values("AvgMonetary", ascending=False)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_count = px.bar(
            seg_order, x="Segment", y="Customers",
            title="Customers per segment",
            labels={"Segment": "", "Customers": "# customers"},
        )
        fig_count.update_traces(marker_color="#5b7a63")
        fig_count.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_count, use_container_width=True)

    with col_b:
        fig_spend = px.bar(
            seg_order, x="Segment", y="AvgMonetary",
            title="Average spend per segment (£)",
            labels={"Segment": "", "AvgMonetary": "Avg spend (£)"},
        )
        fig_spend.update_traces(marker_color="#c08a5a")
        fig_spend.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_spend, use_container_width=True)

    st.markdown("### All product pairings")
    display_rules = rules.sort_values("lift", ascending=False).reset_index(drop=True).copy()
    display_rules["support"] = (display_rules["support"] * 100).round(1)
    display_rules["confidence"] = (display_rules["confidence"] * 100).round(1)
    display_rules["lift"] = display_rules["lift"].round(1)
    display_rules = display_rules.rename(columns={
        "antecedent": "If a customer buys",
        "consequent": "...they also tend to buy",
        "support": "% of all orders with this pair",
        "confidence": "% of the time this pairing happens",
        "lift": "Strength of connection (×)",
    })
    st.dataframe(
        display_rules,
        use_container_width=True,
        height=300,
    )
