import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# Carregando os dados do arquivo CSV (certifique-se de que o arquivo "goals.csv" está no mesmo diretório)
data = pd.read_csv('goals.csv')

# Inicializando o aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Metas"),
    # dcc.Graph(
    #     id='bar-chart',
    #     figure={
    #         'data': [
    #             go.Bar(
    #                 x=data['Categoria'],
    #                 y=data['Metas'],
    #                 text=data['Metas'],
    #                 textposition='auto'
    #             )
    #         ],
    #         'layout': go.Layout(
    #             title='Metas por Categoria',
    #             xaxis={'title': 'Categoria'},
    #             yaxis={'title': 'Metas'}
    #         )
    #     }
    # )
])

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
