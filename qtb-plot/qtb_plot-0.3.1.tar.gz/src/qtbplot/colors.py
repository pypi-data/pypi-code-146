from __future__ import annotations

light_gray = ".8"
dark_gray = ".15"

colorschemes = {
    "mpl": (
        "#1f77b4",
        "#ff7f0e",
        "#2ca02c",
        "#d62728",
        "#9467bd",
        "#8c564b",
        "#e377c2",
        "#7f7f7f",
        "#bcbd22",
        "#17becf",
    ),  # Credit: category10 color palette developed at Tableau
    "stone": (
        "#396AB1",
        "#DA7C30",
        "#3E9651",
        "#CC2529",
        "#535154",
        "#6B4C9A",
        "#922428",
        "#948B3D",
    ),  # Credit: Maureen Stone
    "flatui": (
        "#1abc9c",  # TURQUOISE
        "#2ecc71",  # EMERALD
        "#3498db",  # PETER RIVER
        "#9b59b6",  # AMETHYST
        "#34495e",  # WET ASPHALT
        "#f1c40f",  # SUN FLOWER
        "#e67e22",  # CARROT
        "#e74c3c",  # ALIZARIN
        "#ecf0f1",  # CLOUDS
        "#95a5a6",  # CONCRETE
    ),  # Credit: flatuicolors.com
    "flatui_dark": (
        "#16a085",  # GREEN SEA
        "#27ae60",  # NEPHRITIS
        "#2980b9",  # BELIZE HOLE
        "#8e44ad",  # WISTERIA
        "#2c3e50",  # MIDNIGHT BLUE
        "#f39c12",  # ORANGE
        "#d35400",  # PUMPKIN
        "#c0392b",  # POMEGRANATE
        "#bdc3c7",  # SILVER
        "#7f8c8d",  # ASBESTOS
    ),  # Credit: flatuicolors.com
    "us": (
        "#55efc4",  # LIGHT GREENISH BLUE
        "#81ecec",  # FADED POSTER
        "#74b9ff",  # GREEN DARNER TAIL
        "#a29bfe",  # SHY MOMENT
        "#dfe6e9",  # CITY LIGHTS
        "#ffeaa7",  # SOUR LEMON
        "#fab1a0",  # FIRST DATE
        "#ff7675",  # PINK GLAMOUR
        "#fd79a8",  # PICO-8 PINK
        "#636e72",  # AMERICAN RIVER
    ),  # Credit: flatuicolors.com
    "us_dark": (
        "#00b894",  # MINT LEAF
        "#00cec9",  # ROBIN'S EGG BLUE
        "#0984e3",  # ELECTRON BLUE
        "#6c5ce7",  # EXODUS FRUIT
        "#b2bec3",  # SOOTHING BREEZE
        "#fdcb6e",  # BRIGHT YARROW
        "#e17055",  # ORANGEVILLE
        "#d63031",  # CHI-GONG
        "#e84393",  # PRUNUS AVIUM
        "#2d3436",  # DRACULA ORCHID
    ),  # Credit: flatuicolors.com
    "au": (
        "#f6e58d",  # BEEKEEPER
        "#ffbe76",  # SPICED NECTARINE
        "#ff7979",  # PINK GLAMOUR
        "#badc58",  # JUNE BUD
        "#dff9fb",  # COASTAL BREEZE
        "#7ed6df",  # MIDDLE BLUE
        "#e056fd",  # HELIOTROPE
        "#686de0",  # EXODUS FRUIT
        "#30336b",  # DEEP KOAMARU
        "#95afc0",  # SOARING EAGLE
    ),  # Credit: flatuicolors.com
    "au_dark": (
        "#f9ca24",  # TURBO
        "#f0932b",  # QUINCE JELLY
        "#eb4d4b",  # CARMINE PINK
        "#6ab04c",  # PURE APPLE
        "#c7ecee",  # HINT OF ICE PACK
        "#22a6b3",  # GREENLAND GREEN
        "#be2edd",  # STEEL PINK
        "#4834d4",  # BLURPLE
        "#130f40",  # DEEP COVE
        "#535c68",  # WIZARD GREY
    ),  # Credit: flatuicolors.com
    "gb": (
        "#00a8ff",  # PROTOSS PYLON
        "#9c88ff",  # PERIWINKLE
        "#fbc531",  # RISE-N-SHINE
        "#4cd137",  # DOWNLOAD PROGRESS
        "#487eb0",  # SEABROOK
        "#e84118",  # NASTURCIAN FLOWER
        "#f5f6fa",  # LYNX WHITE
        "#7f8fa6",  # BLUEBERRY SODA
        "#273c75",  # MAZARINE BLUE
        "#353b48",  # BLUE NIGHTS
    ),  # Credit: flatuicolors.com
    "gb_dark": (
        "#0097e6",  # VANADYL BLUE
        "#8c7ae6",  # MATT PURPLE
        "#e1b12c",  # NANOHANACHA GOLD
        "#44bd32",  # SKIRRET GREEN
        "#40739e",  # NAVAL
        "#c23616",  # HARLEY DAVIDSON ORANGE
        "#dcdde1",  # HINT OF PENSIVE
        "#718093",  # CHAIN GANG GREY
        "#192a56",  # PICO VOID
        "#2f3640",  # ELECTROMAGNETIC
    ),  # Credit: flatuicolors.com
    "ca": (
        "#ff9ff3",  # JIGGLYPUFF
        "#feca57",  # CASANDORA YELLOW
        "#ff6b6b",  # PASTEL RED
        "#48dbfb",  # MEGAMAN
        "#1dd1a1",  # WILD CARIBBEAN GREEN
        "#00d2d3",  # JADE DUST
        "#54a0ff",  # JOUST BLUE
        "#5f27cd",  # NASU PURPLE
        "#c8d6e5",  # LIGHT BLUE BALLERINA
        "#576574",  # FUEL TOWN
    ),  # Credit: flatuicolors.com
    "ca_dark": (
        "#f368e0",  # LIÁN HÓNG LOTUS PINK
        "#ff9f43",  # DOUBLE DRAGON SKIN
        "#ee5253",  # AMOUR
        "#0abde3",  # CYANITE
        "#10ac84",  # DARK MOUNTAIN MEADOW
        "#01a3a4",  # AQUA VELVET
        "#2e86de",  # BLEU DE FRANCE
        "#341f97",  # BLUEBELL
        "#8395a7",  # STORM PETREL
        "#222f3e",  # IMPERIAL PRIMER
    ),  # Credit: flatuicolors.com
    "cn": (
        "#eccc68",  # GOLDEN SAND
        "#ff7f50",  # CORAL
        "#ff6b81",  # WILD WATERMELON
        "#a4b0be",  # PEACE
        "#57606f",  # GRISAILLE
        "#7bed9f",  # LIME SOAP
        "#70a1ff",  # FRENCH SKY BLUE
        "#5352ed",  # SATURATED SKY
        "#ffffff",  # WHITE
        "#dfe4ea",  # CITY LIGHTS
    ),  # Credit: flatuicolors.com
    "cn_dark": (
        "#ffa502",  # ORANGE
        "#ff6348",  # BRUSCHETTA TOMATO
        "#ff4757",  # WATERMELON
        "#747d8c",  # BAY WHARF
        "#2f3542",  # PRESTIGE BLUE
        "#2ed573",  # UFO GREEN
        "#1e90ff",  # CLEAR CHILL
        "#3742fa",  # BRIGHT GREEK
        "#f1f2f6",  # ANTI-FLASH WHITE
        "#ced6e0",  # TWINKLE BLUE
    ),  # Credit: flatuicolors.com
    "nl": (
        "#ffc312",  # SUNFLOWER
        "#c4e538",  # ENERGOS
        "#12cbc4",  # BLUE MARTINA
        "#fda7df",  # LAVENDER ROSE
        "#ed4c67",  # BARA RED
        "#ee5a24",  # PUFFINS BILL
        "#009432",  # PIXELATED GRASS
        "#0652dd",  # MERCHANT MARINE BLUE
        "#9980fa",  # FORGOTTEN PURPLE
        "#833471",  # HOLLYHOCK
    ),  # Credit: flatuicolors.com
    "nl_dark": (
        "#f79f1f",  # RADIANT YELLOW
        "#a3cb38",  # ANDROID GREEN
        "#1289a7",  # MEDITERRANEAN SEA
        "#d980fa",  # LAVENDER TEA
        "#b53471",  # VERY BERRY
        "#ea2027",  # RED PIGMENT
        "#006266",  # TURKISH AQUA
        "#1b1464",  # 20000 LEAGUES UNDER THE SEA
        "#5758bb",  # CIRCUMORBITAL RING
        "#6f1e51",  # MAGENTA PURPLE
    ),  # Credit: flatuicolors.com
    "fr": (
        "#fad390",  # FLAT FLESH
        "#f8c291",  # MELON MELODY
        "#6a89cc",  # LIVID
        "#82ccdd",  # SPRAY
        "#b8e994",  # PARADISE GREEN
        "#fa983a",  # ICELAND POPPY
        "#eb2f06",  # TOMATO RED
        "#1e3799",  # YUÈ GUĀNG LÁN BLUE
        "#3c6382",  # GOOD SAMARITAN
        "#38ada9",  # WATERFALL
    ),  # Credit: flatuicolors.com
    "fr_dark": (
        "#f6b93b",  # SQUASH BLOSSOM
        "#e55039",  # MANDARIN RED
        "#4a69bd",  # AZRAQ BLUE
        "#60a3bc",  # DUPAIN
        "#78e08f",  # AURORA GREEN
        "#e58e26",  # CARROT ORANGE
        "#b71540",  # JALAPENO RED
        "#0c2461",  # DARK SAPPHIRE
        "#0a3d62",  # FOREST BLUES
        "#079992",  # REEF ENCOUNTER
    ),  # Credit: flatuicolors.com
    "de": (
        "#fc5c65",  # FUSION RED
        "#fd9644",  # ORANGE HIBISCUS
        "#fed330",  # FLIRTATIOUS
        "#26de81",  # REPTILE GREEN
        "#2bcbba",  # MAXIMUM BLUE GREEN
        "#45aaf2",  # HIGH BLUE
        "#4b7bec",  # C64 NTSC
        "#a55eea",  # LIGHTER PURPLE
        "#d1d8e0",  # TWINKLE BLUE
        "#778ca3",  # BLUE GREY
    ),  # Credit: flatuicolors.com
    "de_dark": (
        "#eb3b5a",  # DESIRE
        "#fa8231",  # BENIUKON BRONZE
        "#f7b731",  # NYC TAXI
        "#20bf6b",  # ALGAL FUEL
        "#0fb9b1",  # TURQUOISE TOPAZ
        "#2d98da",  # BOYZONE
        "#3867d6",  # ROYAL BLUE
        "#8854d0",  # GLOOMY PURPLE
        "#a5b1c2",  # INNUENDO
        "#4b6584",  # BLUE HORIZON
    ),  # Credit: flatuicolors.com
    "in": (
        "#fea47f",  # ORCHID ORANGE
        "#25ccf7",  # SPIRO DISCO BALL
        "#eab543",  # HONEY GLOW
        "#55e6c1",  # SWEET GARDEN
        "#cad3c8",  # FALLING STAR
        "#b33771",  # FIERY FUCHSIA
        "#3b3b98",  # BLUEBELL
        "#fd7272",  # GEORGIA PEACH
        "#9aecdb",  # OASIS STREAM
        "#d6a2e8",  # BRIGHT UBE
    ),  # Credit: flatuicolors.com
    "in_dark": (
        "#f97f51",  # RICH GARDENIA
        "#1b9cfc",  # CLEAR CHILL
        "#f8efba",  # SARAWAK WHITE PEPPER
        "#58b19f",  # KEPPEL
        "#2c3a47",  # SHIP'S OFFICER
        "#6d214f",  # MAGENTA PURPLE
        "#182c61",  # ENDING NAVY BLUE
        "#fc427b",  # SASQUATCH SOCKS
        "#bdc581",  # PINE GLADE
        "#82589f",  # HIGHLIGHTER LAVENDER
    ),  # Credit: flatuicolors.com
    "ru": (
        "#f3a683",  # CREAMY PEACH
        "#f7d794",  # ROSY HIGHLIGHT
        "#778beb",  # SOFT BLUE
        "#e77f67",  # BREWED MUSTARD
        "#cf6a87",  # OLD GERANIUM
        "#786fa6",  # PURPLE MOUNTAIN MAJESTY
        "#f8a5c2",  # ROGUE PINK
        "#63cdda",  # SQUEAKY
        "#ea8685",  # APPLE VALLEY
        "#596275",  # PENCIL LEAD
    ),  # Credit: flatuicolors.com
    "ru_dark": (
        "#f19066",  # SAWTOOTH AAK
        "#f5cd79",  # SUMMERTIME
        "#546de5",  # CORNFLOWER
        "#e15f41",  # TIGERLILY
        "#c44569",  # DEEP ROSE
        "#574b90",  # PURPLE CORALLITE
        "#f78fb3",  # FLAMINGO PINK
        "#3dc1d3",  # BLUE CURACAO
        "#e66767",  # PORCELAIN ROSE
        "#303952",  # BISCAY
    ),  # Credit: flatuicolors.com
    "es": (
        "#40407a",  # JACKSONS PURPLE
        "#706fd3",  # C64 PURPLE
        "#f7f1e3",  # SWAN WHITE
        "#34ace0",  # SUMMER SKY
        "#33d9b2",  # CELESTIAL GREEN
        "#ff5252",  # FLUORESCENT RED
        "#ff793f",  # SYNTHETIC PUMPKIN
        "#d1ccc0",  # CROCODILE TOOTH
        "#ffb142",  # MANDARIN SORBET
        "#ffda79",  # SPICED BUTTERNUT
    ),  # Credit: flatuicolors.com
    "es_dark": (
        "#2c2c54",  # LUCKY POINT
        "#474787",  # LIBERTY
        "#aaa69d",  # HOT STONE
        "#227093",  # DEVIL BLUE
        "#218c74",  # PALM SPRINGS SPLASH
        "#b33939",  # EYE OF NEWT
        "#cd6133",  # CHILEAN FIRE
        "#84817a",  # GREY PORCELAIN
        "#cc8e35",  # ALAMEDA OCHRE
        "#ccae62",  # DESERT
    ),  # Credit: flatuicolors.com
    "se": (
        "#ef5777",  # HIGHLIGHTER PINK
        "#575fcf",  # DARK PERIWINKLE
        "#4bcffa",  # MEGAMAN
        "#34e7e4",  # FRESH TURQUOISE
        "#0be881",  # MINTY GREEN
        "#ffc048",  # NÂRENJI ORANGE
        "#ffdd59",  # YRIEL YELLOW
        "#ff5e57",  # SUNSET ORANGE
        "#d2dae2",  # HINT OF ELUSIVE BLUE
        "#485460",  # GOOD NIGHT!
    ),  # Credit: flatuicolors.com
    "se_dark": (
        "#f53b57",  # SIZZLING RED
        "#3c40c6",  # FREE SPEECH BLUE
        "#0fbcf9",  # SPIRO DISCO BALL
        "#00d8d6",  # JADE DUST
        "#05c46b",  # GREEN TEAL
        "#ffa801",  # CHROME YELLOW
        "#ffd32a",  # VIBRANT YELLOW
        "#ff3f34",  # RED ORANGE
        "#808e9b",  # LONDON SQUARE
        "#1e272e",  # BLACK PEARL
    ),  # Credit: flatuicolors.com
    "tr": (
        "#cd84f1",  # BRIGHT LILAC
        "#ffcccc",  # PRETTY PLEASE
        "#ff4d4d",  # LIGHT RED
        "#ffaf40",  # MANDARIN SORBET
        "#fffa65",  # UNMELLOW YELLOW
        "#32ff7e",  # WINTERGREEN
        "#7efff5",  # ELECTRIC BLUE
        "#18dcff",  # NEON BLUE
        "#7d5fff",  # LIGHT SLATE BLUE
        "#4b4b4b",  # SHADOWED STEEL
    ),  # Credit: flatuicolors.com
    "tr_dark": (
        "#c56cf0",  # LIGHT PURPLE
        "#ffb8b8",  # YOUNG SALMON
        "#ff3838",  # RED ORANGE
        "#ff9f1a",  # RADIANT YELLOW
        "#fff200",  # DORN YELLOW
        "#3ae374",  # WEIRD GREEN
        "#67e6dc",  # HAMMAM BLUE
        "#17c0eb",  # SPIRO DISCO BALL
        "#7158e2",  # LIGHT INDIGO
        "#3d3d3d",  # BALTIC SEA
    ),  # Credit: flatuicolors.com
    "qtb_5a": (
        "#00A287",  # Türkis
        "#A600A6",  # Lila
        "#FA569B",  # Rosa
        "#FF9200",  # Orange
        "#9B9B9B",  # Hellgrau
    ),
    "qtb_5b": (
        "#6740E3",  # Blau
        "#E93D3D",  # Rot
        "#FFE100",  # Gelb
        "#00CC00",  # Grün
        "#9B9B9B",  # Hellgrau
    ),
    "qtb_10": (
        "#6740E3",  # Blau
        "#E93D3D",  # Rot
        "#FFE100",  # Gelb
        "#00CC00",  # Grün
        "#9B9B9B",  # Hellgrau
        "#A600A6",  # Lila
        "#FF9200",  # Orange
        "#FA569B",  # Rosa
        "#00A287",  # Türkis
        "#6A6A6A",  # Dunkelgrau
    ),
}
