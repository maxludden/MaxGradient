![MaxGradient](Images/maxgradient.png)

# MaxGradient

MaxGradient automating printing gradient colored text to the console. It's built upon the great [rich](http://rich.readthedocs.io/en/latest/) library.

## Installation

MaxGradient can be installed from PyPi using your favorite package manager:

### PDM (recommended)

    ```bash
    pdm add maxgradient
    ```

### Pip

    ```bash
    pip install maxgradient
    ```

## Usage

### Basic Usage

The basic usage is to create a console object and use it to print gradient text:

<figure width="50%">
    <img src="/Users/maxludden/dev/py/maxgradient/Images/gradient_basic.svg" alt="gradient_basic" style="zoom: 10%;" />
</figure>

### Gradient

You may also instantiate a Gradient Object. The Gradient class is a subclass of the
rich.text.Text class, and can be used in the same way. The Gradient class has a
few extra arguments available though.

```python
from maxgradient import Console, Gradient

gradient = Gradient(
    "Hello World!",
    colors=["red", "orange", "yellow"]
)
```

[MaxGradient][https://GitHub.com/maxludden/maxgradient/Images/maxgradient.png]
