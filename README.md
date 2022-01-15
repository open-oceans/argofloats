# argofloats: Simple CLI for ArgoVis and Argofloats

[![Twitter URL](https://img.shields.io/twitter/follow/samapriyaroy?style=social)](https://twitter.com/intent/follow?screen_name=samapriyaroy)
[![Hits-of-Code](https://hitsofcode.com/github/samapriya/argofloats?branch=main)](https://hitsofcode.com/github/samapriya/argofloats?branch=main)
[![CI argofloats](https://github.com/samapriya/argofloats/actions/workflows/CI.yml/badge.svg)](https://github.com/samapriya/argofloats/actions/workflows/CI.yml)
![PyPI - License](https://img.shields.io/pypi/l/argofloats)
![PyPI](https://img.shields.io/pypi/v/argofloats)
[![Downloads](https://pepy.tech/badge/argofloats/month)](https://pepy.tech/project/argofloats)

Argo is an international program that collects information from inside the ocean using a fleet of robotic instruments that drift with the ocean currents and move up and down between the surface and a mid-water level. Each instrument (float) spends almost all its life below the surface. The name Argo was chosen because the array of floats works in partnership with the Jason earth observing satellites that measure the shape of the ocean surface. (In Greek mythology Jason sailed on his ship the Argo in search of the golden fleece). To learn more about Argo, how it works, [its data and technology, and its scientific and environmental impact, click here](https://argo.ucsd.edu/).


![float_cycle_1](https://user-images.githubusercontent.com/6677629/127728607-85e6328f-0323-4ca2-a8da-4d3e8a79d141.png)

The argofloats tool builds on the argovis API and allows the user to perform basic operations like search for and export platform and profile data, parse metadata and so on and more functionality will be added to this tool in the future.

Disclaimer: This is an unofficial tool. It is created and maintained by Samapriya Roy.

#### Tool Citation

```

```


#### Citation

These data were collected and made freely available by the International Argo Program and the national programs that contribute to it.  (https://argo.ucsd.edu,  https://www.ocean-ops.org).  The Argo Program is part of the Global Ocean Observing System.

The general Argo DOI is below.

Argo (2000). Argo float data and metadata from Global Data Assembly Centre (Argo GDAC). SEANOE. https://doi.org/10.17882/42182

If you used data from a particular month, please add the month key to the end of the DOI url to make it reproducible.  The key is comprised of the hashtag symbol (#) and then numbers.  For example, the key for August 2020 is 76230. The citation would look like:

Argo (2020). Argo float data and metadata from Global Data Assembly Centre (Argo GDAC) – Snapshot of Argo GDAC of August 2020. SEANOE. https://doi.org/10.17882/42182#76230

#### ArgoVis citation
Argovis API was used to parse through and get to the datasets, you can cite argovis using the following

```
Tucker, T., D. Giglio, M. Scanderbeg, and S.S. Shen, 2020: Argovis: A Web Application for Fast Delivery,
Visualization, and Analysis of Argo Data. J. Atmos. Oceanic Technol., 37 (3), 401-416
https://doi.org/10.1175/JTECH-D-19-0041.1
```


Readme Docs [available online](https://samapriya.github.io/argofloats)

## Table of contents
* [Installation](#installation)
* [Getting started](#getting-started)
* [Simple CLI for ArgoVis and Argofloats](#simple-cli-for-argovis-and-argofloats)
    * [overview](#overview)
    * [Platform Metadata](#platform-metadata)
    * [Profile Metadata](#profile-metadata)
    * [Profile Export](#profile-export)

## Installation
This assumes that you have native python & pip installed in your system, you can test this by going to the terminal (or windows command prompt) and trying

```python``` and then ```pip list```

**argofloats only supports Python v3.4 or higher**


**This command line tool is dependent on functionality from GDAL**
For installing GDAL in Ubuntu
```
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get install gdal-bin
sudo apt-get install python-gdal
```
## Windows Setup
Shapely and a few other libraries are notoriously difficult to install on windows machines so follow the steps mentioned here **before installing porder**. You can download and install shapely and other libraries from the [Unofficial Wheel files from here](https://www.lfd.uci.edu/~gohlke/pythonlibs) download depending on the python version you have. **Do this only once you have install GDAL**. I would recommend the steps mentioned above to get the GDAL properly installed. However I am including instructions to using a precompiled version of GDAL similar to the other libraries on windows. You can test to see if you have gdal by simply running

```gdalinfo```

in your command prompt. If you get a read out and not an error message you are good to go. If you don't have gdal try Option 1,2 or 3 in that order and that will install gdal along with the other libraries

#### Option 1:
Simply run ```argofloats -h``` after installation. This should go fetch the extra libraries you need and install them. Once installation is complete, the porder help page will show up. This should save you from the few steps below.

#### Option 2:
If this does not work or you get an unexpected error try the following commands. You can also use these commands if you simply want to update these libraries.

```
pipwin refresh
pipwin install gdal
```

#### Option 3
For Windows I also found this [guide](https://webcache.googleusercontent.com/search?q=cache:UZWc-pnCgwsJ:https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows+&cd=4&hl=en&ct=clnk&gl=us) from UCLA

Also for Ubuntu Linux I saw that this is necessary before the install

```sudo apt install libcurl4-openssl-dev libssl-dev```

**This also needs earthengine cli to be [installed and authenticated on your system](https://developers.google.com/earth-engine/python_install_manual) and earthengine to be callable in your command line or terminal**

To install **argofloats: Simple CLI for Earth Engine Uploads** you can install using two methods.

```pip install argofloats```

or you can also try

```
git clone https://github.com/samapriya/argofloats.git
cd argofloats
python setup.py install
```
For Linux use sudo or try ```pip install argofloats --user```.

I recommend installation within a virtual environment. Find more information on [creating virtual environments here](https://docs.python.org/3/library/venv.html).

## Getting started

As usual, to print help:

```
argofloats -h
usage: argofloats [-h] {overview,pm,plm,profile-export} ...

Simple CLI for ArgoVis & Argofloats

positional arguments:
  {overview,pm,plm,profile-export}
    overview            Get overview of platforms and profiles
    pm                  Get Platform metadata
    plm                 Get Platform Profile metadata
    profile-export      Export profile based on Platform Profile ID, Lat, Long
                        or Geometry GeoJSON file

optional arguments:
  -h, --help            show this help message and exit
```

To obtain help for specific functionality, simply call it with _help_ switch, e.g.: `argofloats pm -h`. If you didn't install argofloats, then you can run it just by going to *argofloats* directory and running `python argofloats.py [arguments go here]`

## Simple CLI for ArgoVis and Argofloats
The tool is designed to interact with the [Argofloats Argovis API](https://argovis.colorado.edu/api-docs/)

### overview
The overview tool fetches the latest information about platform and profile count, last updated as well as the distribution of datasets across the different data centes or DACs. There are no arguments for this tool

![argofloats_overview](https://user-images.githubusercontent.com/6677629/149610503-333cc770-b94d-4779-b154-21b11e81e6be.gif)

### Platform Metadata
The tool fetches metadata about a platform as pretty prints the information as a JSON object. This does require a Platform ID also called WMO number for the argo float.

![argofloats_pm](https://user-images.githubusercontent.com/6677629/149610502-32d5a654-7c2e-4dcd-a07e-4e437fab2b68.gif)


### Profile metadata
Each platform consists of profiles where each profile is attached to a platform and is a single cycle of data collection. So platforms can have multiple profiles and generally represented as PlatformID_ProfileNo. This is the argument used by the tool and it pulls the metadata for that specific profile for that platform/argo float.

![argofloats_plm](https://user-images.githubusercontent.com/6677629/149610501-18fb7d24-e1d5-4aa3-a6d3-0164a845c26b.gif)

### Profile Export
This tool allows you to search the argo floats database using either a lat long and a buffer area , or a geometry.geojson file or a given profile id. This tool is also capable to running long time searches overcoming the 3 month limit constrained by the argovis API. All use cases are shown below. The outputs are written as CSV file with a prefix argoprofile_

#### Using Profile ID
This uses the pofile ID and simply exports the profile as a CSV

![argofloats_export_plid](https://user-images.githubusercontent.com/6677629/149610498-d0b64a04-2abb-4644-b874-911323e32cb9.gif)

#### Using point geometry
This uses a lat long and radius to search in kilometers along with start and end date and exports all matching profiles to individual CSV files

![argofloats_export](https://user-images.githubusercontent.com/6677629/149610499-f04d00df-2cb6-4fdd-a865-b240e846c5cb.gif)

#### Using geometry GeoJSON file
This makes uses of a geojson file along with start and end date and exports all matching profiles to individual CSV files

![argofloats_export_geom](https://user-images.githubusercontent.com/6677629/149610496-f188d470-97e5-48bc-add6-5e55175b79ce.gif)

### Changelog

#### v0.0.3
- Added readme to the overall tool.
- Improved profile metadata parsing
- Added version check for all future pypi versions

#### v0.0.2
- Added readme and created new branch.
