# Toradex kernel-fitimage.bbclass extension
#
# This bbclass extends OE's kernel-fitimage.bbclass by overridding
# some functions according to Toradex specific requirements.
#
# Copyright 2021 (C) Toradex AG

inherit toradex-fitimage

kernel_do_deploy_append() {
	# Update deploy directory
	if echo ${KERNEL_IMAGETYPES} | grep -wq "fitImage"; then
		echo "Copying fit-image.its source file..."
		install -m 0644 ${B}/fit-image.its "$deployDir/fitImage-its-${KERNEL_FIT_NAME}.its"
		ln -snf fitImage-its-${KERNEL_FIT_NAME}.its "$deployDir/fitImage-its-${IMAGE_NAME}"

		echo "Copying linux.bin file..."
		install -m 0644 ${B}/linux.bin $deployDir/fitImage-linux.bin-${KERNEL_FIT_NAME}.bin
		ln -snf fitImage-linux.bin-${KERNEL_FIT_NAME}.bin "$deployDir/fitImage-linux.bin-${IMAGE_NAME}"

		if [ -n "${INITRAMFS_IMAGE}" ]; then
			echo "Copying fit-image-${INITRAMFS_IMAGE}.its source file..."
			install -m 0644 ${B}/fit-image-${INITRAMFS_IMAGE}.its "$deployDir/fitImage-its-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}.its"
			ln -snf fitImage-its-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}.its "$deployDir/fitImage-its-${INITRAMFS_IMAGE_NAME}-${IMAGE_NAME}"

			echo "Copying fitImage-${INITRAMFS_IMAGE} file..."
			install -m 0644 ${B}/arch/${ARCH}/boot/fitImage-${INITRAMFS_IMAGE} "$deployDir/fitImage-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}.bin"
			ln -snf fitImage-${INITRAMFS_IMAGE_NAME}-${KERNEL_FIT_NAME}.bin "$deployDir/fitImage-${INITRAMFS_IMAGE_NAME}.bin"
		fi
		if [ "${UBOOT_SIGN_ENABLE}" = "1" -a -n "${UBOOT_DTB_BINARY}" ] ; then
			# UBOOT_DTB_IMAGE is a realfile, but we can't use
			# ${UBOOT_DTB_IMAGE} since it contains ${PV} which is aimed
			# for u-boot, but we are in kernel env now.
			install -m 0644 ${B}/u-boot-${MACHINE}*.dtb "$deployDir/"
		fi
	fi
}