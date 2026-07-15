# REDS — Research Evaluation and Development Studies

Static multi-page website (HTML, CSS, JavaScript only). No build step, database, or backend.

## Pages

| Page | File |
|------|------|
| Home | `index.html` |
| About Us | `about.html` |
| Services | `services.html` |
| Expertise | `expertise.html` |
| Contact | `contact.html` |

## How to view

Open `index.html` in a browser, or serve the folder with any static server:

```bash
npx --yes serve .
```

Then visit the URL shown in the terminal (typically `http://localhost:3000`).

## Notes

- Logo: `assets/logo/reds-logo.png`
- Animations: GSAP + ScrollTrigger (CDN)
- Contact form opens the user’s email client via `mailto:` (no server)
- Address, phone, and client names are placeholders until real details are provided
- Service images use Unsplash placeholders; replace with project photography when available
