include iot-edge-image.bb

IMAGE_NAME = "image-initramfs-iot-edge"
IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"

PACKAGE_INSTALL = "${IMAGE_INSTALL}"