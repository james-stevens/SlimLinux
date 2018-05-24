#include <stdio.h>
#include <memory.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>


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
	mask = ntohl(inet_addr(argv[2]));

	first = addr & mask;
	last = mask ^ 0xFFFFFFFF;
	last |= addr;

	printf ("%s . ",ipchar(htonl(last-1)));
	for(loop=first+1;loop<last;loop++) if (loop!=addr) printf ("%s . ",ipchar(htonl(loop)));

	return 0;
}
