# stdlib
import json
import os
import sys
from typing import Any, Dict, List, Optional

# local
import lib.packer
from lib.log import log

# =============================================================================
#
# private io functions
#
# =============================================================================

# =============================================================================
# _get_working_dir_path
# =============================================================================
def _get_working_dir_path() -> str:
    return sys.argv[1]


# =============================================================================
# _get_working_dir_file_path
# =============================================================================
def _get_working_dir_file_path(
        working_dir_path: str, file_name: str) -> str:
    return os.path.join(working_dir_path, file_name)


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
    input_payload = _read_payload()
    template_file_path: str = input_payload['params']['template']
    var_file_paths: Optional[List[str]] = None
    vars: Optional[Dict] = None
    if 'var_files' in input_payload['params']:
        var_file_paths = input_payload['params']['var_files']
    if 'vars' in input_payload['params']:
        vars = input_payload['params']['vars']
    lib.packer.version()
    lib.packer.validate(
        template_file_path,
        var_file_paths=var_file_paths,
        vars=vars)
    lib.packer.build(
        template_file_path,
        var_file_paths=var_file_paths,
        vars=vars)
    # _write_payload({
    #     "version": {
    #         'ami': 'ami-00000000000000000'
    #     }
    # })
