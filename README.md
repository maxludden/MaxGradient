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

The basic usage is to create a console obejct and use it to print colored text:

```python
from maxgradient import Console