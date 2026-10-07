/* ChihiroPack portable Windows launcher. MIT license. */
#ifndef UNICODE
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif
#include <windows.h>
#include <wchar.h>
#include <stdio.h>
#include <stdlib.h>

static wchar_t command[65536];
static size_t position;
static void put(wchar_t c) {
    if(position+1 >= sizeof(command)/sizeof(command[0])) {
        fwprintf(stderr,L"Command line is too long\n");exit(1);
    }
    command[position++]=c;command[position]=0;
}
static void argument(const wchar_t *s) {
    if(position)put(L' ');
    put(L'"');
    while(*s) {
        unsigned slashes=0;
        while(*s==L'\\'){slashes++;s++;}
        if(*s==L'"') {
            for(unsigned i=0;i<slashes*2+1;i++)put(L'\\');
            put(*s++);
        }else if(!*s) {
            for(unsigned i=0;i<slashes*2;i++)put(L'\\');
        }else {
            for(unsigned i=0;i<slashes;i++)put(L'\\');
            put(*s++);
        }
    }
    put(L'"');
}
int wmain(int argc,wchar_t **argv) {
    wchar_t home[32768],python[32768],script[32768];
    DWORD n=GetModuleFileNameW(NULL,home,32768);
    if(!n||n>=32768)return 1;
    wchar_t *slash=wcsrchr(home,L'\\');if(!slash)return 1;*slash=0;
    if(wcslen(home)>32000)return 1;
    swprintf(python,32768,L"%ls\\runtime\\python.exe",home);
    swprintf(script,32768,L"%ls\\chihiro_pack.py",home);
    argument(python);argument(L"-X");argument(L"utf8");argument(script);
    for(int i=1;i<argc;i++)argument(argv[i]);
    DWORD ids[4];DWORD console=GetConsoleProcessList(ids,4);
    if(console==1)argument(L"--pause");
    STARTUPINFOW si={0};PROCESS_INFORMATION pi={0};si.cb=sizeof(si);
    if(!CreateProcessW(python,command,NULL,NULL,TRUE,0,NULL,NULL,&si,&pi)) {
        fwprintf(stderr,L"Could not start bundled Python (%lu). Extract the whole ZIP and keep runtime beside ChihiroPack.exe.\n",GetLastError());
        if(console==1){fwprintf(stderr,L"Press Enter to close...\n");getwchar();}
        return 1;
    }
    WaitForSingleObject(pi.hProcess,INFINITE);DWORD status=1;GetExitCodeProcess(pi.hProcess,&status);
    CloseHandle(pi.hThread);CloseHandle(pi.hProcess);return (int)status;
}
