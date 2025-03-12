import pickle, ast
import pandas as pd
import numpy as np
import streamlit as st
import gdown
from pathlib import Path
file_id = "1opg8jecgJN7ox6lE5lnM80bqQZ5sBdEU"
output = "matrix.pkl"
if not Path(output).exists():
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)
df = pd.DataFrame(pickle.load(open('df.pkl', 'rb')))
similars = np.array(pickle.load(open('matrix.pkl', 'rb')))
def recommend(anime, n = 5):
    ind = df[df['title'] == anime].index[0]
    names = []
    img_paths = []
    lis = sorted(list(enumerate(similars[ind])), reverse = True, key= lambda x:x[1])[1:n+1]
    for i in lis:
        names.append(df.iloc[i[0]].title)
        tmp = ast.literal_eval(df.iloc[i[0]].imgs)
        img_paths.append(tmp['jpg']['large_image_url'])
    return names, img_paths

st.title("You might also like...")
option = st.selectbox(
        "",
        df['title'].values,
    )
if st.button("Recommend"):
    names, paths = recommend(option,6)
    row1 = st.columns(3, gap = 'large')
    row2 = st.columns(3, gap = 'large')
    i = 0
    for col in row1+row2:
        tile = col.container(height=280, key = names[i], border = True)
        tile.text(names[i])
        tile.image(paths[i])
        i+=1
