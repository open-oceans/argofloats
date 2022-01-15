# Profile metadata

Each platform consists of profiles where each profile is attached to a platform and is a single cycle of data collection. So platforms can have multiple profiles and generally represented as PlatformID_ProfileNo. This is the argument used by the tool and it pulls the metadata for that specific profile for that platform/argo float.

![argofloats_plm](https://user-images.githubusercontent.com/6677629/149610501-18fb7d24-e1d5-4aa3-a6d3-0164a845c26b.gif)


```
argofloats plm -h
usage: argofloats plm [-h] --plid PLID

optional arguments:
  -h, --help   show this help message and exit

Required named arguments.:
  --plid PLID  Platform Profile ID
```
