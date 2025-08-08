from dash import Dash, html, dcc
from PIL import Image
import dash
import dash_bootstrap_components as dbc
from flask import send_file
import os

# Colors
prevalon_purple = 'rgb(72,49,120)'
prevalon_lavender = 'rgb(166,153,193)'
prevalon_yellow = 'rgb(252,215,87)'
prevalon_cream = 'rgb(245,225,164)'
prevalon_slate = 'rgb(208,211,212)'
prevalon_gray = 'rgb(99,102,106)'


dash_app = Dash(__name__, use_pages=True,
                external_stylesheets=["https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/litera/bootstrap.min.css",
                                      "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )

server = dash_app.server

logo = Image.open("logo.png")

page_layout = []
for page in dash.page_registry.values():
    page_layout.append(dbc.NavItem(dbc.NavLink(page["name"], href=page["path"], active="exact"),))


dash_app.layout = dbc.Container([

    dbc.Row([
        dbc.Col(
            html.A(
                children=html.Img(src=logo, width=180),
                href='https://www.heronpower.com/why',
                target="_blank", # creates a new tab
            ),
            width=2,  # Fixed width for logo on the left
            style={'display': 'flex', 'align-items': 'center'}  # Align logo vertically
        ),
    dbc.Col(width=9),  # Empty column to balance the layout
    dbc.NavbarSimple(
                    children = page_layout,
                    dark=True,
                    className="bg-transparent",
                ),
    ], style={'width': '100%'}),

    html.A(
        dbc.Container([
                        dash.page_container, 
                        ], fluid=True, ), 
                        ), 


  ], fluid=True, style={
    "backgroundImage": "url('https://images.squarespace-cdn.com/content/v1/66e0bdbafbbd3837e98e5b79/bc21a2b7-061e-493f-b4d1-8f67d3396b5f/Back3.png')",  # Path to your image
    "backgroundSize": "200%",  # Ensure the image covers the entire container
    # "backgroundPosition": "center",  # Center the image
    # "minHeight": "120vh",  # Ensure the container takes the full height of the viewport
    # "padding": "20px",  # Add some padding for better layout
    "backgroundRepeat": "no-repeat",  # Prevent the image from repeating
    # "backgroundColor": "rgba(255, 255, 255, 1)" #/* Semi-transparent overlay */
})

@dash_app.server.route('/download/<path:path>')
def serve_static(path):
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    dash_app.run(debug=True)