
let currentTheme = 'light';

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
        background-color: #2b2b2b;
    }

.caption-tall {
    color: #d4d4d4;
}
`;


function enableDarkMode() {
    document.head.appendChild(styleElement);
    currentTheme = 'dark';
}

function disableDarkMode() {
    styleElement.remove();
    currentTheme = 'light';
}

function isDarkModeHour() {
    const currentTime = new Date();
    const currentHour = currentTime.getHours();

    return currentHour < 6 || currentHour > 20;
}

/** Round a date to the next 6am, or 8pm */
function getNextSunriseSunsetDate() {
    var currentDate = new Date();

    // Check if it's before 6:00 am
    if (currentDate.getHours() < 6) {
        currentDate.setHours(6, 0, 0, 0); // Set to 6:00 am on the current day
    }
    // Check if it's between 6:00 am and 8:00 pm
    else if (currentDate.getHours() >= 6 && currentDate.getHours() < 20) {
        currentDate.setHours(20, 0, 0, 0); // Set to 8:00 pm on the current day
    }
    // Otherwise, it's after 8:00 pm
    else {
        currentDate.setDate(currentDate.getDate() + 1); // Move to the next day
        currentDate.setHours(6, 0, 0, 0); // Set to 6:00 am on the next day
    }

    return currentDate;
}

/** Check if the dark/light mode theme has an over-ridden state by the user
 *  that is still valid (not expired)
 */
function themeOverridden() {
    const themeData = JSON.parse(localStorage.getItem("userTheme"));

    if (!themeData) return;

    // If expired, reset the state of user override
    if (new Date(themeData.expiration) <= new Date()) {
        localStorage.setItem("userTheme", null);
        return;
    }

    return themeData.theme;
}

/** Change the current theme to @param theme 
 *  and set the preference in localStorage
 */
function overrideTheme(theme) {
    if (!['light', 'dark'].includes(theme))
        throw `Invalid theme type: ${theme}`;

    const data = {
        theme: theme,
        expiration: getNextSunriseSunsetDate(),
    };
    localStorage.setItem("userTheme", JSON.stringify(data));

    if (currentTheme !== theme) {
        if (theme === 'dark')
            enableDarkMode();
        else
            disableDarkMode();
    }
}

/** Check the current theme, and enable dark mode if necessary */
function checkDarkMode() {
    const override = themeOverridden();
    console.log("end", override)

    if (override === 'dark'){
        enableDarkMode();
        return;
    }
    if (override === 'light')
        return;
    
    if (isDarkModeHour())
        enableDarkMode();
}

const setLightTheme = () => overrideTheme('light');
const setDarkTheme = () => overrideTheme('dark');

// Initalize the dark theme element
const styleElement = document.createElement("style");
styleElement.innerHTML = darkModeStyles;

checkDarkMode();
