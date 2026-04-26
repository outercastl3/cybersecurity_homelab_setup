# Prerequisite for the SSH authorized_keys checker
- we let syscheck also check authorized_keys for changes
- so we can then create a multi-chain with successful SSH login and authorized_keys changes
- By changing ossec.conf inside <syscheck> block with:
    - <directories realtime="yes" check_all="yes">/root/.ssh,'/home/*/.ssh'</directories
