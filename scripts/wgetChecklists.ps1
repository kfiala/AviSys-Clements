# Download state checklists from eBird
# Run from PowerShell command line

# The eBird URL could change from time to time; adjustments may be necessary

$States =
'US-AL','US-AK','US-AZ','US-AR','US-CA','US-CO','US-CT','US-DE',
'US-DC','US-FL','US-GA','US-HI','US-ID','US-IL','US-IN','US-IA',
'US-KS','US-KY','US-LA','US-ME','US-MD','US-MA','US-MI','US-MN',
'US-MS','US-MO','US-MT','US-NE','US-NV','US-NH','US-NJ','US-NM',
'US-NY','US-NC','US-ND','US-OH','US-OK','US-OR','US-PA','US-RI',
'US-SC','US-SD','US-TN','US-TX','US-UT','US-VT','US-VA','US-WA',
'US-WV','US-WI','US-WY','CA-AB','CA-BC','CA-MB','CA-NB','CA-NL',
'CA-NT','CA-NS','CA-ON','CA-PE','CA-QC','CA-SK','CA-YT','CA-NU'



$URLbase = 'http://ebird.org/ebird/subnational1/'
$URLquery = '?yr=all&m=&rank=mrec&hs_sortBy=taxon_order&hs_o=asc'
$folder = 'State checklists\html\'   # Important: The folder must exist

Foreach ($state IN $states)
{
   $wget = ('Invoke-webRequest -URI "' + $URLbase + $state + $URLquery + '" -outfile "' + $folder + $state + '.html"')
   Write-Host $wget
   Invoke-Expression $wget
}
