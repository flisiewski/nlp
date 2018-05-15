import plotly
import plotly.offline as py
import plotly.graph_objs as go

def plot_counter(counter):
    x, y = zip(*counter.items())

    data = [go.Bar(
        x=x,
        y=y,
        text=y,
        opacity=0.8,
        textposition = 'auto',
    )]

    layout = go.Layout(
        font=dict(
            size=20,
            color='#000'
        ),
        width=1500,
        height=1000,
        margin=dict(
            b=500,
        ),
    )

    plotly.offline.plot(
        {
            "data": data,
            "layout": layout
        },
        image='jpeg',
    )
