import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress
from dash import Dash, html, dcc


df = pd.read_csv('../data/dados_poluentes_rio.csv')


mean_value = df["Concentração de Poluentes (mg/L)"].mean()
median_value = df["Concentração de Poluentes (mg/L)"].median()

mode_value = df["Concentração de Poluentes (mg/L)"].mode()

if len(mode_value) > 0:
    mode_values_str = ', '.join([f"{val:.2f}" for val in mode_value])
else:
    mode_values_str = "N/A"

std_deviation = df["Concentração de Poluentes (mg/L)"].std()
variance = df["Concentração de Poluentes (mg/L)"].var()
first_quartile = df["Concentração de Poluentes (mg/L)"].quantile(0.25)
third_quartile = df["Concentração de Poluentes (mg/L)"].quantile(0.75)

slope, intercept, r_value, p_value, std_err = linregress(df["Distância a Jusante (km)"], df["Concentração de Poluentes (mg/L)"])
df['Regressão Linear'] = intercept + slope * df["Distância a Jusante (km)"]


fig_scatter = go.Figure()
fig_scatter.add_trace(go.Scatter(
    x=df["Distância a Jusante (km)"], 
    y=df["Concentração de Poluentes (mg/L)"],
    mode='markers',
    name='Dados Observados'
))
fig_scatter.add_trace(go.Scatter(
    x=df["Distância a Jusante (km)"], 
    y=df["Regressão Linear"],
    mode='lines',
    name='Linha de Regressão',
    line=dict(color='red')
))
fig_scatter.update_layout(
    title="Relação entre Distância a Jusante e Concentração de Poluentes",
    xaxis_title="Distância a Jusante (km)",
    yaxis_title="Concentração de Poluentes (mg/L)",
    template="plotly_white"
)

fig_box = px.box(df, y="Concentração de Poluentes (mg/L)", title="Box Plot da Concentração de Poluentes")
fig_box.update_layout(template="plotly_white")

fig_hist = px.histogram(df, x="Concentração de Poluentes (mg/L)", nbins=10, title="Histograma da Concentração de Poluentes")
fig_hist.update_layout(template="plotly_white")


app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Análise de Poluentes no Rio', style={'textAlign': 'center'}),
    
  
    html.Div(children=[
        html.Div(children=[
            html.H3(children='Média'),
            html.P(f"{mean_value:.2f} mg/L"),
        ], style={'display': 'inline-block', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
        
        html.Div(children=[
            html.H3(children='Mediana'),
            html.P(f"{median_value:.2f} mg/L"),
        ], style={'display': 'inline-block', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
        
        
            # html.Div(children=[
            #     html.H3(children='Moda'),
            #     html.P(f"{mode_value:.2f} mg/L"),
            # ], style={'display': 'inline-block', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
            
        html.Div(children=[
            html.H3(children='Desvio Padrão'),
            html.P(f"{std_deviation:.2f} mg/L"),
        ], style={'display': 'inline-block', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
        
        html.Div(children=[
            html.H3(children='Variância'),
            html.P(f"{variance:.2f} mg/L"),
        ], style={'display': 'inline-block', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
        
        html.Div(children=[
            html.H3(children='1º Quartil'),
            html.P(f"{first_quartile:.2f} mg/L"),
        ], style={'display': 'inline-block', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
        
        html.Div(children=[
            html.H3(children='3º Quartil'),
            html.P(f"{third_quartile:.2f} mg/L"),
        ], style={'display': 'inline-block', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px'}),
    ], style={'textAlign': 'center'}),
    
    
    html.Div(children=[
        dcc.Graph(
            id='scatter-plot',
            figure=fig_scatter
        ),
        dcc.Graph(
            id='box-plot',
            figure=fig_box
        ),
        dcc.Graph(
            id='histogram',
            figure=fig_hist
        )
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
