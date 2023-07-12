
const darkModeStyles = `
.image-block {
    background-color: #1d1d1d;
}

.image-block-tall {
    background-color: #1d1d1d;
    color: #d4d4d4;
}

    .image-block-tall img {
        padding: 3px;
        background-color: #2b2b2b
    }

.caption-tall {
    color: white;
}
`;

function injectDarkModeStyles() {
    const styleElement = document.createElement("style");
    styleElement.innerHTML = darkModeStyles;
    document.head.appendChild(styleElement);
}

function enableDarkMode() {
    injectDarkModeStyles();
}

enableDarkMode();
