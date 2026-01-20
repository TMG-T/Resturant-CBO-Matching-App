from dash import Dash, html, dcc, callback, Input, Output
from data import cbo_df, restaurant_df, meals_df
from jaccard import find_best_restaurants as find_best_restaurants_jaccard, create_jaccard_section, create_match_scores_plot

app = Dash(__name__)
server = app.server

jaccard_section = create_jaccard_section(cbo_df, restaurant_df)

app.layout = html.Div(
    [
        html.H1("Rethink CBO Match Maker", style={"textAlign": "center", "marginTop": 20}),
        jaccard_section,
    ],
    style={"maxWidth": 1000, "margin": "0 auto", "fontFamily": "Arial, sans-serif"},
)


@callback(
    Output("jaccard-results-output", "children"),
    [Input("jaccard-cbo-dropdown", "value"), Input("jaccard-topn-dropdown", "value")]
)
def update_jaccard_results(cbo_name, top_n):
    if not cbo_name or not top_n:
        return html.Div("Select a CBO to see restaurant matches")
    
    results_df = find_best_restaurants_jaccard(cbo_name, cbo_df, restaurant_df, top_n=top_n)
    
    if results_df is None:
        return html.Div(f"CBO '{cbo_name}' not found.")
    
    # Create table headers
    columns = results_df.columns.tolist()
    
    # Create table rows
    rows = []
    for idx, row in results_df.iterrows():
        cells = []
        for col in columns:
            value = row[col]
            # Format numeric values
            if isinstance(value, float):
                value = f"{value:.4f}"
            cells.append(html.Td(str(value), style={"padding": "10px", "borderBottom": "1px solid #ddd"}))
        rows.append(html.Tr(cells))
    
    # Create header row
    header_cells = [html.Th(col, style={"padding": "10px", "backgroundColor": "#f0f0f0", "fontWeight": "bold", "borderBottom": "2px solid #ddd"}) for col in columns]
    header_row = html.Thead(html.Tr(header_cells))
    
    # Create table
    table = html.Table(
        [header_row, html.Tbody(rows)],
        style={"width": "100%", "borderCollapse": "collapse", "marginTop": "20px", "fontSize": "12px"}
    )
    
    return html.Div(
        [
            html.H4(f"Top {top_n} Matches for {cbo_name}", style={"marginBottom": "20px"}),
            table,
            dcc.Graph(
                figure=create_match_scores_plot(results_df, cbo_name),
                config={
                    "displayModeBar": False,
                    "doubleClick": False,
                    "scrollZoom": False,
                    "modeBarButtonsToRemove": ["zoom2d", "pan2d", "select2d", "lasso2d", "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d"]
                }
            )
        ]
    )


if __name__ == "__main__":
    app.run(debug=True, port=8050)
