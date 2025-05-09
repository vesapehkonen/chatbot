#!/bin/bash
set -e

MOUNT_POINT="/mnt/models"
DEVICE="/dev/nvme1n1"

# Check if already mounted
if mount | grep -q "$MOUNT_POINT"; then
  echo "NVMe already mounted at $MOUNT_POINT"
  exit 0
fi

# Create mount point if needed
echo "Creating mount point at $MOUNT_POINT..."
sudo mkdir -p "$MOUNT_POINT"

# Format the device if it doesn't have a filesystem
if ! sudo blkid "$DEVICE" >/dev/null 2>&1; then
  echo "Formatting $DEVICE with ext4..."
  sudo mkfs.ext4 "$DEVICE"
fi

# Mount the disk
echo "Mounting $DEVICE to $MOUNT_POINT..."
sudo mount "$DEVICE" "$MOUNT_POINT"

# Optional: persist in /etc/fstab
# Uncomment if you want it auto-mounted on reboot
# if ! grep -qs "$DEVICE" /etc/fstab; then
#   echo "$DEVICE $MOUNT_POINT ext4 defaults,nofail 0 0" | sudo tee -a /etc/fstab > /dev/null
#   echo " Added to /etc/fstab for persistence"
# fi

# Set permissions
sudo chmod 777 /mnt
sudo chmod 777 "$MOUNT_POINT"

echo "NVMe disk is mounted and ready at $MOUNT_POINT"
