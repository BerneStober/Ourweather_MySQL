cd C:\Users\berny\source\repos\
SET /A XCOUNT=1
:here
	Echo run python from command line   %XCOUNT%
	
SET /A XCOUNT+=1

python C:\Users\berny\source\repos\JustWriteMySQLData.py


TIMEOUT 60

rem GOTO:here