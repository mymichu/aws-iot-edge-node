# Simple initramfs image. Mostly used for live images.
DESCRIPTION = "Small image capable of booting a device. The kernel includes \
the Minimal RAM-based Initial Root Filesystem (initramfs), which one can use \
to check the hardware efficiently."

PACKAGE_INSTALL = "initramfs-debug\
    busybox\
    base-passwd \
    e2fsprogs-mke2fs \
    dosfstools \
    curl \
    lz4 \
    lzop \
    xz \
    tar \
    pv \
    mmc-utils"

# Do not pollute the initrd image with rootfs features
IMAGE_FEATURES = ""

export IMAGE_BASENAME = "image-initramfs"
IMAGE_LINGUAS = ""

IMAGE_FSTYPES = "${INITRAMFS_FSTYPES}"
inherit core-image

IMAGE_ROOTFS_SIZE = "8192"
IMAGE_ROOTFS_EXTRA_SPACE = "0"

BAD_RECOMMENDATIONS += "busybox-syslog"
