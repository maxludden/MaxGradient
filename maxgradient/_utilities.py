from functools import wraps
from rich.console import Console
from rich.table import Table
from rich.traceback import install as install_rich_traceback
from loguru import logger

from maxgradient.theme import GradientTheme
from maxgradient.color import Color

console = Console(theme=GradientTheme())
install_rich_traceback(console=console)

logger.add(
    "debug.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="5 MB",
    colorize=True,
    catch=True,
)
log = logger.bind(name="debug")


def debug(*, entry: bool = True, exit: bool = True, level="DEBUG"):
    def wrapper(func):
        name = func.__name__
        @wraps(func)
        def wrapped(*args, **kwargs):
            log_ =logger.opt(depth=1)
            if entry:
                log_.log(level, f"Entering `{name}` (args={args}, kwargs={kwargs}))")
            result = func(*args, **kwargs)
            if exit:
                log_.log(level, f"Exiting `{name}` (result={result})")
            return result
        return wrapped
    return wrapper
    

@debug()
def hello_world():
    console.log("Hello World!")


if __name__=="__main__":
    hello_world()