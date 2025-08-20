CANVAS_SPOOFING_SCRIPT = """
    (() => {
        const toBlob = HTMLCanvasElement.prototype.toBlob;
        const toDataURL = HTMLCanvasElement.prototype.toDataURL;
        const getImageData = CanvasRenderingContext2D.prototype.getImageData;

        // Add noise to canvas data
        const noisify = function(canvas, context) {
            const {width, height} = canvas;
            const imageData = getImageData.apply(context, [0, 0, width, height]);
            for (let i = 0; i < imageData.data.length; i += 4) {
                const r = Math.random() * 2 - 1; // -1 to 1
                imageData.data[i] = imageData.data[i] + r;
                imageData.data[i+1] = imageData.data[i+1] + r;
                imageData.data[i+2] = imageData.data[i+2] + r;
            }
            context.putImageData(imageData, 0, 0);
        };

        HTMLCanvasElement.prototype.toBlob = function() {
            noisify(this, this.getContext("2d"));
            return toBlob.apply(this, arguments);
        };

        HTMLCanvasElement.prototype.toDataURL = function() {
            noisify(this, this.getContext("2d"));
            return toDataURL.apply(this, arguments);
        };

        CanvasRenderingContext2D.prototype.getImageData = function() {
            noisify(this.canvas, this);
            return getImageData.apply(this, arguments);
        };
    })();
"""
