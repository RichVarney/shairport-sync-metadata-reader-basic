import os
import base64
import re
import sys


"""A small python3 script which will print the current song and artist information when streaming over shairport-sync 
(airplay)

Point the script towards the metadata file as created by [shairport-sync](https://github.com/mikebrady/shairport-sync) 
and this script will print a dictionary of song name, artist and album.

The default metadata file is at /tmp/shairport-sync-metadata on linux systems running shairport-sync and is poorly 
formatted XML. This script stores each 'item' of XML as a string, then parses the string looking for 'code's and 'data' 
which can then be decoded into plain text.

See here for more information on how to decode the messages: https://github.com/mikebrady/shairport-sync-metadata-reader
"""

file_path = os.path.abspath('/tmp/shairport-sync-metadata')
# file_path = os.path.abspath(r'C:\Users\richard.varney\AppData\Local\Temp\fifo.xml')
xml_string = ''
current_song = ''
song_info = {}


try:
    with open(file_path, 'r') as fifo:
        # for line in fifo.readlines():
        for line in fifo:
            if '<item>' in line:
                xml_string = ''
            xml_string += line.rstrip()

            # once the full <data>...</data> XML has been recorded for one item, decode the lot
            if '</data>' in xml_string:
                # put 'code' XML into the song_info dictionary
                regex_match = '<code>([0-9a-zA-Z]*)'
                matches = re.findall(regex_match, xml_string)
                for match in matches:
                    bytes_object = bytes.fromhex(match)
                    ascii_string = bytes_object.decode('ascii')
                    song_info['code'] = ascii_string

                # put 'data' XML into the song_info dictionary
                data_matches = re.findall('<data encoding="base64">([0-9a-zA-Z=]*)', xml_string)
                for match in data_matches:
                    try:
                        base64_bytes = match.encode('ascii')
                        message_bytes = base64.b64decode(base64_bytes)
                        message = message_bytes.decode('ascii')
                        # song_info['data'] = message
                        if song_info['code'] == 'minm':  # dmap.itemname
                            # print(song_info)
                            song_info['song'] = message
                        if song_info['code'] == 'asar':  # daap.songartist
                            # print(song_info)
                            song_info['artist'] = message
                        if song_info['code'] == 'asal':  # daap.songalbum
                            # print(song_info)
                            song_info['album'] = message
                        if song_info['code'] == 'ascp':  # daap.songcomposer
                            # print(song_info)
                            song_info['composer'] = message
                    except Exception as e:
                        break
                try:
                    if song_info['song'] != current_song:
                        current_song = song_info['song']
                        print(song_info)
                except Exception:
                    song_info['song'] = 'Loading...'
except KeyboardInterrupt:
    sys.exit(0)
