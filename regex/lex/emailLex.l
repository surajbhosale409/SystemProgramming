%%
[a-z][a-z|0-9|.|_]*[@][a-z]+[.][a-z]+ { printf("Accpeted %s",yytext);}
.* {printf("Not Accepted %s",yytext);}
%%

int main()
{
 yylex();
 return 0;
}
