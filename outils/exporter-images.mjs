// Exporte les illustrations en PNG à 1x, 2x et 3x, fond transparent.
//
// Le brief (outils/images-gs.json, cadrage.technique) déclare le SVG comme
// maître et le PNG 1x/2x/3x transparent comme forme livrée à l'application. Ce
// script est l'étape qui produit cette forme. Il ne dessine rien : les dessins
// sont dans outils/generer-images.py, et c'est le seul endroit où on les
// corrige. Régénérer les PNG après toute correction des SVG.
//
// Dépendance : @resvg/resvg-js. Elle n'est pas installée dans le projet — le
// SVG reste le maître, et l'export est une étape de construction, pas une
// source. Pour l'exécuter :
//
//   NODE_PATH=<espace de travail node>/node_modules node outils/exporter-images.mjs
//
// Usage :
//   node exporter-images.mjs            # écrit contenu/images/png/

import { readdirSync, readFileSync, writeFileSync, mkdirSync, statSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

// `import "@resvg/resvg-js"` échoue ici : la résolution ESM ignore NODE_PATH,
// et le paquet n'est pas dans un node_modules du projet (le SVG est le maître,
// l'export est une étape de construction). `require`, lui, consulte NODE_PATH.
// D'où ce détour — il n'est pas décoratif, il est la seule façon de faire
// tourner le script sans installer de node_modules dans le dépôt.
const require = createRequire(import.meta.url);
const { Resvg } = require("@resvg/resvg-js");

const ICI = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(ICI, "..", "contenu", "images");
const CIBLE = join(SOURCE, "png");

// La taille logique est celle du brief : 512 points. Les trois densités suivent.
const DENSITES = [
  ["1x", 512],
  ["2x", 1024],
  ["3x", 1536],
];

const svg = readdirSync(SOURCE)
  .filter((f) => f.startsWith("ill_") && f.endsWith(".svg"))
  .sort();

if (svg.length === 0) {
  console.error("aucun ill_*.svg dans " + SOURCE + " — lancer d'abord generer-images.py");
  process.exit(2);
}

mkdirSync(CIBLE, { recursive: true });

let octets = 0;
let plusGros = { nom: "", taille: 0 };
let ecrits = 0;

for (const fichier of svg) {
  const contenu = readFileSync(join(SOURCE, fichier), "utf8");
  const base = fichier.replace(/\.svg$/, "");
  for (const [densite, largeur] of DENSITES) {
    // Pas de `background` : resvg laisse alors le fond transparent, ce que le
    // brief exige. Un fond opaque passerait inaperçu à l'œil sur un écran clair
    // et se verrait sur le fond sombre de l'application.
    const rendu = new Resvg(contenu, { fitTo: { mode: "width", value: largeur } });
    const sortie = join(CIBLE, `${base}@${densite}.png`);
    const png = rendu.render().asPng();
    writeFileSync(sortie, png);
    octets += png.length;
    ecrits += 1;
    if (png.length > plusGros.taille) {
      plusGros = { nom: `${base}@${densite}.png`, taille: png.length };
    }
  }
}

console.log(`${ecrits} PNG écrits dans contenu/images/png/`);
console.log(`mots couverts : ${svg.length} × ${DENSITES.length} densités`);
console.log(`total : ${octets} octets`);
console.log(`plus gros : ${plusGros.nom} — ${plusGros.taille} octets`);
console.log(`contrôle : ${statSync(CIBLE).isDirectory() ? "dossier présent" : "dossier absent"}`);
