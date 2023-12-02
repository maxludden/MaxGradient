# Changelog

## v0.2.12

<span class="highlight">December 1, 2023</span> | Added Tests

- Updated banner image for `README.md` and `docs/index.md`
- Seperated Changelog into its own file: `docs/CHANGELOG.md`
- Added `py.typed` file to project                    directory

## v0.2.11

<span class="highlight">November 28, 2023</span> | Added Tests

- Removed color_sample and invert from gradient attributes
- Added tests for console, color, and gradient

## v0.2.10

<span class="highlight">November 25, 2023</span> | Added Dates

- Updated changlog to have dates
- added logo and favicon to changelog

## v0.2.9

<span class="highlight">November 25, 2023</span> | Updated Banner

- Updated MaxGradient Logo:
<img src="img/MaxGradient.svg" width="50%" alt="MaxGradient Logo" />
- and Favicon:
<img src="img/MaxGradient_favicon.svg" width="50%" alt="MaxGradient Favicon" />
- Updated banner to include new logo as http rather than referencing the SVG file locally.

## v0.2.8

<span class="highlight">November 25, 2023</span> | Fixed `cli.py`

- Fixed `cli.py` so that it works with the new `gradient` method
- Removed logging

## v0.2.7

<span class="highlight">November 25, 2023</span> | Bug Fixes

- Combined multiple CSS stylesheets into one:
    - `next-btn.css` -> `style.css`
    - `gradient.css` -> `style.css`
- General corrections to every file after correcting for Mypy

## v0.2.6

<span class="highlight">November 18, 2023</span> | Type Stubs

- Added type stubs - Mypy should work now
- Simplified `maxgradient.log.py` and fixed line lengths

## v0.2.4

- Rewrote `MaxGradient.console.Console` to replicate `rich.console.Console`
    - added `gradient` method
    - added `gradient_rule` method
- Switched to [`ruff`](https://docs.astral.sh/ruff/) for linting
- Pruned dependencies
- Updated default_styles.GRADIENT_STYLES

## v0.2.3

- Updated docs and added more examples and reference
- Fixed bugs
    - Fixed bug where gradient would not print if gradient was the only thing in the console
    - Fixed bug where gradient wouldn't print if the style wasn't a `rich.style.Style` object

## v0.2.2

- Added examples to docs and fixed some typos and bugs
- Disabled logging
- Fixed gradient class
- Added gradient rules
