// Bundles the Stageshow hero into assets/demo.js, the kit's CSS into
// assets/kit/stageshow.css and copies the hero's own CSS to assets/demo-ezeos.css.
// Uses the skill's node_modules (esbuild, react), so nothing installs here:
//   node _src/build.mjs
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'
import { homedir } from 'node:os'
import { mkdirSync, renameSync, copyFileSync } from 'node:fs'

const mods = join(homedir(), '.claude', 'skills', 'stageshow', 'node_modules')
const { build } = createRequire(join(mods, 'x.js'))('esbuild')

const here = dirname(fileURLToPath(import.meta.url))
await build({
  entryPoints: { demo: join(here, 'entry.tsx') },
  outdir: join(here, '..', 'assets'),
  bundle: true,
  minify: true,
  format: 'iife',
  target: 'es2020',
  jsx: 'automatic',
  nodePaths: [mods],
  define: { 'process.env.NODE_ENV': '"production"' },
  loader: { '.svg': 'dataurl', '.png': 'dataurl', '.jpg': 'dataurl', '.woff2': 'dataurl' },
  logLevel: 'info',
})

const assets = join(here, '..', 'assets')
mkdirSync(join(assets, 'kit'), { recursive: true })
renameSync(join(assets, 'demo.css'), join(assets, 'kit', 'stageshow.css'))
copyFileSync(join(here, 'hero', 'ezeos.css'), join(assets, 'demo-ezeos.css'))
