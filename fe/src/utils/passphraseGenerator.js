import seedrandom from "seedrandom";

const abilitiesMasculine = ["vesely", "hravy", "mily", "zabavny", "radostny", "usmevavy", "pratelsky", "stastny", "energicky", "rozverny", "vynalezavy", "kouzelny", "hodny", "kouzelnicky", "sikovny", "bystry", "chytry", "zvedavy", "roztomily", "blaznivy", "neposedny", "pohodovy", "rozesmaty", "rozkosny", "hrdinsky", "napadity", "laskavy", "nezkazeny", "kamaradsky", "dobrosrdecny", "nadherny", "dobrodruzny", "hrdy", "odvazny", "skotacivy", "vtipny", "jedinecny", "slunecny"];
const abilitiesFeminine = ["vesela", "hrava", "mila", "zabavna", "radostna", "usmevava", "pratelska", "stastna", "energicka", "rozverna", "vynalezava", "kouzelna", "hodna", "kouzelnicka", "sikovna", "bystra", "chytra", "zvedava", "roztomila", "blazniva", "neposedna", "pohodova", "rozesmata", "rozkosna", "hrdinska", "napadita", "laskava", "nezkazena", "kamaradska", "dobrosrdecna", "nadherna", "dobrodruzna", "nevinna", "hrda", "odvazna", "skotaciva", "vtipna", "jedinecna", "slunecna"];

const colorsMasculine = ["cerny", "modry", "zeleny", "zluty", "fialovy", "oranzovy", "ruzovy", "bily", "hnedy", "sedy", "zluty", "stribrny", "bezovy", "mentolovy", "tyrkysovy", "neonovy", "olivovy", "safirovy", "kremovy", "medeny", "perletovy", "zlatavy"];
const colorsFeminine = ["cerna", "modra", "zelena", "zluta", "fialova", "oranzova", "ruzova", "bila", "hneda", "seda", "zlata", "stribrna", "bezova", "mentolova", "tyrkysova", "neonova", "olivova", "safirova", "kremova", "medena", "perletova", "zlatava"];

const animalsMasculine = ["tygr", "slon", "lev", "krab", "pes", "vlk", "medved", "krokodyl","pstros", "labrador", "plamenak", "srnec", "delfin", "kockodan", "hroch", "byk", "krecek", "los", "jelen", "bizon", "kocour", "kolibrik", "pav", "albatros", "holub", "netopyr", "mroz", "papousek", "klokan"]
const animalsFeminime = ["zirafa", "orlice", "kukacka", "koala", "panda", "sova", "liska", "vcela", "vydra", "antilopa", "opice", "koza", "slepice", "lama", "zebra", "mys", "velryba"]

const getRandomItem = (arr, rng) => arr[Math.floor(rng() * arr.length)];

const generatePassphrase = (seed = Date.now().toString()) => {
    const rng = seedrandom(seed);

    const gender = Math.random() < 0.5 ? "masculine" : "feminine";

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
