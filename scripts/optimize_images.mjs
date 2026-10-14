import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { mkdirSync, readdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const output = join(root, 'static/img/background');
const input = process.argv[2] ? resolve(process.argv[2]) : output;
const filenames = readdirSync(input).filter(name => /^\d{2}\.jpg$/.test(name)).sort();
if (filenames.length !== 23) throw new Error('Expected 23 JPEG images (00.jpg to 22.jpg).');
mkdirSync(output, { recursive: true });
const images = [];

for (const filename of filenames) {
    const original = join(input, filename);
    const metadata = JSON.parse(execFileSync('ffprobe', [
        '-v', 'error', '-select_streams', 'v:0', '-show_entries',
        'stream=width,height', '-of', 'json', original,
    ], { encoding: 'utf8' })).streams[0];
    const variants = [];
    const widths = [...new Set([Math.min(480, metadata.width), Math.min(800, metadata.width)])];
    for (const width of widths) {
        const temporary = join(output, `${filename.slice(0, -4)}-${width}.tmp.webp`);
        execFileSync('ffmpeg', [
            '-hide_banner', '-loglevel', 'error', '-y', '-i', original,
            '-vf', `scale=w=${width}:h=-2:flags=lanczos`, '-frames:v', '1',
            '-c:v', 'libwebp', '-quality', '75', '-compression_level', '6',
            '-map_metadata', '-1', temporary,
        ]);
        const hash = createHash('sha256').update(readFileSync(temporary)).digest('hex').slice(0, 12);
        const name = `${filename.slice(0, -4)}-${width}.${hash}.webp`;
        renameSync(temporary, join(output, name));
        variants.push({ width, url: `static/img/background/${name}` });
    }
    images.push({
        width: metadata.width,
        height: metadata.height,
        fallback: `static/img/background/${filename}`,
        variants,
    });
}

writeFileSync(join(output, 'manifest.json'), `${JSON.stringify(images)}\n`);
console.log(`Generated responsive WebP variants for ${images.length} images.`);