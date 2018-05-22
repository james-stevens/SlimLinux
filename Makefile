
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

initrd: mkiso.cfg
	sh mkiso initrd

config:
	rm -f mkiso.cfg
	./configure
	sh -c "make all"

mkiso.cfg: ./configure
