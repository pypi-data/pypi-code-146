template = {
    "layout": {
        "colorway": [
            "rgb(245,82,82)",
            "rgb(20,175,166)",
            "rgb(255,155,75)",
            "rgb(92,210,114)",
            "rgb(66,180,224)",
            "rgb(188,173,221)",         
            "rgb(0,95,151)",
            "rgb(137,48,112)",
            "rgb(70,70,76)",   
        ],
        "margin": {
            "b": 0,
            "t": 20,
            "l": 0,
            "r": 20,
        },
        "legend": {
            "yanchor": "bottom",
            "xanchor": "center",
            "orientation": "h",
            "y": -0.5,
            "x": 0.5,
            # "itemsizing": "constant",
        },
        "font": {"color": "rgb(0,0,0)", "family": "Hind", "size": 10},
        "hovermode": "closest",
        "hoverlabel": {"align": "left"},
        "paper_bgcolor": "rgb(230,230,232)",
        "plot_bgcolor": "rgb(230,230,232)",
        "polar": {
            "bgcolor": "rgb(230,230,232)",
            "angularaxis": {
                "gridcolor": "white",
                "linecolor": "white",
                "showgrid": True,
                "ticks": "outside",
            },
            "radialaxis": {
                "gridcolor": "white",
                "linecolor": "white",
                "showgrid": True,
                "ticks": "outside",
            },
        },
        "ternary": {
            "bgcolor": "rgb(230,230,232)",
            "aaxis": {
                "gridcolor": "white",
                "linecolor": "white",
                "showgrid": True,
                "ticks": "outside",
            },
            "baxis": {
                "gridcolor": "white",
                "linecolor": "white",
                "showgrid": True,
                "ticks": "outside",
            },
            "caxis": {
                "gridcolor": "white",
                "linecolor": "white",
                "showgrid": True,
                "ticks": "outside",
            },
        },
        "coloraxis": {
            "colorbar": {
                "outlinewidth": 0,
                "tickcolor": "black",
                "ticklen": 8,
                "ticks": "outside",
                "tickwidth": 2,
            }
        },
        "colorscale": {
            "sequential": [
                [0.0, "rgb(2,4,25)"],
                [0.06274509803921569, "rgb(24,15,41)"],
                [0.12549019607843137, "rgb(47,23,57)"],
                [0.18823529411764706, "rgb(71,28,72)"],
                [0.25098039215686274, "rgb(97,30,82)"],
                [0.3137254901960784, "rgb(123,30,89)"],
                [0.3764705882352941, "rgb(150,27,91)"],
                [0.4392156862745098, "rgb(177,22,88)"],
                [0.5019607843137255, "rgb(203,26,79)"],
                [0.5647058823529412, "rgb(223,47,67)"],
                [0.6274509803921569, "rgb(236,76,61)"],
                [0.6901960784313725, "rgb(242,107,73)"],
                [0.7529411764705882, "rgb(244,135,95)"],
                [0.8156862745098039, "rgb(245,162,122)"],
                [0.8784313725490196, "rgb(246,188,153)"],
                [0.9411764705882353, "rgb(247,212,187)"],
                [1.0, "rgb(250,234,220)"],
            ],
            "sequentialminus": [
                [0.0, "rgb(2,4,25)"],
                [0.06274509803921569, "rgb(24,15,41)"],
                [0.12549019607843137, "rgb(47,23,57)"],
                [0.18823529411764706, "rgb(71,28,72)"],
                [0.25098039215686274, "rgb(97,30,82)"],
                [0.3137254901960784, "rgb(123,30,89)"],
                [0.3764705882352941, "rgb(150,27,91)"],
                [0.4392156862745098, "rgb(177,22,88)"],
                [0.5019607843137255, "rgb(203,26,79)"],
                [0.5647058823529412, "rgb(223,47,67)"],
                [0.6274509803921569, "rgb(236,76,61)"],
                [0.6901960784313725, "rgb(242,107,73)"],
                [0.7529411764705882, "rgb(244,135,95)"],
                [0.8156862745098039, "rgb(245,162,122)"],
                [0.8784313725490196, "rgb(246,188,153)"],
                [0.9411764705882353, "rgb(247,212,187)"],
                [1.0, "rgb(250,234,220)"],
            ],
        },
        "xaxis": {
            "gridcolor": "white",
            "linecolor": "black",
            "showgrid": True,
            "ticks": "outside",
            "title": {"standoff": 15},
            "zerolinecolor": "white",
            "automargin": True,
        },
        "yaxis": {
            "gridcolor": "white",
            "linecolor": "black",
            "showgrid": True,
            "ticks": "outside",
            "title": {"standoff": 15},
            "zerolinecolor": "black",
            "automargin": True,
        },
        "scene": {
            "xaxis": {
                "backgroundcolor": "rgb(230,230,232)",
                "gridcolor": "white",
                "linecolor": "white",
                "showbackground": True,
                "showgrid": True,
                "ticks": "outside",
                "zerolinecolor": "white",
                "gridwidth": 2,
            },
            "yaxis": {
                "backgroundcolor": "rgb(230,230,232)",
                "gridcolor": "white",
                "linecolor": "white",
                "showbackground": True,
                "showgrid": True,
                "ticks": "outside",
                "zerolinecolor": "white",
                "gridwidth": 2,
            },
            "zaxis": {
                "backgroundcolor": "rgb(230,230,232)",
                "gridcolor": "white",
                "linecolor": "white",
                "showbackground": True,
                "showgrid": True,
                "ticks": "outside",
                "zerolinecolor": "white",
                "gridwidth": 2,
            },
        },
        "shapedefaults": {
            "fillcolor": "rgb(67,103,167)",
            "line": {"width": 0},
            "opacity": 0.5,
        },
        "annotationdefaults": {"arrowcolor": "rgb(67,103,167)"},
        "geo": {
            "bgcolor": "white",
            "landcolor": "rgb(230,230,232)",
            "subunitcolor": "white",
            "showland": True,
            "showlakes": True,
            "lakecolor": "white",
        },
    },
    "data": {
        "histogram2dcontour": [
            {
                "type": "histogram2dcontour",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
                "colorscale": [
                    [0.0, "rgb(2,4,25)"],
                    [0.06274509803921569, "rgb(24,15,41)"],
                    [0.12549019607843137, "rgb(47,23,57)"],
                    [0.18823529411764706, "rgb(71,28,72)"],
                    [0.25098039215686274, "rgb(97,30,82)"],
                    [0.3137254901960784, "rgb(123,30,89)"],
                    [0.3764705882352941, "rgb(150,27,91)"],
                    [0.4392156862745098, "rgb(177,22,88)"],
                    [0.5019607843137255, "rgb(203,26,79)"],
                    [0.5647058823529412, "rgb(223,47,67)"],
                    [0.6274509803921569, "rgb(236,76,61)"],
                    [0.6901960784313725, "rgb(242,107,73)"],
                    [0.7529411764705882, "rgb(244,135,95)"],
                    [0.8156862745098039, "rgb(245,162,122)"],
                    [0.8784313725490196, "rgb(246,188,153)"],
                    [0.9411764705882353, "rgb(247,212,187)"],
                    [1.0, "rgb(250,234,220)"],
                ],
            }
        ],
        "choropleth": [
            {
                "type": "choropleth",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
            }
        ],
        "histogram2d": [
            {
                "type": "histogram2d",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
                "colorscale": [
                    [0.0, "rgb(2,4,25)"],
                    [0.06274509803921569, "rgb(24,15,41)"],
                    [0.12549019607843137, "rgb(47,23,57)"],
                    [0.18823529411764706, "rgb(71,28,72)"],
                    [0.25098039215686274, "rgb(97,30,82)"],
                    [0.3137254901960784, "rgb(123,30,89)"],
                    [0.3764705882352941, "rgb(150,27,91)"],
                    [0.4392156862745098, "rgb(177,22,88)"],
                    [0.5019607843137255, "rgb(203,26,79)"],
                    [0.5647058823529412, "rgb(223,47,67)"],
                    [0.6274509803921569, "rgb(236,76,61)"],
                    [0.6901960784313725, "rgb(242,107,73)"],
                    [0.7529411764705882, "rgb(244,135,95)"],
                    [0.8156862745098039, "rgb(245,162,122)"],
                    [0.8784313725490196, "rgb(246,188,153)"],
                    [0.9411764705882353, "rgb(247,212,187)"],
                    [1.0, "rgb(250,234,220)"],
                ],
            }
        ],
        "heatmap": [
            {
                "type": "heatmap",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
                "colorscale": [
                    [0.0, "rgb(2,4,25)"],
                    [0.06274509803921569, "rgb(24,15,41)"],
                    [0.12549019607843137, "rgb(47,23,57)"],
                    [0.18823529411764706, "rgb(71,28,72)"],
                    [0.25098039215686274, "rgb(97,30,82)"],
                    [0.3137254901960784, "rgb(123,30,89)"],
                    [0.3764705882352941, "rgb(150,27,91)"],
                    [0.4392156862745098, "rgb(177,22,88)"],
                    [0.5019607843137255, "rgb(203,26,79)"],
                    [0.5647058823529412, "rgb(223,47,67)"],
                    [0.6274509803921569, "rgb(236,76,61)"],
                    [0.6901960784313725, "rgb(242,107,73)"],
                    [0.7529411764705882, "rgb(244,135,95)"],
                    [0.8156862745098039, "rgb(245,162,122)"],
                    [0.8784313725490196, "rgb(246,188,153)"],
                    [0.9411764705882353, "rgb(247,212,187)"],
                    [1.0, "rgb(250,234,220)"],
                ],
            }
        ],
        "heatmapgl": [
            {
                "type": "heatmapgl",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
                "colorscale": [
                    [0.0, "rgb(2,4,25)"],
                    [0.06274509803921569, "rgb(24,15,41)"],
                    [0.12549019607843137, "rgb(47,23,57)"],
                    [0.18823529411764706, "rgb(71,28,72)"],
                    [0.25098039215686274, "rgb(97,30,82)"],
                    [0.3137254901960784, "rgb(123,30,89)"],
                    [0.3764705882352941, "rgb(150,27,91)"],
                    [0.4392156862745098, "rgb(177,22,88)"],
                    [0.5019607843137255, "rgb(203,26,79)"],
                    [0.5647058823529412, "rgb(223,47,67)"],
                    [0.6274509803921569, "rgb(236,76,61)"],
                    [0.6901960784313725, "rgb(242,107,73)"],
                    [0.7529411764705882, "rgb(244,135,95)"],
                    [0.8156862745098039, "rgb(245,162,122)"],
                    [0.8784313725490196, "rgb(246,188,153)"],
                    [0.9411764705882353, "rgb(247,212,187)"],
                    [1.0, "rgb(250,234,220)"],
                ],
            }
        ],
        "contourcarpet": [
            {
                "type": "contourcarpet",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
            }
        ],
        "contour": [
            {
                "type": "contour",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
                "colorscale": [
                    [0.0, "rgb(2,4,25)"],
                    [0.06274509803921569, "rgb(24,15,41)"],
                    [0.12549019607843137, "rgb(47,23,57)"],
                    [0.18823529411764706, "rgb(71,28,72)"],
                    [0.25098039215686274, "rgb(97,30,82)"],
                    [0.3137254901960784, "rgb(123,30,89)"],
                    [0.3764705882352941, "rgb(150,27,91)"],
                    [0.4392156862745098, "rgb(177,22,88)"],
                    [0.5019607843137255, "rgb(203,26,79)"],
                    [0.5647058823529412, "rgb(223,47,67)"],
                    [0.6274509803921569, "rgb(236,76,61)"],
                    [0.6901960784313725, "rgb(242,107,73)"],
                    [0.7529411764705882, "rgb(244,135,95)"],
                    [0.8156862745098039, "rgb(245,162,122)"],
                    [0.8784313725490196, "rgb(246,188,153)"],
                    [0.9411764705882353, "rgb(247,212,187)"],
                    [1.0, "rgb(250,234,220)"],
                ],
            }
        ],
        "surface": [
            {
                "type": "surface",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
                "colorscale": [
                    [0.0, "rgb(2,4,25)"],
                    [0.06274509803921569, "rgb(24,15,41)"],
                    [0.12549019607843137, "rgb(47,23,57)"],
                    [0.18823529411764706, "rgb(71,28,72)"],
                    [0.25098039215686274, "rgb(97,30,82)"],
                    [0.3137254901960784, "rgb(123,30,89)"],
                    [0.3764705882352941, "rgb(150,27,91)"],
                    [0.4392156862745098, "rgb(177,22,88)"],
                    [0.5019607843137255, "rgb(203,26,79)"],
                    [0.5647058823529412, "rgb(223,47,67)"],
                    [0.6274509803921569, "rgb(236,76,61)"],
                    [0.6901960784313725, "rgb(242,107,73)"],
                    [0.7529411764705882, "rgb(244,135,95)"],
                    [0.8156862745098039, "rgb(245,162,122)"],
                    [0.8784313725490196, "rgb(246,188,153)"],
                    [0.9411764705882353, "rgb(247,212,187)"],
                    [1.0, "rgb(250,234,220)"],
                ],
            }
        ],
        "mesh3d": [
            {
                "type": "mesh3d",
                "colorbar": {
                    "outlinewidth": 0,
                    "tickcolor": "black",
                    "ticklen": 8,
                    "ticks": "outside",
                    "tickwidth": 2,
                },
            }
        ],
        "scatter": [
            {
                "type": "scatter",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "parcoords": [
            {
                "type": "parcoords",
                "line": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "scatterpolargl": [
            {
                "type": "scatterpolargl",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "bar": [
            {
                "error_x": {"color": "black"},
                "error_y": {"color": "black"},
                "marker": {"line": {"color": "rgb(230,230,232)", "width": 0.5}},
                "type": "bar",
            }
        ],
        "scattergeo": [
            {
                "type": "scattergeo",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "scatterpolar": [
            {
                "type": "scatterpolar",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "histogram": [
            {
                "type": "histogram",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "scattergl": [
            {
                "type": "scattergl",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "scatter3d": [
            {
                "type": "scatter3d",
                "line": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "scattermapbox": [
            {
                "type": "scattermapbox",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "scatterternary": [
            {
                "type": "scatterternary",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "scattercarpet": [
            {
                "type": "scattercarpet",
                "marker": {
                    "colorbar": {
                        "outlinewidth": 0,
                        "tickcolor": "black",
                        "ticklen": 8,
                        "ticks": "outside",
                        "tickwidth": 2,
                    }
                },
            }
        ],
        "carpet": [
            {
                "aaxis": {
                    "endlinecolor": "black",
                    "gridcolor": "white",
                    "linecolor": "white",
                    "minorgridcolor": "white",
                    "startlinecolor": "black",
                },
                "baxis": {
                    "endlinecolor": "black",
                    "gridcolor": "white",
                    "linecolor": "white",
                    "minorgridcolor": "white",
                    "startlinecolor": "black",
                },
                "type": "carpet",
            }
        ],
        "table": [
            {
                "cells": {
                    "fill": {"color": "rgb(231,231,240)"},
                    "line": {"color": "white"},
                },
                "header": {
                    "fill": {"color": "rgb(183,183,191)"},
                    "line": {"color": "white"},
                },
                "type": "table",
            }
        ],
        "barpolar": [
            {
                "marker": {"line": {"color": "rgb(230,230,232)", "width": 0.5}},
                "type": "barpolar",
            }
        ],
        "pie": [{"automargin": True, "type": "pie"}],
    },
}