import db
import pandas as pd
import getid

def get_df(path):
    df_active = pd.read_excel(path,0)