# Offload

A private, installable feed for everything you don't want to forget: notes, checklists and reminders, filed by category and #tag.

Offload is a progressive web app (PWA). It installs to the home screen, works offline, and keeps your entries on your own device.

## Features

- **Notes, checklists and reminders.** Lists take one item per line; end the first line with `:` to name the list. Reminders can repeat on chosen days.
- **Categories.** Starts with Work, Ideas and Personal. Add, rename, recolor or delete them from **Edit** in the filter row. Pick one from the dropdown when saving, or type `@work` in an entry.
- **#tags and search.** Tap a tag to filter by it. Search covers every entry.
- **Share target.** On Android, share a link or text into Offload to start a note.
- **Your choice of look.** Light, dark or system theme; sans, serif or mono font.
- **Backup.** Copy a JSON backup and import it on another device.

**Live app:** https://ggranger757.github.io/OffloadApp/

## Project layout

```
index.html            the app, served by GitHub Pages (built from src/app.html)
manifest.webmanifest  install details: name, icons, colors
sw.js                 offline support (built from src/sw.js)
icons/                app icons
.nojekyll             tells GitHub Pages to serve the files as they are
src/                  source for index.html and sw.js
build.py              rebuilds index.html, sw.js and manifest.webmanifest
tools/make_icons.py   regenerates the icons (needs Pillow)
```

## Publish with GitHub Pages

The built app is committed at the top of the repository, so GitHub Pages serves it directly.

1. Push the files to the `main` branch.
2. Open **Settings → Pages**. Set **Source** to **Deploy from a branch**, branch **main**, folder **/ (root)**, and save.
3. Wait a minute, then open https://ggranger757.github.io/OffloadApp/.

### Making changes

Edit `src/app.html`, then rebuild and commit the result:

```sh
python3 build.py
git add -A && git commit -m "Update app" && git push
```

To try it locally first, run `python3 -m http.server 8080` in the repository folder and open http://localhost:8080.

### Install on a phone

- **iPhone (Safari):** open the address, tap Share → Add to Home Screen.
- **Android (Chrome):** open the address, tap the menu → Install app.

## Limits

- Entries live on one device. Use **Settings → Backup** to move them.
- Reminders alert while the app is open or running in the background. A fully closed web app can't fire alarms without a push server.

## License

MIT. See [LICENSE](LICENSE).
