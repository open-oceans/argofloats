import pandas as pd
import json
import requests
import geojson
import sys
import pkg_resources
import subprocess
import platform
import os
import time
import math
import argparse
from area import area
from os.path import expanduser
from tenacity import retry, stop_after_attempt, wait_exponential
from bs4 import BeautifulSoup

if str(platform.system().lower()) == "windows":
    # Get python runtime version
    version = sys.version_info[0]
    try:
        import pipwin

        if pipwin.__version__ == "0.5.0":
            pass
        else:
            a = subprocess.call(
                "{} -m pip install pipwin==0.5.0".format(sys.executable),
                shell=True,
                stdout=subprocess.PIPE,
            )
            b = subprocess.call(
                "{} -m pip install wheel".format(sys.executable),
                shell=True,
                stdout=subprocess.PIPE,
            )
            subprocess.call("pipwin refresh", shell=True)
        """Check if the pipwin cache is old: useful if you are upgrading porder on windows
        [This section looks if the pipwin cache is older than two weeks]
        """
        home_dir = expanduser("~")
        fullpath = os.path.join(home_dir, ".pipwin")
        file_mod_time = os.stat(fullpath).st_mtime
        if int((time.time() - file_mod_time) / 60) > 90000:
            print("Refreshing your pipwin cache")
            subprocess.call("pipwin refresh", shell=True)
    except ImportError:
        a = subprocess.call(
            "{} -m pip install pipwin==0.5.0".format(sys.executable),
            shell=True,
            stdout=subprocess.PIPE,
        )
        subprocess.call("pipwin refresh", shell=True)
    except Exception as e:
        print(e)
    try:
        import gdal
    except ImportError:
        try:
            from osgeo import gdal
        except ModuleNotFoundError:
            subprocess.call("pipwin install gdal", shell=True)
    except ModuleNotFoundError or ImportError:
        subprocess.call("pipwin install gdal", shell=True)
    except Exception as e:
        print(e)
    try:
        import pyproj
    except ImportError:
        subprocess.call("pipwin install pyproj", shell=True)
    except Exception as e:
        print(e)
    try:
        import shapely
    except ImportError:
        subprocess.call("pipwin install shapely", shell=True)
    except Exception as e:
        print(e)
    try:
        import fiona
    except ImportError:
        subprocess.call("pipwin install fiona", shell=True)
    except Exception as e:
        print(e)
    try:
        import geopandas as gpd
    except ImportError:
        subprocess.call("pip install geopandas", shell=True)
    except Exception as e:
        print(e)
import geopandas as gpd


class Solution:
    def compareVersion(self, version1, version2):
        versions1 = [int(v) for v in version1.split(".")]
        versions2 = [int(v) for v in version2.split(".")]
        for i in range(max(len(versions1), len(versions2))):
            v1 = versions1[i] if i < len(versions1) else 0
            v2 = versions2[i] if i < len(versions2) else 0
            if v1 > v2:
                return 1
            elif v1 < v2:
                return -1
        return 0


ob1 = Solution()

# Get package version
def argofloats_version():
    url = "https://pypi.org/project/argofloats/"
    source = requests.get(url)
    html_content = source.text
    soup = BeautifulSoup(html_content, "html.parser")
    company = soup.find("h1")
    vcheck = ob1.compareVersion(
        company.string.strip().split(" ")[-1],
        pkg_resources.get_distribution("argofloats").version,
    )
    if vcheck == 1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Current version of argofloats is {} upgrade to lastest version: {}".format(
                pkg_resources.get_distribution("argofloats").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )
    elif vcheck == -1:
        print(
            "\n"
            + "========================================================================="
        )
        print(
            "Possibly running staging code {} compared to pypi release {}".format(
                pkg_resources.get_distribution("argofloats").version,
                company.string.strip().split(" ")[-1],
            )
        )
        print(
            "========================================================================="
        )


argofloats_version()

headers = {
    "Connection": "keep-alive",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Language": "en-US,en;q=0.9",
}

profile_list = []

################################################ Date block #################################################################


def numOfDays(date1, date2):
    return (date2 - date1).days


def date_range(start, end):
    from datetime import datetime

    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    days = numOfDays(start, end)
    intv = math.ceil(days / 30)
    diff = (end - start) / intv
    for i in range(intv):
        yield (start + diff * i).strftime("%Y-%m-%dT%H:%M:%SZ")
    yield end.strftime("%Y-%m-%dT%H:%M:%SZ")


######################################################geometry block ################################################################################
def getarea(geom):
    obj = {"type": "Polygon", "coordinates": []}
    obj["coordinates"] = geom
    poly_area = area(obj)
    return poly_area / 1000000


# point to square buffer function
def generate_buffer_meter(lat, lng, radius):
    data = pd.DataFrame({"Longitude": [lng], "Latitude": [lat]})
    data = gpd.GeoDataFrame(
        data,
        geometry=gpd.points_from_xy(data.Longitude, data.Latitude, crs="epsg:4326"),
    )
    data = data.to_crs("+proj=aeqd +units=m  +x_0=0 +y_0=0")
    data["geometry"] = data["geometry"].buffer(radius, cap_style=3)
    data = data.to_crs("epsg:4326")
    bound = json.loads(data.to_json())
    coord = bound["features"][0]["geometry"]["coordinates"]
    return coord


######################### Profile Map find all profile ids for give aoi and time ################################
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(4))
def profile_id(params):
    response = requests.get(
        "https://argovis.colorado.edu/selection/profiles/map",
        headers=headers,
        params=params,
    )
    if response.status_code == 200 and len(response.json()) > 0:
        for items in response.json():
            profile_list.append(items["_id"])
        return profile_list
    elif response.status_code != 200:
        raise Exception


######################### Profile measurements and exporter ################################
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(2))
def profiler(plid, fpath):
    pf = requests.get(f"https://argovis.colorado.edu/catalog/profiles/{plid}")
    if pf.status_code == 200:
        profile = pf.json()
        meas_keys = profile["measurements"][0].keys()
        df = pd.DataFrame(columns=meas_keys)
        profileDf = pd.DataFrame(profile["measurements"])
        profileDf["cycle_number"] = profile["cycle_number"]
        profileDf["profile_id"] = profile["_id"]
        profileDf["latitude"] = profile["lat"]
        profileDf["longitude"] = profile["lon"]
        profileDf["date"] = profile["date"]
        df = pd.concat([df, profileDf], sort=False)
        filepath = os.path.join(fpath, f"argoprofile_{plid}.csv")
        print(f"Exporting to {filepath}")
        df.to_csv(filepath, index=False)
    elif response.status_code != 200:
        raise Exception


################################### Export all profiles per platform #################################################################
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(2))
def profile_catalog(pid):
    url = f"https://argovis.colorado.edu/catalog/platforms/{pid}"
    resp = requests.get(url)
    if not resp.status_code == 200:
        raise Exception
    elif resp.status_code == 200:
        platformProfiles = resp.json()
    return platformProfiles


def get_profiles(profiles):
    meas_keys = profiles[0]["measurements"][0].keys()
    df = pd.DataFrame(columns=meas_keys)
    for profile in profiles:
        profileDf = pd.DataFrame(profile["measurements"])
        profileDf["cycle_number"] = profile["cycle_number"]
        profileDf["profile_id"] = profile["_id"]
        profileDf["latitude"] = profile["lat"]
        profileDf["longitude"] = profile["lon"]
        profileDf["date"] = profile["date"]
        df = pd.concat([df, profileDf], sort=False)
    return df


def platform2profiles(pid, fpath):
    if fpath is None:
        fpath = expanduser("~")
    profiles = profile_catalog(pid)
    pidf = get_profiles(profiles)
    platform_counts = pidf["profile_id"].nunique()
    print(f"Total unique profiles: {platform_counts}")
    print(f"Total measurements: {pidf.shape[0]}")
    filepath = os.path.join(fpath, f"all_profiles-{pid}.csv")
    print(f"Exporting to {filepath}")
    pidf.to_csv(filepath, index=False)


def platform2profiles_from_parser(args):
    platform2profiles(pid=args.pid, fpath=args.path)


def overview():
    response = requests.get(
        "https://argovis.colorado.edu/selection/overview", headers=headers
    )
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Overview failed with error code {response.status_code}")


def overview_from_parser(args):
    overview()


def platform_metadata(pid):
    response = requests.get(
        f"https://argovis.colorado.edu/catalog/platform_metadata/{pid}", headers=headers
    )
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed with error code {response.status_code}")


def pm_from_parser(args):
    platform_metadata(pid=args.pid)


def platform_profile_metadata(plid):
    response = requests.get(
        f"https://argovis.colorado.edu/catalog/profiles/{plid}/map", headers=headers
    )
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Failed with error code {response.status_code}")


def plm_from_parser(args):
    platform_metadata(plid=args.plid)


def argoexp(lat, lng, radius, start, end, geometry, fpath, plid):
    if geometry is not None:
        with open(geometry) as f:
            gj = geojson.load(f)
        shp = gj["features"][0]["geometry"]["coordinates"]
        ar = round(getarea(shp), 2)
        ar = "{:,}".format(ar)
        print(f"Processing {os.path.basename(geometry)} with area {ar} square km")
    elif plid is not None:
        profiler(plid, fpath)
        print(f"Processing for Platform Profile ID {plid}")
    elif lat is not None and lng is not None:
        if radius is None:
            radius = 1000000
        elif radius is not None:
            radius = float(radius) * 1000
        shp = generate_buffer_meter(float(lat), float(lng), float(radius))
        print(f"Processing for {float(radius)/1000} km around {lat},{lng}")
    else:
        sys.exit("Please provie lat long pair or full path to geometry.geojson file")
    if start is not None and end is not None:
        dates = date_range(start, end)
        dates = list(dates)
        for x in range(len(dates) - 1):
            st = dates[x]
            ed = dates[x + 1]
            params = {
                "startDate": st,
                "endDate": ed,
                "shape": f"{shp}",
                "presRange": "[0,2000]",
            }
            profile_id(params)
        if profile_list:
            for plid in profile_list:
                profiler(plid, fpath)
    if plid is None and start is None and end is None:
        print("Provide start and end dates for Geometry or point searches")


def argoexp_from_parser(args):
    argoexp(
        lat=args.lat,
        lng=args.lon,
        radius=args.radius,
        start=args.start,
        end=args.end,
        geometry=args.geometry,
        fpath=args.path,
        plid=args.plid,
    )


def main(args=None):
    parser = argparse.ArgumentParser(description="Simple CLI for ArgoVis & Argofloats")
    subparsers = parser.add_subparsers()

    parser_overview = subparsers.add_parser(
        "overview", help="Get overview of platforms and profiles"
    )
    parser_overview.set_defaults(func=overview_from_parser)

    parser_pm = subparsers.add_parser("pm", help="Get Platform metadata")
    required_named = parser_pm.add_argument_group("Required named arguments.")
    required_named.add_argument("--pid", help="Platform ID", required=True)
    parser_pm.set_defaults(func=pm_from_parser)

    parser_plm = subparsers.add_parser("plm", help="Get Platform Profile metadata")
    required_named = parser_plm.add_argument_group("Required named arguments.")
    required_named.add_argument("--plid", help="Platform Profile ID", required=True)
    parser_plm.set_defaults(func=plm_from_parser)

    parser_platform2profiles = subparsers.add_parser(
        "platform-profiles", help="Export all profiles for a given platform"
    )
    required_named = parser_platform2profiles.add_argument_group(
        "Required named arguments."
    )
    required_named.add_argument("--pid", help="Platform ID", required=True)
    optional_named = parser_platform2profiles.add_argument_group(
        "Optional named arguments"
    )
    optional_named.add_argument(
        "--path",
        help="Full path to folder to export platform profiles CSV",
        default=None,
    )
    parser_platform2profiles.set_defaults(func=platform2profiles_from_parser)

    parser_argoexp = subparsers.add_parser(
        "profile-export",
        help="Export profile based on Platform Profile ID, Lat, Long or Geometry GeoJSON file",
    )
    required_named = parser_argoexp.add_argument_group("Required named arguments.")
    required_named.add_argument(
        "--path",
        help="Full path to folder to export platform profile CSVs",
        required=True,
    )
    optional_named = parser_argoexp.add_argument_group("Optional named arguments")
    optional_named.add_argument("--lat", help="Latitude", type=float, default=None)
    optional_named.add_argument("--lon", help="Longitude", type=float, default=None)
    optional_named.add_argument(
        "--radius", help="Search radius in meters for square buffer", default=None
    )
    optional_named.add_argument("--start", help="Start Date YYYY-MM-DD", default=None)
    optional_named.add_argument("--end", help="End Date YYYY-MM-DD", default=None)
    optional_named.add_argument("--plid", help="Platform Profile ID", default=None)
    optional_named.add_argument(
        "--geometry", help="Full path to geometry.geojson file", default=None
    )
    parser_argoexp.set_defaults(func=argoexp_from_parser)

    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error("too few arguments")
    func(args)


if __name__ == "__main__":
    main()
