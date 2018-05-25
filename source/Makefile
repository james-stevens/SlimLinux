
INSTALL_CMD=install -vC

TARGETS=all_addrs regexp switch_screen

CC=gcc -Wall -O2

all: $(TARGETS)

clean:
	rm -f $(TARGETS)

strip:
	strip -p $(TARGETS)

install:
	strip -p $(TARGETS)
	$(INSTALL_CMD) $(TARGETS) ../install_os/sbin
