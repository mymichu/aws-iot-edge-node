inherit core-image kernel-artifact-names 

DESCRIPTION = "Small image capable of flashing and partition the emmc flash."
LICENSE = "MIT"

export IMAGE_BASENAME = "image-initramfs"
MACHINE_NAME ?= "${MACHINE}"
IMAGE_NAME = "${MACHINE_NAME}_${IMAGE_BASENAME}"


add_symlink_image (){
    rm -rf ${DEPLOY_DIR_IMAGE}/fitImage-deploy.bin
    ln -s ${DEPLOY_DIR_IMAGE}/fitImage-${IMAGE_BASENAME}-${MACHINE}-${KERNEL_ARTIFACT_NAME}.bin ${DEPLOY_DIR_IMAGE}/fitImage-deploy.bin
}

PACKAGE_INSTALL = "initramfs-debug\
    busybox\
    base-passwd \
    parted \
    wget \
    tftp-hpa \
    lz4 \
    lzop \
    xz \
    tar \
    pv \
    mmc-utils"

# Do not pollute the initrd image with rootfs features
IMAGE_FEATURES = ""

IMAGE_LINGUAS = ""

IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"


IMAGE_ROOTFS_SIZE = "8192"
IMAGE_ROOTFS_EXTRA_SPACE = "0"

BAD_RECOMMENDATIONS += "busybox-syslog"
