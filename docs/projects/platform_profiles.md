# Platform Profiles Export

Each platform consists of profiles where each profile is attached to a platform and is a single cycle of data collection. So platforms can have multiple profiles and generally represented as PlatformID_ProfileNo. This tool fetches all platforms linked to a specific platform and exports it as a single CSV including platform profile id and measurements. If no path is provided the profile CSV is saved onto the home folder.

![platform_profiles](https://user-images.githubusercontent.com/6677629/149677824-590bd4ec-252e-47bd-bd04-07720dba86b5.gif)

```
argofloats platform-profiles -h
usage: argofloats platform-profiles [-h] --pid PID [--path PATH]

optional arguments:
  -h, --help   show this help message and exit

Required named arguments.:
  --pid PID    Platform ID

Optional named arguments:
  --path PATH  Full path to folder to export platform profiles CSV
```
