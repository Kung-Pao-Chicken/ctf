#include<stdio.h>
#include<stdlib.h>
#include<time.h>

void main(int argc,char **argv)
{
	double a=time(0);
	int i=0;
//	printf("Time:%.0lf\n",a);
	if(argc>1)
	{
		a=atof(argv[1]);
	}
	srand(a);
	for(;i<100;i++)
	{
		srand(rand());
		double tmp=rand()%99999+1;
		printf("%.0lf\n",tmp);
	}	
}
