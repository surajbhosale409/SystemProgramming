section .data
a dd 10

section .text
global xyz

xyz:
	add dword[a],10
