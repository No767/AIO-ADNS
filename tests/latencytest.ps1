#####################Variables#####################
$numberoftests = 10
###################################################
#####################Main#####################
cls
$dnsserver = "127.0.0.1"
$totalmeasurement = 0
$i = 0
while ($i -ne $numberoftests)
{
    $measurement = (Measure-Command {Resolve-DnsName www.bing.com -Server $dnsserver –Type A}).TotalSeconds

    $totalmeasurement += $measurement

    $i += 1
}
$totalmeasurement = $totalmeasurement / $numberoftests
"DNS Server: " + $dnsserver + ", Response time: " + $totalmeasurement + " seconds"

#Script from https://social.technet.microsoft.com/wiki/contents/articles/38126.how-to-measure-the-response-time-of-dns-servers-when-performing-name-server-lookups.aspx