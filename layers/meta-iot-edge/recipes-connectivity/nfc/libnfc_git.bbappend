SUMMARY = "Add NFC config"
DESCRIPTION = "NFC Config"
HOMEPAGE = ""
LICENSE = "MIT"

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "\
    file://libnfc.conf \
    file://spidev.conf \
"

do_install_append() {
    install -d ${D}/etc/nfc
    install -m 0644 ${WORKDIR}/libnfc.conf ${D}/etc/nfc
    install -d ${D}/etc/modules-load.d
    install -m 0644 ${WORKDIR}/spidev.conf ${D}/etc/modules-load.d
}