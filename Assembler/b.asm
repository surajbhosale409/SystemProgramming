section .data
a dd 10

section .text
global main

main:
	add dword[a],10
