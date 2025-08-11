import plotly.graph_objects as go

# Colors
prevalon_purple = 'rgb(72,49,120)'
prevalon_lavender = 'rgb(166,153,193)'
prevalon_yellow = 'rgb(252,215,87)'
prevalon_cream = 'rgb(245,225,164)'
prevalon_slate = 'rgb(208,211,212)'
prevalon_gray = 'rgb(99,102,106)'



def create_schematic(solar_mw, storage_mw, dc_load_mw, kVA_at_max_temp, max_sst_per_skid, number_ssts_solar, number_ssts_storage, mv_vol, 
                     number_ssts_dc_load, number_skids_solar, number_skids_storage, number_skids_dc_load):
    
        fig = go.Figure()

        # 1) Add all the block shapes
        shapes = [
            # Vertical bus line
            dict(type='line', x0=5.0, y0=2.0, x1=5.0, y1=10.0,
                line=dict(color='black', width=4)),

            # Busbar
            dict(type='rect', x0=4.1, y0=4.5, x1=5.9, y1=5,
                line=dict(color='black', width=2), fillcolor='white'),
        ]


        if solar_mw > 0:
               shapes.extend([
                    # Solar
                    dict(type='rect', x0=0.5, y0=8.0, x1=2.5, y1=9.0,
                        line=dict(color='orange', width=2), fillcolor='white'),
                    dict(type='rect', x0=3.0, y0=8.0, x1=4.0, y1=9.0,
                        line=dict(color='black', width=2), fillcolor='white'),
               ])
        
        if storage_mw > 0:
               shapes.extend([
                    # BESS
                    dict(type='rect', x0=0.5, y0=6.0, x1=2.5, y1=7.0,
                        line=dict(color=prevalon_purple, width=2), fillcolor='white'),
                    dict(type='rect', x0=3.0, y0=6.0, x1=4.0, y1=7.0,
                        line=dict(color='black', width=2), fillcolor='white'),
               ])        

        if dc_load_mw > 0:
               shapes.extend([
                    # Right‐side blocks - DC Load
                    dict(type='rect', x0=6.0, y0=7, x1=7.0, y1=8,
                        line=dict(color='black', width=2), fillcolor='white'),
                    dict(type='rect', x0=7.5, y0=7, x1=9.5, y1=8,
                        line=dict(color='green', width=2), fillcolor='white'),
                ])


        fig.update_layout(shapes=shapes)

        # 2) Add text labels + arrows
        annotations = [
            # Label - Common AC Bus Bar
            dict(x=5, y=4.75, text=f'{mv_vol}kV Common AC Busbar', showarrow=False, font=dict(size=10)),

        ]

        if solar_mw > 0:
               annotations.extend([
                    # Labels
                    dict(x=1.5, y=8.5, text=f'{solar_mw}MW Solar', showarrow=False, font=dict(size=14)),
                    dict(x=3.5, y=8.75, text=f'{number_ssts_solar} X Heron Links', showarrow=False, font=dict(size=9)),
                    dict(x=3.5, y=8.25, text=f'{number_skids_solar} X {kVA_at_max_temp*max_sst_per_skid*0.001:,.1f}MVA Skids', showarrow=False, font=dict(size=9)),

                    # Arrows b/w Solar
                    dict(
                        x=3.0, y=8.5, ax=2.5, ay=8.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),

                    dict(
                        x=5.0, y=8.5, ax=4, ay=8.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),
               ])
                   
        if storage_mw > 0:
               annotations.extend([
                    # Labels
                    dict(x=1.5, y=6.5, text=f'{storage_mw}MW BESS', showarrow=False, font=dict(size=14)),
                    dict(x=3.5, y=6.75, text=f'{number_ssts_storage} X Heron Links', showarrow=False, font=dict(size=9)),
                    dict(x=3.5, y=6.25, text=f'{number_skids_storage} X {kVA_at_max_temp*max_sst_per_skid*0.001:,.1f}MVA Skids', showarrow=False, font=dict(size=9)),

                    # Arrows b/w BESS
                    dict(
                        x=3, y=6.5, ax=2.5, ay=6.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),
                    dict(
                        x=2.5, y=6.5, ax=3.0, ay=6.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),

                    dict(
                        x=5.0, y=6.5, ax=4, ay=6.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),

                    dict(
                        x=4, y=6.5, ax=5, ay=6.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),
                ])

        if dc_load_mw > 0:
               annotations.extend([
                    # Labels
                    dict(x=8.5, y=7.5, text=f'{dc_load_mw}MW DC Load', showarrow=False, font=dict(size=14)),
                    dict(x=6.5, y=7.75, text=f'{number_ssts_dc_load} X Heron Links', showarrow=False, font=dict(size=9)),
                    dict(x=6.5, y=7.25, text=f'{number_skids_dc_load} X {kVA_at_max_temp*max_sst_per_skid*0.001:,.1f}MVA Skids', showarrow=False, font=dict(size=9)),

                    # Arrows b/w DC Load
                    dict(
                        x=6, y=7.5, ax=5, ay=7.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),
                    dict(
                        x=7.5, y=7.5, ax=7, ay=7.5,
                        xref='x', yref='y', axref='x', ayref='y',
                        showarrow=True, arrowhead=2, arrowwidth=2
                    ),
                ])
                   

        fig.update_layout(
            title=dict(
                text="System Schematic",
                font=dict(size=18, color="black"),
                x=0.5,  # Center the title
                y = 0.9,
                xanchor="center"
            ),
            annotations=annotations,
            xaxis=dict(visible=False, range=[0, 10]),
            yaxis=dict(visible=False, range=[4, 11]),
            margin=dict(l=20, r=20, t=20, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(255,255,255,0)'
        )

        return fig