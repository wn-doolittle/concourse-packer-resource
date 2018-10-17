# stdlib
import subprocess
from typing import List

# local
from lib.log import log


# =============================================================================
#
# constants
#
# =============================================================================

PACKER_BIN_FILE_PATH = 'packer'


# =============================================================================
#
# private exe functions
#
# =============================================================================

# =============================================================================
# _run
# =============================================================================
def _run(bin: str, *args: str, input=None) -> subprocess.CompletedProcess:
    command_output = subprocess.run([bin] + list(args),
                                    capture_output=True,
                                    encoding='utf-8',
                                    input=input)
    # log stderr if present
    if command_output.stderr:
        log(f"{bin} stderr:")
        log(command_output.stderr)

    # check the return code
    try:
        command_output.check_returncode()
    except subprocess.CalledProcessError:
        # log stdout
        if command_output.stdout:
            log(f"{bin} stdout:")
            log(command_output.stdout)
        # re-raise
        raise

    # return the command output
    return command_output


# =============================================================================
# _packer
# =============================================================================
def _packer(*args: str, input=None) -> subprocess.CompletedProcess:
    return _run(PACKER_BIN_FILE_PATH,
                '-machine-readable',
                *args,
                input=input)


# =============================================================================
#
# public packer functions
#
# =============================================================================

def validate(
        template_file_path: str,
        var_file_paths: List[str] = None,
        vars: dict = None) -> None:
    packer_command_args = []
    # add any specified var file paths
    if var_file_paths:
        for var_file_path in var_file_paths:
            packer_command_args.append(f"-var-file={var_file_path}")
    # add any specified vars
    if vars:
        for var_name, var_value in vars.items():
            packer_command_args.append(f"-var '{var_name}={var_value}'")
    # execute validate command
    _packer(
        'validate',
        *packer_command_args,
        template_file_path)


def build(
        template_file_path: str,
        var_file_paths: List[str] = None,
        vars: dict = None) -> None:
    packer_command_args = []
    # add any specified var file paths
    if var_file_paths:
        for var_file_path in var_file_paths:
            packer_command_args.append(f"-var-file={var_file_path}")
    # add any specified vars
    if vars:
        for var_name, var_value in vars.items():
            packer_command_args.append(f"-var '{var_name}={var_value}'")
    # execute build command
    _packer(
        'build',
        *packer_command_args,
        template_file_path)
