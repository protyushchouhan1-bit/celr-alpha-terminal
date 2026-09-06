import os
import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import plotly.express as px

# Initialize Dash App
app = dash.Dash(__name__, title="CELR Alpha Terminal")

# Load Data
df = pd.read_csv("output/celr_ranked_assets.csv")

# High-Vibrancy Color Palette
COLOR_MAP = {
    'Tier 1 Alpha Asset': '#10B981',     # Electric Emerald
    'High-Yield Volatile': '#8B5CF6',    # Vibrant Violet
    'Distressed Equity': '#FF4D4D',      # Sunset Coral
    'Dormant Capital': '#F59E0B'         # Bright Amber
}

app.layout = html.Div(style={
    'backgroundColor': '#F1F5F9',
    'minHeight': '100vh',
    'padding': '28px',
    'fontFamily': "'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
}, children=[
    
    # HEADER BANNER
    html.Div(style={
        'background': 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%)',
        'padding': '28px',
        'borderRadius': '18px',
        'color': 'white',
        'boxShadow': '0 10px 25px -5px rgba(124, 58, 237, 0.4)',
        'marginBottom': '28px'
    }, children=[
        html.H1("⚡ CELR Capital Preservation Terminal", style={'margin': '0 0 6px 0', 'fontWeight': '800', 'fontSize': '32px'}),
        html.P("Real-Time Institutional Equity Liquidation Risk & Yield Engine", style={'margin': '0', 'opacity': '0.92', 'fontSize': '16px'})
    ]),

    # USP SECTION: RESCUE CAPITAL INTERVENTION SIMULATOR
    html.Div(style={
        'backgroundColor': '#FFFFFF',
        'borderRadius': '16px',
        'padding': '22px',
        'marginBottom': '28px',
        'borderLeft': '8px solid #8B5CF6',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'
    }, children=[
        html.H3("🎯 USP: Rescue Capital Intervention Simulator", style={'margin': '0 0 12px 0', 'color': '#1E293B', 'fontWeight': '700'}),
        html.P("Model retention yield recovery by setting rescue budget allocation and target intervention effectiveness.", style={'color': '#64748B', 'fontSize': '14px', 'marginBottom': '18px'}),
        
        html.Div(style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr 1.2fr', 'gap': '20px', 'alignItems': 'center'}, children=[
            html.Div([
                html.Label("Intervention Budget (£):", style={'fontWeight': '600', 'color': '#334155'}),
                dcc.Slider(id='budget-slider', min=5000, max=100000, step=5000, value=25000,
                           marks={i: f"£{i//1000}k" for i in range(10000, 101000, 30000)})
            ]),
            html.Div([
                html.Label("Rescue Success Rate (%):", style={'fontWeight': '600', 'color': '#334155'}),
                dcc.Slider(id='rescue-rate-slider', min=5, max=50, step=5, value=20,
                           marks={i: f"{i}%" for i in range(5, 51, 15)})
            ]),
            html.Div(id='simulator-output', style={
                'backgroundColor': '#F8FAFC',
                'padding': '16px',
                'borderRadius': '12px',
                'border': '1px solid #E2E8F0',
                'textAlign': 'center'
            })
        ])
    ]),

    # CONTROLS & KPI GRID
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '320px 1fr', 'gap': '24px', 'marginBottom': '28px'}, children=[
        
        # Sidebar Controls
        html.Div(style={
            'backgroundColor': '#FFFFFF',
            'padding': '22px',
            'borderRadius': '16px',
            'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'
        }, children=[
            html.H4("🎛️ Terminal Filters", style={'marginTop': '0', 'color': '#0F172A', 'marginBottom': '16px'}),
            
            html.Label("Select Asset Tiers:", style={'fontWeight': '600', 'color': '#475569', 'fontSize': '14px'}),
            dcc.Dropdown(
                id='tier-filter',
                options=[{'label': t, 'value': t} for t in df['Asset_Tier'].unique()],
                value=list(df['Asset_Tier'].unique()),
                multi=True,
                style={'marginBottom': '20px', 'marginTop': '6px'}
            ),

            html.Label("Liquidation Risk Window (%):", style={'fontWeight': '600', 'color': '#475569', 'fontSize': '14px'}),
            dcc.RangeSlider(
                id='risk-slider',
                min=0, max=100, step=5,
                value=[0, 100],
                marks={0: '0%', 50: '50%', 100: '100%'},
            ),
            
            html.Div(style={'marginTop': '24px'}, children=[
                html.Label("Search Customer ID:", style={'fontWeight': '600', 'color': '#475569', 'fontSize': '14px'}),
                dcc.Input(id='search-id', type='text', placeholder='e.g. 12346', style={
                    'width': '100%', 'padding': '10px', 'borderRadius': '8px', 'border': '1px solid #CBD5E1', 'marginTop': '6px'
                })
            ])
        ]),

        # Top Metric Cards
        html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(3, 1fr)', 'gap': '18px'}, children=[
            html.Div(id='kpi-total-celr', style={'borderRadius': '16px', 'padding': '20px', 'color': 'white'}),
            html.Div(id='kpi-distressed-count', style={'borderRadius': '16px', 'padding': '20px', 'color': 'white'}),
            html.Div(id='kpi-avg-yield', style={'borderRadius': '16px', 'padding': '20px', 'color': 'white'})
        ])
    ]),

    # CHARTS GRID
    html.Div(style={'display': 'grid', 'gridTemplateColumns': '1.2fr 1fr', 'gap': '24px', 'marginBottom': '28px'}, children=[
        html.Div(style={'backgroundColor': '#FFFFFF', 'padding': '20px', 'borderRadius': '16px', 'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'}, children=[
            dcc.Graph(id='scatter-plot')
        ]),
        html.Div(style={'backgroundColor': '#FFFFFF', 'padding': '20px', 'borderRadius': '16px', 'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'}, children=[
            dcc.Graph(id='pie-chart')
        ])
    ]),

    # DATA LEDGER TABLE
    html.Div(style={'backgroundColor': '#FFFFFF', 'padding': '22px', 'borderRadius': '16px', 'boxShadow': '0 4px 15px rgba(0,0,0,0.05)'}, children=[
        html.H4("🚨 High-Priority Capital Ledger", style={'marginTop': '0', 'color': '#0F172A'}),
        dash_table.DataTable(
            id='data-table',
            columns=[
                {'name': 'Customer ID', 'id': 'Customer ID'},
                {'name': 'Asset Tier', 'id': 'Asset_Tier'},
                {'name': 'Liquidation Prob', 'id': 'Liquidation_Probability'},
                {'name': 'Projected Yield (£)', 'id': 'Projected_Asset_Yield'},
                {'name': 'CELR Score (£)', 'id': 'CELR'}
            ],
            page_size=8,
            sort_action='native',
            style_header={'backgroundColor': '#F8FAFC', 'fontWeight': 'bold', 'color': '#1E293B', 'borderBottom': '2px solid #E2E8F0'},
            style_cell={'padding': '12px', 'textAlign': 'left', 'fontFamily': 'sans-serif'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#F8FAFC'},
                {'if': {'column_id': 'CELR'}, 'fontWeight': 'bold', 'color': '#EF4444'}
            ]
        )
    ])
])

# CALLBACKS
@app.callback(
    [Output('kpi-total-celr', 'children'),
     Output('kpi-total-celr', 'style'),
     Output('kpi-distressed-count', 'children'),
     Output('kpi-distressed-count', 'style'),
     Output('kpi-avg-yield', 'children'),
     Output('kpi-avg-yield', 'style'),
     Output('scatter-plot', 'figure'),
     Output('pie-chart', 'figure'),
     Output('data-table', 'data'),
     Output('simulator-output', 'children')],
    [Input('tier-filter', 'value'),
     Input('risk-slider', 'value'),
     Input('search-id', 'value'),
     Input('budget-slider', 'value'),
     Input('rescue-rate-slider', 'value')]
)
def update_terminal(selected_tiers, risk_range, search_term, budget, rescue_rate):
    filtered = df[
        (df['Asset_Tier'].isin(selected_tiers)) &
        (df['Liquidation_Probability'] * 100 >= risk_range[0]) &
        (df['Liquidation_Probability'] * 100 <= risk_range[1])
    ]

    if search_term and str(search_term).strip():
        filtered = filtered[filtered['Customer ID'].astype(str).str.contains(str(search_term).strip())]

    total_celr = filtered['CELR'].sum()
    distressed_cnt = len(filtered[filtered['Asset_Tier'] == 'Distressed Equity'])
    avg_yield = filtered['Projected_Asset_Yield'].mean() if not filtered.empty else 0

    kpi1_children = [html.Div("Capital at Risk (CELR)", style={'opacity': 0.8, 'fontSize': '14px'}), html.H2(f"£{total_celr:,.2f}", style={'margin': '4px 0 0 0'})]
    kpi1_style = {'background': 'linear-gradient(135deg, #FF4D4D, #F43F5E)', 'boxShadow': '0 4px 12px rgba(255, 77, 77, 0.35)'}

    kpi2_children = [html.Div("Distressed Assets", style={'opacity': 0.8, 'fontSize': '14px'}), html.H2(f"{distressed_cnt:,}", style={'margin': '4px 0 0 0'})]
    kpi2_style = {'background': 'linear-gradient(135deg, #F59E0B, #D97706)', 'boxShadow': '0 4px 12px rgba(245, 158, 11, 0.35)'}

    kpi3_children = [html.Div("Avg Projected Yield", style={'opacity': 0.8, 'fontSize': '14px'}), html.H2(f"£{avg_yield:,.2f}", style={'margin': '4px 0 0 0'})]
    kpi3_style = {'background': 'linear-gradient(135deg, #10B981, #059669)', 'boxShadow': '0 4px 12px rgba(16, 185, 129, 0.35)'}

    fig_scatter = px.scatter(
        filtered, x='Projected_Asset_Yield', y='Liquidation_Probability',
        color='Asset_Tier', size='CELR', hover_data=['Customer ID'],
        color_discrete_map=COLOR_MAP, title="<b>Risk vs Projected Yield Horizon</b>"
    )
    fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#334155'))

    fig_pie = px.pie(
        filtered, names='Asset_Tier', color='Asset_Tier',
        color_discrete_map=COLOR_MAP, title="<b>Portfolio Tier Distribution</b>", hole=0.4
    )
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#334155'))

    table_df = filtered[['Customer ID', 'Asset_Tier', 'Liquidation_Probability', 'Projected_Asset_Yield', 'CELR']].copy()
    table_df['Liquidation_Probability'] = (table_df['Liquidation_Probability'] * 100).map("{:.1f}%".format)
    table_df['Projected_Asset_Yield'] = table_df['Projected_Asset_Yield'].map("£{:,.2f}".format)
    table_df['CELR'] = table_df['CELR'].map("£{:,.2f}".format)
    table_data = table_df.head(10).to_dict('records')

    distressed_celr = filtered[filtered['Asset_Tier'] == 'Distressed Equity']['CELR'].sum()
    rescued_capital = distressed_celr * (rescue_rate / 100.0)
    net_roi = ((rescued_capital - budget) / budget * 100) if budget > 0 else 0

    sim_ui = [
        html.Div([
            html.Span("Estimated Rescued Capital: ", style={'color': '#64748B', 'fontSize': '14px'}),
            html.Strong(f"£{rescued_capital:,.2f}", style={'color': '#10B981', 'fontSize': '18px'})
        ]),
        html.Div([
            html.Span("Intervention ROI: ", style={'color': '#64748B', 'fontSize': '14px'}),
            html.Strong(f"{net_roi:,.1f}%", style={'color': '#8B5CF6' if net_roi > 0 else '#EF4444', 'fontSize': '18px'})
        ])
    ]

    return (kpi1_children, kpi1_style, kpi2_children, kpi2_style, kpi3_children, kpi3_style,
            fig_scatter, fig_pie, table_data, sim_ui)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False)
