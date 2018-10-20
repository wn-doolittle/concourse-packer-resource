# stdlib
import subprocess
from typing import List

# local
from lib.log import log, log_pretty


# temporary
import json


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

def _parse_packer_machine_readable_output_line(output_line: str) -> dict:
    # machine readable format
    # from https://www.packer.io/docs/commands/index.html
    parsed_line = None
    if output_line:
        # # split output on line breaks
        # output_lines: list = output.splitlines()
        # for output_line in output_lines:
        #     message_item: dict = {
        #         'timestamp': None,
        #         'target': None,
        #         'type': None,
        #         'data': []
        #     }
        #     # split each line on commas
        #     line_tokens: list = output_line.split(',')
        #     for i, line_token in enumerate(line_tokens):
        #         # log(f"token #{i}: {line_token}")
        #         # assign payload fields based on token number
        #         if i == 0:
        #             message_item['timestamp'] = line_token
        #         elif i == 1:
        #             message_item['target'] = line_token
        #         elif i == 2:
        #             message_item['type'] = line_token
        #         elif i > 2:
        #             message_item['data'].append(line_token)
        #     output_payload.append(message_item)

        message_item: dict = {
            'timestamp': None,
            'target': None,
            'type': None,
            'data': []
        }
        # split each line on commas
        line_tokens: list = output_line.split(',')
        # log(f"line tokens: {line_tokens}")
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
                # strip trailing newline from data
                message_item['data'].append(line_token.rstrip('\n'))
        parsed_line = message_item
    return parsed_line


def _format_packer_machine_readable_output_line(
    timestamp: str,
    target: str,
    type: str,
    data: str,
    subtype=None
) -> str:
    # most messages won't have a target
    # which means it's global
    if not target:
        target = 'global'
    # consistent padding for the 'version' types
    if type.startswith('version'):
        type = f"{type:16}"
    # replace the packer comma
    data = data.replace('%!(PACKER_COMMA)', ',')
    if subtype:
        return f"{timestamp} | {target} | {type} | {subtype:8} | {data}"
    else:
        return f"{timestamp} | {target} | {type} | {data}"


def _print_parsed_packer_machine_readable_output_line(
        parsed_line: dict) -> None:
    if parsed_line:
        # log_pretty(parsed_line)
        if len(parsed_line['data']) > 0:
            subtype = None
            # check for subtype
            if parsed_line['data'][0] in ['say', 'error', 'message']:
                # pop found subtype from the parsed line
                subtype = parsed_line['data'].pop(0)
            for item in parsed_line['data']:
                # split on \\n
                # item_lines = item.splitlines(True)
                item_lines = item.split('\\n')
                # log(f"item lines: {item_lines}")
                for item_line in item_lines:
                    log(_format_packer_machine_readable_output_line(
                        parsed_line['timestamp'],
                        parsed_line['target'],
                        parsed_line['type'],
                        item_line,
                        subtype=subtype))


# 1539968935 | ubuntu18-ami | artifact-count | 1
# 1539968935 | ubuntu18-ami | artifact | 0
# 1539968935 | ubuntu18-ami | artifact | builder-id
# 1539968935 | ubuntu18-ami | artifact | mitchellh.amazonebs
# 1539968935 | ubuntu18-ami | artifact | 0
# 1539968935 | ubuntu18-ami | artifact | id
# 1539968935 | ubuntu18-ami | artifact | us-east-1:ami-0c532a15a65f5b8e1
# 1539968935 | ubuntu18-ami | artifact | 0
# 1539968935 | ubuntu18-ami | artifact | string
# 1539968935 | ubuntu18-ami | artifact | AMIs were created:
# 1539968935 | ubuntu18-ami | artifact | us-east-1: ami-0c532a15a65f5b8e1
# 1539968935 | ubuntu18-ami | artifact |
# 1539968935 | ubuntu18-ami | artifact | 0
# 1539968935 | ubuntu18-ami | artifact | files-count
# 1539968935 | ubuntu18-ami | artifact | 0
# 1539968935 | ubuntu18-ami | artifact | 0
# 1539968935 | ubuntu18-ami | artifact | end

def _parse_packer_build_output_for_manifest(output: str) -> dict:
    output = """1539971796,,ui,say,==> ubuntu18-ami: Prevalidating AMI Name: concourse-packer-test-2018-10-19T17-56-36Z
1539971798,,ui,message,    ubuntu18-ami: Found Image ID: ami-00000000000000000
1539971798,,ui,say,==> ubuntu18-ami: Creating temporary keypair: packer_5bca1ad4-5fd5-ded5-fd5f-a8701bfbdf01
1539971798,,ui,say,==> ubuntu18-ami: Creating temporary security group for this instance: packer_5bca1ad6-9a18-cb19-483c-b3685ddfba8a
1539971799,,ui,say,==> ubuntu18-ami: Authorizing access to port 22 from 0.0.0.0/0 in the temporary security group...
1539971799,,ui,say,==> ubuntu18-ami: Launching a source AWS instance...
1539971799,,ui,say,==> ubuntu18-ami: Adding tags to source instance
1539971799,,ui,message,    ubuntu18-ami: Adding tag: "Name": "Packer Builder"
1539971800,,ui,message,    ubuntu18-ami: Instance ID: i-00000000000000000
1539971800,,ui,say,==> ubuntu18-ami: Waiting for instance (i-00000000000000000) to become ready...
1539971832,,ui,say,==> ubuntu18-ami: Using ssh communicator to connect: 54.237.249.166
1539971832,,ui,say,==> ubuntu18-ami: Waiting for SSH to become available...
1539971848,,ui,say,==> ubuntu18-ami: Connected to SSH!
1539971848,,ui,say,==> ubuntu18-ami: Provisioning with shell script: /tmp/packer-shell321674949
1539971851,,ui,message,    ubuntu18-ami: Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [83.2 kB]
1539971851,,ui,message,    ubuntu18-ami: Get:2 http://security.ubuntu.com/ubuntu bionic-security/main amd64 Packages [186 kB]
1539971851,,ui,message,    ubuntu18-ami: Hit:3 http://archive.ubuntu.com/ubuntu bionic InRelease
1539971851,,ui,message,    ubuntu18-ami: Get:4 http://security.ubuntu.com/ubuntu bionic-security/main Translation-en [72.1 kB]
1539971851,,ui,message,    ubuntu18-ami: Get:5 http://security.ubuntu.com/ubuntu bionic-security/universe amd64 Packages [89.0 kB]
1539971851,,ui,message,    ubuntu18-ami: Get:6 http://security.ubuntu.com/ubuntu bionic-security/universe Translation-en [48.5 kB]
1539971851,,ui,message,    ubuntu18-ami: Get:7 http://security.ubuntu.com/ubuntu bionic-security/multiverse amd64 Packages [1440 B]
1539971851,,ui,message,    ubuntu18-ami: Get:8 http://archive.ubuntu.com/ubuntu bionic-updates InRelease [88.7 kB]
1539971851,,ui,message,    ubuntu18-ami: Get:9 http://security.ubuntu.com/ubuntu bionic-security/multiverse Translation-en [996 B]
1539971851,,ui,message,    ubuntu18-ami: Get:10 http://archive.ubuntu.com/ubuntu bionic-backports InRelease [74.6 kB]
1539971851,,ui,message,    ubuntu18-ami: Get:11 http://archive.ubuntu.com/ubuntu bionic/universe amd64 Packages [8570 kB]
1539971858,,ui,message,    ubuntu18-ami: Get:12 http://archive.ubuntu.com/ubuntu bionic/universe Translation-en [4941 kB]
1539971861,,ui,message,    ubuntu18-ami: Get:13 http://archive.ubuntu.com/ubuntu bionic/multiverse amd64 Packages [151 kB]
1539971861,,ui,message,    ubuntu18-ami: Get:14 http://archive.ubuntu.com/ubuntu bionic/multiverse Translation-en [108 kB]
1539971862,,ui,message,    ubuntu18-ami: Get:15 http://archive.ubuntu.com/ubuntu bionic-updates/main amd64 Packages [407 kB]
1539971862,,ui,message,    ubuntu18-ami: Get:16 http://archive.ubuntu.com/ubuntu bionic-updates/main Translation-en [152 kB]
1539971862,,ui,message,    ubuntu18-ami: Get:17 http://archive.ubuntu.com/ubuntu bionic-updates/universe amd64 Packages [565 kB]
1539971863,,ui,message,    ubuntu18-ami: Get:18 http://archive.ubuntu.com/ubuntu bionic-updates/universe Translation-en [148 kB]
1539971863,,ui,message,    ubuntu18-ami: Get:19 http://archive.ubuntu.com/ubuntu bionic-updates/multiverse amd64 Packages [5708 B]
1539971863,,ui,message,    ubuntu18-ami: Get:20 http://archive.ubuntu.com/ubuntu bionic-updates/multiverse Translation-en [3176 B]
1539971863,,ui,message,    ubuntu18-ami: Get:21 http://archive.ubuntu.com/ubuntu bionic-backports/universe amd64 Packages [2852 B]
1539971863,,ui,message,    ubuntu18-ami: Get:22 http://archive.ubuntu.com/ubuntu bionic-backports/universe Translation-en [1200 B]
1539971864,,ui,message,    ubuntu18-ami: Fetched 15.7 MB in 13s (1240 kB/s)
1539971864,,ui,message,    ubuntu18-ami: Reading package lists...
1539971865,,ui,say,==> ubuntu18-ami: Stopping the source instance...
1539971865,,ui,message,    ubuntu18-ami: Stopping instance%!(PACKER_COMMA) attempt 1
1539971865,,ui,say,==> ubuntu18-ami: Waiting for the instance to stop...
1539971927,,ui,say,==> ubuntu18-ami: Creating unencrypted AMI concourse-packer-test-2018-10-19T17-56-36Z from instance i-00000000000000000
1539971927,,ui,message,    ubuntu18-ami: AMI: ami-00000000000000000
1539971927,,ui,say,==> ubuntu18-ami: Waiting for AMI to become ready...
1539972004,,ui,say,==> ubuntu18-ami: Modifying attributes on AMI (ami-00000000000000000)...
1539972004,,ui,message,    ubuntu18-ami: Modifying: description
1539972005,,ui,say,==> ubuntu18-ami: Modifying attributes on snapshot (snap-00000000000000000)...
1539972005,,ui,say,==> ubuntu18-ami: Terminating the source AWS instance...
1539972021,,ui,say,==> ubuntu18-ami: Cleaning up any extra volumes...
1539972021,,ui,say,==> ubuntu18-ami: No volumes to clean up%!(PACKER_COMMA) skipping
1539972021,,ui,say,==> ubuntu18-ami: Deleting temporary security group...
1539972021,,ui,say,==> ubuntu18-ami: Deleting temporary keypair...
1539972021,,ui,say,Build 'ubuntu18-ami' finished.
1539972021,,ui,say,\\n==> Builds finished. The artifacts of successful builds are:
1539972021,ubuntu18-ami,artifact-count,1
1539972021,ubuntu18-ami,artifact,0,builder-id,mitchellh.amazonebs
1539972021,ubuntu18-ami,artifact,0,id,us-east-1:ami-00000000000000000
1539972021,ubuntu18-ami,artifact,0,string,AMIs were created:\\nus-east-1: ami-00000000000000000\\n
1539972021,ubuntu18-ami,artifact,0,files-count,0
1539972021,ubuntu18-ami,artifact,0,end
1539972021,,ui,say,--> ubuntu18-ami: AMIs were created:\\nus-east-1: ami-00000000000000000\\n"""
    # output = "1539972021,,ui,say,--> ubuntu18-ami: AMIs were created:\nus-east-1: ami-00000000000000000\n"
    # log(output)
    parsed_lines = []
    for output_line in output.splitlines():
        parsed_line = _parse_packer_machine_readable_output_line(output_line)
        parsed_lines.append(parsed_line)
        _print_parsed_packer_machine_readable_output_line(parsed_line)

    manifest = {
        'artifacts': {}
    }
    # log_pretty(parsed_output)
    # create collection of targets
    targets = {}
    for parsed_item in parsed_lines:
        if parsed_item['target']:
            target_name = parsed_item['target']
            if target_name not in targets:
                targets[target_name] = []
            del parsed_item['target']
            targets[target_name].append(parsed_item)
    log_pretty(targets)
    # go through targets
    for target in targets.keys():
        # log('target:')
        # log_pretty(target)
        # split into artifacts
        target_artifacts = {}
        for target_item in targets[target]:
            # log('target_item:')
            # log_pretty(target_item)
            if target_item['type'] == 'artifact':
                # first index of data will be the artifact number
                artifact_number = target_item['data'][0]
                # second index of data will be the artifact key
                artifact_key = target_item['data'][1]
                # skip adding the 'end' key
                if artifact_key == 'end':
                    continue
                # third index of data will be the artifact value, if present
                if len(target_item['data']) > 2:
                    artifact_value = target_item['data'][2]
                else:
                    artifact_value = None
                # create the target artifact dict, if missing
                if artifact_number not in target_artifacts:
                    target_artifacts[artifact_number] = {}
                # assign the artifact key and value
                target_artifacts[artifact_number][artifact_key] = \
                    artifact_value
        # log_pretty(target_artifacts)
        manifest['artifacts'][target] = target_artifacts
    log_pretty(manifest)
    print(json.dumps(manifest))
    return manifest


# =============================================================================
#
# private exe functions
#
# =============================================================================


# =============================================================================
# _packer
# =============================================================================
def _packer(*args: str, input=None) -> List[dict]:
    # runs packer bin with forced machine readable output
    process_args = [
        PACKER_BIN_FILE_PATH,
        '-machine-readable',
        *args
    ]
    parsed_lines = []
    # use Popen so we can read lines as they come
    with subprocess.Popen(
            process_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # redirect stderr to stdout
            bufsize=1,
            universal_newlines=True,
            stdin=input) as pipe:
        for line in pipe.stdout:
            # parse the machine readable output as it arrives
            parsed_line = _parse_packer_machine_readable_output_line(line)
            parsed_lines.append(parsed_line)
            _print_parsed_packer_machine_readable_output_line(parsed_line)
    if pipe.returncode != 0:
        # args are masked to prevent credentials leaking
        raise subprocess.CalledProcessError(
            pipe.returncode, [PACKER_BIN_FILE_PATH])
    return parsed_lines


# =============================================================================
#
# public packer functions
#
# =============================================================================

def version() -> None:
    # execute version command
    _packer('version')


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
            packer_command_args.append(f"-var={var_name}={var_value}")
    # execute build command
    # packer_command_result = _packer(
    #     'build',
    #     *packer_command_args,
    #     template_file_path)
    # packer_build_manifest = \
    #     _parse_packer_build_output_for_manifest(packer_command_result.stdout)

    _parse_packer_build_output_for_manifest('')

    # packer_command_result = _packer('version')

    # packer_command_result = _packer(
    #     'validate',
    #     template_file_path)
