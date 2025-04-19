from flask import Flask, render_template, send_from_directory, request, abort
import os, json
from PIL import Image
from pathlib import Path

app = Flask(__name__)
MEDIA_ROOT = "/Users/lei/Downloads/web_media"
CONFIG_FILE = "config.json"
THUMBNAIL_DIR = "static/thumbnail_cache"
IMAGE_EXT = {'.jpg', '.jpeg', '.png', '.gif'}
VIDEO_EXT = {'.mp4', '.webm', '.mov', '.3gp'}

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    name_map = json.load(f)

def get_display_name(name):
    return name_map.get(name, name)

def list_dir(path):
    abs_path = os.path.join(MEDIA_ROOT, path)
    try:
        entries = os.listdir(abs_path)
        entries.sort()
        result = []
        for entry in entries:
            full = os.path.join(abs_path, entry)
            rel = os.path.join(path, entry)
            if os.path.isdir(full):
                result.append({'type': 'dir', 'name': entry, 'display': get_display_name(entry), 'path': rel})
            else:
                ext = Path(entry).suffix.lower()
                if ext in IMAGE_EXT:
                    thumb_path = os.path.join(THUMBNAIL_DIR, rel + '.jpg')
                    os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
                    if not os.path.exists(thumb_path):
                        try:
                            img = Image.open(full)
                            img.thumbnail((200, 200))
                            img.save(thumb_path, 'JPEG')
                        except:
                            pass
                    result.append({'type': 'image', 'name': entry, 'display': get_display_name(entry), 'path': rel, 'thumb': '/' + thumb_path})
                elif ext in VIDEO_EXT:
                    result.append({'type': 'video', 'name': entry, 'display': get_display_name(entry), 'path': rel})
        return result
    except Exception as e:
        return []

@app.route('/')
def index():
    root_dirs = list_dir("")
    tabs = [d for d in root_dirs if d['type'] == 'dir']
    if tabs:
        return browse(tabs[0]['path'])
    return render_template("index.html", tabs=tabs, items=[], breadcrumb=[])

@app.route('/browse/<path:subpath>')
def browse(subpath):
    root_dirs = list_dir("")
    tabs = [d for d in root_dirs if d['type'] == 'dir']
    items = list_dir(subpath)
    parts = subpath.strip('/').split('/')
    breadcrumb = []
    for i in range(len(parts)):
        name = parts[i]
        breadcrumb.append((get_display_name(name), '/'.join(parts[:i+1])))
    return render_template("index.html", tabs=tabs, items=items, current=subpath, breadcrumb=breadcrumb)

@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory(MEDIA_ROOT, filename)

@app.route('/thumbnail/<path:filename>')
def thumbnail(filename):
    return send_from_directory(THUMBNAIL_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
