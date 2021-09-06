inherit core-image

SUMMARY = "IoT Edge image for aws"
DESCRIPTION = "TODO"

LICENSE = "MIT"

#Prefix to the resulting deployable tarball name
export IMAGE_BASENAME = "iot-edge-node"
MACHINE_NAME ?= "${MACHINE}"
IMAGE_NAME = "${MACHINE_NAME}_${IMAGE_BASENAME}"

# Copy Licenses to image /usr/share/common-license
COPY_LIC_MANIFEST ?= "1"
COPY_LIC_DIRS ?= "1"

add_rootfs_version () {
    printf "${DISTRO_NAME} ${DISTRO_VERSION} (${DISTRO_CODENAME}) \\\n \\\l\n" > ${IMAGE_ROOTFS}/etc/issue
    printf "${DISTRO_NAME} ${DISTRO_VERSION} (${DISTRO_CODENAME}) %%h\n" > ${IMAGE_ROOTFS}/etc/issue.net
    printf "${IMAGE_NAME}\n\n" >> ${IMAGE_ROOTFS}/etc/issue
    printf "${IMAGE_NAME}\n\n" >> ${IMAGE_ROOTFS}/etc/issue.net
}
# add the rootfs version to the welcome banner
ROOTFS_POSTPROCESS_COMMAND += " add_rootfs_version;"

#CONMANPKGS ?= "connman connman-plugin-loopback connman-plugin-ethernet connman-plugin-wifi connman-client"

IMAGE_LINGUAS = "en-us"

#IMAGE_FEATURES+="read-only-rootfs"


IMAGE_INSTALL += " \
    packagegroup-boot \
    packagegroup-basic \
    dosfstools \
    e2fsprogs-mke2fs \
    iproute2 \
    libgomp \
    libsoc \
    mtd-utils \
    set-hostname \
    u-boot-fw-utils \
    bmode-usb \
    avahi-autoipd \
    curl \
    linuxptp \
    ppp \
    ptpd \
    linux-firmware-ath10k    \
    linux-firmware-sd8686    \
    linux-firmware-sd8688    \
    linux-firmware-sd8787    \
    linux-firmware-sd8797    \
    linux-firmware-sd8887    \
    linux-firmware-sd8997    \
    linux-firmware-ralink    \
    linux-firmware-rtl8192cu \
    linux-firmware-rtl8188   \
    udev-extraconf \
    wpa-supplicant \
    greengrass \
    networkmanager \
    libnfc \
    i2c-tools \
    ${@bb.utils.contains('DISTRO_FEATURES', 'systemd', 'systemd-analyze', '', d)} \
"