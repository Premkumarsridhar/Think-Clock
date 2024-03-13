from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import json  # This line imports the json module

def create_bode_plot(frequencies, Z):
    # Calculate magnitude and phase
    Z_mag = 20 * np.log10(np.abs(Z))
    Z_phase = np.angle(Z, deg=True)
    
    # Create subplots
    fig = go.Figure()
    
    # Add traces
    fig.add_trace(go.Scatter(x=frequencies, y=Z_mag, mode='lines', name='Magnitude'))
    fig.add_trace(go.Scatter(x=frequencies, y=Z_phase, mode='lines', name='Phase', yaxis='y2'))

    # Update the layout
    fig.update_layout(
        title='Bode Plot',
        xaxis=dict(
            type='log',
            title='Frequency (Hz)'
        ),
        yaxis=dict(
            title='Magnitude (dB)'
        ),
        yaxis2=dict(
            title='Phase (degrees)',
            overlaying='y',
           side='right'
        ),
        template='plotly_dark'  # You can choose other templates or customize the look
    )

    ## Serialize the figure to JSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON