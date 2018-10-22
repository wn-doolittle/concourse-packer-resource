#!/usr/bin/env python3

# stdlib
import json

# local
import lib.concourse
from lib.log import log, log_pretty


# =============================================================================
#
# private test functions
#
# =============================================================================

# =============================================================================
# _test__create_concourse_out_payload_from_packer_build_manifest
# =============================================================================
def _test__create_concourse_out_payload_from_packer_build_manifest(
        build_manifest: dict) -> None:
    log_pretty(
        lib.concourse._create_concourse_out_payload_from_packer_build_manifest(
            build_manifest))


# =============================================================================
#
# general
#
# =============================================================================

# =============================================================================
# do_test
# =============================================================================
def do_test() -> None:
    # single artifact single image
    log('single artifact single image')
    single_artifact_single_image_build_manifest = {
        'artifacts': {
            'ubuntu18-ami': {
                '0': {
                    'builder-id': 'mitchellh.amazonebs',
                    'files-count': '0',
                    'id': 'us-east-1:ami-00000000000000000',
                    'string': 'AMIs were created:\\nus-east-1: ami-00000000000000000\\n'
                }
            }
        }
    }
    _test__create_concourse_out_payload_from_packer_build_manifest(
        single_artifact_single_image_build_manifest)

    # single artifact multiple images
    log('single artifact multiple images')
    single_artifact_multiple_images_build_manifest = {
        'artifacts': {
            'ubuntu18-ami': {
                '0': {
                    'builder-id': 'mitchellh.amazonebs',
                    'files-count': '0',
                    'id': 'us-east-1:ami-00000000000000000',
                    'string': 'AMIs were created:\\nus-east-1: ami-00000000000000000\\n'
                },
                '1': {
                    'builder-id': 'mitchellh.amazonebs',
                    'files-count': '0',
                    'id': 'us-east-1:ami-00000000000000001',
                    'string': 'AMIs were created:\\nus-east-1: ami-00000000000000001\\n'
                }
            }
        }
    }
    _test__create_concourse_out_payload_from_packer_build_manifest(
        single_artifact_multiple_images_build_manifest)

    # multiple artifacts single images
    log('multiple artifacts single images')
    single_artifact_multiple_images_build_manifest = {
        'artifacts': {
            'ubuntu18-ami': {
                '0': {
                    'builder-id': 'mitchellh.amazonebs',
                    'files-count': '0',
                    'id': 'us-east-1:ami-00000000000000000',
                    'string': 'AMIs were created:\\nus-east-1: ami-00000000000000000\\n'
                }
            },
            'amazon-linux-ami': {
                '0': {
                    'builder-id': 'mitchellh.amazonebs',
                    'files-count': '0',
                    'id': 'us-east-1:ami-10000000000000000',
                    'string': 'AMIs were created:\\nus-east-1: ami-10000000000000000\\n'
                }
            }
        }
    }
    _test__create_concourse_out_payload_from_packer_build_manifest(
        single_artifact_multiple_images_build_manifest)


# =============================================================================
#
# main
#
# =============================================================================

if __name__ == "__main__":
    do_test()
