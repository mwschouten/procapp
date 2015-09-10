#!/bin/bash
echo ' $1 : ' $1
echo '    : ' matlab  -nosplash -nodesktop -r "try; $1; catch e; fprintf('Error: %s\n', e.message); exit(1);end;exit(0)"
matlab  -nosplash -nodesktop -r "try; $1; catch e; fprintf('Error: %s\n', e.message); exit(1);end;exit(0)"
exit $?

