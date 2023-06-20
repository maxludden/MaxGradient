"""Example of how to used the MaxGradient.color.Color class."""
# pylint: disable=E0401
import maxgradient as mg

def color_example(record: bool = False):
    """Demonstrate printing an X11 color.

    Args:
        record (bool, optional): Record the output. Defaults to False.
    """
    if record:
        console = mg.Console(record=True, width=40)
    else:
        console = mg.Console()
        console.clear()
        console.line(2)

    lime = mg.Color("lime")
    console.print(f"[bold {lime.hex}]This is a a vibrant green color!")

    if record:
        console.save_svg(
            "Images/color_example.svg",
            title="Color Example",
        )

if __name__ == "__main__":
    color_example(True)