import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { chapters } from "../content/chapters.mjs";
import { renderChapter } from "./render-html.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.join(__dirname, "..");
const outDir = path.join(root, "dist", "html");

fs.mkdirSync(outDir, { recursive: true });

for (const ch of chapters) {
  const html = renderChapter(ch);
  const filename = `${ch.grade}-Unit${String(ch.unit).padStart(2, "0")}-${ch.slug}.html`;
  fs.writeFileSync(path.join(outDir, filename), html, "utf8");
  console.log("Wrote", filename);
}

console.log(`Generated ${chapters.length} HTML files in dist/html/`);
