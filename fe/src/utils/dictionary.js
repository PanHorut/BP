/**
 * ================================================================================
 * File: dictionary.js
 * Description:
 *       Utility for handling Czech-English translation of application.
 * Author: Dominik Horut (xhorut01)
 * ================================================================================
 */

// Dictionary of Czech and English translations for various application strings
export const dictionary = {
    cs: {
        logo: "DRILLOVAČKA",
        login: "Přihlásit se",
        register: "Registrovat se",
        registerText: "Ještě nemám účet - registrovat se",
        loginText: "Už mám účet - přihlásit se",
        adminText: "Jsem administrátor aplikace",
        adminLoginText: "Jsem administrátor aplikace",
        nickname: "Přezdívka",
        nicknamePlaceholder: "Tvá přezdívka",
        accessCode: "Přístupový kód",
        part1: "část 1",
        part2: "část 2",
        part3: "část 3",
        usernameError: "Prosím, zadejte přezdívku.",
        usernameForgot: "Zapomněl sis vytvořit přezdívku",
        passphraseError: "Prosím, zadejte všechny části přístupového kódu.",
        passphraseForgot: "Nejprve si musíš vygenerovat přístupový kód",
        loginSuccess: "Přihlášení proběhlo úspěšně",
        registrationSuccess: "Registrace proběhla úspěšně",
        invalidCredentials: "Neplatné přihlašovací údaje",
        somethingWentWrong: "Něco se pokazilo. Zkuste to znovu později.",
        logout: "Odhlásit se",
        logoutSuccess: "Odhlášení proběhlo úspěšně",
        inactivityLogout: "Byl jsi odhlášen z důvodu neaktivity",
        generatePassphrase: "Vygenerovat kód",
        generatePassphrasePlaceholder: "Vygeneruj si svůj přístupový kód",
        copied: "Zkopírováno",
        hi: "Ahoj",
        profile: "Profil",
        chooseTopic: "Jaké příklady chceš procvičit?",
        chooseOperation: "Vyber operace, které chceš procvičit",
        startPractice: "Jdeme na to",
        quit: "Ukončit",
        done: "Hotovo",
        skip: "Přeskočit",
        correctAnswer: "Správná odpověď",
        finish: "Hotovo!",
        exampleCountText: "Spočítal jsi",
        backtoMainMenu: "Zpět na hlavní stránku",
        noMistakes: "Bez chyby",
        oneMistake: "Jedna chyba",
        twoMistakes: "Dvě chyby",
        threeMistakes: "Tři chyby",
        skipped: "Přeskočeno",
        continue: "Pokračovat",
        summarySurveyText: "Jak se ti líbilo procvičování s touto aplikací?",
        clickMicText: "Klikni na mikrofon a odpověz prosím na otázku",
        chooseOptionText: "Vyber možnost která pro tebe platí",
        searchPlaceholderText: "Napiš název cvičení, které hledáš",

    },

    en: {
        logo: "DRILLAPP",
        login: "Login",
        register: "Register",
        registerText: "I don't have an account yet - register",
        loginText: "I already have an account - log in",
        adminText: "I am an app administrator",
        adminLoginText: "I am an app administrator",
        nickname: "Nickname",
        nicknamePlaceholder: "Your nickname",
        accessCode: "Acess code",
        part1: "part 1",
        part2: "part 2",
        part3: "part 3",
        usernameError: "Please enter a username.",
        usernameForgot: "You forgot to create a username",
        passphraseError: "Please enter all parts of the passphrase.",
        passphraseForgot: "You need to generate an access code first",
        loginSuccess: "Login was successful",
        registrationSuccess: "Registration was successful",
        invalidCredentials: "Invalid credentials",
        somethingWentWrong: "Something went wrong. Please try again later.",
        logout: "Logout",
        logoutSuccess: "Logout was successful",
        inactivityLogout: "You have been logged out due to inactivity",
        generatePassphrase: "Generate passphrase",
        generatePassphrasePlaceholder: "Generate your passphrase",
        copied: "Copied",
        hi: "Hi",
        profile: "Profile",
        chooseTopic: "What examples do you want to practice?",
        chooseOperation: "Select the operations you want to practice",
        startPractice: "Let's go",
        quit: "Quit",
        done: "Done",
        skip: "Skip",
        correctAnswer: "Correct answer",
        finish: "That's it!",
        exampleCountText: "You counted",
        backtoMainMenu: "Back to main menu",
        noMistakes: "No mistake",
        oneMistake: "One mistake",
        twoMistakes: "Two mistakes",
        threeMistakes: "Three mistakes",
        skipped: "Skipped",
        continue: "Continue",
        summarySurveyText: "How did you like practicing with this app?",
        clickMicText: "Click on the microphone and please answer the question",
        chooseOptionText: "Choose the option that applies to you",
        searchPlaceholderText: "Type the name of the exercise you are looking for",
    }
};

/**
 * Translates a skill name from Czech to English depending on the selected language.
 * 
 * @param {string} czechName - name of the skill in Czech
 * @param {string} lang - language code ('cs' or 'en')
 * @returns {string} translated skill name
 */
export const getSkillName = (czechName, lang) => {
    const skillMap = {
        "Sčítání": "Addition",
        "Odčítání": "Subtraction",
        "Násobení": "Multiplication",
        "Dělení": "Division",
        "Druhá mocnina": "Square",
        "Druhá odmocnina": "Square Root",
        "Krácení": "Simplification",
        "Celá čísla": "Integers",
        "Desetinná čísla": "Decimal Numbers",
        "Zlomky": "Fractions",
        "Pythagorova věta": "Pythagorean Theorem",
        "Rovnice": "Equations",
        "Do 20": "Up to 20",
        "Přes 20": "Over 20",
        "Do 100": "Up to 100",
        "Nad 100": "Over 100",
        "Do 50": "Up to 50",
        "Přes 10": "Over 10",
        "Do 10": "Up to 10",
        "Desetiny": "Decimals",
        "Poměry": "Ratio"
    };

    return lang === "cs" ? czechName : skillMap[czechName] || czechName;
};
