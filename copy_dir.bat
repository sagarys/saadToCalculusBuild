echo "copying....."
ROBOCOPY %1 %2 /S /R:1 /W:1 /LOG:%3﻿
echo "copied !!!!!!!!"

IF %ERRORLEVEL% NEQ 1 ( 
   echo "Error While Copying directory" 
   EXIT 1
)

EXIT 0