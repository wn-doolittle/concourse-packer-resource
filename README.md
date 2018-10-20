# concourse packer resource

a [concourse-ci](https://concourse-ci.org) resource for building [amazon machine images](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) (AMIs) via [packer](https://www.packer.io/docs/builders/amazon.html)

## table of contents

- [behavior](#behavior)

	- [out](#out-build-a-new-ami)

## behaviour

### `out`: build a new ami

**parameters**

- `template`: _required_. the path to the packer template file.

- `var_files`: _optional_. the list of paths to [external JSON variable file(s)](https://www.packer.io/docs/templates/user-variables.html).

- `vars`: _optional_. dict of explicit packer variable key/value pairs.

**note**: in an effort to prevent credentials leaking to logs, the packer command line will not be printed on failure -- however, you should still mark any relevant variables as _sensitive variables_ in the packer template to prevent packer from printing them in log output

## examples

```yaml
resource_types:
- name: packer
  type: docker-image
  source:
    repository: snapkitchen/concourse-packer-resource

resources:
- name: build-ami
  type: packer

jobs:
- name: my-ami
  plan:
  - get: my-ami-template
  - put: build-ami
    params:
      template: my-ami-template/template.json
      var_files:
      - my-ami-template/my-vars.json
      vars:
        aws_access_key_id: ((aws_access_key_id))
        aws_secret_access_key: ((aws_secret_access_key))
        aws_region: ((aws_region))
```

# license

see [LICENSE](LICENSE)
