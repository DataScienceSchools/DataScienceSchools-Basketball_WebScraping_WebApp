
import base64
import pandas as pd
import seaborn as sns
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
      page_title='NBA Player Stats Explorer',
      page_icon="🧊",
      layout="wide",
      initial_sidebar_state="expanded")

image_back = Image.open('back.png')
st.image(image_back, use_column_width=True)

st.markdown("""
[Data Science School](https://datascienceschools.github.io/)
""")
st.write('---')

st.title('NBA Player Stats Explorer')

with st.beta_expander("source"):
    st.markdown("""
    This app performs simple webscraping of NBA player stats data!
    * **Data source:** [Basketball Reference](https://www.basketball-reference.com/leagues/)
    * **Tutorial source:** [Data Professor](http://dataprofessor.org/)

    """)

# User Input Features
st.sidebar.header('Filter:')
# Sidebar - Year selection
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2021))))


# Web scraping of NBA player stats
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header = 0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)


# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Tm.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
#unique_pos = ['C','PF','SF','PG','SG']
unique_pos = sorted(playerstats.Pos.unique())
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)


# Filtering data
df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

st.header('Player Stats of Selected Team(s) & Position(s), Year: ' + str(selected_year ))
st.write('\n')
st.dataframe(df_selected_team)
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns')

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.write('---')
st.header('Download CSV File:')
st.write('\n\n\n')
st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

st.write('---')

# Heatmap
st.header('Intercorrelation Matrix Heatmap:')
st.write('\n\n\n')

if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(10, 10))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)
