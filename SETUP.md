# What is in this zip

| Path | Purpose |
|---|---|
| `README.md` | Your GitHub profile README (animated, links to the live 3D site) |
| `assets/` | Animated GIFs of the 3D site, animated SVG buttons, headings, divider |
| `profile_banner.png` | 1280x640 static banner (also works as the repo "Social preview" image) |
| `profile_card.png` | Developer ID card image |
| `index.html` | The full 3D website in ONE file (HTML + CSS + JS inside) |
| `website/` | The same 3D website split into `index.html`, `css/style.css`, `js/main.js` |
| `.github/workflows/snake.yml` | Optional: animated contribution snake |

# Push from cmd (Windows)

## 1. Profile README  (repo: sukhee-2626/sukhee-2626)
```bat
cd /d D:\
git clone https://github.com/sukhee-2626/sukhee-2626.git
tar -xf "%USERPROFILE%\Downloads\sukhee-profile-pack.zip" -C sukhee-2626
cd sukhee-2626
rmdir /s /q website
del index.html SETUP.md
git add .
git commit -m "Animated 3D portfolio README"
git push origin main
```

## 2. Live 3D website  (repo: sukhee-2626/portfolio, create it empty on github.com first)
```bat
cd /d D:\
mkdir portfolio && cd portfolio
tar -xf "%USERPROFILE%\Downloads\sukhee-profile-pack.zip" index.html
git init
git add .
git commit -m "3D portfolio website"
git branch -M main
git remote add origin https://github.com/sukhee-2626/portfolio.git
git push -u origin main
```
Then: Settings -> Pages -> Source: main branch -> Save.
Live at https://sukhee-2626.github.io/portfolio/

Optional: upload `profile_banner.png` in the portfolio repo under Settings -> Social preview.
