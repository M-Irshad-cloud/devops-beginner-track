function Query-Loki([string]$q, [string]$Since = "6h", [int]$Limit = 15) {
  $uri = "http://localhost:3100/loki/api/v1/query_range?direction=backward&limit=$Limit&since=$Since&query=" + [uri]::EscapeDataString($q)
  $r = Invoke-RestMethod $uri
  $rows = foreach ($s in $r.data.result) { foreach ($v in $s.values) {
    $ts = [DateTimeOffset]::FromUnixTimeMilliseconds([long]([decimal]$v[0] / 1000000)).ToLocalTime()
    [pscustomobject]@{ ts = $ts; when = $ts.ToString("MM-dd HH:mm:ss"); line = $v[1] } } }
  if ($rows) { $rows | Sort-Object ts -Descending | Select-Object -First $Limit -Property when, line | Format-Table -AutoSize -Wrap } else { "no matching lines" }
}

function Query-LokiMetric([string]$q) {
  $r = Invoke-RestMethod ("http://localhost:3100/loki/api/v1/query?query=" + [uri]::EscapeDataString($q))
  if (-not $r.data.result) { "no data"; return }
  foreach ($x in $r.data.result) {
    $labels = ($x.metric.PSObject.Properties | ForEach-Object { "$($_.Name)=$($_.Value)" }) -join ","
    "{0}  =>  {1}" -f $labels, [math]::Round([double]$x.value[1], 3)
  }
}

$P = '| pattern `<ip> - - [<ts>] "<method> <path> <_>" <status> <size> "<_>" "<agent>" "<_>"`'
