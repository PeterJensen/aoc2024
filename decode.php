<?php

function formatTime($day, $t) {
  if ($t == 0) {
    return "DNF     ";
  }
  $startTime = mktime(21, 0, 0, 12, intval($day)-1, 2021);
  $elapsedTime = $t - $startTime;
//  if ($elapsedTime >= 24*60*60) {
//    return ">24h    ";
//  }
  return gmdate("z:H:i:s", $elapsedTime);
}

function main() {
  date_default_timezone_set('America/Los_Angeles');
  global $argv;
  $json = json_decode(file_get_contents($argv[1]));
  foreach ($json->members as $member) {
    printf("%s\n", $member->name);
    $ao = new ArrayObject($member->completion_day_level);
    $ao->ksort();
    foreach ($ao as $day => $levels) {
      $l1Time = formatTime($day, $levels->{"1"}->get_star_ts);
      $l2Ts = isset($levels->{"2"}->get_star_ts) ? $levels->{"2"}->get_star_ts : 0;
      $l2Time = formatTime($day, $l2Ts);
      printf("Day %s: %s, %s\n", $day, $l1Time, $l2Time);
    }
  }
//  $jsonStr = json_encode($json, JSON_PRETTY_PRINT);
//  echo $jsonStr;
}

main()

?>
