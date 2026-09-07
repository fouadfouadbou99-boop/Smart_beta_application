from io import BytesIO
import pandas as pd

def export_excel(**sheets):
    out=BytesIO()
    with pd.ExcelWriter(out,engine='openpyxl') as writer:
        for n,d in sheets.items():
            d.to_excel(writer,sheet_name=n,index=False)
    return out.getvalue()
