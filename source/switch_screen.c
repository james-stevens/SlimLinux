#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <linux/vt.h>


int main(int argc, char * argv[])
{
int fd,scrn;

	scrn = atoi(argv[1]);
	fd = open("/dev/console",O_RDONLY);
	ioctl(fd,VT_ACTIVATE,scrn);
	close(fd);
	return 0;
}
