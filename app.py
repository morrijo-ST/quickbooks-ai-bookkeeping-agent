import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="AI Bookkeeping Agent", layout="wide")
st.title("QuickBooks AI Bookkeeping Agent")
st.caption("Synthetic transaction classification, confidence scoring, controls, and human review.")

random.seed(42)
MERCHANTS = {
    "AWS": ("Software & Cloud", "Software Subscriptions"),
    "Delta": ("Travel", "Travel - Airfare"),
    "Marriott": ("Travel", "Travel - Lodging"),
    "Home Depot": ("Project Costs", "Materials"),
    "Google Ads": ("Marketing", "Digital Advertising"),
    "Staples": ("Office", "Office Supplies"),
    "Uber": ("Travel", "Ground Transportation"),
    "Unknown Vendor": ("Review", "Uncategorized Expense"),
}
rows=[]
for i in range(180):
    merchant=random.choice(list(MERCHANTS))
    category,account=MERCHANTS[merchant]
    amount=round(random.uniform(18,4800),2)
    confidence=round(random.uniform(.90,.99),2) if merchant!="Unknown Vendor" else round(random.uniform(.42,.69),2)
    if amount>3500: confidence=min(confidence,.82)
    rows.append({"transaction_id":f"TX-{i+1:04}","date":pd.Timestamp("2026-01-01")+pd.Timedelta(days=random.randint(0,240)),"merchant":merchant,"amount":amount,"suggested_category":category,"suggested_account":account,"confidence":confidence,"project":random.choice(["Client Alpha","Client Beta","Internal","Unassigned"])})
df=pd.DataFrame(rows)
df["review_required"]=(df.confidence<.80)|(df.suggested_category=="Review")|(df.amount>4000)
# deterministic duplicate flags
for idx in [12,57,133]:
    df.loc[idx,"review_required"]=True
    df.loc[idx,"suggested_category"]="Possible Duplicate"

threshold=st.sidebar.slider("Auto-post confidence threshold",0.60,0.98,0.85,0.01)
f=df.copy()
f["decision"]=f.apply(lambda r:"Review" if r.review_required or r.confidence<threshold else "Auto-ready",axis=1)

c1,c2,c3,c4=st.columns(4)
c1.metric("Transactions",len(f))
c2.metric("Auto-ready",int((f.decision=="Auto-ready").sum()))
c3.metric("Review queue",int((f.decision=="Review").sum()))
c4.metric("Spend",f"${f.amount.sum():,.0f}")

st.subheader("Classification coverage")
bycat=f.groupby("suggested_category",as_index=False).agg(transactions=("transaction_id","count"),spend=("amount","sum"))
st.plotly_chart(px.bar(bycat,x="suggested_category",y="spend",hover_data=["transactions"]),use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader("Confidence distribution")
    st.plotly_chart(px.histogram(f,x="confidence",nbins=15),use_container_width=True)
with right:
    st.subheader("Decision mix")
    mix=f.groupby("decision",as_index=False).size()
    st.plotly_chart(px.pie(mix,names="decision",values="size"),use_container_width=True)

st.subheader("Human review queue")
review=f[f.decision=="Review"].sort_values(["confidence","amount"],ascending=[True,False])
st.dataframe(review[["transaction_id","date","merchant","amount","suggested_account","project","confidence","suggested_category"]],use_container_width=True,hide_index=True)

st.subheader("Agent control logic")
st.code("""IF merchant rule is known AND confidence >= threshold AND amount is below approval limit:
    mark transaction Auto-ready
ELSE:
    route to human review

Never post ambiguous or high-risk transactions without review.""")
