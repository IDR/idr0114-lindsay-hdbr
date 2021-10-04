$dir_files = Read-Host - Prompt "Enter the name of the folder containing the SVS files"
$dir_name = "converted_files"
$dir_intermediate = "conversion_intermediate"
$working_dir = Get-Location

if(!(Test-Path $dir_name)) {
    New-Item -Path $working_dir -Name $dir_name -ItemType "directory"
}

if(!(Test-Path $dir_intermediate)) {
   New-Item -Path $working_dir -Name $dir_intermediate -ItemType "directory"
}

foreach($file in Get-ChildItem $dir_files -Recurse -Filter *.svs) {
    $name_zarr = -join($file.Basename, ".zarr")
    $name_tiff = -join($file.Basename, ".ome.tiff")
    $f = Join-Path -Path $dir_files -ChildPath $file
    $f_zarr = Join-Path -Path $dir_intermediate -ChildPath $name_zarr
    $f_tiff = Join-Path -Path $dir_intermediate -ChildPath $name_tiff
    bioformats2raw $f $f_zarr
    raw2ometiff $f_zarr $f_tiff
    $check = Join-Path -Path $dir_name -ChildPath $file
    if(!(Test-Path $check)) {
        Move-Item $f_tiff -Destination $dir_name
    }
    Remove-Item $f_zarr -Recurse -Force -Confirm:$false
}

Remove-Item $dir_intermediate -Recurse -Force -Confirm:$false
