from maxgradient.color import RGBA, ColorTriplet


def test_rgba():
    # Test the initialization of RGBA
    rgba = RGBA(0.5, 0.2, 0.8, None)
    assert rgba.red == 0.5
    assert rgba.green == 0.2
    assert rgba.blue == 0.8
    assert rgba.alpha is None

    # Test the __getitem__() method
    assert rgba[0] == 0.5
    assert rgba[1] == 0.2
    assert rgba[2] == 0.8
    assert rgba[3] is None

    # Test the as_triplet() method
    triplet = rgba.as_triplet()
    assert isinstance(triplet, ColorTriplet)
    assert triplet.red == 128
    assert triplet.green == 51
    assert triplet.blue == 204

    # Test the from_triplet() method
    new_rgba = RGBA.from_triplet(triplet)
    assert isinstance(new_rgba, RGBA)
    assert new_rgba.red == 0.5019607843137255
    assert new_rgba.green == 0.2
    assert new_rgba.blue == 0.8
    assert new_rgba.alpha is None

    # Test the from_rgb() method
    rgb = "rgb(255, 0, 0)"
    new_rgba = RGBA.from_rgb(rgb)
    assert isinstance(new_rgba, RGBA)
    assert new_rgba.red == 1.0
    assert new_rgba.green == 0.0
    assert new_rgba.blue == 0.0
    assert new_rgba.alpha is None

    # Test the float_to_255() method
    assert RGBA.float_to_255(0.5) == 128

    # Test the __repr__() method
    assert repr(rgba) == "RGBA(0.5, 0.2, 0.8, None)"
