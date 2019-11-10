"""this contains visualisation methods"""
import plotly.graph_objects as go

def draw_sunburst(
        sunburst_data
        ):
    """
    sunburst_data: dict{}
        labels=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parents=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
        values=[10, 14, 160, 10, 2, 6, 6, 4, 4],
    """
    fig =go.Figure(go.Sunburst(
        labels=sunburst_data['labels'],
        parents=sunburst_data['parents'],
        values=sunburst_data['values'],
    ))
    # Update layout for tight margin
    # See https://plot.ly/python/creating-and-updating-figures/
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    fig.show()
