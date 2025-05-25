from textual.app import App
from textual.containers import Grid
from textual.widgets import Header, Footer
from plugin_loader import load_plugins

class HollywoodOS(App):
    CSS_PATH = "style.css"

    def compose(self):
        yield Header()
        yield Grid(id="plugin-grid")
        yield Footer()

    def on_mount(self):
        grid = self.query_one("#plugin-grid", Grid)
        plugins = load_plugins("plugins")
        for plugin in plugins:
            widget = plugin.create_widget()
            grid.mount(widget)

if __name__ == "__main__":
    HollywoodOS().run()