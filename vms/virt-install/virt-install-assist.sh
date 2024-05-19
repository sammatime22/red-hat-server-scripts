# Just a simple script to navigate the creation of a VM with virt-install
# author: sammatime22, 2024
# v1: basic virt-install navigation without much error checking, etc.

endprog() {
    tput sgr0
    exit
}

if ! command -v virt-install &> /dev/null
then
    printf "\033[31m]"
    echo "virt-install is not on this machine"
    endprog
fi

# Ask for the VMs name
read -p "Provide the name of the VM you wish to create: " vm_name

# Ask the user to provide a description
read -p "Please give a description for the VM: " vm_description

# In GB, ask how much RAM is required
read -p "How much RAM is in use for the VM? (GBs): " vm_ram 
# RAM is in units of 1024 MB/GB
declare -i vm_ram=${vm_ram}*1024

# In GB, ask how much storage is required
read -p "How much storage is in use for the VM? (GBs): " vm_storage

# Provide the number of VCPUs the VM will use
read -p "How many VCPUs will the VM use?: " vm_vcpus

# (don't) Ask for the OS type and variant
echo "The OS type and variant will be detected from the ISO"

# Ask for the path to the ISO
read -p "Provide the full filepath to the ISO in use: " iso_filepath
# Ensure qemu can read the ISO
sudo chmod +0555 ${iso_filepath}

# Ask for the name of the network interface
ifconfig
read -p "Provide the name of the network interface you'd like to use: " network_interface

# Check with the user on their selections
echo "listed below are your selections"
echo "VM Name:           ${vm_name}"
echo "VM Description:    ${vm_description}"
echo "VM RAM:            ${vm_ram}"
echo "VM Storage:        ${vm_storage}"
echo "VM VCPUs:          ${vm_vcpus}"
echo "ISO Filepath:      ${iso_filepath}"
echo "Network Interface: ${network_interface}"
read -p "Are you okay with your selections? [y/<anything else>]: " confirm_selection

if [[ ${confirm_selection} != "y" ]]
then
    endprog
fi

# Check with the user that the final command looks okay
echo "The following is the command to be submitted"
echo "
sudo virt-install \
  --name ${vm_name} \
  --description \"${vm_description}\" \
  --ram=${vm_ram} \
  --vcpus=${vm_vcpus} \
  --osinfo detect=on \
  --disk path=/var/lib/libvirt/images/${vm_name}.qcow2,bus=virtio,size=${vm_storage} \
  --graphics none \
  --location ${iso_filepath} \
  --console pty,target_type=serial -x 'console=ttyS0,115200n8 serial'\
  --network bridge:${network_interface}
"
read -p "Would you like to move forward with this command? [y/<anything else>]: " confirm_command
if [[ ${confirm_command} != "y" ]]
then 
    endprog
fi

# Submit!
sudo virt-install --name ${vm_name} --description "${vm_description}" --ram=${vm_ram} --vcpus=${vm_vcpus} --osinfo detect=on --disk path=/var/lib/libvirt/images/${vm_name}.qcow2,bus=virtio,size=${vm_storage} --graphics none --location ${iso_filepath} --console pty,target_type=serial -x 'console=ttyS0,115200n8 serial' --network bridge:${network_interface}