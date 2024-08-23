import pandas as pd
import plotly.graph_objects as go
from dash import Dash, html, dcc
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import numpy as np

# Carregando os dados
df = pd.read_csv('../data/dados_poluentes_rio.csv')

# 1. Definição Estatística do Modelo de Regressão Linear Simples
# O modelo de regressão linear simples pode ser definido pela equação:
# Y = β0 + β1*X + ε
# onde Y é a variável dependente (Concentração de Poluentes), X é a variável independente (Distância a Jusante),
# β0 é o intercepto, β1 é o coeficiente angular, e ε é o termo de erro.

# Regressão Linear usando scikit-learn (Método dos Mínimos Quadrados Ordinários)
X = df["Distância a Jusante (km)"].values.reshape(-1, 1)  # Variável independente (X)
y = df["Concentração de Poluentes (mg/L)"].values  # Variável dependente (y)

modelo = LinearRegression()
modelo.fit(X, y)  # Treinamento do modelo

# Previsão para a linha de regressão
df['Regressão Linear'] = modelo.predict(X)

# Estimação dos Parâmetros (MQO)
intercepto = modelo.intercept_
coeficiente = modelo.coef_[0]

# Análise da Bondade do Ajuste
r2 = r2_score(y, df['Regressão Linear'])
mse = mean_squared_error(y, df['Regressão Linear'])


fig_scatter = go.Figure()

fig_scatter.add_trace(go.Scatter(
    x=df["Distância a Jusante (km)"],
    y=df["Concentração de Poluentes (mg/L)"],
    mode='markers',
    name='Dados Observados'
))

fig_scatter.add_trace(go.Scatter(
    x=df["Distância a Jusante (km)"],
    y=df['Regressão Linear'],
    mode='lines',
    name='Linha de Regressão',
    line=dict(color='red')
))

fig_scatter.update_layout(
    title=f"Relação entre Distância a Jusante e Concentração de Poluentes<br>R² = {r2:.2f}, MSE = {mse:.2f}",
    xaxis_title="Distância a Jusante (km)",
    yaxis_title="Concentração de Poluentes (mg/L)",
    template="plotly_white"
)


app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Análise de Poluentes no Rio', style={'textAlign': 'center', 'padding-top': '20px', 'font-family': 'Arial'}),

   
    html.Div(children=[
        html.H2(children='Fórmulas e Cálculos', style={'textAlign': 'center', 'padding': '10px', 'font-family': 'Arial'}),

        dcc.Markdown(f'''
        **Equação da Regressão Linear Simples:**

        A regressão linear simples pode ser representada pela equação:

        \[
        Y = \beta_0 + \beta_1 X + \epsilon
        \]

        **Cálculo do Coeficiente Angular (\(\\beta_1\)):**

        O coeficiente angular (\(\\beta_1\)) é calculado como:

        \[
        \\beta_1 = \\frac{{\sum{{(X_i - \bar{{X}})(Y_i - \bar{{Y}})}}}}{{\sum{{(X_i - \bar{{X}})^2}}}} = {coeficiente:.2f}
        \]

        **Cálculo do Intercepto (\(\\beta_0\)):**

        O intercepto (\(\\beta_0\)) é calculado usando:

        \[
        \\beta_0 = \bar{{Y}} - \\beta_1\bar{{X}} = {intercepto:.2f}
        \]

        **Coeficiente de Determinação (\(R^2\)):**

        O coeficiente de determinação \(R^2\) mede a proporção da variação em \(Y\) que é explicada pelo modelo de regressão linear:

        \[
        R^2 = {r2:.2f}
        \]

        **Erro Quadrático Médio (MSE):**

        O erro quadrático médio é dado por:

        \[
        MSE = \\frac{{1}}{{n}} \sum{{(Y_i - \hat{{Y}}_i)^2}} = {mse:.2f}
        \]
        ''', style={'padding': '20px', 'font-family': 'Arial'}),
    ], style={'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'margin': '20px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),


    html.Div(children=[
        html.H2(children='Estatísticas Descritivas', style={'textAlign': 'center', 'padding': '10px', 'font-family': 'Arial'}),

        html.Div(children=[
            html.Div(children=[
                html.H3(children='Média', style={'textAlign': 'center', 'color': '#333', 'font-family': 'Arial'}),
                html.P(f"{df['Concentração de Poluentes (mg/L)'].mean():.2f} mg/L", style={'textAlign': 'center', 'font-size': '20px', 'font-family': 'Arial'}),
            ], style={'display': 'inline-block', 'width': '30%', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px'}),

            html.Div(children=[
                html.H3(children='Mediana', style={'textAlign': 'center', 'color': '#333', 'font-family': 'Arial'}),
                html.P(f"{df['Concentração de Poluentes (mg/L)'].median():.2f} mg/L", style={'textAlign': 'center', 'font-size': '20px', 'font-family': 'Arial'}),
            ], style={'display': 'inline-block', 'width': '30%', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px'}),

            html.Div(children=[
                html.H3(children='Desvio Padrão', style={'textAlign': 'center', 'color': '#333', 'font-family': 'Arial'}),
                html.P(f"{df['Concentração de Poluentes (mg/L)'].std():.2f} mg/L", style={'textAlign': 'center', 'font-size': '20px', 'font-family': 'Arial'}),
            ], style={'display': 'inline-block', 'width': '30%', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px'}),
        ], style={'textAlign': 'center'}),

        html.Div(children=[
            html.Div(children=[
                html.H3(children='Variância', style={'textAlign': 'center', 'color': '#333', 'font-family': 'Arial'}),
                html.P(f"{df['Concentração de Poluentes (mg/L)'].var():.2f} mg/L", style={'textAlign': 'center', 'font-size': '20px', 'font-family': 'Arial'}),
            ], style={'display': 'inline-block', 'width': '30%', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px'}),

            html.Div(children=[
                html.H3(children='1º Quartil', style={'textAlign': 'center', 'color': '#333', 'font-family': 'Arial'}),
                html.P(f"{df['Concentração de Poluentes (mg/L)'].quantile(0.25):.2f} mg/L", style={'textAlign': 'center', 'font-size': '20px', 'font-family': 'Arial'}),
            ], style={'display': 'inline-block', 'width': '30%', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px'}),

            html.Div(children=[
                html.H3(children='3º Quartil', style={'textAlign': 'center', 'color': '#333', 'font-family': 'Arial'}),
                html.P(f"{df['Concentração de Poluentes (mg/L)'].quantile(0.75):.2f} mg/L", style={'textAlign': 'center', 'font-size': '20px', 'font-family': 'Arial'}),
            ], style={'display': 'inline-block', 'width': '30%', 'padding': '20px', 'border': '1px solid #ddd', 'margin': '10px', 'backgroundColor': '#fff', 'borderRadius': '10px'}),
        ], style={'textAlign': 'center'}),
    ], style={'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px', 'margin': '20px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),


    html.Div(children=[
        dcc.Graph(
            id='scatter-plot',
            figure=fig_scatter
        )
    ], style={'padding': '20px'}),
], style={'max-width': '1000px', 'margin': 'auto'})

if __name__ == '__main__':
    app.run_server(debug=True)
