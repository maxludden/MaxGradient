from maxgradient.color import Color
from maxgradient._simple_gradient import SimpleGradient
from rich.style import Style
from pydantic_core import PydanticCustomError


def test_simple_gradient():
    # Create a SimpleGradient instance
    gradient = SimpleGradient(
        text="Hello, World!",
        color1=Color("red"),
        color2=Color("blue"),
        style=Style(bold=True),
    )

    # Test the text property
    assert gradient.text == "Hello, World!"

    # Test the color1 and color2 properties
    assert gradient.color1 == Color("red")
    assert gradient.color2 == Color("blue")

    # Test the style property
    assert gradient.style == Style(bold=True)

    # Test the __repr__() method
    assert repr(gradient) == "Gradient('Hello, World!', 'red', 'blue')"

    # Test the __add__() method
    result = gradient + "!"
    assert isinstance(result, SimpleGradient)
    assert result.text == "Hello, World!!"

    # Test the __eq__() method
    assert gradient == SimpleGradient(
        text="Hello, World!",
        color1=Color("red"),
        color2=Color("blue"),
        style=Style(bold=True),
    )
    assert gradient != SimpleGradient(
        text="Hello, World!",
        color1=Color("red"),
        color2=Color("green"),
        style=Style(bold=True),
    )

    # Test the generate_spans() method
    spans = list(gradient.generate_spans())
    assert len(spans) == len(gradient.text)
    assert spans[0].style == Style(bold=True, color="red")
    assert spans[-1].style == Style(bold=True, color="blue")

