import dash
from dash.dependencies import Input, Output, State
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from reportlab.graphics.shapes import *
from PIL import Image
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go

from sld import create_SLD
from schematic import create_schematic


# Colors
prevalon_purple = 'rgb(72,49,120)'
prevalon_lavender = 'rgb(166,153,193)'
prevalon_yellow = 'rgb(252,215,87)'
prevalon_cream = 'rgb(245,225,164)'
prevalon_slate = 'rgb(208,211,212)'
prevalon_gray = 'rgb(99,102,106)'


fig = go.Figure()
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(255,255,255,0)',
    xaxis=dict(showgrid=False, visible=False),
    yaxis=dict(showgrid=False, visible=False),
)


# Register the page in Dash
dash.register_page(__name__, name = "Home", path='/', order=1)


# Define the layout of the website
layout = dbc.Container([

dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Heron Link Sizing Tool", 
                       style={'color': prevalon_purple, 'text-align': 'center'}),
                        xs=12, sm=12, md=12, lg=12, xl=12)
    ], className="bg-transparent", justify='around', align='center'),
    ], fluid=True, className="text-white text-center", style={"backgroundColor": "rgba(255,255,255,0.3)"}),

dbc.Container([
    
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H5("Project Details",
                        style={'color':'black', 'text-align': 'left'}),
                        xs=12, sm=12, md=12, lg=12, xl=12)
    ], justify='around', align='left'),
    
    dbc.Row([
        dbc.Col([
            html.P('Project Name'),
            dbc.Input(id='inp_projnm', value="Pilot Project", className='form-control form-control-sm'),
        ], xs=12, sm=12, md=12, lg=2, xl=2),

        dbc.Col([
            html.P('Project Location'),
            dbc.Input(id='inp_projloct', value="Scotts Valley", className='form-control form-control-sm'),
            ], xs=12, sm=12, md=12, lg=2, xl=2),
    ], justify='around'),

    
    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H5("Grid Overview",
                        style={'color':'black', 'text-align': 'left'}),
                        xs=12, sm=12, md=12, lg=12, xl=12)
    ], justify='around', align='left'),

    dbc.Row([
        dbc.Col([
            html.Img(
                src="/assets/solar_panel_icon.png",  # Path to the battery icon
                style={"width": "150px", "marginBottom": "10px"}
            ),
            html.P('DC Power Sources - Solar'),
        ], xs=12, sm=12, md=12, lg=4, xl=4),

        dbc.Col([
            html.Img(
                src="/assets/battery_icon.png",  # Path to the battery icon
                style={"width": "150px", "marginBottom": "10px"}, 
            ),
            html.P('DC Power Sources - Storage'),
            ], xs=12, sm=12, md=12, lg=4, xl=4),

        dbc.Col([
            html.Img(
                src="/assets/data_center.png",  # Path to the battery icon
                
                style={"width": "150px", "marginBottom": "10px"}
            ),
            html.P('DC Loads (ex. Datacenters)'),
            ], xs=12, sm=12, md=12, lg=4, xl=4),

    ], justify='around'),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.P('Rated Power (MW) - Solar'),
            dbc.Input(id='inp_solar_pwr', type='number', value=100, min=0, className='form-control form-control-sm text-center'),
            html.P(id='err_solar_pwr', className='text-danger', children=''),  # <-- inline error
        ], xs=12, sm=12, md=12, lg=2, xl=2),

        dbc.Col([
            html.P('Rated Power (MW) - Storage'),
            dbc.Input(id='inp_storage_pwr', type='number', value=100, min=0, className='form-control form-control-sm text-center'),
            html.P(id='err_storage_pwr', className='text-danger', children=''),  # <-- inline error
            ], xs=12, sm=12, md=12, lg=2, xl=2),

        dbc.Col([
            html.P('DC Load Rating (MW)'),
            dbc.Input(id='inp_dc_load', type='number', value=100, min=0, className='form-control form-control-sm text-center'),
            html.P(id='err_dc_load', className='text-danger', children=''),  # <-- inline error
            ], xs=12, sm=12, md=12, lg=2, xl=2),
    
    ], justify='around'),
    
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.P('DC Voltage Range - Solar', style={'whiteSpace': 'normal', 'textAlign': 'center'}),
            dcc.RangeSlider(
                500, 1500, step=200, value=[700, 1100], id='dc_voltage_solar',
                marks={i: {"label": str(i), "style": {"color": "white"}} for i in range(500, 1501, 100)}            
            ),
            html.P(id='err_dc_voltage_solar', className='text-danger', children=''),  # <-- inline error
        ], xs=12, sm=12, md=12, lg=2, xl=4),

        dbc.Col([
            html.P('DC Voltage Range - Storage', style={'whiteSpace': 'normal', 'textAlign': 'center'}),
            dcc.RangeSlider(
                800, 1500, step=100, value=[1100, 1500], id='dc_voltage_storage',
                marks={i: {"label": str(i), "style": {"color": "white"}} for i in range(800, 1501, 100)}            
            ),
            html.P(id='err_dc_voltage_storage', className='text-danger', children=''),  # <-- inline error
        ], xs=12, sm=12, md=12, lg=2, xl=4),

        dbc.Col([
            html.P('DC Voltage Range - DC Load', style={'whiteSpace': 'normal', 'textAlign': 'center'}),
            dcc.RangeSlider(
                400, 900, step=200, value=[750, 850], id='dc_voltage_load',
                className="text-white text-center", 
                marks={i: {"label": str(i), "style": {"color": "white"}} for i in range(400, 901, 100)}            
                ),
            html.P(id='err_dc_voltage_load', className='text-danger', children=''),  # <-- inline error
        ], xs=12, sm=12, md=12, lg=2, xl=4),
    ], justify='around'),

    html.Br(),
    html.Br(),

    dbc.Row([
        dbc.Col(html.H5("Project Interconnect Overview",
                        style={'color':'black', 'text-align': 'left'}),
                        xs=12, sm=12, md=12, lg=12, xl=12)
    ], justify='around', align='left'),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.P('Interconnect Voltage (kV)'),
            dbc.Input(id='inp_mv_voltage', type='number', value=34.5, min=12, max=34.5, className='form-control form-control-sm text-center'),
            html.P(id='err_mv_voltage', className='text-danger', children=''),  # <-- inline error
        ], xs=12, sm=12, md=12, lg=2, xl=2),

        dbc.Col([
            html.P('Required Power Factor'),
            dbc.Input(id='inp_pwr_factor', type='number', value=0.95, min=0, max=1, className='form-control form-control-sm text-center'),
            html.P(id='err_pwr_factor', className='text-danger', children=''),  # <-- inline error
            ], xs=12, sm=12, md=12, lg=2, xl=2),

        dbc.Col([
            html.P('Max Site Temp'),
            dbc.Input(id='inp_max_temp', type='number', value=45, min=30, max=60, className='form-control form-control-sm text-center'),
            html.P(id='err_max_temp', className='text-danger', children=''),  # <-- inline error
            ], xs=12, sm=12, md=12, lg=2, xl=2),

    ], justify='around'),

    html.Br(),

    dbc.Row([
        dbc.Col([
            html.P('Step 1 - Run Sizing', id='generate_sizing', className="btn btn-primary mt-4")
        ], xs=12, sm=12, md=12, lg=12, xl=12),

    ], justify='around'),

    dbc.Row([
        dbc.Col([
            dbc.Spinner(dcc.Graph(id = "plot",
                                  figure = fig,
                                  style = {"height":"80vh"}, className="bg-transparent"),), 

                ], xs=12, sm=12, md=12, lg=8, xl=8),

        dbc.Col([
    
    html.Br(),
    html.Br(),

            html.H5("Downloads Section - ",
                                    style={'color':'black', 'text-align': 'left'}),
    html.Br(),
    
            dbc.Spinner(html.A('Step 2 - Download Single Line Diagram', 
                                   id='download_sld', 
                                   href='',  
                                   style={'width':'300px'},
                                   className="btn bg-warning mt-4")
                                     ),
                ], xs=8, sm=8, md=8, lg=4, xl=4),

        
    ], justify='left', className="bg-transparent"),



], fluid=True, className="text-white text-center", style={"backgroundColor": "rgba(255,255,255,0.3)"}),

], fluid=True)


@dash.callback(
    Output('generate_sizing', 'n_clicks'),
    Output('plot', 'figure'),
    Output('download_sld', 'href'),
    [Input('inp_projnm', 'value'),
     Input('inp_projloct', 'value'),
     Input('inp_solar_pwr', 'value'),
     Input('inp_storage_pwr', 'value'),
     Input('inp_dc_load', 'value'),
     Input('dc_voltage_solar', 'value'),
     Input('dc_voltage_storage', 'value'),
     Input('dc_voltage_load', 'value'),
     Input('inp_mv_voltage', 'value'),
     Input('inp_pwr_factor', 'value'),
     Input('inp_max_temp', 'value'),
     Input('generate_sizing', 'n_clicks'),
     ]
)
def calculate_number_sst(proj_name, proj_location, solar_mw, storage_mw, dc_load_mw, 
                         solar_dc_vol, storage_dc_vol, load_dc_vol, mv_vol, required_pf, max_temp, n_clicks):
    if n_clicks:
        # print(solar_mw, storage_mw, dc_load_mw, solar_dc_vol, storage_dc_vol, load_dc_vol, mv_vol, pf, max_temp)

        sst_model = "Heron Link"

        df_sst_details = pd.read_excel("sst_details.xlsx")

        max_sst_per_skid = int(df_sst_details[sst_model].iloc[0])
        
        # Perform linear interpolation to find kva at max_temp
        kVA_list = df_sst_details[sst_model].iloc[1:]
        temp_list = [i for i in range(40, 61, 5)]
        if np.interp(max_temp, temp_list, kVA_list) > kVA_list.iloc[0]:
            kVA_at_max_temp = kVA_list.iloc[0]
        else:
            kVA_at_max_temp = np.interp(max_temp, temp_list, kVA_list)

        pcs_string = f'upto {(kVA_at_max_temp*max_sst_per_skid):,.0f}kVA'
        temp_string = f'at {(max_temp):,.0f} deg C'
            
        def kVA_at_sst(mw_rating):

            kVAR_losses = 0.09 #9% of Reactive Power losses due to MV AC cables
            kW_losses = 0.03 #3% losses on Active Power due to MV AC Cables

            kW_at_POM = mw_rating*1000
            kVA_at_POM = kW_at_POM/required_pf
            kVAR_at_POM = np.sqrt(kVA_at_POM**2 - kW_at_POM**2)
            
            kVAR_at_sst = kVAR_at_POM/(1-kVAR_losses)
            kW_at_sst = kW_at_POM/(1-kW_losses)

            kVA_at_sst = np.sqrt(kW_at_sst**2 + kVAR_at_sst**2)
            return kVA_at_sst

        # 1 - Find out how many SSTs are needed for Solar / Storage / DC Load
        number_ssts_solar = int(math.ceil(kVA_at_sst(solar_mw)/kVA_at_max_temp/max_sst_per_skid) * max_sst_per_skid)
        number_ssts_storage = int(math.ceil(kVA_at_sst(storage_mw)/kVA_at_max_temp/max_sst_per_skid) * max_sst_per_skid)
        number_ssts_dc_load = int(math.ceil(kVA_at_sst(dc_load_mw)/kVA_at_max_temp/max_sst_per_skid) * max_sst_per_skid)

        skid_kVA_at_max_temp = kVA_at_max_temp*max_sst_per_skid

        # 1 - Find out how many SST skids are needed for Solar / Storage / DC Load
        number_skids_solar = int(math.ceil(number_ssts_solar/max_sst_per_skid))
        number_skids_storage = int(math.ceil(number_ssts_storage/max_sst_per_skid))
        number_skids_dc_load = int(math.ceil(number_ssts_dc_load/max_sst_per_skid))

        schematic_figure = create_schematic(solar_mw, storage_mw, dc_load_mw, number_ssts_solar, number_ssts_storage, mv_vol, 
                     number_ssts_dc_load, number_skids_solar, number_skids_storage, number_skids_dc_load)
        
        sld_diagram_pdf = '/download/{}'.format(create_SLD(proj_location, proj_name, mv_vol, skid_kVA_at_max_temp, max_sst_per_skid, 
                                                            solar_mw, number_skids_solar, solar_dc_vol, 
                                                            storage_mw, number_skids_storage, storage_dc_vol, 
                                                            dc_load_mw, number_skids_dc_load, load_dc_vol, 
                                                            pcs_string, temp_string))

        n_clicks = 0
        return n_clicks, schematic_figure, sld_diagram_pdf
    else:
        raise PreventUpdate


# --------- Simple inline validation for red error messages ---------
@dash.callback(
    Output('err_solar_pwr', 'children'),
    Output('err_storage_pwr', 'children'),
    Output('err_dc_load', 'children'),
    Output('err_dc_voltage_solar', 'children'),
    Output('err_dc_voltage_storage', 'children'),
    Output('err_dc_voltage_load', 'children'),
    Output('err_mv_voltage', 'children'),
    Output('err_pwr_factor', 'children'),
    Output('err_max_temp', 'children'),
    Input('inp_solar_pwr', 'value'),
    Input('inp_storage_pwr', 'value'),
    Input('inp_dc_load', 'value'),
    Input('dc_voltage_solar', 'value'),
    Input('dc_voltage_storage', 'value'),
    Input('dc_voltage_load', 'value'),
    Input('inp_mv_voltage', 'value'),
    Input('inp_pwr_factor', 'value'),
    Input('inp_max_temp', 'value'),
)
def simple_inline_validation(solar_mw, storage_mw, dc_load_mw,
                             solar_rng, storage_rng, load_rng,
                             mv_kv, pf, max_temp):
    # Defaults: no error text
    errors = [""] * 9

    # MWs >= 0
    if solar_mw is None or solar_mw < 0:
        errors[0] = "Solar MW must be ≥ 0."
    if storage_mw is None or storage_mw < 0:
        errors[1] = "Storage MW must be ≥ 0."
    if dc_load_mw is None or dc_load_mw < 0:
        errors[2] = "DC Load MW must be ≥ 0."

    # Range checker helper
    def check_range(rng, lo, hi, label):
        if not rng or len(rng) != 2:
            return f"{label} must have two values."
        a, b = rng
        if a > b:
            return f"{label}: min cannot exceed max."
        if a < lo or b > hi:
            return f"{label} must be between {lo} and {hi}."
        return ""

    errors[3] = check_range(solar_rng,   500, 1500, "Solar DC Voltage")
    errors[4] = check_range(storage_rng, 800, 1500, "Storage DC Voltage")
    errors[5] = check_range(load_rng,    400,  900, "DC Load Voltage")

    # Interconnect voltage
    if mv_kv is None or not (12 <= mv_kv <= 34.5):
        errors[6] = "Interconnect Voltage must be between 12 and 34.5 kV."

    # Power factor
    if pf is None or not (0 <= pf <= 1):
        errors[7] = "Power Factor must be between 0 and 1.0."

    # Max temp
    if max_temp is None or not (30 <= max_temp <= 60):
        errors[8] = "Max Site Temp must be between 30°C and 60°C."

    return errors
    
# --------- Enable/disable Run button based on errors ---------
@dash.callback(
    Output('generate_sizing', 'disable_n_clicks'),
    Input('err_solar_pwr', 'children'),
    Input('err_storage_pwr', 'children'),
    Input('err_dc_load', 'children'),
    Input('err_dc_voltage_solar', 'children'),
    Input('err_dc_voltage_storage', 'children'),
    Input('err_dc_voltage_load', 'children'),
    Input('err_mv_voltage', 'children'),
    Input('err_pwr_factor', 'children'),
    Input('err_max_temp', 'children'),
)
def toggle_run_button(*err_texts):
    """Disable Run Sizing if ANY error message is non-empty."""
    has_errors = any(bool(msg) for msg in err_texts)
    return has_errors