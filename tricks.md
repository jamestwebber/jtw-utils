## For customizing the PATH during conda activate:

 - Create files `~/miniconda3/envs/[env name]/etc/{de,}activate.d/env_vars.sh`
 - Set and unset the path changes in those files
 - This will probably screw up if you do something else in between

### `activate.d/env_vars.sh`

```
#!/bin/sh

export PATH="/Users/jwebber/.cargo/bin:$PATH"
```

### `deactivate.d/env_vars.sh`

```
#!/bin/sh

export PATH=${PATH#'/Users/jwebber/.cargo/bin:$PATH'}
```

### For setting up remote github access

Just create a new ssh key with a passphrase: `ssh-keygen -t ed25519 -C "james@whatever.domain"`

And add it to [GitHub settings](https://github.com/settings/keys)
