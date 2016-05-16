@echo off
   :begin
	
	set/p pdmFile= pdm file Name (.\pdm\ctshop.pdm):
	set/p tableName= Table Name (all):

	del /q /s .\src\* > nul

	if "%pdmFile%"=="" (
		python DB2java.py .\pdm\ctshop.pdm %tableName%
	) else (
   		python DB2java.py %pdmFile% %tableName%	
	)

	start .\src
   pause
eof