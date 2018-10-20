# stdlib
import sys
from typing import Any
from pprint import PrettyPrinter, pprint


# =============================================================================
#
# functions
#
# =============================================================================

# =============================================================================
# log
# =============================================================================
def log(value: Any, stream=sys.stderr, **kwargs) -> None:
    print(value, file=stream, **kwargs)


# =============================================================================
# NoStringWrappingPrettyPrinter
# c\o: https://stackoverflow.com/questions/31485402/
#       can-i-make-pprint-in-python3-not-split-strings-like-in-python2
# =============================================================================
class NoStringWrappingPrettyPrinter(PrettyPrinter):
    def _format(self, object, *args) -> None:
        if isinstance(object, str):
            width = self._width
            self._width = sys.maxsize
            try:
                super()._format(object, *args)
            finally:
                self._width = width
        else:
            super()._format(object, *args)


# =============================================================================
# log_pretty
# =============================================================================
def log_pretty(value: Any, stream=sys.stderr) -> None:
    NoStringWrappingPrettyPrinter(stream=stream).pprint(value)
