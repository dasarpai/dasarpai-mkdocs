# Define the search text and destination folder
$searchText = '{% include embed-audio.html src'
$destinationFolder = "docs\samskrutyatra\chanting"
$sourcefolder = "docs\samskrutyatra"

# Create the destination folder if it doesn't exist
if (-not (Test-Path $destinationFolder)) {
    New-Item -ItemType Directory -Path $destinationFolder | Out-Null
}

# Search all files in the source folder recursively
Get-ChildItem -Path $sourcefolder -Recurse -File | ForEach-Object {
    $filePath = $_.FullName
    $targetPath = Join-Path $destinationFolder $_.Name

    # Skip if file is already in destination (case-insensitive comparison)
    if ($filePath -ieq $targetPath) {
        Write-Host "Skipping (already in destination): $filePath"
        return
    }

    # Skip if file exists in destination and came from same directory
    if (Test-Path $targetPath -PathType Leaf) {
        Write-Host "Skipping (already exists in destination): $filePath"
        return
    }

    # Use Select-String to find the text in the file
    if (Select-String -Path $filePath -Pattern $searchText -Quiet) {
        Write-Host "Copying file: $filePath"
        Copy-Item -Path $filePath -Destination $destinationFolder -Force
    }
}