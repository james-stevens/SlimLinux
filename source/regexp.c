#include <stdio.h>
#include <stdlib.h>
#include <regex.h>


int main(int argc,char * argv[])
{
regex_t re;
	
	if (regcomp(&re, argv[1], REG_EXTENDED|REG_NOSUB) != 0) { perror(argv[1]); exit(1); }
	if (regexec(&re, argv[2], (size_t) 0, NULL, 0)==0) exit(0); else exit(1);
}
