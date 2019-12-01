"""this contains visualisation methods"""
import plotly.graph_objects as go
from plotly.offline import plot

def draw_sunburst(
        sunburst_data
        ):
    """
    sunburst_data: dict{}
        labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
        values=[10, 14, 160, 10, 2, 6, 6, 4, 4],
    """
    sunburst = go.Sunburst(
        labels=sunburst_data['labels'],
        parents=sunburst_data['parents'],
        values=sunburst_data['values'],
    )
    fig =go.Figure(sunburst)
    # Update layout for tight margin
    # See https://plot.ly/python/creating-and-updating-figures/
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    print("[1] Generate a .html file (Choose this if you are on Docker\
    \n[2] Open in the browser directly")
    offline = input() == '1'
    if not offline:
        fig.show()
    else:
        plot([sunburst],auto_open=False,filename='your_todag.html')
