# update_arcgis_layers

## About:
The code in this repository was used to create a regional bike infrastructure map that could be easily updated with the latest data. The scripts used in this project aimed to solve two issues with manually downloading open source data:
1. hi

## How to use each function:

```python
cb_to_features(path)
```
#### Creates a layer of updating CitiBike dock locations
#### Input: 
- path = folder path to save CitiBike JSON data to (string)
#### Output: 
- JSON file of most recent CitiBike docks in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of most recent CitiBike docks
  - location: ArcGIS Project geodatabase

```python
osm_to_features(path, query, file_name)
```
#### Creates a layer of any Open Street Map data
#### Input:
- path = folder path to save Open Street Map JSON data to (string)
- query = Overpass Query Langauge, one of Open Street Map's API's query languages, query* (string)
- file_name = name for output JSON file and ArcGIS feature class/layer (string)
#### Output:
- JSON file of queried Open Street Map data in GeoJSON format
  - location: input folder path
- ArcGIS feature class & layer of Open Street Map data
  - location: ArcGIS Project geodatabase
