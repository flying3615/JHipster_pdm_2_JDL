@echo off
   :begin
	for  /f "delims=." %%f in ('dir /b .jhipster') do yo jhipster:entity %%f --force
	pause
eof
