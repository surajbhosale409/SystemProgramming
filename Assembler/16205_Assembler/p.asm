section .data
 fmt db "%d  ",0
 a dd 0

section .bss
 sum resd 1


section .text
 global main

main:
  
   
    mov ecx,5
    mov eax,0
    mov ebx,1
    mov edx,0
    add dword[a],10

    pusha
    push eax
    push fmt
    add esp,8
    popa

    pusha
    push ebx
    push fmt
    add esp,8
    popa

lp:
    mov edx,0
    add edx,eax
    add edx,ebx
    pusha
    push edx
    push fmt
    add esp,8
    popa
    mov eax,ebx
    mov ebx,edx

    ret

