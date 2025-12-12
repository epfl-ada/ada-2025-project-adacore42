import streamlit as st
import plotly.graph_objects as go
import numpy as np
from _webappp.assets.app_content import PagesData

from _webappp.assets.app_definitions import get_absolute_project_root
get_absolute_project_root()
from src.utils.web_app_plots.app_plots import PWA
PWA.set_root_path()

plots = PWA.load_plots()


pageData = PagesData.AXIS_1.value

pageData.page_firstBlock()
"Gnangana"

# Un exemple de coment plotter un plot a l'aide de plotly
if plots:
    plot = plots[0]

    # Plotly line figure
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=plot.Y_data,
            y=plot.X_data,
            mode="lines",
            line=dict(width=1),
            name=plot.title,
        )
    )

    fig.update_layout(
        title=plot.title,
        xaxis_title=plot.X_label,
        yaxis_title=plot.Y_label,
        template="plotly_white",
        height=400,
        margin=dict(l=40, r=40, t=50, b=40),
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("No stored plots found.")

