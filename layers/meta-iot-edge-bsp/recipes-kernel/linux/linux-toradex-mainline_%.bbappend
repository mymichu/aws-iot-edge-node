FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
SRC_URI += "file://tp-linkwn725.cfg \
            file://0001-add-iot-edge-dt.patch \
            file://imx6dl-colibri-iot-edge.dts"

do_configure_prepend() {
    cp ${WORKDIR}/imx6dl-colibri-iot-edge.dts ${S}/arch/arm/boot/dts
}