# shairport-sync-metadata
A small python3 script which will print the current song and artist information when streaming over shairport-sync (airplay)

Point the script towards the metadata file as created by [shairport-sync](https://github.com/mikebrady/shairport-sync) and this script will print a dictionary of song name, artist and album.

The default metadata file is at /tmp/shairport-sync-metadata on linux systems running shairport-sync and is poorly formatted XML. This script stores each 'item' of XML as a string, then parses the string looking for 'code's and 'data' which can then be decoded into plain text.

See here for more information on how to decode the messages: https://github.com/mikebrady/shairport-sync-metadata-reader
