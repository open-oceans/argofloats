# Global Search

The global search tool was created to look for quick snapshots of all platforms and platforms in a single month. The tool allows you to provide a start and end date and it generates monthly reports pertaining to profiles that are globally available for a specific month and year. The tool can further use filters like setting bgc to True to get only those profiles/platforms that has BGC data or providing a specific platform ID to get only those profiles pertaining to specific platform.


```
argofloats global-search -h                                                               
usage: argofloats global-search [-h] --start START --end END --path PATH [--pid PID] [--bgc BGC]    

optional arguments:                                                                                 
  -h, --help     show this help message and exit                                                    

Required named arguments.:                                                                          
  --start START  Start date for global search YYYY-MM-DD                                            
  --end END      End date for global search YYYY-MM-DD                                              
  --path PATH    Full path to folder to export global search CSVs                                   

Optional named arguments:                                                                           
  --pid PID      Platform ID: search and export all global profiles for specific platform ID        
  --bgc BGC      Boolean: search and export all global profiles with BGC True or False
```

You can provide a filter for example here bgc is set to true to look for all those platforms & profiles with BGC data

![argofloats_global_search](https://user-images.githubusercontent.com/6677629/154848970-542c6208-26f0-4906-925f-28a59c78239f.gif)


You can also search with no arguments or filters to get all profiles in a month and year

![argofloats_global_search_all](https://user-images.githubusercontent.com/6677629/154849132-5cad42d6-3a20-4f62-8f67-d3aa7e828a78.gif)
