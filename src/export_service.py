import pandas as pd
from pathlib import Path
DATA=Path('data'); DATA.mkdir(exist_ok=True)
RECENT=DATA/'lead_results.csv'
MASTER=DATA/'all_leads_database.csv'
COLS=['Lead Name','Website','Website Available','Phone','Location','Industry', 'Lead Score', 'Priority', 'Recommended Services', 'Issues']
def export_csv(df):
    if isinstance(df,list):
        df=pd.DataFrame(df)
    for c in COLS:
        if c not in df.columns:
            df[c]=''
    df=df[COLS]
    df.to_csv(RECENT,index=False)
    master=pd.read_csv(MASTER) if MASTER.exists() else pd.DataFrame(columns=COLS)
    updated=pd.concat([master,df],ignore_index=True).drop_duplicates(subset=['Lead Name','Website','Location','Industry'])
    updated.to_csv(MASTER,index=False)
    return len(updated)
