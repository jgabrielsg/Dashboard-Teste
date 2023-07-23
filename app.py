import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from graphs import (graph_goals_per_club, graph_shoots_per_club, graph_victories_inter, 
                    graph_cards_per_team, graph_best_goal_scorers, graph_results_per_team,
                    graph_goals_per_team)

goals_data = pd.read_csv('csvs/goals.csv')
stats_data = pd.read_csv('csvs/stats.csv')
results_data = pd.read_csv('csvs/results.csv')
cards_data = pd.read_csv('csvs/cards.csv')


# Inicializando o aplicativo Dash
app = dash.Dash(__name__)

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Gols por Equipe"),
    html.Div(children=[
        html.Div(children=[
            graph_goals_per_club()],
                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '95px'}),

        html.Div(children=[
            graph_shoots_per_club()],
                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '95px'}),
        
        html.Div(children=[
        dcc.Dropdown(
        id='team-dropdown',
        options=[{'label': time, 'value': time} for time in sorted(results_data['mandante'].unique())],
        value=results_data['mandante'].unique()[0],  # Valor inicial do dropdown
    ),
            graph_victories_inter()],
                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '95px'}),
        
        html.Div(children=[
            graph_cards_per_team()],
                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '95px'}),

        html.Div(children=[
            graph_best_goal_scorers()],
                    style={'width': '95%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '95px'}),

        # Dropdown para selecionar o time
        dcc.Dropdown(
            id='team-dropdown2',
            options=[{'label': time, 'value': time} for time in sorted(results_data['mandante'].unique())],
            value=results_data['mandante'].unique()[0],  # Valor inicial do dropdown
        ),

        html.Div(children=[
            graph_results_per_team()],
                    style={'width': '47%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '95px'}),
        
        html.Div(children=[
            graph_goals_per_team()]
                    ,style={'width': '47%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-top': '95px'})

    ])
])


# Callback para atualizar o gráfico de vitórias com base no time selecionado
@app.callback(
    Output('graph-victories-inter', 'figure'),
    [Input('team-dropdown', 'value')]
)
def update_victories_graph(selected_team):
    # Filtrar os dados para partidas em que o time selecionado foi o mandante
    mandante_selected_team = results_data[results_data['mandante'] == selected_team]

    # Filtrar os dados para partidas em que o time selecionado foi o visitante
    visitante_selected_team = results_data[results_data['visitante'] == selected_team]

    # Contar o número de vitórias do time selecionado como mandante
    vitorias_mandante_selected_team = mandante_selected_team[mandante_selected_team['vencedor'] == selected_team].shape[0]

    # Contar o número de vitórias do time selecionado como visitante
    vitorias_visitante_selected_team = visitante_selected_team[visitante_selected_team['vencedor'] == selected_team].shape[0]

    # Calcular a porcentagem de vitórias como mandante e visitante
    total_jogos_mandante = mandante_selected_team.shape[0]
    total_jogos_visitante = visitante_selected_team.shape[0]

    porcentagem_vitorias_mandante = (vitorias_mandante_selected_team / total_jogos_mandante) * 100
    porcentagem_vitorias_visitante = (vitorias_visitante_selected_team / total_jogos_visitante) * 100

    df_inter = pd.DataFrame({
        'local': ['Mandante', 'Visitante'],
        'vitórias': [vitorias_mandante_selected_team, vitorias_visitante_selected_team],
        'porcentagem_vitórias': [porcentagem_vitorias_mandante, porcentagem_vitorias_visitante]
    })

    fig = px.bar(
        df_inter, 
        x="local",
        y="vitórias",
        text="porcentagem_vitórias",  # Mostrar a porcentagem de vitórias como texto
        labels={"value": "", "variable": ""},
        height=420
    )

    fig.update_layout(
        title={
            'text': f'<b style="color:#222E66;">Vitórias por Time: {selected_team}</b>',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        plot_bgcolor='#B8D8D8',
        paper_bgcolor='rgba(44, 146, 213, 0.06)',
        xaxis_title='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=10, r=10, t=10, b=0),  # Define as margens do gráfico
    )

    return fig

# Callback para atualizar o gráfico de resultados e de gols quando um novo time for selecionado
@app.callback(
    [Output('results-graph', 'children'),
     Output('goals-graph', 'children')],
    Input('team-dropdown2', 'value')
)
def update_graphs(selected_team):
    graph_results = graph_results_per_team(selected_team)
    graph_goals = graph_goals_per_team(selected_team)
    return graph_results, graph_goals

# Executar o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)
