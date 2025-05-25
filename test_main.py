from textual.app import App
from textual.containers import Grid
from textual.widgets import Header, Footer, Static

class SimpleHollywoodOS(App):
    CSS = """
    #plugin-grid {
        layout: grid;
        grid-columns: 1fr 1fr 1fr;
        grid-rows: auto auto auto;
        grid-gutter: 1;
        padding: 1;
    }
    
    .window {
        border: solid gray;
        background: black;
        color: green;
        height: 10;
        padding: 1;
    }
    """

    def compose(self):
        yield Header()
        yield Grid(id="plugin-grid")
        yield Footer()

    def on_mount(self):
        grid = self.query_one("#plugin-grid", Grid)
        
        # Create some test windows
        for i in range(6):
            window = Static(f"Test Window {i+1}\nScrolling content...", classes="window")
            grid.mount(window)

if __name__ == "__main__":
    SimpleHollywoodOS().run()