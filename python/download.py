import pandas as pd

def addtofile(x,y,z,itemnum):
    df = pd.read_excel('rustoleumfile.xlsx', header=None)
    if df.empty: 
        data = {'Lowes':x,'Home Depot':y,'Ace':z}
        df=pd.DataFrame(data,[pd.Index([itemnum])])
        df.to_excel("/Users/carlosborjes/Desktop/real-rustoleum/rustoleumfile.xlsx", startrow=0, startcol=0)
    else:
        new_row = {'Lowes': x, 'Home Depot': y, 'Ace': z}
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel('rustoleumfile.xlsx', index=False)
