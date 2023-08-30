import io
import pandas as pd

data = []

while True:
    try:
        input_ = input()
        data.append(input_)
    except EOFError:
         break


    
data = '\n'.join(data)
df = pd.read_csv(io.StringIO(data))
df_2 = df 
for i in range(len(df_2.columns)):
    df_2.columns[i] = 'inv_' +  str(df_2.columns[i])         
print(df_2.columns)    