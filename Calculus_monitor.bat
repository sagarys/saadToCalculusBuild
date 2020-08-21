cd "C:\Sustaining_Daily_Builds"
python "C:\Sustaining_Daily_Builds\Calculus_monitor.py"
ROBOCOPY "\\bauser\Fiery-products\Sustaining_builds" "\\bawdfs01\OUTBOX\TO-FC\Sustaining_Builds" /S /R:1 /W:1 /LOG:BuildCopy.txt