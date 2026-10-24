// Records the real portfolio page (particles, typing, tilt, reveals) and converts it to GIFs.
// Usage: npm run record      (needs ffmpeg installed)
import { chromium } from "playwright";
import { execSync } from "node:child_process";
import { mkdirSync, readdirSync, rmSync, renameSync } from "node:fs";
import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

const W = 1000, H = 560;
const root = resolve(import.meta.dirname, "..");
const tmp = resolve(root, ".rec");
const out = resolve(root, "assets");
rmSync(tmp, { recursive: true, force: true });
mkdirSync(tmp, { recursive: true });
mkdirSync(out, { recursive: true });

const browser = await chromium.launch();
const ctx = await browser.newContext({
  viewport: { width: W, height: H },
  colorScheme: "dark",
  recordVideo: { dir: tmp, size: { width: W, height: H } },
});
const page = await ctx.newPage();
await page.goto(pathToFileURL(resolve(root, "index.html")).href, { waitUntil: "networkidle" }).catch(() => {});
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(800);

// Part 1: hero, mouse circles over the particle sphere
let t0 = Date.now();
while (Date.now() - t0 < 9000) {
  const t = (Date.now() - t0) / 1000;
  await page.mouse.move(W * 0.62 + Math.cos(t * 1.3) * W * 0.28, H * 0.5 + Math.sin(t * 1.7) * H * 0.32);
  await page.waitForTimeout(30);
}
// Part 2: tour through all sections (card tilt + reveal)
await page.mouse.move(W * 0.3, H * 0.5);
for (let i = 0; i < 14; i++) {
  await page.evaluate(() => window.scrollBy({ top: 380, behavior: "instant" }));
  const t1 = Date.now();
  while (Date.now() - t1 < 1100) {
    const t = (Date.now() - t1) / 1000;
    await page.mouse.move(W * 0.2 + t * W * 0.55, H * 0.35 + Math.sin(t * 5 + i) * H * 0.2);
    await page.waitForTimeout(30);
  }
}
await ctx.close();
await browser.close();

const vid = resolve(tmp, readdirSync(tmp).find((f) => f.endsWith(".webm")));
const gif = (ss, t, fps, w, colors, name) =>
  execSync(
    `ffmpeg -y -v error -ss ${ss} ${t ? `-t ${t}` : ""} -i "${vid}" -vf "fps=${fps},scale=${w}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=${colors}:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" "${resolve(out, name)}"`,
    { stdio: "inherit" }
  );
gif(0.6, 9, 12, 720, 64, "particles.gif");
gif(9.8, 0, 10, 600, 48, "tour.gif");
rmSync(tmp, { recursive: true, force: true });
console.log("Done: assets/particles.gif, assets/tour.gif");
