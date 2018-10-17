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

**warning**: python will print the values of the packer command line arguments when a packer command fails

while 'secret variables' will be sanitized from packer output, if specified as `vars`, these values will not be sanitized by python's error output and thus may be visible in concourse logs

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
