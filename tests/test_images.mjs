import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { runInNewContext } from 'node:vm';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const images = JSON.parse(readFileSync(resolve(root, 'static/img/background/manifest.json')));
const script = readFileSync(resolve(root, 'static/js/phb_photos_animation.js'), 'utf8');

test('responsive assets exist and use content-versioned WebP URLs', () => {
    assert.equal(images.length, 23);
    for (const [index, image] of images.entries()) {
        assert.ok(image.width > 0 && image.height > 0);
        assert.equal(image.fallback, `static/img/background/${String(index).padStart(2, '0')}.jpg`);
        assert.ok(existsSync(resolve(root, image.fallback)));
        assert.deepEqual(image.variants.map(variant => variant.width), [480, 800]);
        for (const variant of image.variants) {
            const bytes = readFileSync(resolve(root, variant.url));
            assert.equal(bytes.toString('ascii', 0, 4), 'RIFF');
            assert.equal(bytes.toString('ascii', 8, 12), 'WEBP');
            const hash = createHash('sha256').update(bytes).digest('hex').slice(0, 12);
            assert.ok(variant.url.endsWith(`-${variant.width}.${hash}.webp`));
        }
    }
});

async function renderCarousel(withObserver = true) {
    const observers = [];
    const createElement = function(tag) {
        return {
            tag, children: [], dataset: {}, style: {},
            append(...children) { this.children.push(...children); },
            appendChild(child) { this.children.push(child); },
            querySelector(selector) { return this.children.find(child => child.tag === selector); },
            hasAttribute(name) { return Object.hasOwn(this, name); },
            classList: {
                classes: new Set(),
                add(name) { this.classes.add(name); },
                toggle(name, enabled) {
                    if (enabled) this.classes.add(name);
                    else this.classes.delete(name);
                },
            },
        };
    };
    const container = createElement('div');
    container.parentElement = createElement('div');
    let ready;
    class MockObserver {
        constructor(callback, options) {
            this.callback = callback;
            this.options = options;
            this.targets = new Set();
            observers.push(this);
        }
        observe(target) { this.targets.add(target); }
        unobserve(target) { this.targets.delete(target); }
        disconnect() { this.targets.clear(); }
    }
    const context = {
        document: {
            querySelector: () => container,
            createElement,
            addEventListener: (event, callback) => { ready = callback; },
        },
        fetch: async () => ({ ok: true, json: async () => images }),
        window: withObserver ? { IntersectionObserver: MockObserver } : {},
        IntersectionObserver: MockObserver,
    };
    runInNewContext(script, context);
    await ready();
    return { container, observers };
}

test('carousel reserves dimensions and defers downloads until near the gallery', async () => {
    const { container, observers } = await renderCarousel();
    assert.equal(container.children.length, 46);
    const [photoObserver, galleryObserver] = observers;
    assert.equal(photoObserver.options.root, container.parentElement);
    assert.equal(photoObserver.options.rootMargin, '0px 800px');
    assert.equal(galleryObserver.options.rootMargin, '400px 0px');
    assert.equal(photoObserver.targets.size, 0);
    for (const picture of container.children) {
        const img = picture.querySelector('img');
        assert.ok(img.width > 0 && img.height > 0);
        assert.match(picture.style.width, /^\d+px$/);
        assert.equal(img.src, undefined);
        assert.equal(picture.querySelector('source').srcset, undefined);
    }
    galleryObserver.callback([{ isIntersecting: true }]);
    assert.equal(photoObserver.targets.size, 46);
    assert.ok(container.classList.classes.has('is-visible'));
    const first = container.children[0];
    photoObserver.callback([{ target: first, isIntersecting: false }]);
    assert.equal(first.querySelector('img').src, undefined);
    photoObserver.callback([{ target: first, isIntersecting: true }]);
    assert.equal(first.querySelector('img').src, images[0].fallback);
    assert.match(first.querySelector('source').srcset, /480w, .*800w/);
    assert.equal(photoObserver.targets.size, 45);
    galleryObserver.callback([{ isIntersecting: false }]);
    assert.equal(photoObserver.targets.size, 0);
    assert.ok(!container.classList.classes.has('is-visible'));
    galleryObserver.callback([{ isIntersecting: true }]);
    assert.equal(photoObserver.targets.size, 45);
});

test('without IntersectionObserver, native lazy loading remains available', async () => {
    const { container, observers } = await renderCarousel(false);
    assert.equal(observers.length, 0);
    assert.ok(container.classList.classes.has('is-visible'));
    for (const picture of container.children) {
        assert.equal(picture.querySelector('img').loading, 'lazy');
        assert.ok(picture.querySelector('img').src);
        assert.ok(picture.querySelector('source').srcset);
    }
});