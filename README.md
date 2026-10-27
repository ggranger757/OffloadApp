# Offload

A private, installable feed for everything you don't want to forget: notes, checklists and reminders, filed by category and #tag, captured by typing or by asking Siri.

Offload is a progressive web app (PWA). It installs to the home screen, works offline, and keeps your entries on your own device.

## Features

- **Notes, checklists and reminders.** Lists take one item per line; end the first line with `:` to name the list. Reminders can repeat on chosen days.
- **Categories.** Starts with Work, Ideas and Personal. Add, rename, recolor or delete them from **Edit** in the filter row. Pick one from the dropdown when saving, or type `@work` in an entry.
- **#tags and search.** Tap a tag to filter by it. Search covers every entry.
- **Siri capture.** Say "Hey Siri, Offload this" and speak. See [Siri capture](#siri-capture).
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
server/               optional Siri inbox: Cloudflare Worker + D1 database
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

## Siri capture

What you say to Siri goes to a small inbox server. The app collects new items whenever it opens, files them, and deletes them from the server. The server stores only a hash of each person's capture key.

It runs on Cloudflare's free plan.

### 1. Deploy the inbox server

Either from your computer (needs Node.js 18+ and a free Cloudflare account):

```sh
cd server
npm install
npx wrangler login
npm run db:create      # prints a database_id; paste it into wrangler.toml
npm run db:schema
npm run deploy         # prints https://offload-inbox.<you>.workers.dev
```

Or from GitHub: run `npx wrangler d1 create offload` once to get a database id, then add these under **Settings → Secrets and variables → Actions** and run **Deploy Siri inbox (Cloudflare)** from the **Actions** tab:

| Name | Kind | Value |
|---|---|---|
| `CLOUDFLARE_API_TOKEN` | Secret | API token with Workers Scripts Edit and D1 Edit |
| `CLOUDFLARE_ACCOUNT_ID` | Secret | Your Cloudflare account id |
| `D1_DATABASE_ID` | Variable | The id from `wrangler d1 create` |

### 2. Point the app at it

Rebuild with your server address so every copy of the app uses it, then commit and push:

```sh
OFFLOAD_SERVER=https://offload-inbox.you.workers.dev python3 build.py
```

Or paste the address into the app under the microphone button → **Inbox server address**.

### 3. Make the Shortcut

Tap the microphone button in the app and follow the six steps. To spare your users the setup, build the shortcut once, add an **Import Question** for the Authorization header, and share it as an iCloud link.

**Things you can say:**

| You say | You get |
|---|---|
| "Podcast idea interview a barista, category work" | Note in Work |
| "Remind me to call Mom tomorrow at 6 PM" | Reminder, tomorrow 6:00 PM |
| "Remind me every Monday at 9 to send the report" | Repeating reminder |
| "Grocery list milk, eggs and bread" | Checklist with three items |
| "Add coffee to my grocery list" | Item added to that list |

### Server API

Every request needs `Authorization: Bearer <capture key>`.

| Request | Body | Response |
|---|---|---|
| `POST /capture` | JSON `{"text": "..."}`, form field `text`, or plain text | `Saved to Offload.` |
| `GET /inbox` | | `{"items": [{"id", "text", "source", "created"}]}` |
| `DELETE /inbox` | `{"ids": [...]}` | `{"deleted": n}` |

Limits: 4,000 characters per capture, 500 unsynced items per key.

## Limits

- Entries live on one device. Use **Settings → Backup** to move them.
- Reminders alert while the app is open or running in the background. A fully closed web app can't fire alarms without a push server.
- Siri capture needs the app to be opened before new items appear.

## License

MIT. See [LICENSE](LICENSE).
