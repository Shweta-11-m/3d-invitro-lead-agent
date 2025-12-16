# Save this code as app.py

import streamlit as st
import pandas as pd
import random

# ==========================================
# 1. CONFIGURATION & PROBABILITY ENGINE
# ==========================================

# Criteria Keywords from your Business Plan
HIGH_SCORE_TITLES = [
    "Toxicology", "Safety Assessment", "Preclinical", "Hepatic", 
    "3D", "In-Vitro", "Liver", "DILI", "Investigative"
]
HIGH_VALUE_HUBS = [
    "Cambridge", "Boston", "San Francisco", "Bay Area", 
    "Basel", "London", "Oxford", "Golden Triangle", "Zurich"
]
HIGH_INTENT_PAPERS = [
    "Drug-Induced Liver Injury", "Organ-on-chip", "Hepatic spheroids", 
    "Microphysiological systems", "Toxicity testing"
]

def calculate_propensity_score(lead):
    """
    Calculates the 'Propensity to Buy' score (0-100) based on weighted signals.
    """
    score = 0
    breakdown = []

    # Signal 1: Role Fit (+30)
    if any(t.lower() in lead['Title'].lower() for t in HIGH_SCORE_TITLES):
        score += 30
        breakdown.append(" Role Fit (+30)")
    
    # Signal 2: Company Intent (+20) - Series A/B or High Growth
    if lead['Funding_Stage'] in ['Series A', 'Series B', 'IPO/Public', 'Grant']:
        score += 20
        breakdown.append(f" Funding: {lead['Funding_Stage']} (+20)")

    # Signal 3: Technographic (+15) - Uses similar tech
    if lead['Uses_NAMs']:
        score += 15
        breakdown.append(" Uses NAMs/3D Tech (+15)")

    # Signal 4: Location Hub (+10)
    if any(hub.lower() in lead['HQ_Location'].lower() for hub in HIGH_VALUE_HUBS):
        score += 10
        breakdown.append(" Hub Location (+10)")

    # Signal 5: Scientific Intent (+40) - Recent relevant paper
    if lead['Recent_Paper_Topic']:
        score += 40
        breakdown.append(f" Published on {lead['Recent_Paper_Topic']} (+40)")

    final_score = min(100, score)
    return final_score, ", ".join(breakdown)

# ==========================================
# 2. MOCK DATA GENERATOR (Simulating the Crawler)
# ==========================================
# (The real-world version would replace this function with API calls)
def load_data():
    data = [
        {"Name": "Dr. Jan Lichtenberg", "Title": "CEO & Co-Founder", "Company": "InSphero", "HQ_Location": "Zurich, Switzerland", "Person_Location": "Zurich, Switzerland", "Email": "j.lichtenberg@insphero.com", "Funding_Stage": "Series C", "Uses_NAMs": True, "Recent_Paper_Topic": "3D Liver Microtissues", "LinkedIn_URL": "https://www.linkedin.com/in/janlichtenberg/"},
        {"Name": "Katherine Malone", "Title": "Principal Scientist, Toxicology", "Company": "Charles River Laboratories", "HQ_Location": "Wilmington, MA", "Person_Location": "Remote, NC", "Email": "k.malone@crl.com", "Funding_Stage": "IPO/Public", "Uses_NAMs": True, "Recent_Paper_Topic": "Anti-Drug Antibody Assessment", "LinkedIn_URL": "https://www.linkedin.com/in/katherine-malone-tox/"},
        {"Name": "Dr. Sylvia Escher", "Title": "Head of Dept. In-Vitro Toxicology", "Company": "Fraunhofer ITEM", "HQ_Location": "Hannover, Germany", "Person_Location": "Hannover, Germany", "Email": "sylvia.escher@item.fraunhofer.de", "Funding_Stage": "Grant", "Uses_NAMs": True, "Recent_Paper_Topic": "Inhalation Toxicity NAMs", "LinkedIn_URL": "https://www.linkedin.com/in/sylvia-escher-item/"},
        {"Name": "Jim Corbett", "Title": "CEO", "Company": "Emulate Bio", "HQ_Location": "Boston, MA", "Person_Location": "Boston, MA", "Email": "jim.corbett@emulatebio.com", "Funding_Stage": "Series E", "Uses_NAMs": True, "Recent_Paper_Topic": "Organ-on-Chip Technology", "LinkedIn_URL": "https://www.linkedin.com/in/jimcorbett-bio/"},
        {"Name": "Michael Smith", "Title": "Junior Lab Tech", "Company": "BioStart Generic", "HQ_Location": "Austin, TX", "Person_Location": "Austin, TX", "Email": "mike.smith@biostart.com", "Funding_Stage": "Seed", "Uses_NAMs": False, "Recent_Paper_Topic": None, "LinkedIn_URL": "https://www.linkedin.com/in/mikesmith-lab/"},
        {"Name": "Sarah Chen", "Title": "Director of Safety Assessment", "Company": "LiverBio Therapeutics", "HQ_Location": "Cambridge, MA", "Person_Location": "Remote, CO", "Email": "s.chen@liverbio.com", "Funding_Stage": "Series B", "Uses_NAMs": True, "Recent_Paper_Topic": "Drug-Induced Liver Injury", "LinkedIn_URL": "https://www.linkedin.com/in/sarahchen-safety/"},
        {"Name": "Biman B. Mandal", "Title": "Professor, Bioscience", "Company": "IIT Guwahati", "HQ_Location": "Guwahati, India", "Person_Location": "Guwahati, India", "Email": "biman.m@iitg.ac.in", "Funding_Stage": "Grant", "Uses_NAMs": True, "Recent_Paper_Topic": "3D Bio-printed Liver Models", "LinkedIn_URL": "https://www.linkedin.com/in/biman-mandal/"},
         {"Name": "David Jones", "Title": "Procurement Manager", "Company": "MegaPharma Inc", "HQ_Location": "New York, NY", "Person_Location": "New York, NY", "Email": "d.jones@megapharma.com", "Funding_Stage": "IPO/Public", "Uses_NAMs": False, "Recent_Paper_Topic": None, "LinkedIn_URL": "https://www.linkedin.com/in/davidjones-procure/"}
    ]
    
    df = pd.DataFrame(data)
    df[['Score', 'Score_Reason']] = df.apply(
        lambda row: pd.Series(calculate_propensity_score(row)), axis=1
    )
    df = df.sort_values(by='Score', ascending=False)
    return df

# ==========================================
# 3. STREAMLIT UI LAYOUT
# ==========================================

st.set_page_config(page_title="3D Bio-Agent Leads", layout="wide")
st.title("🧬 3D In-Vitro Lead Generation Agent")
st.markdown("---")

# --- Sidebar Filters ---
st.sidebar.header("Filter Leads")
min_score = st.sidebar.slider("Minimum Propensity Score", 0, 100, 50)
location_filter = st.sidebar.text_input("Filter by Location (e.g., Boston)")
role_filter = st.sidebar.text_input("Filter by Title (e.g., Director)")

df = load_data()

# --- Apply UI Filters ---
filtered_df = df[df['Score'] >= min_score]
if location_filter:
    filtered_df = filtered_df[filtered_df['HQ_Location'].str.contains(location_filter, case=False) | filtered_df['Person_Location'].str.contains(location_filter, case=False)]
if role_filter:
    filtered_df = filtered_df[filtered_df['Title'].str.contains(role_filter, case=False)]

# --- Main Table Display ---
st.subheader(" Prioritized Lead List")

# Display as a dynamic table
st.dataframe(
    filtered_df[['Score', 'Name', 'Title', 'Company', 'Score_Reason', 'HQ_Location', 'Person_Location', 'Recent_Paper_Topic', 'LinkedIn_URL']],
    column_config={
        "Score": st.column_config.ProgressColumn("Probability", help="Propensity to Buy Score (0-100)", format="%f", min_value=0, max_value=100),
        "LinkedIn_URL": st.column_config.LinkColumn("LinkedIn"),
    },
    hide_index=True,
    use_container_width=True
)

# --- CSV Download ---
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label=" Download Leads as CSV (Excel/Google Sheets)",
    data=csv,
    file_name='qualified_leads_3d_invitro.csv',
    mime='text/csv',
)
