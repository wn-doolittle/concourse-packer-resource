# stdlib
import json
import os
import sys
from typing import Any

# local
import lib.packer
from lib.log import log

# =============================================================================
#
# private io functions
#
# =============================================================================

# =============================================================================
# _get_dir_path_from_input
# =============================================================================
def _get_dir_path_from_input() -> str:
    return sys.argv[1]


# =============================================================================
# _read_payload
# =============================================================================
def _read_payload(stream=sys.stdin) -> Any:
    return json.load(stream)


# =============================================================================
# _write_payload
# =============================================================================
def _write_payload(payload: Any, stream=sys.stdout) -> None:
    json.dump(payload, stream)


# =============================================================================
# _get_repository_file_path
# =============================================================================
def _get_repository_file_path(
        repository_dir_path: str, file_name: str) -> str:
    return os.path.join(repository_dir_path, file_name)


# =============================================================================
#
# public lifecycle functions
#
# =============================================================================

def do_check() -> None:
    # not implemented
    _write_payload([{'ami': 'ami-00000000000000000'}])


def do_in() -> None:
    # not implemented
    _write_payload({
        "version": {
            'ami': 'ami-00000000000000000'
        }
    })


def do_out() -> None:
    # input_payload = _read_payload()
    # lib.packer.validate('example.json')
    _write_payload({
        "version": {
            'ami': 'ami-00000000000000000'
        }
    })
