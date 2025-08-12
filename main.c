#include "com.h"
#include <time.h>
int fd;
char read_buffer[BUFFER_SIZE];
int read_buffer_size, now;
char* comp = "$GPGGA";


int main()
{
  fd = open_port("/dev/ttyACM0");
  if(set_com_config(fd, 115200, 8, 'N', 1) < 0) //配置串口
  {
    perror("set_com_config");
    return 1;
  }
  while (1) {
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    char date_format[25];
    sprintf(date_format,"device_%d-%02d-%02d_%02d.txt",tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday, tm.tm_hour);

    FILE *fp = fopen(date_format, "a");
    if (fp == NULL) {
        perror("Error opening file");
        return 1;
    }
    memset(read_buffer,0, BUFFER_SIZE);
    read_buffer_size= read_Buffer(fd, read_buffer);
    if(read_buffer_size > 0){
      char *token = strtok(read_buffer, "\n");
      while (token != NULL) {
	  char temp[6];
	  strncpy(temp,token,6);
	  temp[6]='\0';
	  if(strcmp(comp, temp)== 0){
	     fprintf(fp, "%s\n",token);
             printf("%s\n", token);
	  }
          token = strtok(NULL, "\n");
      }
    }
    fclose(fp);
  }
}
