chinese = set(
    [
        "chinese", "chineses", "china", "chen", "chow", "mein", "kung", "pao",
        "hong", "kong"
        "tsos", "teryaki", "hunan", "szechuan", "taiwan", "taiwanese", "udon",
        "dumpling", "poke", "boba"
    ]
)
japanese = set(
    [
        "japanese", "sushi", "sashimi", "yakitori", "tapas", "teryaki", "unagi",
        "sukiyaki", "nobu", "anime", "katsu", "japonaise"
    ]
)
vietnamese = set(["vietnamese", "pho", "banh", "mi"])
thai = set(
    ["thai", "panang", "curry", "satai", "satay", "kha", "pad", "bangkok"]
)
hawaiian = set(["hawaiian", "ohana", "mahalo", "kalua", "poke"])
american = set(
    [
        "steakhouse", "boston", "burger", "burgers", "pizza", "chips",
        "sandwich", "sandwiches", "cordon", "bleu", "steak", "ribeye", "mignon",
        "eggs", "benedict", "omlette", "toast", "buffalo", "bbq", "wings",
        "maggianos", "beer", "meatballs", "americana", "sausage", "latte",
        "cajun", "jazz", "waffles", "coffee", "starbucks", "deli", "irish",
        "sundae", "frozen", "cream", "yogurt, cheesecake", "beignets"
    ]
)
french = set(["french", "crepe", "omlette", "baguette", "Paris"])
greek = set(["greek", "spanakopita"])
italian = set(
    [
        "italian", "pasta", "ravioli", "pizza", "fettuccine", "fries",
        "maggianos", "italy", "spaghetti", "meatballs"
    ]
)
mexican = set(
    [
        "mexican", "burrito", "taco", "tacos", "enchillida", "quesidilla",
        "queso", "nacho", "nachos", "tortilla", "asada", "pollo", "comida",
        "mexicana", "salsa"
    ]
)
spanish = set(["spanish"])
cuban = set(["cuban", "cubano"])
moroccan = set(["moroccan"])
indian = set(
    [
        "indian", "india", "curry", "naan", "dosa", "masala", "biryani", "puri",
        "tandoori", "paneer", "tikka", "idlee", "chutney", "madras", "hyderbad",
        "cumin", "chana", "punjabi", "gujurati", "thali"
    ]
)
middle_eastern = set(
    [
        "persian", "lebanese", "kebab", "kabob", "kebob", "kabab", "kebob",
        "shish", "gyro", "shwarma", "shawarma", "zereshk", 'halal', "hummus",
        "syrian", "israel", "israeli"
    ]
)
salon = set(
    ["barber", "salon", "hair", "hairdresser", "trim", "nails", "manicure"]
)
medical = set(
    [
        "optical", "optometrist", "pharmacy", "eye", "eyes", "doctor", "dental",
        "dentist", "prescription", "chiro", "chiropractor", "dermatology",
        "dermatologist", "skincare", "dr"
    ]
)
hotel = set(["hotel", "room", "bed", "bedroom", "lobby", "inn"])
bar = set(
    [
        "beer", "beers", "liquour", "liquours"
        "dance", "stage", "bar", "pool", "billiards", "game", "sports",
        "stand-up", "comedian", "clubbing", "club", "pub", "party", "rum",
        "whiskey", "scotch"
    ]
)
store = set(
    [
        "bookstore", "store", "shop", "gift", "comics", "gear", "shoe",
        "warehouse", "CD", "CDs", "CD's"
        "labels", "accessories", "costume", "grocery", "produce"
    ]
)
zoo = set(
    [
        "zoo", "seaword", "giraffe", "animals", "wildlife", "safari", "exhibit",
        "museum"
    ]
)

cheap = set(["cheap", "inexpensive", "affordable", "dingy", "bargain"])
expensive = set(["expensive", "pricey", "ripoff", "upscale", "fancy"])
unclassified = set([])

segment_keywords_map = {
    "chinese": chinese,
    "japanese": japanese,
    "vietnamese": vietnamese,
    "thai": thai,
    "hawaiian": hawaiian,
    "american": american,
    "french": french,
    "greek": greek,
    "italian": italian,
    "mexican": mexican,
    "spanish": spanish,
    "cuban": cuban,
    "moroccan": moroccan,
    "indian": indian,
    "middle_eastern": middle_eastern,
    "salon": salon,
    "medical": medical,
    "hotel": hotel,
    "bar": bar,
    "store": store,
    "zoo": zoo,
    "unclassified": unclassified,
}

segment_name_to_id_map = {
    "chinese": 0,
    "japanese": 1,
    "vietnamese": 2,
    "thai": 3,
    "hawaiian": 4,
    "american": 5,
    "french": 6,
    "greek": 7,
    "italian": 8,
    "mexican": 9,
    "spanish": 10,
    "cuban": 11,
    "moroccan": 12,
    "indian": 13,
    "middle_eastern": 14,
    "salon": 15,
    "medical": 16,
    "hotel": 17,
    "bar": 18,
    "store": 19,
    "zoo": 20,
    "unclassified": 21,
}

positive_group = [3, 4]
