 #!/bin/bash

 kadeploy3 --no-kexec -a public/kmem_dax_env.dsc -f $OAR_NODE_FILE -k
 ssh root@$(uniq $OAR_NODE_FILE | head -n 1) 'apt update -y && apt upgrade -y && apt autoremove -y'
 ssh root@$(uniq $OAR_NODE_FILE | head -n 1) 'ndctl create-namespace --mode=devdax --map=mem'