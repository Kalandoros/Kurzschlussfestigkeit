# import dependencies
import plotly.express as px     # `import as` enables abbreviation
import pandas as pd
import solara

# define global variables
df = px.data.iris()
columns = list(df.columns)

# define reactive variables
x_axis = solara.reactive("sepal_length")
y_axis = solara.reactive("sepal_width")
click_data = solara.reactive(None)

# define function to find nearest neighboring data points
def find_nearest_neighbours(df, xcol, ycol, x, y, n=10):
    df = df.copy()
    df["distance"] = ((df[xcol] - x)**2 + (df[ycol] - y)**2)**0.5
    return df.sort_values('distance')[1:n+1]

def Layout(children):
    route, routes = solara.use_route()
    #dark_effective = solara.lab.use_dark_effective()
    return solara.AppLayout(children=children,  color=None, sidebar_open=False)  # if dark_effective else "primary")

# define app's main component
@solara.component
def Page():

    def toggle_settings():
        pass

    with solara.AppBar():
        solara.lab.ThemeToggle()
        solara.Button(icon_name="settings", on_click=toggle_settings, icon=True)
    with solara.AppBarTitle():
        solara.Text("Mechanische Kurzschlussfestigkeit")
    with solara.Sidebar():
        with solara.Card(title="Menu", subtitle="Kurzschlussfestigkeit", margin=0, elevation=0, ):
            with solara.Column():
                with solara.lab.Tab("Leiterseile", icon_name="mdi-flash"):
                    solara.Markdown("Hello")
                with solara.lab.Tab("Biegefeste Leiter", icon_name="mdi-flash-outline"):
                    solara.Markdown("World")
        """
        with solara.Card(title="", subtitle="Erdung", margin=0, elevation=0):
            with solara.Column():
                with solara.lab.Tab("Tab 3", icon_name="mdi-arrow-down-circle"):
                    solara.Markdown("Hello")
                with solara.lab.Tab("Tab 4", icon_name="mdi-arrow-down-circle-outline"):
                    solara.Markdown("World")
        """
    # add scatter plot using plotly express
    fig = px.scatter(df, x_axis.value, y_axis.value, color="species", custom_data=[df.index])

    # store click data
    if click_data.value is not None:
        x = click_data.value["points"]["xs"][0]
        y = click_data.value["points"]["ys"][0]

        # add a star indicator upon clicking data point
        fig.add_trace(px.scatter(x=[x], y=[y], text=["⭐️"]).data[0])

        # reactively obtain nearest neighbors upon clicking data point
        df_nearest = find_nearest_neighbours(df, x_axis.value, y_axis.value, x, y, n=3)
    else:
        df_nearest = None

    with solara.ColumnsResponsive(4):
        """
        with solara.VBox():

            # plot figure
            solara.FigurePlotly(fig, on_click=click_data.set, )

            # enable UI dropdown widget to select axis categories
            solara.Select(label="X-axis", value=x_axis, values=columns)
            solara.Select(label="Y-axis", value=y_axis, values=columns)

            with solara.Card(title="Todo App"):
                # show dataframe of the clicked point's nearest n neighbors
                if df_nearest is not None:
                    solara.Markdown("## Nearest 3 neighbours")
                    solara.DataFrame(df_nearest)
                else:
                    solara.Info("Click to select a point")

        with solara.VBox():

            # plot figure
            solara.FigurePlotly(fig, on_click=click_data.set, )

            # enable UI dropdown widget to select axis categories
            solara.Select(label="X-axis", value=x_axis, values=columns)
            solara.Select(label="Y-axis", value=y_axis, values=columns)

            with solara.Card(title="Todo App"):
                # show dataframe of the clicked point's nearest n neighbors
                if df_nearest is not None:
                    solara.Markdown("## Nearest 3 neighbours")
                    solara.DataFrame(df_nearest)
                else:
                    solara.Info("Click to select a point")
        """
        with solara.VBox():
            leiterseilbefestigung: list[str] = ["Abgespannt", "Aufgelegt"]
            standardkurzschlussströme: list[int|float] = [10, 12.5, 16, 20, 25, 31.5, 40, 50, 63, 80]
            teilleiter: list[int] = [1, 2, 3, 4, 5, 6]
            leiterseiltyp: list[str] = ["182-AL3", "299-AL3", "400-AL3", "626-AL3", "1000-AL3"]
            steifigkeitsnorm: list[int] = [100000, 150000, 1300000, 400000, 2000000, 600000, 3000000]

            solara.Select(label="Art der Leiterseilbefestigung", value=leiterseilbefestigung, values=leiterseilbefestigung)
            solara.Select(label="I''\u2096 [A] Anfangs-Kurzschlusswechselstrom beim dreipoligen Kurzschluss (Effektivwert)", value=standardkurzschlussströme, values=standardkurzschlussströme)
            solara.InputFloat("a [m] Leitermittenabstand")
            solara.InputFloat("li [m] Länge einer Abspann-Isolatorkette")
            solara.Select(label="n (dimensionslos) Anzahl der Teilleiter eines Hauptleiters", value=teilleiter, values=teilleiter)
            solara.Select(label="Leiterseiltyp",value=leiterseiltyp, values=leiterseiltyp)
            solara.InputFloat("Fst80 [N] statische Seilzugkraft in einem Hauptleiter")
            solara.InputFloat("Fst-20 [N] statische Seilzugkraft in einem Hauptleiter")
            solara.Select(label="N [1/N]Steifigkeitsnorm einer Anordnung mit Leiterseilen", value=steifigkeitsnorm, values=steifigkeitsnorm)
            solara.InputFloat("Tk [s] Kurzschlussdauer", value=1.0)





Page()