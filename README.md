# Santa's Grotto — grotto.auldontoys.com

Static booking site for Auldon Toys' Santa's Grotto. One file (`index.html`), hosted free on **GitHub Pages**.
All prices, slots and availability come live from the API (`https://api.auldontoys.com`, repo `auldon-grotto-api`), so nothing here needs editing when prices change.

## Publish (first time)

1. Create a **public** GitHub repo named `auldon-grotto` and push these files:
   ```bash
   git init && git add . && git commit -m "Santa's Grotto site"
   git branch -M main
   git remote add origin https://github.com/<owner>/auldon-grotto.git
   git push -u origin main
   ```
2. Repo → **Settings → Pages** → Source: *Deploy from a branch* → `main` / `/ (root)` → Save.
3. **Cloudflare DNS** for auldontoys.com (DNS only / grey cloud, not proxied):
   | Type | Name | Target |
   |---|---|---|
   | CNAME | `grotto` | `<owner>.github.io` |
4. Back in **Settings → Pages → Custom domain**: enter `grotto.auldontoys.com`, Save, wait for the DNS check, then tick **Enforce HTTPS**. (The `CNAME` file in this repo keeps the domain set across deploys.)
5. Open https://grotto.auldontoys.com — the hero should show the Christmas countdown and the packages. If a red "booking temporarily unavailable" banner shows, the API isn't reachable yet (check `https://api.auldontoys.com/health` and the `CORS_ORIGINS` setting on the API).

## Update
Edit `index.html`, commit, push. Pages redeploys in about a minute.

## Behaviour
- Loads `/api/config` on open; falls back to a display-only catalogue with booking disabled if the API is down.
- Live slot availability from `/api/availability`; server-side quote from `/api/quote`.
- Booking creates a one-off Flutterwave virtual account; the page polls `/api/bookings/:ref` every 5 s and reveals the Golden Ticket when the transfer lands. A refresh resumes the pending payment (reference kept in `localStorage`).
- Ticket links look like `https://grotto.auldontoys.com/#ticket-TKT-XXXXXX` and reload the ticket from `/api/tickets/:code`. The ticket QR encodes that link.
- Add to calendar downloads an `.ics`; Share uses the phone's share sheet.

## Changing the API domain
One line near the top of `index.html`: `window.GROTTO_API = "https://api.auldontoys.com";`
