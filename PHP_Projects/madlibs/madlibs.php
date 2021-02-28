<?php
    function generateStory($season1, $season2, $location, $adjective) {
        $file = fopen("richardIII.txt", "r") or die("Unable to open file!");
        $text = fread($file,filesize("richardIII.txt"));
        fclose($file);
        $holders = array("SEASON1","ADJECTIVE","SEASON2","LOCATION");
        $replace_arr = array($season1, $adjective, $season2, $location);
        $text = str_replace($holders, $replace_arr, $text);
        return $text; 
    }

    $season1 = readline("Enter a season: ");
    $season2 = readline("Enter another season: ");
    $location = readline("Enter a location: ");
    $adjective = readline("Enter an adjective: ");
    echo generateStory($season1,$season2,$location,$adjective);
