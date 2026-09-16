# Putting this on GitHub

Everything here is committed and ready. This session has no GitHub account
attached to it, so the last two steps are yours. They take about three minutes.

## 1. Make the repository

On github.com, click **New repository** and use exactly this name:

```
judge-audit
```

The name matters: the QR code on the closing slide already points at
`github.com/ImSuMyatNoe/judge-audit`, so a different name means reprinting
the QR. Leave it public, and do **not** tick "add a README", because this
folder already has one.

## 2. Push what is here

From inside this folder:

```bash
git remote add origin https://github.com/ImSuMyatNoe/judge-audit.git
git branch -M main
git push -u origin main
```

If git asks for a password, GitHub wants a personal access token rather than
your account password. Settings, Developer settings, Personal access tokens,
Tokens classic, Generate new token, tick `repo`.

## 3. Turn on GitHub Pages

In the repository: **Settings**, then **Pages** in the left sidebar.

| Field | Choose |
|---|---|
| Source | Deploy from a branch |
| Branch | `main` |
| Folder | `/docs` |

Save. The first build takes a minute or two. After that the slides are live at:

```
https://imsumyatnoe.github.io/judge-audit/
```

That link opens the deck itself, full screen, fonts and all. Anyone can open it
on a phone in the room. The three demos run there exactly as they do locally,
because nothing in the page talks to a server.

The written docs sit next to it and render on github.com:

- `docs/checklist.md` the five point checklist
- `docs/calibration.md` where every simulator number comes from
- `docs/using-your-own-data.md` how to point the audits at your own CSV

## 4. Optional, put a link on your portfolio

`imsumyatnoe.github.io` is a separate repository. Adding one line there gives
the talk a permanent home next to your papers:

```html
<a href="https://imsumyatnoe.github.io/judge-audit/">
  LLM as a Judge Is Probably Lying to You &middot; Beyond the Vibes, Sep 2026
</a>
```

## If you change a slide later

Edit `talk/_btv_template.html`, never the built files, then:

```bash
python talk/build.py
git add -A && git commit -m "talk: tweak a slide" && git push
```

`build.py` writes both `talk/btv-slides.html` and `docs/index.html` from the
same template, so the copy you present from and the copy on the web never drift
apart. Pages redeploys on its own within a minute of the push.
