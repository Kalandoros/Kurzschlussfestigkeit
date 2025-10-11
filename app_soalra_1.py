import solara


@solara.component
def Page():
    route, routes = solara.use_route()

    with solara.Column():
        solara.Markdown("Hello")
        solara.Markdown("World")


    def toggle_settings():
        pass

    with solara.AppBar():
        solara.lab.ThemeToggle()
        solara.Button(icon_name="settings", on_click=toggle_settings, icon=True)
    with solara.AppBarTitle():
        solara.Text("Application title")
    with solara.Sidebar():
        with solara.Card(title="Menu", subtitle="Kurzschluss", margin=0, elevation=0, ):
            with solara.Column():
                with solara.lab.Tab("Tab 1", icon_name="mdi-flash"):
                    solara.Markdown("Hello")
                with solara.lab.Tab("Tab 2", icon_name="mdi-flash-outline"):
                    solara.Markdown("World")
        with solara.Card(title="", subtitle="Erdung", margin=0, elevation=0):
            with solara.Column():
                with solara.lab.Tab("Tab 3", icon_name="mdi-arrow-down-circle"):
                    solara.Markdown("Hello")
                with solara.lab.Tab("Tab 4", icon_name="mdi-arrow-down-circle-outline"):
                    solara.Markdown("World")


@solara.component
def Layout(children=[]):
    route_current, routes_all = solara.use_route()
    dark_effective = solara.lab.use_dark_effective()
    with solara.Column():
        with solara.Row():
            for route in routes_all:
                with solara.Link(route):
                    solara.Button(route.path, color="red" if route_current == route else None)

    return solara.AppLayout(children=children, toolbar_dark=dark_effective, color=None,
                            sidebar_open=False)  # if dark_effective else "primary")


Page()