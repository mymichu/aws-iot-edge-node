inherit core-image kernel-artifact-names 
# Simple initramfs image. Mostly used for live images.
DESCRIPTION = "Small image capable of booting a device. The kernel includes \
the Minimal RAM-based Initial Root Filesystem (initramfs), which one can use \
to check the hardware efficiently."
LICENSE = "MIT"

export IMAGE_BASENAME = "image-initramfs"
MACHINE_NAME ?= "${MACHINE}"
IMAGE_NAME = "${MACHINE_NAME}_${IMAGE_BASENAME}"

add_rootfs_version () {
    printf "${DISTRO_NAME} ${DISTRO_VERSION} (${DISTRO_CODENAME}) \\\n \\\l\n" > ${IMAGE_ROOTFS}/etc/issue
    printf "${DISTRO_NAME} ${DISTRO_VERSION} (${DISTRO_CODENAME}) %%h\n" > ${IMAGE_ROOTFS}/etc/issue.net
    printf "${IMAGE_NAME}\n\n" >> ${IMAGE_ROOTFS}/etc/issue
    printf "${IMAGE_NAME}\n\n" >> ${IMAGE_ROOTFS}/etc/issue.net
}

add_symlink_image (){
    rm -rf ${DEPLOY_DIR_IMAGE}/fitImage-deploy.bin
    ln -s ${DEPLOY_DIR_IMAGE}/fitImage-${IMAGE_BASENAME}-${MACHINE}-${KERNEL_ARTIFACT_NAME}.bin ${DEPLOY_DIR_IMAGE}/fitImage-deploy.bin
}
# add the rootfs version to the welcome banner
ROOTFS_POSTPROCESS_COMMAND += " add_rootfs_version;"
#IMAGE_POSTPROCESS_COMMAND += " add_symlink_image;"

#${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}

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
