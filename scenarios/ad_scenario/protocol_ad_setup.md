# Active Directory Setup
a detailed how to Active Directory setup from my perspective with all necessary screenshots and configf

## First Steps
- download the windows server iso off Microsoft official website
- i chose the 2025 version, as its the newest one and endorsed to use by Microsoft
- after iso is downloaded onto our machine, we can create the machine in virt-manager
- we assign 4 CPU cores and at least 6gb memory to the machine, as windows manager is heavy reliant on resources
![Virtual Machine Setup](screenshots/virtualmachine_setup.png)
- also we assign size for the disk image, minimum is at 32gb i will be assigning 40gb
![Virtual Machine Disk Space allocation](screenshots/vm_diskspace.png)
- also we change Cache mode in out disk to none for security and performance reasons
![Disk Setup](screenshots/storage_setup.png)
- we start installation, set language we would like to install
    - english in my case
![Language](screenshots/language.png)
- at the image type, i select a headless standard evaluation
![Image Type](screenshots/image_type.png)
- and lastly we choose our 40gb partition for installation location
![Install Location](screenshots/install_location.png)
- then we proceed with installation
- we setup password and proceed into Command Line of the server
![Password Setup](screenshots/password.png)
![Command Line](screenshots/command_line.png)
