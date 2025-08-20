# This file contains JavaScript snippets to be injected into the page to spoof fingerprints.

# Based on https://github.com/puppeteer/puppeteer/blob/main/packages/puppeteer-extra-plugin-stealth/src/evasions/canvas/index.ts
CANVAS_SPOOFING_SCRIPT = """
    (seed) => {
        const _native = {
            getImageData: CanvasRenderingContext2D.prototype.getImageData
        };

        // A seeded random function
        const seededRandom = (seed) => {
            let s = seed % 2147483647;
            return () => {
                s = (s * 16807) % 2147483647;
                return (s - 1) / 2147483646;
            };
        };

        const random = seededRandom(seed);

        // Add noise to canvas data
        const noisify = (canvas, context) => {
            if (context) {
                const { width, height } = canvas;
                const imageData = _native.getImageData.apply(context, [0, 0, width, height]);
                for (let i = 0; i < height; i++) {
                    for (let j = 0; j < width; j++) {
                        const n = i * (width * 4) + j * 4;
                        imageData.data[n + 0] = imageData.data[n + 0] + (random() * 2 - 1);
                        imageData.data[n + 1] = imageData.data[n + 1] + (random() * 2 - 1);
                        imageData.data[n + 2] = imageData.data[n + 2] + (random() * 2 - 1);
                    }
                }
                context.putImageData(imageData, 0, 0);
            }
        };

        // Overriding the native methods
        HTMLCanvasElement.prototype.toDataURL = function() {
            noisify(this, this.getContext('2d'));
            return this.toDataURL.apply(this, arguments);
        };

        CanvasRenderingContext2D.prototype.getImageData = function() {
            noisify(this.canvas, this);
            return _native.getImageData.apply(this, arguments);
        };
    }
"""

AUDIO_SPOOFING_SCRIPT = """
    () => {
        const originalGetChannelData = AudioBuffer.prototype.getChannelData;
        AudioBuffer.prototype.getChannelData = function() {
            const data = originalGetChannelData.apply(this, arguments);
            for (let i = 0; i < data.length; i++) {
                data[i] += (Math.random() * 0.0000001 - 0.00000005);
            }
            return data;
        };
    }
"""

FONTS_SPOOFING_SCRIPT = """
    () => {
        const commonFonts = [
            "Arial", "Courier New", "Georgia", "Times New Roman", "Trebuchet MS", "Verdana",
            "Roboto", "Open Sans", "Lato", "Montserrat", "Oswald", "Source Sans Pro",
            "Calibri", "Candara", "Segoe UI"
        ];

        const originalFontIsAvailable = document.fonts.check;
        document.fonts.check = function(font, text) {
            if (commonFonts.some(common => font.toLowerCase().includes(common.toLowerCase()))) {
                return true;
            }
            return originalFontIsAvailable.apply(this, arguments);
        };

        // Hiding the full font list
        Object.defineProperty(document.fonts, 'entries', {
            value: function*() {
                for (const font of commonFonts) {
                    // This is a simplification. A real implementation would need to create FontFace objects.
                    yield { family: font };
                }
            }
        });
    }
"""

HARDWARE_SPOOFING_SCRIPT = """
    ({ concurrency, memory }) => {
        Object.defineProperty(navigator, 'hardwareConcurrency', {
            get: () => concurrency,
            configurable: true
        });
        Object.defineProperty(navigator, 'deviceMemory', {
            get: () => memory,
            configurable: true
        });
    }
"""

WEBGL_SPOOFING_SCRIPT = """
    ({ vendor, renderer }) => {
        const getParameter = WebGLRenderingContext.prototype.getParameter;
        WebGLRenderingContext.prototype.getParameter = function(parameter) {
            if (parameter === this.VERSION) {
                return 'WebGL 1.0';
            }
            if (parameter === this.VENDOR) {
                return vendor;
            }
            if (parameter === this.RENDERER) {
                return renderer;
            }
            return getParameter.apply(this, arguments);
        };
    }
"""
