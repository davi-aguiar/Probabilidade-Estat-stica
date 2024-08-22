import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress







df = pd.read_csv('../data/dados_poluentes_rio.csv')


slope, intercept, r_value, p_value, std_err = linregress(df["Distância a Jusante (km)"], df["Concentração de Poluentes (mg/L)"])


df['Regressão Linear'] = intercept + slope * df["Distância a Jusante (km)"]


fig = go.Figure()


fig.add_trace(go.Scatter(
    x=df["Distância a Jusante (km)"], 
    y=df["Concentração de Poluentes (mg/L)"],
    mode='markers',
    name='Dados Observados'
))


fig.add_trace(go.Scatter(
    x=df["Distância a Jusante (km)"], 
    y=df["Regressão Linear"],
    mode='lines',
    name='Linha de Regressão',
    line=dict(color='red')
))


fig.update_layout(
    title="Relação entre Distância a Jusante e Concentração de Poluentes",
    xaxis_title="Distância a Jusante (km)",
    yaxis_title="Concentração de Poluentes (mg/L)",
    template="plotly_white"
)


fig.write_html("../outputs/grafico.html")

fig.show()
