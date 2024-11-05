import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Criação do app Dash
app = dash.Dash(__name__)

# Dados de exemplo para o gráfico de rosca
df = pd.DataFrame({
    "Categoria": ["Tecnologia", "Saúde", "Educação", "Entretenimento", "Alimentação"],
    "Valores": [25, 30, 15, 20, 10]
})

# Layout do dashboard
app.layout = html.Div([
    html.H1("Gráfico de categorias", style={'text-align': 'center'}),
    
    # Gráfico de Rosca
    dcc.Graph(id="grafico_rosca"),
    
    # Filtro para selecionar uma categoria específica
    html.Label("Selecione uma Categoria:", style={'font-weight': 'bold'}),
    dcc.Dropdown(
        id="filtro_categoria",
        options=[{"label": "Todas", "value": "Todas"}] + 
                 [{"label": cat, "value": cat} for cat in df["Categoria"]],
        value="Todas",
        clearable=False,
        style={'width': '50%', 'margin': '20px auto'}
    )
])

# Callback para atualizar o gráfico com base no filtro
@app.callback(
    Output("grafico_rosca", "figure"),
    [Input("filtro_categoria", "value")]
)
def update_graph(selected_category):
    # Filtra os dados com base na categoria selecionada
    if selected_category == "Todas":
        filtered_df = df
    else:
        filtered_df = df[df["Categoria"] == selected_category]
    
    # Criação do gráfico de rosca com cores
    fig = px.pie(
        filtered_df,
        names="Categoria",
        values="Valores",
        title="Distribuição por Categoria",
        hole=0.5  # Define o "furo" do gráfico de rosca
    )

    # Personalização das cores
    fig.update_traces(marker=dict(colors=px.colors.qualitative.Pastel))

    # Atualização do layout do gráfico
    fig.update_layout(
        showlegend=True,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title_x=0.5  # Centraliza o título
    )
    return fig

# Executa o app
if __name__ == "__main__":
    app.run_server(debug=True)
