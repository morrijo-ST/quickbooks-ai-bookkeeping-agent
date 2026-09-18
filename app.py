
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def chart(fig, height=340):
    fig.update_layout(template='plotly_white',paper_bgcolor=PANEL,plot_bgcolor=PANEL,font=dict(color=INK,size=12),colorway=PALETTE,height=height,margin=dict(l=55,r=25,t=55,b=55),legend=dict(orientation='h',y=-.24,x=0),hoverlabel=dict(bgcolor=PANEL,font_color=INK))
    fig.update_xaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    fig.update_yaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    st.plotly_chart(fig,use_container_width=True,theme=None)

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="AI Bookkeeping Agent", layout="wide")
shell('BOOKKEEPING DESK','Every transaction deserves a reason.','Review suggested coding, inspect control flags, and record a local demo decision before export.','indigo')

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
# Duplicate candidates use repeated merchant/date/amount values.
for idx in [12,57,133]:
    for column in ['merchant','date','amount']:
        df.loc[idx,column]=df.loc[idx-1,column]
duplicate=df.duplicated(['merchant','date','amount'],keep=False)
df.loc[duplicate,'review_required']=True
df.loc[duplicate,'suggested_category']='Possible Duplicate'

threshold=st.sidebar.slider("Readiness score threshold",0.60,0.98,0.85,0.01)
f=df.copy()
f["decision"]=f.apply(lambda r:"Review" if r.review_required or r.confidence<threshold else "Auto-ready",axis=1)


metrics([('Transactions',str(len(f))),('Ready for review',str(int(f.decision.eq('Auto-ready').sum()))),('Exceptions',str(int(f.decision.eq('Review').sum()))),('Imported spend',money(f.amount.sum()))])
brief('Rule-based coding demonstration. Confidence scores are simulated, not calibrated AI probabilities. No QuickBooks connection or automatic posting is active.')
review_tab,coverage_tab=st.tabs(['Transaction workbench','Coding coverage'])
with review_tab:
    a,b=st.columns([1.5,1])
    review=f[f.decision=='Review'].sort_values(['confidence','amount'],ascending=[True,False])
    with a:
        st.subheader('Needs your attention')
        table(review,'bookkeeping_exceptions')
    with b:
        st.subheader('Coding decision')
        if len(review):
            tx=st.selectbox('Transaction',review.transaction_id.tolist())
            r=review[review.transaction_id==tx].iloc[0]
            st.write(f'**{r.merchant} · {money(r.amount)}**')
            st.write(f'Suggested account: {r.suggested_account}')
            st.write(f'Rule score: {r.confidence:.0%}')
            reason='Duplicate candidate' if r.suggested_category=='Possible Duplicate' else ('Approval limit exceeded' if r.amount>4000 else 'Low score or unknown merchant')
            st.warning(reason)
            account=st.selectbox('Reviewer account',sorted({v[1] for v in MERCHANTS.values()}),key='account_'+tx)
            action=st.radio('Review disposition',['Hold','Coding reviewed','Exclude duplicate'],key='action_'+tx)
            if st.button('Save demo decision'):
                st.session_state.setdefault('decisions',{})[tx]={'transaction_id':tx,'account':account,'decision':action}
                st.success('Saved for this browser session only. No accounting entry was posted.')
        if st.session_state.get('decisions'):table(pd.DataFrame(st.session_state.decisions.values()),'review_decisions',200)
with coverage_tab:
    bycat=f.groupby('suggested_category',as_index=False).amount.sum()
    chart(px.bar(bycat,x='amount',y='suggested_category',orientation='h',title='Spend by suggested category'),420)
    table(f,'all_transactions')
