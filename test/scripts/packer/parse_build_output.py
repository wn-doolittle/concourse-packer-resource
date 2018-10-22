#!/usr/bin/env python3

# local
import lib.packer


# =============================================================================
#
# private test functions
#
# =============================================================================

# =============================================================================
# _test__parse_packer_parsed_output_for_build_manifest
# =============================================================================
def _test__parse_packer_parsed_output_for_build_manifest() -> dict:
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
1539971832,,ui,say,==> ubuntu18-ami: Using ssh communicator to connect: 00.000.000.000
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
        parsed_line = \
            lib.packer._parse_packer_machine_readable_output_line(output_line)
        parsed_lines.append(parsed_line)
        lib.packer._print_parsed_packer_machine_readable_output_line(
            parsed_line)
    lib.packer._parse_packer_parsed_output_for_build_manifest(parsed_lines)


# =============================================================================
#
# general
#
# =============================================================================

# =============================================================================
# do_test
# =============================================================================
def do_test() -> None:
    _test__parse_packer_parsed_output_for_build_manifest()


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    do_test()
