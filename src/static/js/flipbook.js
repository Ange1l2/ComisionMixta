$(document).ready(function () {
    const numPages = 98;
    const flipbook = $('#flipbook');
    const pdfPagesPath = flipbook.data('pdf-pages');

    if (!pdfPagesPath) {
        console.error("La ruta de las imágenes no está definida. Asegúrate de haber definido 'data-pdf-pages' en el HTML.");
        return;
    }

    // Cargar las imágenes en el flipbook
    for (let i = 1; i <= numPages; i++) {
        const imgSrc = `${pdfPagesPath}pagina${i}.jpg`;
        const img = $('<img>', { src: imgSrc, alt: `Page ${i}` });
        const pageDiv = $('<div class="page"></div>').css({
        }).append(img);
        flipbook.append(pageDiv);
    }

    function adjustFlipbookSize() {
        const windowWidth = $(window).width();
        let newWidth, newHeight;

        if (windowWidth < 768) {
            newWidth = windowWidth * 0.9; 
        } else {
            newWidth = Math.min(windowWidth * 0.8, 800);
        }

        newHeight = newWidth * 1.41; 
        flipbook.turn('size', newWidth, newHeight);
    }

    // Inicializar el flipbook con Turn.js
    flipbook.turn({
        width: flipbook.width(),
        height: flipbook.width(),
        
        autoCenter: true
    });
    
    adjustFlipbookSize();
    $(window).resize(adjustFlipbookSize);
});
