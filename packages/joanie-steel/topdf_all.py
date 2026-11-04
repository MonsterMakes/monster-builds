import json, re
src = open('topdf.py').read()
ids = json.load(open('all_ids.json'))
src = src.replace('mono-stringer-drawings.html', 'combined-drawings.html').replace('mono-stringer-drawings.pdf', 'combined-drawings.pdf')
src = re.sub(r'IDS = \[.*?\]', 'IDS = ' + json.dumps(ids), src, flags=re.S)
exec(src)


