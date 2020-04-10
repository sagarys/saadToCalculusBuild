echo "copying....."
ROBOCOPY %1 %2 %3  /R:1 /W:1 /LOG:%4
echo "copied !!!!!!!!"

IF %ERRORLEVEL% NEQ 1 ( 
   echo %ERRORLEVEL%
   echo "Error While Copying file" 
   EXIT 1
)

rem pause 
EXIT 0