import seedrandom from "seedrandom";

// Define lists of abilities, colors, and animals in masculine and feminine forms
const abilitiesMasculine = ["vesely", "hravy", "mily", "zabavny", "radostny", "usmevavy", "pratelsky", "stastny", "energicky", "rozverny", "vynalezavy", "kouzelny", "hodny", "kouzelnicky", "sikovny", "bystry", "chytry", "zvedavy", "roztomily", "blaznivy", "neposedny", "pohodovy", "rozesmaty", "rozkosny", "sneni", "hrdinsky", "napadity", "laskavy", "nezkazeny", "hrdinny", "kamaradsky", "dobrosrdecny", "nadherny", "dobrodruzny", "vitalni", "svetly", "nevinny", "hrdy", "odvazny", "skotacivy", "vtipny", "jedinecny", "slunecny"];
const abilitiesFeminine = ["vesela", "hrava", "mila", "zabavna", "radostna", "usmevava", "pratelska", "stastna", "energicka", "rozverna", "vynalezava", "kouzelna", "hodna", "kouzelnicka", "sikovna", "bystra", "chytra", "zvedava", "roztomila", "blazniva", "neposedna", "pohodova", "rozesmata", "rozkosna", "sneni", "hrdinska", "napadita", "laskava", "nezkazena", "hrdinna", "kamaradska", "dobrosrdecna", "nadherna", "dobrodruzna", "vitalni", "svetla", "nevinna", "hrda", "odvazna", "skotaciva", "vtipna", "jedinecna", "slunecna"];

const colorsMasculine = ["cerny", "modry", "zeleny", "zluty", "fialovy", "oranzovy", "ruzovy", "bily", "hnedy", "sedy", "zluty", "stribrny", "bezovy", "bordovy", "mentolovy", "tyrkysovy", "indigo", "neonovy", "olivovy", "safirovy", "fuchsiovy", "lily", "kremovy", "medeny", "perletovy", "zlatavy", "zelenozluty", "morska"];
const colorsFeminine = ["cerna", "modra", "zelena", "zluta", "fialova", "oranzova", "ruzova", "bila", "hneda", "seda", "zlata", "stribrna", "bezova", "bordo", "mentolova", "tyrkysova", "indigo", "neonova", "olivova", "safirova", "fuchsiova", "lila", "kremova", "medena", "perletova", "zlatava", "zelenozluta", "biloseda", "zelenomodra", "morska"];

const animalsMasculine = ["tygr", "slon", "lev", "krab", "pes", "vlk", "medved", "krokodyl","pstros", "labrador", "plamenak", "srnec", "delfin", "kockodan", "hroch", "byk", "krecek", "los", "jelen", "bizon", "kocour", "kolibrik", "pav", "albatros", "holub", "netopyr", "mroz", "papousek", "klokan"]
const animalsFeminime = ["zirafa", "orlice", "kukacka", "koala", "panda", "sova", "liska", "vcela", "vydra", "antilopa", "opice", "koza", "slepice", "lama", "zebra", "myš", "velryba"]

// Function to get a random item from an array using a seeded random generator
const getRandomItem = (arr, rng) => arr[Math.floor(rng() * arr.length)];

// Function to generate a passphrase using a seed and random gender selection
const generatePassphrase = (seed = Date.now().toString()) => {
    const rng = seedrandom(seed); // Create a seeded random generator

    // Randomly choose gender
    const gender = Math.random() < 0.5 ? "masculine" : "feminine"; // 50% chance to choose either

    let ability, color, animal;

    if (gender === "masculine") {
        ability = getRandomItem(abilitiesMasculine, rng);
        color = getRandomItem(colorsMasculine, rng);
        animal = getRandomItem(animalsMasculine, rng);
    } else {
        ability = getRandomItem(abilitiesFeminine, rng);
        color = getRandomItem(colorsFeminine, rng);
        animal = getRandomItem(animalsFeminime, rng);
    }

    return `${ability}-${color}-${animal}`;
};

export default generatePassphrase;
