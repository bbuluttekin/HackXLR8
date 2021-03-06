import random
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import Line, VBar
from bokeh.plotting import figure
from bokeh.charts import Line, Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def main():
    bars_count = 7
    data = {"days": [], "usage": [], "costs": []}
    for i in range(1, bars_count + 1):
        data['days'].append(i)
        data['usage'] = [5.7, 12.3, 5.7, 12.3, 5.7, 5.9, 6.2]
        data['costs'] = [6.58, 11.350, 6.9, 10.9, 6.7, 6.2, 5.8]
        hover = create_hover_tool()
        plot = create_line_chart(data, "Usage per day", "days",
                            "usage", hover_tool=hover)
        script, div = components(plot)
        hover2 = create_hover_tool()
        plot2 = create_line_chart(data, "Forecasted Usage per day", "days",
                            "costs", fill_color="#e26c31", hover_tool=hover2)
        script2, div2 = components(plot2)


    return render_template("template.html", bars_count=bars_count, the_div=div, the_script=script, div_2=div2, script_2=script2)

def create_hover_tool():
    # we'll code this function in a moment
     """Generates the HTML for the Bokeh's hover data tool on our graph."""
     hover_html = """<div><span class="hover-tooltip">$x</span></div><div><span class="hover-tooltip">@usage Wh</span></div><div><span class="hover-tooltip">$@costs{0.00}</span></div>"""
     return HoverTool(tooltips=hover_html)


def create_line_chart(data, title, x_name, y_name, hover_tool=None,
                     width=800, height=300, fill_color="#fcb900"):
    """Creates a bar chart plot with the exact styling for the centcom
       dashboard. Pass in data as a dictionary, desired plot title,
       name of x axis, y axis and the hover tool HTML.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666",background_fill_alpha=0.0, border_fill_alpha=0.0)

    #glyph = Line(x=x_name, y=y_name, line_color="#F46D43", line_width=6, line_alpha=0.6)
    glyph = VBar(x=x_name, top=y_name, bottom=0, width=1,
                 fill_color=fill_color)
    #glyph2 = VBar(x=x_name, top='costs', bottom=0, width=1, fill_color='#e12127')
    #e12127
    plot.add_glyph(source, glyph)
    #plot.add_glyph(source, glyph2)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "usage"
    plot.ygrid.grid_line_alpha = 0.1
    plot.xaxis.axis_label = "days"
    plot.xaxis.major_label_orientation = 1
    return plot


if __name__ == '__main__':
    app.run(debug=True)
