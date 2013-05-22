#include <cstdio>
#include <string>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <stdint.h>

// EAX CPU support flags
#define EAX_CPU_INFO 0x00000001
#define EAX_CPU_CACHE 0x00000002
#define EAX_CPU_HIGHEST_EXT_FUNC 0x80000h


typedef char code_t;
typedef struct cpuinfo {
	int eax;
	int ebx;
	int ecx;
	int edx;
	char _pad[12];
} cpuinfo_t;

void cpuid(cpuinfo_t *CPUInfo, code_t code)
{
	__asm__ __volatile__ (
		// Assembly
		"cpuid"
		: // Output operands
		"=a" (CPUInfo->eax), // EAX
		"=b" (CPUInfo->ebx), // EBX
		"=c" (CPUInfo->ecx), // ECX
		"=d" (CPUInfo->edx) // EDX
		: // Input operands
		"a" (code)
	);
}


int main()
{
	cpuinfo_t inf;
	cpuid(&inf, EAX_CPU_INFO);
	printf("%d %d %d %d\n", inf.eax, inf.ebx, inf.ecx, inf.edx);
	return 0;
}
