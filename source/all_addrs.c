#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

struct v4_netmask_st {
    char * mask;
    uint32_t bmask,bits,adds;
    };

struct v4_netmask_st v4masks[] = {
    { "0.0.0.0", 0x00000000, 0, 4294967295 },
    { "128.0.0.0", 0x80000000, 1, 2147483647 },
    { "192.0.0.0", 0xC0000000, 2, 1073741823 },
    { "224.0.0.0", 0xE0000000, 3, 536870911 },
    { "240.0.0.0", 0xF0000000, 4, 268435455 },
    { "248.0.0.0", 0xF8000000, 5, 134217727 },
    { "252.0.0.0", 0xFC000000, 6, 67108863 },
    { "254.0.0.0", 0xFE000000, 7, 33554431 },
    { "255.0.0.0", 0xFF000000, 8, 16777215 },
    { "255.128.0.0", 0xFF800000, 9, 8388607 },
    { "255.192.0.0", 0xFFC00000, 10, 4194303 },
    { "255.224.0.0", 0xFFE00000, 11, 2097151 },
    { "255.240.0.0", 0xFFF00000, 12, 1048575 },
    { "255.248.0.0", 0xFFF80000, 13, 524287 },
    { "255.252.0.0", 0xFFFC0000, 14, 262143 },
    { "255.254.0.0", 0xFFFE0000, 15, 131071 },
    { "255.255.0.0", 0xFFFF0000, 16, 65535 },
    { "255.255.128.0", 0xFFFF8000, 17, 32767 },
    { "255.255.192.0", 0xFFFFC000, 18, 16383 },
    { "255.255.224.0", 0xFFFFE000, 19, 8191 },
    { "255.255.240.0", 0xFFFFF000, 20, 4095 },
    { "255.255.248.0", 0xFFFFF800, 21, 2047 },
    { "255.255.252.0", 0xFFFFFC00, 22, 1023 },
    { "255.255.254.0", 0xFFFFFE00, 23, 511 },
    { "255.255.255.0", 0xFFFFFF00, 24, 255 },
    { "255.255.255.128", 0xFFFFFF80, 25, 127 },
    { "255.255.255.192", 0xFFFFFFC0, 26, 63 },
    { "255.255.255.224", 0xFFFFFFE0, 27, 31 },
    { "255.255.255.240", 0xFFFFFFF0, 28, 15 },
    { "255.255.255.248", 0xFFFFFFF8, 29, 7 },
    { "255.255.255.252", 0xFFFFFFFC, 30, 3 },
    { "255.255.255.254", 0xFFFFFFFE, 31, 1 },
    { "255.255.255.255", 0xFFFFFFFF, 32, 0 }
    };




char * ipchar(in_addr_t addr)
{
struct in_addr ad;

    memset(&ad,0,sizeof(ad));
    ad.s_addr = addr;
    return inet_ntoa(ad);
}




int main(int argc,char * argv[])
{
in_addr_t addr,mask,first,last,loop;

	addr = ntohl(inet_addr(argv[1]));
	int m = atoi(argv[2]);
	mask = v4masks[m].bmask;

	first = addr & mask;
	last = mask ^ 0xFFFFFFFF;
	last |= addr;

	printf ("%s . ",ipchar(htonl(last-1)));
	for(loop=first+1;loop<last;loop++) if (loop!=addr) printf ("%s . ",ipchar(htonl(loop)));

	return 0;
}
