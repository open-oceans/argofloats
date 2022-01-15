# Profile Export

This tool allows you to search the argo floats database using either a lat long and a buffer area , or a geometry.geojson file or a given profile id. This tool is also capable to running long time searches overcoming the 3 month limit constrained by the argovis API. All use cases are shown below. The outputs are written as CSV file with a prefix argoprofile_

```
argofloats profile-export -h
usage: argofloats profile-export [-h] --path PATH [--lat LAT] [--lon LON]
                                 [--radius RADIUS] [--start START] [--end END]
                                 [--plid PLID] [--geometry GEOMETRY]

optional arguments:
  -h, --help           show this help message and exit

Required named arguments.:
  --path PATH          Full path to export platform profile CSV

Optional named arguments:
  --lat LAT            Latitude
  --lon LON            Longitude
  --radius RADIUS      Search radius in kilometers for square buffer
  --start START        Start Date YYYY-MM-DD
  --end END            End Date YYYY-MM-DD
  --plid PLID          Platform Profile ID
  --geometry GEOMETRY  Full path to geometry.geojson file
```


#### Using Profile ID
This uses the pofile ID and simply exports the profile as a CSV

![argofloats_export_plid](https://user-images.githubusercontent.com/6677629/149610498-d0b64a04-2abb-4644-b874-911323e32cb9.gif)

#### Using point geometry
This uses a lat long and radius to search in kilometers along with start and end date and exports all matching profiles to individual CSV files

![argofloats_export](https://user-images.githubusercontent.com/6677629/149610499-f04d00df-2cb6-4fdd-a865-b240e846c5cb.gif)

#### Using geometry GeoJSON file
This makes uses of a geojson file along with start and end date and exports all matching profiles to individual CSV files

![argofloats_export_geom](https://user-images.githubusercontent.com/6677629/149610496-f188d470-97e5-48bc-add6-5e55175b79ce.gif)
