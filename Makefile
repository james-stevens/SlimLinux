
default: mkiso.cfg
	sh -c "cd source; make"
	sh mkiso

all: mkiso.cfg
	sh -c "cd source; make all"
	sh mkiso

iso: mkiso.cfg default

clean:
	sh -c "cd source; make clean"
	sh mkiso clean

rootfs: mkiso.cfg
	sh mkiso rootfs

initrd: mkiso.cfg iso/isolinux/initrd.img
	sh mkiso initrd

config:
	rm -f mkiso.cfg
	./configure
	sh -c "make clean all"

mkiso.cfg: ./configure

dvd:
	./burn dvd

usb:
	./burn usb

bootusb:
	./burn bootusb
