import json, os, re


def cut_out(map_i, after, until):
    """Cut out the file content between the lines matching the regexps <after> and <until>"""
    f = open('map_%d.bb' % map_i, 'r')
    start = False
    for line in f.readlines():
        if start and re.match(until, line):
            break
        if start:
            yield line
        if re.match(after, line):
            start = True
    f.close()

map_geo = {
    # lvl: width
    1: 160,
    2: 121,
    3: 50,
    4: 100
}

out = open('maps.js', 'w')
out.write('var MAPS = %s;' % json.dumps({
    map_i: {
        'width': map_geo[map_i],
        'tiles': [
            int(tile)
            for line in cut_out(map_i, r'^\.level_texMapData%d$' % map_i, r'^$')
            for tile in re.findall(r'(\d{1,2})-\d', line)
        ]
    } for map_i in range(1,5)})
)
out.close()