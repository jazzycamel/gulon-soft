/*
  WINDOWS SHARED MEMORY FILE EXAMPLE
  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  From: http://comsci.liu.edu/~murali/win32/SharedMemory.htm
*/

#include <windows.h>
#include <assert.h>
#include <stdio.h>

static const LONG BufferSize=100;
static const LONG Buffers=10;
static const char MemoryName[]="Share Memory Name";
static char (*Memory)[Buffers][BufferSize];
static const char WriterSemaphoreName[]="Writer Semaphore";
static const char ReaderSemaphoreName[]="Reader Semaphore";

static HANDLE hWriterSemaphore;
static HANDLE hReaderSemaphore;
static HANDLE hMemory;

int main(void)
    {
    hWriterSemaphore=CreateSemaphore(NULL,Buffers,Buffers,WriterSemaphoreName);
    assert(hWriterSemaphore!=NULL);

    hReaderSemaphore=CreateSemaphore(NULL,0,Buffers,ReaderSemaphoreName);
    assert(hReaderSemaphore!=NULL);

    hMemory=CreateFileMapping((HANDLE)0xFFFFFFFF,NULL,PAGE_READWRITE,0
        ,sizeof(char [Buffers][BufferSize]),MemoryName);
    assert(hMemory!=NULL);

    Memory=(char (*)[Buffers][BufferSize])MapViewOfFile(hMemory
        ,FILE_MAP_WRITE,0,0,sizeof(char [Buffers][BufferSize]));
    assert(Memory!=NULL);

    for(int i=0;;++i)
        {
        WaitForSingleObject(hWriterSemaphore,INFINITE);
        printf("Writing to Buffer %i\n",i);
        wsprintf((*Memory)[i%Buffers],"This is the writer - %i\n",i);
    
        Sleep(1000);

        ReleaseSemaphore(hReaderSemaphore,1,NULL);
        }

    UnmapViewOfFile(Memory); 
    CloseHandle(hWriterSemaphore); CloseHandle(hReaderSemaphore);
    return 0;
    }
