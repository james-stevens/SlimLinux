#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <ctype.h>
#include <sys/stat.h>


#define FILENAME "/etc/init.env"


void do_set_env()
{
struct stat sbuf;
FILE * fp;

	if (stat(FILENAME,&sbuf)) return;

	if ((fp = fopen(FILENAME,"r"))==NULL) {
		fprintf(stderr,"ERROR: '%s' failed to open\n",FILENAME);
		return; }

	char line[200];
	while(fgets(line,sizeof(line),fp)!=NULL) {
		char * end=line+strlen(line),*eq,*cp=line;

		while ((end>=line)&&((end[-1]=='\'')||(end[-1]=='"')||(end[-1]<=' '))) end--;
		*end=0;

		if (end==line) continue;

		while ((cp<end)&&(isblank(*cp))) cp++;

		if (*cp=='#') continue;

		if ((eq = strchr(cp,'='))==NULL) continue;
		*eq=0;eq++;
		if ((*eq=='\'')||(*eq=='"')) eq++;

		if (setenv(cp,eq,1))
			fprintf(stderr,"ERROR: failed to set '%s' to '%s' (%s)\n",cp,eq,strerror(errno));
		}
	fclose(fp);
}



int main(int argc,char * argv[])
{
	if (getpid()==1) do_set_env();
	char * dst = "/usr/sbin/init";
	if (execv(dst,argv)) fprintf(stderr,"ERROR: exec '%s' failed - %s\n",dst,strerror(errno));

	return 0;
}
