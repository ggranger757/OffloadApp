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

## Project layout

```
src/app.html        the whole app: markup, styles and script
src/sw.js           service worker (offline support)
public/icons/       app icons
build.py            assembles dist/ (Python standard library only)
tools/make_icons.py regenerates the icons (needs Pillow)
server/             optional Siri inbox: Cloudflare Worker + D1 database
.github/workflows/  deploys the app to GitHub Pages, and the server to Cloudflare
```

## Run it locally

```sh
python3 build.py
cd dist && python3 -m http.server 8080
```

Open http://localhost:8080. Install and offline support need HTTPS or `localhost`.

## Publish with GitHub Pages

1. Create a repository on GitHub and push this folder to its `main` branch.
2. In the repository, open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Push again, or run **Deploy app to GitHub Pages** from the **Actions** tab.

The app appears at `https://<your-username>.github.io/<repository-name>/`.

### Install on a phone

- **iPhone (Safari):** Share → Add to Home Screen.
- **Android (Chrome):** menu → Install app.

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

Or from GitHub: run `npx wrangler d1 create offload` once to get a database id, then add these under **Settings → Secrets and variables → Actions** and run **Deploy Siri inbox** from the **Actions** tab:

| Name | Kind | Value |
|---|---|---|
| `CLOUDFLARE_API_TOKEN` | Secret | API token with Workers Scripts Edit and D1 Edit |
| `CLOUDFLARE_ACCOUNT_ID` | Secret | Your Cloudflare account id |
| `D1_DATABASE_ID` | Variable | The id from `wrangler d1 create` |

### 2. Point the app at it

Add a repository **variable** named `OFFLOAD_SERVER` with your server address (for example `https://offload-inbox.you.workers.dev`), then rerun the Pages workflow. Every copy of the app will use it.

You can also paste the address into the app under the microphone button → **Inbox server address**.

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
