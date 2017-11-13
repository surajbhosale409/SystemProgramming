section .data
a db "Hello",0
a dw 12
123 dd 10
len equ $-a

section .bss
b resb 5
d resd -10
y dw 10

section .text
global main
main:
      mov al,'a'
      mov esi,a
l1@:
      mov edi,bii
z dd 10
      mov ecx,5
      add eax,1000
he_re_:
he-re-:
      jmp here
      call calc
      repe movsb
