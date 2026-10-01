# -*- coding: utf-8 -*-
"""
Seriesly - ενημέρωση του αποθετηρίου Kodi (GitHub: HermesGR/SerieslyGR, GitHub Pages).

Χρήση:
  1. Βάλε το νέο zip του πρόσθετου (π.χ. plugin.video.seriesly-1.0.2.zip) στον φάκελο «νέα».
  2. Τρέξε:  py build_repo.py
  3. Ανέβασε στο GitHub ό,τι σου γράφει στο τέλος (τα αλλαγμένα αρχεία).

Τι κάνει: για κάθε zip στον φάκελο «νέα» διαβάζει το addon.xml (id + έκδοση), το βάζει στο
repo/zips/<id>/<id>-<έκδοση>.zip μαζί με icon/fanart, και ξαναφτιάχνει τα repo/addons.xml και
repo/addons.xml.md5 με την ΝΕΟΤΕΡΗ έκδοση κάθε πρόσθετου. Το Kodi κάθε χρήστη βλέπει τη νέα έκδοση και
ενημερώνεται μόνο του. Μόνο βιβλιοθήκες της Python — τίποτα για εγκατάσταση.
"""
import hashlib
import os
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

VERSION = "1.0.0"
HERE = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(HERE, "νέα")
REPO = os.path.join(HERE, "repo")
ZIPS = os.path.join(REPO, "zips")
PAGES = "https://hermesgr.github.io/SerieslyGR/"


def version_key(v):
    return [int(x) if x.isdigit() else x for x in re.split(r"[.\-~+]", v)]


def addon_xml_of(zip_path):
    """(id, έκδοση, κείμενο addon.xml, όνομα φακέλου μέσα στο zip)."""
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.count("/") == 1 and n.endswith("/addon.xml")]
        if not names:
            raise ValueError("δεν βρέθηκε <φάκελος>/addon.xml μέσα στο %s" % os.path.basename(zip_path))
        text = z.read(names[0]).decode("utf-8")
        folder = names[0].split("/")[0]
    root = ET.fromstring(text.encode("utf-8"))
    if root.tag != "addon" or not root.get("id") or not root.get("version"):
        raise ValueError("άκυρο addon.xml στο %s" % os.path.basename(zip_path))
    if root.get("id") != folder:
        raise ValueError("ο φάκελος (%s) δεν ταιριάζει με το id (%s)" % (folder, root.get("id")))
    return root.get("id"), root.get("version"), text, folder


def import_inbox():
    changed = []
    if not os.path.isdir(INBOX):
        return changed
    for name in sorted(os.listdir(INBOX)):
        if not name.lower().endswith(".zip"):
            continue
        src = os.path.join(INBOX, name)
        aid, ver, _, folder = addon_xml_of(src)
        dest_dir = os.path.join(ZIPS, aid)
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "%s-%s.zip" % (aid, ver))
        shutil.copyfile(src, dest)
        changed.append(os.path.relpath(dest, HERE))
        with zipfile.ZipFile(src) as z:
            for art in ("icon.png", "fanart.jpg"):
                inner = "%s/%s" % (folder, art)
                if inner in z.namelist():
                    with open(os.path.join(dest_dir, art), "wb") as fh:
                        fh.write(z.read(inner))
                    changed.append(os.path.relpath(os.path.join(dest_dir, art), HERE))
        os.remove(src)
        print("  + %s %s" % (aid, ver))
    return changed


def build_index():
    """repo/addons.xml + .md5 με τη νεότερη έκδοση κάθε πρόσθετου."""
    parts = []
    for aid in sorted(os.listdir(ZIPS)):
        d = os.path.join(ZIPS, aid)
        zips = [f for f in os.listdir(d) if f.startswith(aid + "-") and f.endswith(".zip")]
        if not zips:
            continue
        newest = max(zips, key=lambda f: version_key(f[len(aid) + 1:-4]))
        _, ver, text, _ = addon_xml_of(os.path.join(d, newest))
        text = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", text).strip()
        parts.append(text)
        print("  addons.xml: %s %s" % (aid, ver))
    xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<addons>\n' + "\n\n".join(parts) + "\n</addons>\n"
    ET.fromstring(xml.encode("utf-8"))   # έλεγχος ότι είναι σωστό XML
    with open(os.path.join(REPO, "addons.xml"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(xml)
    md5 = hashlib.md5(xml.encode("utf-8")).hexdigest()
    with open(os.path.join(REPO, "addons.xml.md5"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(md5)
    return ["repo/addons.xml", "repo/addons.xml.md5"]


def build_pages_index():
    """index.html (πηγή για τη Διαχείριση αρχείων του Kodi): σύνδεσμος στο νεότερο zip του αποθετηρίου."""
    d = os.path.join(ZIPS, "repository.seriesly")
    zips = sorted([f for f in os.listdir(d) if f.endswith(".zip")], key=lambda f: version_key(f[len("repository.seriesly") + 1:-4]))
    newest = zips[-1]
    shutil.copyfile(os.path.join(d, newest), os.path.join(HERE, newest))
    html = ('<!DOCTYPE html>\n<html lang="el"><head><meta charset="utf-8"><title>Seriesly για Kodi</title>'
            '<meta name="viewport" content="width=device-width, initial-scale=1"></head>\n<body>\n'
            '<h1>Seriesly για Kodi</h1>\n'
            '<p>Στο Kodi: Ρυθμίσεις &rarr; Διαχείριση αρχείων &rarr; Προσθήκη πηγής &rarr; <b>%s</b></p>\n'
            '<a href="%s">%s</a>\n</body></html>\n') % (PAGES, newest, newest)
    with open(os.path.join(HERE, "index.html"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return ["index.html", newest]


def main():
    print("Seriesly - ενημέρωση αποθετηρίου %s\n" % VERSION)
    os.makedirs(ZIPS, exist_ok=True)
    try:
        changed = import_inbox()
        changed += build_index()
        changed += build_pages_index()
    except (ValueError, OSError, zipfile.BadZipFile, ET.ParseError) as e:
        print("\nΣΦΑΛΜΑ: %s" % e)
        if os.name == "nt":
            input("\nEnter για κλείσιμο...")
        sys.exit(1)
    print("\nΈτοιμο. Ανέβασε στο GitHub (Add file -> Upload files) αυτά τα αρχεία, στους ίδιους φακέλους:")
    for c in sorted(set(changed)):
        print("  " + c.replace(os.sep, "/"))
    if os.name == "nt":
        input("\nEnter για κλείσιμο...")


if __name__ == "__main__":
    main()
