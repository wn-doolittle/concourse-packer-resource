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
# private utility functions
#
# =============================================================================

def _parse_packer_machine_readable_output(output: str) -> list:
    # machine readable format
    # from https://www.packer.io/docs/commands/index.html
    output_payload = []
    if output:
        # split output on line breaks
        output_lines: list = output.splitlines()
        for output_line in output_lines:
            message_item: dict = {
                'timestamp': None,
                'target': None,
                'type': None,
                'data': []
            }
            # split each line on commas
            line_tokens: list = output_line.split(',')
            for i, line_token in enumerate(line_tokens):
                # log(f"token #{i}: {line_token}")
                # assign payload fields based on token number
                if i == 0:
                    message_item['timestamp'] = line_token
                elif i == 1:
                    message_item['target'] = line_token
                elif i == 2:
                    message_item['type'] = line_token
                elif i > 2:
                    message_item['data'].append(line_token)
            output_payload.append(message_item)
    return output_payload


def _format_packer_machine_readable_output(
    timestamp: str,
    target: str,
    type: str,
    data: str,
    subtype=None
) -> str:
    if not target:
        target = 'global'
    # consistent padding for the 'version' types
    if type.startswith('version'):
        type = f"{type:16}"
    if subtype:
        return f"{timestamp} | {target} | {type} | {subtype:8} | {data}"
    else:
        return f"{timestamp} | {target} | {type} | {data}"


def _print_packer_machine_readable_output(output: list) -> None:
    if output:
        for output_item in output:
            if len(output_item['data']) > 0:
                subtype = None
                if output_item['data'][0] in ['say', 'error', 'message']:
                    subtype = output_item['data'].pop(0)
                for item in output_item['data']:
                    item_lines = item.split('\\n')
                    for item_line in item_lines:
                        log(_format_packer_machine_readable_output(
                            output_item['timestamp'],
                            output_item['target'],
                            output_item['type'],
                            item_line,
                            subtype=subtype))
            else:
                log(_format_packer_machine_readable_output(
                    output_item['timestamp'],
                    output_item['target'],
                    output_item['type'],
                    output_item['data']))


def _parse_and_print_packer_machine_readable_output(output: str) -> None:
    parsed_output = _parse_packer_machine_readable_output(output)
    _print_packer_machine_readable_output(parsed_output)


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
        _parse_and_print_packer_machine_readable_output(
            command_output.stderr)

    # check the return code
    try:
        command_output.check_returncode()
    except subprocess.CalledProcessError:
        # log stdout
        if command_output.stdout:
            # attempt to parse as machine readable
            _parse_and_print_packer_machine_readable_output(
                command_output.stdout)
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

def version() -> None:
    # execute version command
    packer_command_output = _packer('version')
    # log the version output
    _parse_and_print_packer_machine_readable_output(
        packer_command_output.stdout)


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
            packer_command_args.append(f"-var={var_name}={var_value}")
    # execute validate command
    packer_command_output = _packer(
        'validate',
        *packer_command_args,
        template_file_path)
    # log the validate output
    _parse_and_print_packer_machine_readable_output(
        packer_command_output.stdout)


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
            packer_command_args.append(f"-var={var_name}={var_value}")
    # execute build command
    _packer(
        'build',
        *packer_command_args,
        template_file_path)
