import {Config} from '@remotion/cli/config';
import path from 'path';
import fs from 'fs';

// Usa o Chrome headless que o Playwright já baixou, sem baixar outro.
const pw = path.join(process.env.LOCALAPPDATA ?? '', 'ms-playwright');
const shell = fs.existsSync(pw)
  ? fs.readdirSync(pw).filter((d) => d.startsWith('chromium_headless_shell-')).sort().pop()
  : undefined;
if (shell) {
  Config.setBrowserExecutable(path.join(pw, shell, 'chrome-headless-shell-win64', 'chrome-headless-shell.exe'));
}
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setCodec('h264');
Config.setCrf(21);
Config.setPixelFormat('yuv420p');
Config.setConcurrency(4);
