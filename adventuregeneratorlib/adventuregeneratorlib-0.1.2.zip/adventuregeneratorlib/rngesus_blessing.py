from random import randint, choice, shuffle

trinket = [
    'mummified goblin hand',
    'piece of crystal that faintly glows in the moonlight',
    'gold coin minted in an unknown land'
    'diary written in a language you don’t know',
    'brass ring that never tarnishes',
    'old chess piece made from glass',
    'pair of knucklebone dice, each with a skull symbol on the side that would normally show six pips',
    'small idol depicting a nightmarish creature that gives you unsettling dreams when you sleep near it',
    'rope necklace from which dangles four mummified elf fingers',
    'deed for a parcel of land in a realm unknown to you',
    '1-ounce block made from an unknown material',
    'small cloth doll skewered with needles',
    'tooth from an unknown beast',
    'enormous scale, perhaps from a dragon',
    'bright green feather',
    'old divination card bearing your likeness',
    'glass orb filled with moving smoke',
    '1-pound egg with a bright red shell',
    'pipe that blows bubbles',
    'glass jar containing a weird bit of flesh floating in pickling fluid',
    'tiny gnome-crafted music box that plays a song you dimly remember from your childhood',
    'small wooden statuette of a smug halfling',
    'brass orb etched with strange runes',
    'multicolored stone disk',
    'tiny silver icon of a raven',
    'bag containing forty-seven humanoid teeth, one of which is rotten',
    'shard of obsidian that always feels warm to the touch',
    'dragon`s bony talon hanging from a plain leather necklace',
    'pair of old socks',
    'blank book whose pages refuse to hold ink, chalk, graphite, or any other substance or marking',
    'silver badge in the shape of a five-pointed star',
    'knife that belonged to a relative',
    'glass vial filled with nail clippings',
    'rectangular metal device with two tiny metal cups on one end that throws sparks when wet',
    'white, sequined glove sized for a human',
    'vest with one hundred tiny pockets',
    'small, weightless stone block',
    'tiny sketch portrait of a goblin',
    'empty glass vial that smells of perfume when opened',
    'gemstone that looks like a lump of coal when examined by anyone but you',
    'scrap of cloth from an old banner',
    'rank insignia from a lost legionnaire',
    'tiny silver bell without a clapper',
    'mechanical canary inside a gnome-crafted lamp',
    'tiny chest carved to look like it has numerous feet on the bottom',
    'dead sprite inside a clear glass bottle',
    'metal can that has no opening but sounds as if it is filled with liquid',
    'glass orb filled with water, in which swims a clockwork goldfish',
    'silver spoon with an M engraved on the handle',
    'whistle made from gold-colored wood',
    'dead scarab beetle the size of your hand',
    'two toy soldiers, one with a missing head',
    'small box filled with different-sized buttons',
    'candle that can’t be lit',
    'tiny cage with no door',
    'old key',
    'indecipherable treasure map',
    'hilt from a broken sword',
    'rabbit’s foot',
    'glass eye',
    'cameo carved in the likeness of a hideous person'
    'silver skull the size of a coin',
    'alabaster mask',
    'pyramid of sticky black incense that smells very bad',
    'nightcap that, when worn, gives you pleasant dreams',
    'single caltrop made from bone',
    'gold monocle frame without the lens',
    '1-inch cube, each side painted a different color',
    'crystal knob from a door',
    'small packet filled with pink dust',
    'fragment of a beautiful song, written as musical notes on two pieces of parchment',
    'silver teardrop earring made from a real teardrop',
    'shell of an egg painted with scenes of human misery in disturbing detail',
    'fan that, when unfolded, shows a sleeping cat',
    'set of bone pipes',
    'four-leaf clover pressed inside a book discussing manners and etiquette',
    'sheet of parchment upon which is drawn a complex mechanical contraption',
    'ornate scabbard that fits no blade you have found so far',
    'invitation to a party where a murder happened',
    'bronze pentacle with an etching of a rat`s head in its center',
    'purple handkerchief embroidered with the name of a powerful archmage',
    'Half of a floorplan for a temple',
    'bit of folded cloth that, when unfolded, turns into a stylish cap',
    'receipt of deposit at a bank in a far-flung city',
    'diary with seven missing pages',
    'empty silver snuffbox bearing an inscription on the surface that says "dreams"',
    'iron holy symbol devoted to an unknown god',
    'book that tells the story of a legendary hero`s rise and fall, with the last chapter missing',
    'vial of dragon blood',
    'ancient arrow of elven design',
    'needle that never bends',
    'ornate brooch of dwarven design',
    'empty wine bottle bearing a pretty label that says, "The Wizard of Wines Winery, Red Dragon Crush, 331422-W"',
    'mosaic tile with a multicolored, glazed surface',
    'petrified mouse',
    'black pirate flag adorned with a dragon`s skull and crossbones',
    'tiny mechanical crab or spider that moves about when it’s not being observed',
    'glass jar containing lard with a label that reads, "Griffon Grease"',
    'wooden box with a ceramic bottom that holds a living worm with a head on each end of its body',
    'metal urn containing the ashes of a hero',
]

firstName = [
    'William', 'Tom', 'Balrus', 'Fabien', 'Malfas', 'Norok', 'Vyn', 'Zarek',
    'Ulfgar', 'Alva', 'Aryn', 'Brina', 'Caelin', 'Dorath', 'Freya', 'Kyla',
    'Lavina', 'Vasha', 'Gandor', 'Shadoras', 'Zynthasius', 'Darcossan',
    'Faelor', 'Nesterin', 'Usandaar', 'Azariah', 'Narbeth', 'Dagurt', 'Borden',
    'Gusak', 'Toki', 'Vuggar', 'Devella', 'Pondral', 'Zika', 'Robin', 'Henrik',
    'Quintin', 'Emmory', 'Cathleen', 'Veronia', 'Grenten', 'Wilford',
    'Crandle', 'Gerald', 'Ludwig', 'Luis', 'Quinn', 'Velector', 'Jennica',
    'Halford', 'Cristoff', 'Lisbeth', 'Gregor', 'Gregorious', 'Sam', 'Edwinn',
    'Claude', 'Alex', 'Siggurd', 'Linn', 'Tandor', 'Hector', 'Vander', 'Luna',
    'Valda', 'Ivery', 'Deon', 'Lorel', 'Gaby', 'Akibrus', 'Angun', 'Balrus',
    'Bulruk', 'Caldor', 'Dagon', 'Darvyn', 'Delvin', 'Dracyian', 'Dray',
    'Eldar', 'Engar', 'Fabien', 'Farkas', 'Galdor', 'Igor', 'Klayden',
    'Laimus', 'Malfas', 'Norok', 'Orion', 'Quintus', 'Rammir', 'Remus',
    'Rorik', 'Sabir', 'Sirius', 'Soril', 'Sulfu', 'Syfas', 'Viktas', 'Vyn',
    'Wilkass', 'Yagul', 'Zakkas', 'Zarek', 'Zorion', 'Aleera', 'Alva', 'Amara',
    'Anya', 'Asralyn', 'Azura', 'Breya', 'Brina', 'Caelia', 'Ciscra', 'Dorath',
    'Drusila', 'Elda', 'Esmeralda', 'Freya', 'Gelda', 'Hadena', 'Kyla', 'Kyra',
    'Lavinia', 'Lyra', 'Mireille', 'Nyssa', 'Olwyn', 'Reyda', 'Sarielle',
    'Shikta', 'Sybella', 'Syfyn', 'Thalia', 'Turilla', 'Vasha', 'Vixen',
    'Yvanna', 'Zaria', 'Zeniya', 'Leolona', 'Idona', 'Acalia', 'Evara',
    'Acandra', 'Yolatha', 'Elerria', 'Adothea', 'Eudia', 'Acanie', 'Limeda',
    'Diora', 'Banthea', 'Liphne', 'Cherena', 'Bania', 'Damalena', 'Anadora',
    'Jarena', 'Fesima', 'Zatria', 'Maemona', 'Chephine', 'Noal', 'Stana',
    'Laorn', 'Haguk', 'Zee', 'Qorith', 'Bakot', 'Bara', 'Barin', 'Krorta',
    'Ruarpo', 'Kaly', 'Deneol', 'Yodas', 'Donda', 'Kreget', 'Larrid', 'Mesad',
    'Rittap', 'Rillap', 'Gizzand', 'Borlon', 'Ginnole', 'Rogrit', 'Golat',
    'Marreli', 'Ana', 'Zaness', 'Mannan', 'Xesi', 'Ualin', 'Mirri', 'Bim',
    'Evrar', 'Secoh', 'Kudrac', 'Raster', 'Leknen', 'Zamras', 'Nugdith',
    'Cadral', 'Bukt', 'Coot', 'Ragan', 'Brac', 'Curdool', 'Laguth', 'Rakril',
    'Hovon', 'Ezon', 'Zorem', 'Gubil', 'Kegen', 'Kaden', 'Amad', 'Arel',
    'Helin', 'Edil', 'Zolan', 'Dalne', 'Sogen', 'Hugne', 'Tanmo', 'Soged',
    'Dorle', 'Hozer', 'Gamer', 'Donla', 'Siesq', 'Sholir', 'Drib', 'Turim',
    'Sobat', 'Thafir', 'Radeul', 'Forkis', 'Robert', 'Ferkier', 'Reuben',
    'Masoon', 'Adur', 'Amob', 'Amen', 'Saked', 'Mamdi', 'Idras', 'Obayl',
    'Chibor', 'Choggo', 'Kussal', 'Tikhon', 'Pyotr', 'Matho', 'Theresa',
    'Bluntud', 'Hermina', 'Ethel', 'Tolad', 'Horatius', 'Lorraine', 'Blalad',
    'Adranos', 'Regina', 'Escul', 'Lydia', 'Uherec', 'Verus', 'Winifred',
    'Lorraine', 'Adehu', 'Edith', 'Cranus', 'Zeeal', 'Supine', 'Elmar',
    'Hsonkac', 'Rhinni', 'Hastol', 'Visedi', 'Rysdant', 'Cussal', 'Zirqo',
    'Hezzo', 'Drarlo', 'Stonky', 'Akra', 'Antrara', 'Arava', 'Biri',
    'Blendaeth', 'Burana', 'Chassath', 'Daar', 'Doudra', 'Driindar', 'Eggren',
    'Findex', 'Furrele', 'Gilkass', 'Harann', 'Hethress', 'Jaxi', 'Kadana',
    'Jezean', 'Jheri', 'Kava', 'Korinn', 'Megren', 'Mijira', 'Mishann', 'Nala',
    'Nuthra', 'Perra', 'Pyxrin', 'Quespa', 'Raiann', 'Rezena', 'Ruloth',
    'Saphara', 'Savaran', 'Sora', 'Surina', 'Synthrin', 'Tatyan', 'Uadjit',
    'Vezera', 'Zykroff', 'Adrex', 'Arjhan', 'Azzakh', 'Balasar', 'Baradad',
    'Bharash', 'Dadalan', 'Dazzazn', 'Donaar', 'Fax', 'Gargax', 'Ghesh',
    'Heskan', 'Ildrex', 'Kaladan', 'Kiirith', 'Kriv', 'Maagog', 'Medrash',
    'Mehen', 'Mreksh', 'Nadarr', 'Nither', 'Nykkan', 'Pandjed', 'Patrin',
    'Pijrik', 'Rhogar', 'Rivaan', 'Shedinn', 'Tarhun', 'Torinn', 'Zedaar',
    'Anbera', 'Artin', 'Audhil', 'Balifra', 'Barbena', 'Bardryn', 'Bolhild',
    'Dagnal', 'Dariff', 'Delre', 'Diesa', 'Eldeth', 'Eridred', 'Falkrunn',
    'Gillydd', 'Gurdis', 'Helgret', 'Helja', 'Hlin', 'Ilde', 'Jarana',
    'Kathra', 'Kilia', 'Morana', 'Nalead', 'Nora', 'Oriff', 'Ovina', 'Riswynn',
    'Sannl', 'Torgga', 'Urshar', 'Valida', 'Vistra', 'Werydd', 'Adrik',
    'Baern', 'Barendd', 'Brottor', 'Dain', 'Dalgal', 'Darrak', 'Delg',
    'Dworic', 'Eberk', 'Einkil', 'Elaim', 'Erias', 'Fallond', 'Fargrim',
    'Gardain', 'Gilthur', 'Gimgen', 'Gimurt', 'Harbek', 'Kildrak', 'Kilvar',
    'Morgran', 'Morkral', 'Nalrak', 'Nordak', 'Olunt', 'Orsik', 'Oskar',
    'Rangrim', 'Reirak', 'Rurik', 'Thorin', 'Tordek', 'Travok', 'Ulfgar',
    'Uraim', 'Veit', 'Vonbin', 'Vondal', 'Mara', 'Naeris', 'Syllin', 'Koeth',
    'Bryn', 'Traki', 'Sumi', 'Adrie', 'Althaea', 'Arara', 'Birel', 'Caelynn',
    'Chaedi', 'Claira', 'Dara', 'Elama', 'Enna', 'Faral', 'Hatae', 'Ilanis',
    'Irann', 'Jarsali', 'Keyleth', 'Lia', 'Malquis', 'Mialee', 'Sariel',
    'Shava', 'Sumnes', 'Thiala', 'Traulam', 'Valna', 'Adran', 'Aelar',
    'Ahvain', 'Arannis', 'Aust', 'Azaki', 'Beiro', 'Berrian', 'Carric',
    'Dreali', 'Erdan', 'Fivin', 'Gennal', 'Heian', 'Himo', 'Laucian', 'Lucan',
    'Naal', 'Peren', 'Rolen', 'Thervan', 'Varis', 'Breena', 'Buvie', 'Cally',
    'Caramip', 'Carlin', 'Cumpen', 'Donella', 'Ella', 'Enidda', 'Lilli',
    'Lorilla', 'Luthra', 'Mardnab', 'Meena', 'Menny', 'Nissa', 'Numba', 'Nyx',
    'Oda', 'Oppah', 'Orla', 'Pyntle', 'Quilla', 'Roywyn', 'Shamil', 'Siffres',
    'Symma', 'Tana', 'Tenea', 'Stibble', 'Ulla', 'Unerva', 'Virra', 'Yebe',
    'Zanna', 'Alston', 'Alvyn', 'Anvert', 'Bilbron', 'Brocc', 'Brox',
    'Burgell', 'Cockaby', 'Dimble', 'Pimble', 'Stimble', 'Eldon', 'Erky',
    'Fablen', 'Fonkin', 'Frouse', 'Frug', 'Gerbo', 'Gimble', 'Glim', 'Igden',
    'Jabble', 'Kellen', 'Kipper', 'Orryn', 'Paggen', 'Pakka', 'Pog', 'Qualen',
    'Ribbles', 'Roondar', 'Sapply', 'Seebo', 'Senteq', 'Sindri', 'Umpen',
    'Warryn', 'Wigg', 'Wobbles', 'Wrenn', 'Zaffrab', 'Zook', 'Alain', 'Andry',
    'Anne', 'Bella', 'Bree', 'Callie', 'Chenna', 'Cora', 'Dee', 'Dell', 'Eida',
    'Eran', 'Georgina', 'Gynnie', 'Harriet', 'Jasmine', 'Jillian', 'Jo',
    'Kithri', 'Lavina', 'Lidda', 'Maegan', 'Marigold', 'Merla', 'Myria',
    'Nedda', 'Nikki', 'Nora', 'Olivia', 'Paela', 'Pearl', 'Olive', 'Pennie',
    'Portia', 'Robbie', 'Rose', 'Saral', 'Shaena', 'Stacee', 'Tawna', 'Thea',
    'Trym', 'Tyna', 'Vani', 'Verna', 'Wella', 'Willow', 'Alton', 'Ander',
    'Bernie', 'Bobbin', 'Cade', 'Callus', 'Corrin', 'Dannad', 'Danniel',
    'Eddie', 'Egart', 'Eldon', 'Errich', 'Fildo', 'Finnan', 'Franklin',
    'Garret', 'Garth', 'Garth', 'Gilbert', 'Gob', 'Harol', 'Igor', 'Jasper',
    'Keith', 'Kevin', 'Lazam', 'Lerry', 'Lindal', 'Lyle', 'Merric', 'Mican',
    'Milo', 'Morrin', 'Nebin', 'Nevil', 'Osborn', 'Ostran', 'Oswalt', 'Perrin',
    'Poppy', 'Reed', 'Roscoe', 'Sam', 'Shardon', 'Tye', 'Ulmo', 'Wellby',
    'Wendel', 'Wenner', 'Wes', 'Arha', 'Baggi', 'Bendoo', 'Bilga', 'Brakka',
    'Creega', 'Drenna', 'Ekk', 'Emen', 'Engong', 'Fistula', 'Gaaki', 'Gorga',
    'Grai', 'Greeba', 'Grigi', 'Gynk', 'Hrathy', 'Huru', 'Ilga', 'Kabbarg',
    'Kansif', 'Lagazi', 'Lezre', 'Murgen', 'Murook', 'Myev', 'Nagrette',
    'Neega', 'Nella', 'Nogu', 'Oolah', 'Ootah', 'Ovak', 'Ownka', 'Puyet',
    'Reeza', 'Shautha', 'Silgre', 'Sutha', 'Tagga', 'Tawar', 'Tomph', 'Ubada',
    'Vanchu', 'Vola', 'Volen', 'Vorka', 'Yevelda', 'Zagga', 'Argran', 'Braak',
    'Brug', 'Cagak', 'Dench', 'Dorn', 'Dren', 'Druuk', 'Feng', 'Gell',
    'Gnarsh', 'Grumbar', 'Gubrash', 'Hagren', 'Henk', 'Hogar', 'Holg', 'Imsh',
    'Karash', 'Karg', 'Keth', 'Korag', 'Krusk', 'Lubash', 'Megged', 'Mhurren',
    'Mord', 'Morg', 'Nil', 'Nybarg', 'Odorr', 'Ohr', 'Rendar', 'Resh', 'Ront',
    'Rrath', 'Sark', 'Scrag', 'Sheggen', 'Shump', 'Tanglar', 'Tarak', 'Thar',
    'Thokk', 'Trag', 'Ugarth', 'Varg', 'Vilberg', 'Yurk', 'Zed', 'Akta',
    'Anakis', 'Aym', 'Azza', 'Beleth', 'Bryseis', 'Bune', 'Criella', 'Ea',
    'Gadreel', 'Hecat', 'Ishte', 'Kali', 'Lilith', 'Manea', 'Naamah', 'Nija',
    'Osah', 'Purah', 'Rieta', 'Ronwe', 'Seddit', 'Seere', 'Shava', 'Shax',
    'Sorath', 'Uzza', 'Vepar', 'Verin', 'Abad', 'Ahrim', 'Akmen', 'Amnon',
    'Andram', 'Astar', 'Balam', 'Bathin', 'Caim', 'Chem', 'Cimer', 'Cressel',
    'Euron', 'Fenriz', 'Forcas', 'Habor', 'Iados', 'Kairon', 'Leucis',
    'Mamnen', 'Mantus', 'Marbas', 'Melech', 'Modean', 'Mordai', 'Mormo',
    'Morthos', 'Nicor', 'Nirgel', 'Oriax', 'Paymon', 'Purson', 'Qemuel',
    'Raam', 'Rimmon', 'Sammal', 'Skamos', 'Tethren', 'Thamuz', 'Therei',
    'Xappan', 'Zepar', 'Zephan', 'Aida', 'Alia', 'Amina', 'Chaima', 'Dalia',
    'Ehsan', 'Elham', 'Farah', 'Iesha', 'Inbar', 'Layla', 'Lupe', 'Najwa',
    'Nawra', 'Nuha', 'Nura', 'Oma', 'Qamar', 'Saadia', 'Sabah', 'Sada',
    'Saffron', 'Sahar', 'Salma', 'Shatha', 'Takhira', 'Thana', 'Yadira',
    'Zahra', 'Zaida', 'Zaina', 'Zeinab', 'Abbad', 'Abdul', 'Akeem', 'Alif',
    'Amir', 'Asim', 'Bashir', 'Bassim', 'Fahim', 'Farid', 'Farouk', 'Fazil',
    'Hakim', 'Heydar', 'Jabari', 'Jafar', 'Jahid', 'Jamal', 'Kalim', 'Karlim',
    'Kazim', 'Khadim', 'Khalim', 'Mansour', 'Nadir', 'Nazim', 'Omar', 'Qadir',
    'Qusay', 'Rafiq', 'Rashad', 'Rakim', 'Rauf', 'Sami', 'Samir', 'Talib',
    'Tamir', 'Tariq', 'Yazid', 'Aife', 'Aina', 'Alane', 'Arienh', 'Beatha',
    'Birgit', 'Briann', 'Caomh', 'Cara', 'Cinnia', 'Donia', 'Elsha', 'Enid',
    'Ethne', 'Evelina', 'Fianna', 'Gilda', 'Gitta', 'Grania', 'Keelin',
    'Mavis', 'Mirna', 'Morgan', 'Muriel', 'Selma', 'Ula', 'Wynne', 'Airell',
    'Airic', 'Alan', 'Anghus', 'Aodh', 'Bardon', 'Bevyn', 'Boden', 'Bran',
    'Brasil', 'Bredon', 'Brian', 'Bryant', 'Cadman', 'Cedric', 'Conalt',
    'Condon', 'Darcy', 'Devin', 'Dillion', 'Donall', 'Duer', 'Eghan', 'Ewyn',
    'Ferghus', 'Galvyn', 'Gildas', 'Guy', 'Harvey', 'Iden', 'Irven', 'Karney',
    'Kayne', 'Kelvyn', 'Leigh', 'Maccus', 'Moryn', 'Neale', 'Owyn', 'Reaghan',
    'Turi', 'Ai', 'Bei', 'Caixia', 'Chen', 'Chou', 'Daiyu', 'Die', 'Ge',
    'Hong', 'Huan', 'Jia', 'Jiao', 'Lan', 'Li', 'Lihua', 'Lin', 'Ling', 'Liu',
    'Meili', 'Ning', 'Qi', 'Qiao', 'Rong', 'Shu', 'Song', 'Ting', 'Wen', 'Xia',
    'Xiaoli', 'Xue', 'Ya', 'Yan', 'Ying', 'Yuan', 'Yue', 'Yun', 'Bo', 'Bolin',
    'Chang', 'Chao', 'Chen', 'Cheng', 'Da', 'Fang', 'Feng', 'Fu', 'Gang',
    'Guang', 'Hai', 'Huan', 'Heng', 'Hong', 'Jian', 'Jiayi', 'Kang', 'Lei',
    'Liang', 'Ling', 'Meilin', 'Niu', 'Peng', 'Ping', 'Qiang', 'Qiu', 'Renshu',
    'Rong', 'Ru', 'Shan', 'Shen', 'Wei', 'Yuang', 'Zhong', 'Ahset', 'Amunet',
    'Atet', 'Betrest', 'Dedyet', 'Hentie', 'Herit', 'Ipwet', 'Itet', 'Joba',
    'Kasmut', 'Khemut', 'Kiya', 'Maia', 'Menhet', 'Merit', 'Muyet', 'Nebet',
    'Nit', 'Nofret', 'Pypuy', 'Rai', 'Redji', 'Sadeh', 'Sadek', 'Sitre',
    'Takhat', 'Tarset', 'Akhom', 'Amasis', 'Anen', 'Bek', 'Huya', 'Ibebi',
    'Idu', 'Ineni', 'Irsu', 'Kawab', 'Khafra', 'Nehi', 'Redjek', 'Sabaf',
    'Sebni', 'Thethi', 'Agatha', 'Agnes', 'Alice', 'Aline', 'Anne',
    'Elizabeth', 'Ella', 'Emma', 'Eva', 'Geva', 'Helen', 'Ida', 'Jean', 'Joan',
    'Mary', 'Oriel', 'Sarah', 'Sybil', 'Adam', 'Anselm', 'Arnold', 'Bernard',
    'Bertram', 'Charles', 'Conrad', 'Drogo', 'Gerald', 'Gilbert', 'Godfrey',
    'Gunter', 'Henry', 'Heward', 'Hubert', 'Hough', 'John', 'Lance', 'Manfred',
    'Miles', 'Norman', 'Odo', 'Peter', 'Ralf', 'Raymond', 'Reynard', 'Richard',
    'Robert', 'Roland', 'Rolf', 'Simon', 'Theobald', 'Thomas', 'Timm',
    'William', 'Wymar', 'Aalis', 'Agnez', 'Alips', 'Amée', 'Anne', 'Dorian',
    'Gila', 'Guoite', 'Jehan', 'Margot', 'Marie', 'Maria', 'Ame', 'Andri',
    'Andriet', 'Bernard', 'Charles', 'Charlot', 'Colin', 'Denis', 'Durant',
    'Ernault', 'Ethor', 'Felix', 'Gilles', 'Henry', 'Hugo', 'Imbert', 'Jean',
    'Louis', 'Louys', 'Loys', 'Martin', 'Michel', 'Mille', 'Nicolas', 'Oudart',
    'Perrin', 'Pierre', 'Richart', 'Robert', 'Simon', 'Vincent', 'Affra',
    'Allet', 'Anna', 'Apell', 'Brida', 'Cecilia', 'Clara', 'Ella', 'Els',
    'Elsbeth', 'Engel', 'Eva', 'Fela', 'Geras', 'Guttel', 'Irmel', 'Kuan',
    'Lucia', 'Margret', 'Marlein', 'Martha', 'Reusin', 'Ursel', 'Vrsula',
    'Berthard', 'Allexander', 'Casper', 'Clas', 'Cristin', 'Cristoff', 'Felix',
    'Frantz', 'Fritz', 'Gerhart', 'Hans', 'Hartmann', 'Heintz', 'Herman',
    'Jacob', 'Jorg', 'Karll', 'Kilian', 'Linhart', 'Lorentz', 'Ludwig', 'Marx',
    'Melchor', 'Mertin', 'Michel', 'Moritz', 'Osswald', 'Ott', 'Peter',
    'Rudolff', 'Sigmund', 'Steffan', 'Symon', 'Thoman', 'Ulrich', 'Wendel',
    'Wilhelm', 'Wolff', 'Wolfgang', 'Aella', 'Chloros', 'Daphne', 'Dione',
    'Elektra', 'Euadne', 'Eudora', 'Helene', 'Ianthe', 'Kallisto', 'Karme',
    'Kirke', 'Kleio', 'Klotho', 'Kynthia', 'Leto', 'Niobe', 'Ourania',
    'Phaenna', 'Theia', 'Adonis', 'Aeson', 'Aias', 'Argos', 'Brontes',
    'Deimos', 'Erbos', 'Hektor', 'Heros', 'Iason', 'Kadmos', 'Kastor', 'Koios',
    'Kreios', 'Laios', 'Linos', 'Lykos', 'Mentor', 'Pallas', 'Phricxus',
    'Xantos', 'Alfhild', 'Arnbjorg', 'Ase', 'Alog', 'Astrid', 'Auda', 'Audhid',
    'Bodil', 'Brenna', 'Brynhild', 'Dagmar', 'Erika', 'Eira', 'Gudrun',
    'Helga', 'Hertha', 'Hilde', 'Ingrid', 'Iona', 'Jorunn', 'Kari', 'Kenna',
    'Magnhild', 'Nanna', 'Olga', 'Ragna', 'Ragnhild', 'Runa', 'Saga',
    'Sigfrid', 'Signe', 'Sigrid', 'Sigrunn', 'Solveg', 'Svanhild', 'Thora',
    'Torborg', 'Torunn', 'Tove', 'Unn', 'Vigdis', 'Ylva', 'Yngvild', 'Agni',
    'Asger', 'Asmund', 'Bjarte', 'Bjorg', 'Brandr', 'Brandt', 'Brynjar',
    'Clader', 'Colborn', 'Cuyler', 'Egil', 'Einar', 'Eric', 'Erlnad', 'Fiske',
    'Fritjof', 'Frode', 'Geir', 'Halvar', 'Hemming', 'Hjalmar', 'Hjotr',
    'Ivar', 'Knud', 'Leif', 'Liufr', 'Oddr', 'Olin', 'Ormr', 'Ove', 'Sigurd',
    'Skari', 'Snorri', 'Sten', 'Sigandr', 'Stigr', 'Sven', 'Trygve', 'Ulf',
    'Vali', 'Vidar', 'Aelia', 'Alba', 'Aquila', 'Calia', 'Camilla', 'Casia',
    'Claudia', 'Cloe', 'Drusa', 'Fabia', 'Fausta', 'Fulvia', 'Glaucia',
    'Iovita', 'Iulia', 'Laelia', 'Livia', 'Lucilla', 'Marcia', 'Nona',
    'Octania', 'Paulina', 'Petronia', 'Porcia', 'Tacita', 'Tullia', 'Vita',
    'Aelia', 'Aetius', 'Atilus', 'Avitus', 'Balbus', 'Brutus', 'Caius',
    'Casian', 'Cato', 'Celsus', 'Ennius', 'Gaius'
]

longName = [
    'Pin',
    'Dez',
    'Lun',
    'Oph',
    'Per',
    'Liv',
    'Hel',
    'Kar',
    'Eod',
    'Sir',
    'Gal',
    'Zidd',
    'Valc',
    'Agn',
    'Vud',
    'Kulc',
    'Peekl',
    'Porl',
    'Bort',
    'Thin',
    'Bolr',
    'Bigr',
    'Ryalf',
    'Byl',
    'Lorr',
    'Ror',
    'Gans',
    'Gradr',
    'Lard',
    'Stusl',
    'Ghol',
    'Zar',
    'Dhob',
    'Dring',
    'Thotr',
    'Nass',
    'Fais',
    'Qas',
    'Ipp',
    'Genn',
    'Yevg',
    'Encr',
    'Virg',
    'Zed',
    'Corn',
    'Crab',
    'Prim',
    'Thes',
    'Dent',
    'Rixx',
    'Knuebr',
    'Crouqr',
    'Phiel',
    'Ypuun',
    'Chop',
    'Muzp',
    'Bexkl',
    'Kreinz',
    'Vum',
    'Drey',
    'Sils',
    'Kod',
    'Laasd',
    'Krentd',
    'Himn',
    'Arln',
    'Verg',
    'Hsarth',
    'Sat',
    'Femn',
    'Aldr',
    'Aas',
    'Dentr',
    'Far',
    'Gesr',
    'Hav',
    'Hill',
    'Pogr',
    'Bidr',
    'Dir',
    'Gr',
    'Hirr',
    'Moz',
    'Mugr',
    'Norkr',
    'Quar',
    'Rathkr',
    'Sethr',
    'Sh',
    'Srorth',
    'Trynn',
    'Val',
    'Vrond',
    'Gunnl',
    'Kristr',
    'Liftr',
    'Mar',
    'Mardr',
    'Therl',
    'Thodr',
    'Thorb',
    'Thordr',
    'Von',
    'Whurdr',
    'Yurg',
]
longName2 = [
    'ar', 'al', 'ex', 'el', 'egr', 'aph', 'em', 'il', 'oth', 'ec', 'ov', 'ol',
    'ak', 'ir', 'ot', 'ev', 'an', 'od', 'irl', 'ag', 'is', 'ogg', 'ind',
    'ienn', 'un', 'oss', 'id', 'am', 'ath', 'im', 'af', 'at', 'arr', 'it',
    'ut', 'ull', 'us', 'uc', 'aal', 'ath', 'id', 'eth', 'il', 'an', 'ek',
    'ecr', 'eeth', 'ath', 'und', 'uuth', 'am', 'en', 'ic', 'or', 'od', 'as',
    'ast', 'ed', 'in', 'er', 'an', 'un'
]
longName3 = [
    'ious',
    'ia',
    'ine',
    'ena',
    'anie',
    'ina',
    'ea',
    'eda',
    'ish',
    'ith',
    'ull',
    'a',
    'i',
    'ione',
    'ath',
    'inzz',
    'iaym',
    'ross',
    'rott',
    'eyss',
    'iy',
    'ius',
    'ioth',
    'draal',
    'hvith',
    'zii',
    'ra',
    'eth',
    'ar',
    'ot',
    'ix',
    'ed',
    'is',
    'en',
    'ak',
    'ikth',
    'on',
    'ash',
    'us',
    'ean',
    'iss',
    'yd',
    'yr',
    'is',
    'id',
]

Wname2 = [
    'Zyll', 'Koll', 'Jam', 'Nes', 'Nuq', 'Vinth', 'Tunn', 'Mil', 'Zix', 'Ros',
    'Wor', 'Vu', 'Drar', 'Vuk', 'Qug', 'Mun', 'Des', 'Dit', 'Liat', 'Lis',
    'Ret', 'Ana', 'Ler', 'Dol', 'Hak', 'Lod', 'Vun', 'Dor', 'Suk', 'Ve', 'Me',
    'Ri', 'Va', 'Ni', 'Tu', 'Lo', 'Vo', 'La', 'Ma', 'Drib', 'Sad', 'Zome',
    'Edna', 'In', 'Qir', 'Dis', 'Nut', 'Ael', 'Ang', 'Ara', 'Ari', 'Aym',
    'Broe', 'Cael', 'Cy', 'Dae', 'Del', 'Eli', 'Eryn', 'Faen', 'Fera', 'Gael',
    'Gar', 'Innil', 'Jar', 'Kan', 'Lael', 'Lue', 'Mai', 'Mella', 'Mya',
    'Naill', 'Nim', 'Phann', 'Py', 'Rael', 'Raer', 'Ren', 'Rue', 'Rinn',
    'Sael', 'Sai', 'Ta', 'Thia', 'Tia', 'Vall', 'Von', 'Wil', 'Za', 'Sebek',
    'Khu'
]
Wname23 = [
    'aar', 'unn', 'ak', 'uzz', 'reuk', 'ad', 're', 'ana', 'hy', 'ara', 'il',
    'er', 'in', 'at'
]

surName = [
    'Walter', 'Baker', 'Adams', 'Carter', 'Foster', 'Crow', 'Lithion',
    'Kaethius', 'Glower', 'Garrick', 'Welber', 'Timbers', 'Reese', 'Nackle',
    'Folkor', 'Beren'
]
surName1 = [
    'Amber', 'Mild', 'Wool', 'Golden', 'Dusk', 'Liechen', 'Silver', 'Pine',
    'Oaken', 'Quick', 'Bright', 'Sly', 'Star', 'Iron', 'Blood', 'Raven',
    'Baffle', 'Wild', 'Waggle', 'Silver', 'Shadow', 'Quill', 'Nuckle',
    'Lingen', 'Glitter', 'Apple', 'Wise', 'Whisper', 'Warm', 'Under', 'Toss',
    'Thistle', 'Ten', 'Hundred', 'Tea', 'Tall', 'Swift', 'Strong', 'Stout',
    'Smooth', 'Silver', 'Nimble', 'Little', 'Jam', 'Honey', 'Hog', 'High',
    'Green', 'Good', 'Elder', 'Deep', 'Copper', 'Cherry', 'Brush', 'Big'
]
surName2 = [
    'hide', 'grip', 'coat', 'mantle', 'rock', 'spear', 'vale', 'dale',
    'shield', 'light', 'song', 'shard', 'shot', 'wood', 'ward', 'tounge',
    'thorne', 'stone', 'wander', 'top', 'thread', 'cloak', 'stamp', 'hall',
    'gem', 'blossom', 'acre', 'heart', 'mouse', 'water', 'foot', 'cobble',
    'penny', 'leaf', 'fellow', 'whistle', 'bones', 'bridge', 'hands', 'eyes',
    'step', 'fingers', 'foot', 'jar', 'pot', 'collar', 'hill', 'bottle',
    'earth', 'barrel', 'berry', 'hollow', 'kettle', 'cheeks', 'gather', 'moon'
]
position = ['Of the West', 'Of the East', 'Of the North', 'Of the South']
titleName1 = [
    'The Great', 'The Mighty', 'The Gorgeous', 'The Righteous', 'The Strong',
    'The Brave', 'The Wise', 'The Poor', 'The Kind', 'The Brutal',
    'The Unkowing', 'The Divine'
]
titleName2 = [
    ', Guardian', ', Secretary', ', Earl', ', Arch mage', ', Arch priest',
    ', General', ', Defender', ', Baron', ', Chief', ', Cardinal',
    ', Commander', ', Admiral', ', Duke', ', Master', ', Apprentice',
    ', Protector'
]
titleName21 = [
    ' Of Fate', ' Of Destiny', ' Of Commerce', ' Of the Flame', ' Of the Law',
    ' Of Order', ' Of the Treasury', ' Of Secrets', ' Of the Lands',
    ' Of the Realms'
]
preName1 = [' Sir', ' Lord', ' King', ' Emperor']
numberName = ['The second', 'The third', 'The fourth', 'The fifth']
Wname3 = [
    'Crab', 'Lion', 'Tiger', 'Wolf', 'Angel', 'Devil', 'Daemon', 'Demon',
    'Fiend', 'Hawk', 'Eagle', 'Elephant', 'Dragon', 'Ant', 'Spider','Eel','Pegasus','Pony','Stag','Lamb','Goat','Spirit','Undead','Eagle','Dog','Satyr'
]
l = ['B', 'D', 'G', 'K', 'L', 'M', 'N', 'Q', 'R', 'T', 'H', 'X']

colours = [
    'red', 'green', 'yellow', 'orange', 'black', 'white', 'grey', 'brown',
    'pale', 'green', 'light red', 'light green', 'light blue', 'light grey',
    'dark red', 'dark green', 'dark blue', 'dark grey', 'golden', 'silver',
    'light', 'dark brown', 'light brown', 'turquoise'
]
length = [
    'long', 'short', 'very long', 'very short', 'incredibly long',
    'incredibly short'
]
texture = [
    'curly', 'flat', 'spiky', 'smooth', 'rough', 'soft', 'stiff', 'fluffy',
    'wavy', 'thick'
]
weight = ['heavy', 'light', 'suprisingly heavy', 'suprisingly light']

armourType = [
    'chainmail', 'plate', 'studded leather', 'leather', 'steel',
    f'{choice(colours)} leather', 'fur', f'{choice(colours)} fur', 'hide',
    f'{choice(colours)} hide'
]
armourPiece = [
    'helmet', 'gauntlets', 'boots', 'chestpiece', 'bracers', 'breastplate',
    'armour'
]

clothingType = [
    'leather', f'{choice(colours)} leather', 'fur', f'{choice(colours)} fur',
    'hide', f'{choice(colours)} hide', 'silk', f'{choice(colours)} silk',
    'linnen', 'wool'
]
clothingPiece = [
    'hat', 'gloves', 'boots', 'jacket', 'pants', 'belt', 'cloak', 'cape',
    'hood', 'handkerchief', 'robe'
]

jewelryPiece = ['necklace', 'amulet', 'ring', 'bracer', 'earrings', 'anklet']
instrument = ['harp', 'flute']

relationship = [
    'friend', 'enemy', 'nemesis', 'lover', 'frenemy', 'firstborn child',
    'rival', 'companion', 'partner', 'distant cousin', 'apprentice'
]
feeling = [
    'love for', 'hate for', 'friendship with', 'rivalry with', 'pact with'
]

adjectiveOther = [
  'silver','golden','staggering','laughing','prancing','gilded','running','howling','slaughtered','leering','drunken','leaping','roaring','frowning','lonely','wandering','mysterious','barking','black','gleaming'
]

weapon = [
    'sword', 'spear', 'dagger', 'shield', 'hammer', 'staff', 'bow', 'flail',
    'axe', 'greatsword', 'greatspear', 'warhammer', 'quarterstaff', 'greatbow',
    'greatflail', 'rod', 'wand', 'scepter', 'mace', 'greatmace', 'whip',
    'rapier', 'scimitar', 'short bow', 'long bow'
]
weaponD = [
    'dagger', 'bow', 'greatbow', 'whip', 'rapier', 'scimitar', 'short bow',
    'long bow'
]
weaponS = [
    'sword', 'spear', 'shield', 'hammer', 'staff', 'flail', 'axe',
    'greatsword', 'greatspear', 'warhammer', 'quarterstaff', 'greatflail',
    'scepter', 'mace', 'greatmace'
]
element = ['fire', 'thunder', 'ice', 'lightning', 'psycic', 'radiant']
element1 = ['flaming', 'thunderous', 'freezing', 'psycic', 'divine']

race = [
    'human', 'high elf', 'wood elf', 'dark elf', 'mountain dwarf',
    'hill dwarf', 'lightfoot halfling', 'stout halfling'
]
race2 = [
    'tiefling', 'half orc', 'forest gnome', 'rock gnome', 'half elf',
    'aasimar', 'firbolg', 'tabaxi', 'triton'
]
race3 = [
    'lizardfolk', 'kenku', 'goblin', 'hobgoblin', 'bugbear', 'yuan-ti', 'orc',
    'kobold'
]
raceP = [
    'humans', 'high elves', 'wood elves', 'dark elves', 'mountain dwarves',
    'hill dwarves', 'tieflings', 'tabaxi', 'lizardfolk', 'firbolgs', 'gnomes',
    'halflings', 'orcs', 'goblins', 'kobolds', 'yuan-ti', 'goliaths', 'tritons'
]

Welement = [
    'Frost', 'Flame', 'Thunder', 'Mind', 'Night', 'Wither', 'Star', 'Dawn',
    'Shadow', 'Moon'
]
Welement2 = [
  'Resistance','Invisibility','Blinking','Shielding','Fury','Telepathy','Seeing','Resurrection', 'Might','Magic','Good','Evil','Fear','Binding','Paralysis', 'Polymorph','Secrets','Tentacles','Blinding','Hiding','Smiting','Shielding','Animation','Health','Devouring','Slaying','Abjuration','Conjuration','Illusion','Transmutation','Evocation','Necromancy','Tricks','Strength','Levitation','Speed','Leaping','Commanding','Defence','Flying','Breathing','Opening','Blasting','Displacement','Protection','Force','Venom','Brightness','Disguies','Disruption','Annihilation','Answering','Draining','Vengeance','Wounding','Detection','Web','Wonder','Warning','Wind','Stars','Teleportation','Mind']
Wgem = [
    'Azur',
    'Sapphire',
    'Ruby',
    'Emerald',
    'Topaz',
    'Ivory',
    'Ebony',
    'Silver',
    'Platinum',
    'Gold',
    'Aquamarine',
    'Jade',
    'Electrum',
    'Obsidian',
    'Copper',
    'Brass',
    'Steel',
    'Iron',
    'Amethyst',
]
jewelryType = Wgem
WgemStone = [
    'Azurite', 'Banded Agate', 'Blue Quartz', 'Hematite', 'Lapis Lazuli',
    'Malachite', 'Moss Agate', 'idan', 'Rhodochrosite', 'Tiger Eye',
    'Turqouise', 'Bloodstone', 'Carnelian', 'Chalcedony', 'Citrine', 'Jasper',
    'Moonstone', 'Onyx', 'Quartz', 'Sardonyx', 'Star Rose', 'Zircon', 'Amber',
    'Amethyst', 'Chrysoberyl', 'Coral', 'Garnet', 'Jade', 'Jet', 'Pearl',
    'Spinel', 'Tourmaline', 'Alexandrite', 'Aquamarine', 'Black Pearl',
    'Blue Spinel', 'Peridot', 'Topaz', 'Black Opal', 'Blue Sapphire',
    'Emerald', 'Fire Opal', 'Star Sapphire', 'Yellow Sapphire',
    'Black Sapphire', 'Diamond', 'Jacinth', 'Ruby'
]
Wcolour = ['Green', 'Black', 'White', 'Red']
Wtype = [
    'blade', 'skewer', 'edge', 'spike', 'steel', 'point', 'tooth', 'razor',
    'fang', 'bringer', 'lance', 'splitter', 'taloon'
]
Wtype2 = [
    'sword', 'spear', 'dagger', 'shield', 'hammer', 'staff', 'bow', 'flail',
    'axe', 'greatsword', 'greatspear', 'warhammer', 'quarterstaff', 'greatbow',
    'greatflail', 'rod', 'wand', 'scepter', 'mace', 'greatmace', 'whip',
    'rapier', 'scimitar', 'short bow', 'long bow'
]
Wtype22 = [
    'hand', 'circlet', 'mask', 'tome', 'cloak', 'cape', 'boots', 'eye',
    'gloves', 'wand', 'scepter', 'rod', 'ring', 'staff', 'talisman', 'amulet'
]
Wtype23 = armourPiece
Wtitle = [
    'Defender', 'Protector', 'Herald', 'Bane', 'Avenger', 'Bringer',
    'Restorer', 'Conqueror', 'Guardian', 'Scourge', 'Voice', 'Warden',
    'Breaker', 'Bannisher'
]
Wtitle1 = [
    'Justice', 'Truth', 'Hope', 'Life', 'Shadow', 'Virtue', 'Bliss', 'Mercy',
    'Purity', 'Law', 'Blood', 'Darkness', 'Time', 'Dusk', 'Dawn', 'Bones',
    'Faith', 'Ignorance'
]  # - the
Wtitle11 = [
    'Arcane', 'Worthy', 'Undead', 'Helpless', 'Ancient', 'Dawn', 'Forest',
    'Plague', 'Damned', 'Divine', 'Night', 'Void', 'Deep', 'Sun', 'Law',
    'Crypt'
]  # + the

event = ['slay', 'befriend']

position = [
    'Guardian', 'Secretary', 'Earl', 'Arch mage', 'Arch priest', 'General',
    'Defender', 'Baron', 'Chief', 'Cardinal', 'Commander', 'Admiral', 'Duke',
    'Master', 'Apprentice', 'Protector'
]

stats = [
    'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom',
    'Charisma'
]
descriptor = [
    'strong', 'dextorous', 'tough', 'intelligent', 'wise', 'charismatic'
]
classS = ['Barbarian', 'Paladin', 'Fighter']
classD = ['Rouge', 'Ranger']
classI = ['Artificer', 'Wizard']
classW = ['Cleric', 'Druid', 'Monk']
classC = ['Bard', 'Warlock', 'Sorcerer']
occupationS = [
    'Blacksmith', 'Miner', 'Knight', 'Butcher', 'Guard', 'Bodyguard','Sailor','Pigkeeper','Boatman','Treasure Hunter','Pirate','Mine Owner','Mule Driver','Brick Maker','Scavanger','Smith','Goldsmith']
occupationD = [
  'Criminal', 'Ranger', 'Talor', 'Farmer','Paper Maker','Shepherd','Glovemaker','Duelist','Highwayman','Leatherworker','Carpenter','Calligrapher','Shoemaker','Weaver','Woodcarver']
occupationI = [
  'Scribe', 'Librarian', 'Schoolar', 'Winemaker', 'Torturer','Runecrafter','Investor','Clock Maker','Judge','Alchemist','Bookbinder','Sage','Document Forger','Wizard','Poisoner','Tinkerer']
occupationW = [
  'Priest', 'Chef', 'Healer', 'Baker','Nurse','Cleric','Miller','Bottler','Beggar','Astrologist','Archeologist','Druid','Hermit','Brewer','Glassblower','Herbalist','Mason','Navigator','Painter','Potter']
occupationC = [
  'Bard', 'Charlatan', 'Tavernkeeper', 'Artist','Debt Collector','Wine Merchant','Musician','Minstrel','Paladin','Herald','Barkeeper','Steward','Genera-Store Keeper','Clothing Seller','Gambler']

beardHair=['Beard','Hair']
singWhistle=['Singing','Whisteling','Humming']
lowHigh=['Low','High']
appearance=[
  'Distinctive Jewelry','Piercings','Flamboyant Clothes','Formal Clothes','Ragged Clothes','Pronounced Scar','Missing Teeth','Missing Fingers','Unusual Eye Colour','Tattoos','Birthmark','Unusual Skin Colour','Bald',f'Braided {choice(beardHair)}','Unusual Hair Colour','Nerveous Eye Twitch','Distinctice Nose','Distinctive Posture','Exceptionally Beautiful','Exceptionally Ugly']
talent=[
  'Plays Musical Instrument','Speaks Several Languages','Unbelivably Lucky','Perfect Memory','Great With Animals','Great With Children','Great at Solving Puzzles','Great at a Game','Great at Impersonations','Draws Beautifully','Paints Beautifully','Sings Beautifully','Drinks Everyone under the Table','Expert Carpenter','Expert Cook','Expert Dart Thrower','Expert Juggler','Skilled Actor','Master of Disguise','Skilled Dancer',"Knows Thieves' Cant"]
mannerism=[
  f'Prone to {choice(singWhistle)} quietly','Speaks in Rhyme or Another Peculiar Way',f'Particularly {choice(lowHigh)} Voice','Lisp or Stutter','Enunciates Overly Clearly','Whispers','Uses Flowery Speech and Long Words','Frequently Uses the Wrong Word','Uses Colourful Oaths and Exclamations','Makes Constant Jokes and Puns','Prone to Predictions of Doom','Fidgets','Squints','Stares into the Distance','Chews Something','Paces','Taps Fingers','Bites Fingernails','Twirls hair','Tugs Beard']
interaction=[
'Argumentative','Arrogant','Blustering','Rude','Curious','Friendly','Honest','Hot Tempered','Irritable','Ponderous','Quiet','Suspicious']
ideal=[
  'Beauty','Charity','Greater Good','Life','Respect','Self-Sacrifice','Community','Fairness','Honor','Logic','Responsibility','Tradition','Balance','Knowledge','Live and let Live','Moderation','Neutrality','People','Domination','Greed','Might','Pain','Retribution','Slaughter','Change','Creativity','Freedom','Independence','No Limits','Whimsy','Aspiration','Discovery','Glory','Nation','Redemption','Power','Faith','Fairness','Friendship','Honesty','Might','Sincerity','Destiny','Generosity','Free Thinking','Family','Obligation','Nature','Self-Improvement','Mastery']
bond=[
  'are Dedicated to Fulfilling a Personal Life Goal','are Protective of Close Family Member','are Protective of Colleagues','are Loyal to Benefactor','are Captivated by Romantic Interest','are Drawn to a Special Place','are Protective of a Sentimental Keepsake','are Protective of a Valuable Possession','are Out For Revenge','Owe their Life to Someone','do Everything for the Common People','are Being Hunted','are Seeking Atonement for their Missdoings','are Protective of the Land']
phobia=['darkness','heights','flying','pain','open spaces or crowds','needles or pointed objects','riding on a horse','choking','flowers','being touched','spiders','numbers','thunder and lightning',
        'disorder or untidiness','imperfection','failure','human-like figures','being alone','sickness','stairs or steep slopes','amphibians','books','plants','ugliness','being ridiculed','mirrors','snow',
        'clocks','time','confined spaces','dogs','trees','accidents','cats','insects','teenagers','horses','speaking in public','blood','reptiles','water','insects','large things','small things','death or dead things',
        'the night','the dark','rain','birds','snakes','paper','love','flying','fire','being stared at','the full moon','speed','magic','witches and witchcraft','animals']
flaw=[
  'posses Forbidden Love','Enjoys Decadent Pleasures','are Arrogant',"Envies Someone's Possesions",'are Greedy','are Prone to Rage','have a Powerful Enemy',f'has a phobia for {choice(phobia)}','has a Shameful History','did a Secret Crime','are Foolhardy Bravery','Judge Others Harshly and Themself Even More Severly','Put to Much Trust into Authority','are Inflexible in Their Thinking','are Suspicious of others','are Obsessive','are Always in Debt','are Cowardly','are a Kleptomaniac','are Forgetfull','have a "Tell" that Shows When They are Lying','would do Anything for Fame','are quite Direct','Love to get Drunk','have Trust Issues','are Jealous','are Bloodthirsty','are Dogmatic','have a Need to Win Arguments','Like Keeping Secrets','Belive They are Better than Everyone','are Bitter','are Violent','belive in the Reign of the Strong','Natuarly Lie a Lot','are Seeking Knowledge','Follow Orders, even to the detriment of themself and others','are Pridefull']

bizzareEvent = [
    'hit by a meteor', 'struck down by a angry god', 'killed by an angry god',
    'killed by a hatching slaad egg'
]
causeOfDeath = [
    'died to an unknown cause', 'was murdered',
    'died in an accident related to their occupation',
    'died of natural causes', 'died to an apparent suicide',
    'was torn apart by an animal or natural disaster',
    'was consumed by a monster',
    'was executed for a crime or tortured to death',
    f'died to a bizzare event (f.ex: {choice(bizzareEvent)})'
]
homeSize = [
    'city', 'town', 'village', 'hamlet', 'neighborhood', 'alley', 'district',
    'farm', 'tribe', 'clan', 'univeristy', 'home'
]
trade = ['trade', 'religion', 'politics', 'the military']
homeEvent = [
    'burned down', f'was bought by {choice(firstName)}',
    f'became a center of {choice(trade)}', f'was raided by {choice(race3)}s',
    'became too boring', 'was deserted'
]
money = [
    'rich', 'poor', 'very rich', 'very poor', 'incredibly rich',
    'incredibly poor', 'decently rich', 'decently poor', 'almost rich',
    'almost poor'
]
size = ['big', 'small', 'huge', 'tiny', 'averagely sized']
money1 = ['middleclass', 'lowerclass', 'upperclass']
family = [
    'alone', 'in an orphanage', 'with a guardian', 'in a temple',
    'in an institution', 'with extended family',
    f'in an adoptive {choice(race)} family'
]
family1 = ['with their single father', 'with their single mother']
lost = [
    f'died (they {choice(causeOfDeath)})', 'was imprisoned', 'abandoned them',
    'was lost to an unknown fate'
]
goal = [
    'honor', 'money', 'justice', 'glory', 'inner peace', 'friendship', 'fame'
]
alliance = [
    'have a strong alliance with', 'are interested in', 'hate',
    'have a weak connection with', 'have a rivalry with', 'are persecuted by',
    'have no connection with', 'are exiled from'
]
factionName1=[
  'School','Univeristy','Guild','Alliance','Church','Library','Inquisition','Kingdom','Order','Cult','Enclave','Society','Knights','Dicipline','Cabal']
shuffle(factionName1)
factionName21=[f'{choice(longName)}{choice(longName2)}{choice(longName3)}',f'{choice(Welement)}',f'the {choice(Wgem)}',f'the {choice(Wname3)}']
factionName22=[f'{choice(longName)}{choice(longName2)}{choice(longName3)}',f'{choice(Welement)}',f'the {choice(Wgem)}',f'the {choice(Wname3)}']
factionName23=[f'{choice(longName)}{choice(longName2)}{choice(longName3)}',f'{choice(Welement)}',f'the {choice(Wgem)}',f'the {choice(Wname3)}']
faction1=f'the {factionName1[0]} of {choice(factionName21)}'
faction2=f'the {factionName1[1]} of {choice(factionName22)}'
faction3=f'the {factionName1[2]} of {choice(factionName23)}'
faction=[faction1,faction2,faction3]

personality = [
    'kind', 'polite', 'thoughtfull', 'mean', 'arrogant', 'oblivious',
    'annoyed', 'agreeing', 'amused', 'anxious', 'careful', 'clever', 'witty',
    'clumsy', 'confused', 'curious', 'disgusted', 'elegant', 'foolish',
    'graceful', 'healthy', 'jealous', 'jolly', 'lucky', 'proud', 'beautiful',
    'righteous', 'brave', 'gentle', 'brutal', 'holy', 'aggressive', 'relieved',
    'scared', 'shy', 'selfish', 'talented', 'upset', 'uptight', 'childish'
]
age = [
    'old', 'young', 'very old', 'very young', 'middle aged', 'a teenager',
    'an adult', 'decently old', 'decently young'
]
tribeAlliance = [
    'exiles', 'diplomats', 'scouts', 'hunters', 'warriors', 'raiders'
]

terrain = ['desert', 'joungle', 'grassland', 'forest', 'mountain']
desert = [
    f'Goblin {choice(homeSize)}', f'Kobold {choice(homeSize)}', 'Pyramid',
    f'Lizardfolk {choice(homeSize)}', 'Manticores nest', 'Hill giant tribe',
    f'Thri-Kreen {choice(homeSize)}', f'Small {choice(homeSize)}'
]
joungle = [
    'Yuan-Ti Temple', 'Fey area', 'Ruined Temple', 'Joungle Tribe',
    'Dinsaur keeper tribe', f'Goblin {choice(homeSize)}',
    f'Yuan-Ti {choice(homeSize)}'
]
grassland = [
    f'Small {choice(homeSize)}', 'Lycanthrope tribe', 'Ruined Temple',
    'Barbarian Tribe', 'Old Wizards Tower', f'Goblin {choice(homeSize)}',
    f'Underdark gate', 'Hag Coven'
]
forest = [
    f'Small {choice(homeSize)}', 'Fey area', 'Ruined Temple',
    'Barbarian Tribe', 'Old Wizards Tower', f'Orc {choice(homeSize)}',
    f'Owlbears Nest', f'Devil Cult'
]
mountain = [
    f'Small {choice(homeSize)}', f'Giant {choice(homeSize)}', 'Ruined Temple',
    'Demon Cult', 'Old Wizards Tower', f'Orc {choice(homeSize)}',
    f'Necromancers {choice(homeSize)}', f'Devil Cult'
]

searching = ['searching for', 'hiding']
withWithout = ['with', 'without']
trapKill = ['trap', 'kill']
cisternWell = ['cistern', 'well']
petGuardBeast = ['pet', 'guard beast']
penPrison = ['pen', 'prison']
trophyMuseum = ['trophy room', 'museum']
latrineBath = ['latrine', 'bath']
minersEarthProtection = ['miners', 'earth', 'protection']
strongVault = ['strongroom', 'vault']
foyerAnteChamber = ['foyer', 'antechamber']
investigateDefend = ['investigate', 'defend']
entryVestibule = ['entry room', 'vestibule']
door = ""

dungeonType = [
    'Death Trap', 'Lair', 'Maze', 'Mine', 'Planar Gate', 'Stronghold',
    'Temple or Shrine', 'Tomb', 'Treasure Vault'
]
dungeonStartingArea = [
    'Square, 20x20 ft.; passage on each wall',
    'Square, 20x20 ft.; door on two walls, passage on third',
    'Square, 40x40 ft.; doors on three walls',
    'Rectangle, 80x20 ft.; with rows of pillars down the middle, two passages leading from each long wall, and doors on each short wall',
    'Rectangle, 20x40 ft.; passage on each wall',
    'Circle 40ft. diameter; one passage on each cardinal direction',
    'Square, 20x20 ft.; door on two walls, passage on third, secret door on fourth',
    'Passage, 10ft. wide; T intersection',
    'Passage, 10ft. wide; four way intersection'
]
dungeonPassage = [
    'Continue straight 30ft., no doors or side passages',
    'Continue Straight 20ft., door to the right, then an additional 10ft. ahead',
    'Continue Straight 20ft., door to the left, then an additional 10ft. ahead',
    'Continue straight 20ft., passage ends in door',
    'Continue straight 20ft. side passage to the right, then an additinal 10ft. ahead',
    'Continue straight 20ft. side passage to the left, then an additinal 10ft. ahead',
    f'Continue straight 20ft., comes to a dead end; {door}',
    'Continue straight 20ft., then the passage turns left and continues 10ft.',
    'Continue straight 20ft., then the passage turns right and continues 10ft.',
    'Chamber (roll on the Chamber table)', 'Stairs (roll on the Stairs table)'
]
dungeonPassageWith = [
    '5ft.', '10ft.', '20ft.', '30ft.',
    '40ft. with row of pillars down the middle',
    '40ft. with double row of pillars', '40ft. wide, 20ft. high',
    '40ft. wide, 20ft. high, gallery 10ft. above floor allows acces to level above'
]
dungeonDoor = [
    'Wooden', 'Wooden, barred or locked', 'Stone', 'Stone, barred or lock',
    'Iron', 'Iron. barred or locked', 'Portcullis',
    'Portcullis, locked in place', 'Secret door',
    'Secret door, barred or locked'
]
dungeonBeyondDoor = [
    'Chamber (roll on the Chamber table)',
    'Passage extending 10ft., then T intersection 10ft. to the right and left',
    'Passage 20ft. straight ahead', 'Stairs (roll on the Stairs table)',
    'False door with trap'
]
dungeonChamber = [
    'Square 20x20ft. S', 'Square 30x30ft. S', 'Square 40x40ft. S',
    'Rectangle 20x30ft. S', 'Rectangle 30x40ft. S', 'Rectangle 40x50ft. L'
]
dungeonChamber1 = [
    'Rectangle 50x80ft. L', 'Circle 30ft. diameter. S',
    'Circle 50ft. diameter. L', 'Octagon 40x40ft. L', 'Octagon 40x40ft.',
    'Trapezoid roughly 40x60ft. L'
]
dungeonChamberExits = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
dungeonChamberExits1 = [0, 1, 1, 2, 2, 3, 3, 4, 5, 6]
dungeonExitLocation = [
    'Wall oppostite entrance', 'Wall oppostite entrance',
    'Wall left of entrance', 'Wall right of entrance', 'Same wall as entrance'
]
dungeonExitType = ['Door, (roll on the Door table)', 'Corridor, 10ft. long']
dungeonStairs = [
    'Down one level to a Chamber', 'Down one level to a Passage 20ft. long',
    'Down two levels to a Chamber', 'Down two levels to a Passage 20ft. long',
    'Down three levels to a Chamber',
    'Down three levels to a Passage 20ft. long', 'Up one level to a Chamber',
    'Up one level to a Passage 20ft. long', 'Up to a dead end',
    'Down to a dead end', 'Chimney up one level to a Passage 20ft. long',
    'Chimney down one level to a Passage 20ft. long',
    f'Shaft {choice(withWithout)} up one level to a Chamber',
    f'Shaft {choice(withWithout)} down one level to a Chamber'
]
dungeonDeathTrap = [
    'Antechamber or waiting room for spectators',
    ' Guardroom fortified against intruders',
    f'Vault for holding Important Treasures, accessible only by locked or Secret door. if {randint(1,100)} is above 25; trapped',
    'Room containing puzzle to bypass monster or trap',
    f'Trap designed to {choice(trapKill)}',
    'Observation room, allowing guards or spectators to observe creatures moving through the dungeon'
]
dungeonLair = [
    'Armory stocked with weapon and armour',
    'Audience chamber, used to recieve guests',
    'Banquet room for important celebrations',
    'Barracks where the Lairs defenders are quartered',
    'Bedroom for use by leaders', 'Chapel where the Lairs inhabitants worship',
    f'{choice(cisternWell)} for drinking water',
    'Guardroom for the defense of the Lair',
    f'Kennel for {choice(petGuardBeast)}s',
    'Kitchen for foodstorage and preparation',
    f'{choice(penPrison)} where captives are held',
    'Storage, mostly nonperishable goods',
    'Throne room where the Lair´s leader holds court',
    'Training and Exercise room', f'{choice(trophyMuseum)}',
    f'{choice(latrineBath)}',
    'Workshop for the construction of Weapons, Armour, Tools, and other Goods'
]
dungeonMaze = [
    'Conjuring room, used to summon creatures that guard the Maze',
    'Guardroom for Sentinels that patrol the Maze',
    'Lair for Guardbeasts that patrol the Maze',
    f'{choice(penPrison)} accessible only by seret door, used to hold captives condemned to the Maze',
    'Shrine to God or other Entity',
    'Storage for food, as well as tools used by the Maze´s guardians to keep the complex in working order',
    f'Trap to {choice(trapKill)} those sent into the Maze',
    'Well that provides drinking water',
    'Workshop where doors, torch cones, and other furnishings are repaired and maintained'
]
dungeonMine = [
    'Barracks for miners', 'Bedroom for a supervior or manager',
    f'Chapel dedicated to {firstName} the patron deity of {choice(minersEarthProtection)}',
    f'{choice(cisternWell)} to provide drinking water for miners', 'Guardroom',
    'Kitchen used to feed workers',
    'Labratory used to conduct tests on strange minerals extracted from the mine',
    f'Lode where the ore is mined. If {randint(1,100)} is below 75, lode is depleted',
    'Office used by supervisor',
    'Smithy for repearing damaged tools and other equipment',
    f'{choice(strongVault)} used to store ore for transport to the surface'
]
dungeonPlanarGate = [
    f'Decorated {choice(foyerAnteChamber)}',
    'Armoury used by the Portal´s guardians',
    'Audience chamber for receiving visitors',
    'Barracks used by the Portal´s guards',
    'Bedroom used by high ranking member of the order that guards the Portal',
    f'Chapel dedicated to {firstName} a diety related to the portal',
    'Cistern providing fresh water',
    'Classroom for use of initiates learning about the portal´s secrets',
    f'Conjuring room for summoning creatures used to {choice(investigateDefend)} the portal',
    'Crypt where the remains of those that died guarding the portal are kept',
    'Dining room',
    'Diviation room used to investigate the portal and events tied to it',
    'Dormitory for visitors and guards', f'{choice(entryVestibule)}',
    'Gallery for displaying throphies and objects related to the portal and those that guard it',
    'Guardroom to protect the Portal', 'Kitchen',
    'Laboratory for conducting experiments relating to the Portal and creatures that emerge from it',
    'Library holding books about the Portal´s history',
    f'{choice(penPrison)} for holding captives and creatures that emerge from the Portal',
    f'Planar junction, where the gate to another plane once stood. If {randint(1,100)} is above 75 then active',
    'Storage',
    f'{choice(strongVault)} for guarding both treasures from the Portal and funds to pay the Planar gate´s guardians',
    'study',
    'Torture chamber, for questioning creatures that pass through the Portal or that attempt to secretly use it',
    f'{choice(latrineBath)}',
    'Workshop for constructing tools and gear needed to study the Portal'
]

def newAdjective():
  global adjective
  adjective = [
        f'{choice(weight)}',
        f'{choice(colours)}',
        f'{choice(texture)}',
        f'{choice(element)}',
        f'{choice(jewelryType)}',
        f'{choice(adjectiveOther)}'
    ]
  adjectiveItem=choice(adjective)
  return adjectiveItem

def newArtifact():
    global Wname
    global artifact
    artifact = 0

    Wname = [
        f'{choice(longName)}{choice(longName2)}{choice(longName3)}',
        f'{choice(firstName)}', f'{choice(Wname2)}-{choice(Wname2)}',
        f'{choice(l)}´{choice(Wname23)}'
    ]

    a = randint(1, 19)

    if a == 1:
        artifact = (f'{choice(Wname)}, {choice(Wtitle)} of {choice(Wtitle1)}')
    elif a == 2:
        artifact = (
            f'{choice(Wname)}, {choice(Wtitle)} of the {choice(Wtitle11)}')
    elif a == 3:
        artifact = (
            f'{choice(Wname)}, {choice(Wtitle)} of the {choice(Welement)}')
    elif a == 4:
        artifact = (f'{choice(Wname)} the {choice(Welement)}{choice(Wtype)}')
    elif a == 5:
        artifact = (f'{choice(Welement)}{choice(Wtype)}')
    elif a == 6:
        a = randint(1, 3)
        if a == 1:
            artifact = (f'{choice(Wname)}´s {choice(Wtype22)}')
        else:
            artifact = (f'{choice(Wname)}´s {choice(Wtype2)}')
        a = 0
    elif a == 7:
        artifact = (f'{choice(Wname)}´s {choice(Wtitle1)}')
    elif a == 8:
        a = randint(1, 3)
        if a == 1:
            artifact = (
                f'{choice(Wname)}, the {choice(Wtype22)} of {choice(firstName)}'
            )
        else:
            artifact = (
                f'{choice(Wname)}, the {choice(Wtype2)} of {choice(firstName)}'
            )
    elif a == 9:
        a = randint(1, 3)
        if a == 1:
            artifact = (f'{choice(Wtype2)} of the {choice(Wname3)}')
        else:
            artifact = (f'{choice(Wtype22)} of the {choice(Wname3)}')
    elif a == 10:
        artifact = (f'the {choice(Welement)}{choice(Wtype)}')
    elif a == 11:
        artifact = (f'the {choice(Wgem)}{choice(Wtype)}')
    elif a == 12:
        artifact = (f'the {choice(Wgem)}{choice(Wtype22)}')
    elif a == 13:
        a = randint(1, 2)
        if a == 1:
            artifact = (f'the {choice(Wtype22)} of {choice(Wname)}')
        elif a == 2:
            artifact = (f'the {choice(Wtype)} of {choice(Wname)}')
    elif a == 14:
        a = randint(1, 3)
        if a == 1:
            artifact = (f'{choice(Wcolour)}{choice(Wtype)}')
        elif a == 2:
            artifact = (f'{choice(Wcolour)}{choice(Wtype2)}')
        elif a == 3:
            artifact = (f'{choice(Wcolour)}{choice(Wtype22)}')
    elif a == 15:
        a = randint(1, 2)
        if a == 1:
            artifact = (f'the {choice(Wtype22)} of {choice(Welement2)}')
        elif a == 2:
            artifact = (f'the {choice(Wtype22)} of {choice(Welement)}')
    elif a == 16:
        a = randint(1, 4)
        if a == 1:
            artifact = (f'{choice(Wcolour)}{choice(Wtype23)}')
        elif a == 2:
            artifact = (f'the {choice(Wtype23)} of the {choice(Welement)}')
        elif a == 3:
            artifact = (f'{choice(Wname)}´s {choice(Wtype23)}')
        elif a == 4:
            artifact = (
                f'{choice(Wname)}´s {choice(Wtype23)} of {choice(Wtitle1)}')
        elif a == 17:
            a = randint(1, 2)
            if a == 1:
                artifact = (f'the {choice(Wname3)}{choice(Wtype)}')
            else:
                artifact = (f'{choice(Wname3)}{choice(Wtype)}')
        elif a == 18:
            a = randint(1, 2)
            if a == 1:
                artifact = (f'the {choice(Wtype2)} of the {choice(Wname3)}kin')
            else:
                artifact = (f'{choice(Wtype2)} of the {choice(Wname3)}kin')

        elif a == 19:
            artifact = (f'the {choice(Wname3)}{choice(Wtype22)}')

    return artifact



def newItem():
    global item
    item = [
        f'{choice(weight)} {choice(weapon)}',
        f'{choice(jewelryType)} {choice(jewelryPiece)}',
        f'{choice(clothingType)} {choice(clothingPiece)}', f'{choice(trinket)}'
    ]
    newItem = choice(item)
    return newItem

def randomItem():
    item = [
        f'{choice(weight)} {choice(weapon)}',
        f'{choice(jewelryType)} {choice(jewelryPiece)}',
        f'{choice(clothingType)} {choice(clothingPiece)}', f'{choice(trinket)}'
    ]

def newItem2():
    global item
    item = [
        f'{choice(texture)} {choice(clothingType)} {choice(clothingPiece)}',
        f'{choice(jewelryType)} {choice(jewelryPiece)}',
        f'{choice(clothingType)} {choice(clothingPiece)}', f'{choice(trinket)}'
    ]
    newItem = choice(item)
    return newItem

def newItem3():
  global item
  item = [
        f'{choice(clothingPiece)}',
        f'{choice(jewelryPiece)}',
        f'{choice(clothingPiece)}',
    ]
  newItem = choice(item)
  return newItem


def newNPC():
    global item
    global newNPC1

    newName = [0]

    newRace = randint(1, 30)
    if newRace == 1:
        newRace = [f'{choice(race2)}']
    elif newRace == 2:
        newRace = [f'{choice(race2)}']
    elif newRace == 3:
        newRace = [f'{choice(race2)}']
    elif newRace == 4:
        newRace = [f'{choice(race2)}']
    elif newRace == 5:
        newRace = [f'{choice(race2)}']
    elif newRace == 6:
        newRace = [f'{choice(race3)}']
    elif newRace == 7:
        newRace = [f'{choice(race3)}']
    else:
        newRace = [choice(race)]

    if choice(newRace) == 'human':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'wood elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'high elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'dark elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'mountain dwarf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'hill dwarf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'lightfoot halfling':
        newName = [choice(firstName)]

    elif choice(newRace) == 'stout halfling':
        newName = [choice(firstName)]

    elif choice(newRace) == 'tiefling':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'half orc':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'forest gnome':
        newName = [choice(firstName)]

    elif choice(newRace) == 'rock gnome':
        newName = [choice(firstName)]

    elif choice(newRace) == 'half elf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'aasimar':
        newName = randint(1, 3)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    if choice(newRace) == 'firbolg':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'triton':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'tabaxi':
        newName = [
            choice(firstName),
            choice(Wgem),
            choice(Welement),
            choice(Welement2),
            choice(Wtype),
            choice(Wgem)
        ]

    elif choice(newRace) == 'lizardfolk':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'kenku':
        newName = [choice(firstName)]

    elif choice(newRace) == 'goblin':
        newName = randint(1, 5)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'hobgoblin':
        newName = randint(1, 4)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'bugbear':
        newName = randint(1, 5)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'orc':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'kobold':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'yuan-ti':
        newName = randint(1, 4)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    ability = [choice(descriptor)]
    occupation = randint(1, 10)
    if occupation == 1:
        occupation = choice(occupationS)
    elif occupation == 2:
        occupation = choice(occupationD)
    elif occupation == 3:
        occupation = choice(occupationI)
    elif occupation == 4:
        occupation = choice(occupationW)
    elif occupation == 5:
        occupation = choice(occupationC)
    else:
        if choice(ability) == 'strong':
            occupation = choice(occupationS)
        elif choice(ability) == 'dextorous':
            occupation = choice(occupationD)
        elif choice(ability) == 'intelligent':
            occupation = choice(occupationI)
        elif choice(ability) == 'wise':
            occupation = choice(occupationW)
        elif choice(ability) == 'charismatic':
            occupation = choice(occupationC)
        else:
            occupation = randint(1, 5)
            if occupation == 1:
                occupation = choice(occupationS)
            elif occupation == 2:
                occupation = choice(occupationD)
            elif occupation == 3:
                occupation = choice(occupationI)
            elif occupation == 4:
                occupation = choice(occupationW)
            elif occupation == 5:
                occupation = choice(occupationC)

    occupation = [occupation]
    newItem2()
    newName2()

    a = randint(1, 3)
    if a == 1:
        money22 = [f' {choice(money1)} ']
        money2 = [' ']
    else:
        money2 = [f' {choice(money)} ']
        money22 = [' ']

    shuffle(personality)

    a = randint(1, 10)
    if a == 1:
        if randint(1, 3) == 1:
            b = [f'{choice(family1)}, the other parent {choice(lost)}']
        else:
            if randint(1, 3) == 1:
                c = f'one of their parents {choice(lost)}, and the other one {choice(lost)}'
            else:
                c = f'their parents {choice(lost)}'

            b = [f'{choice(family)}, {c}']
    else:
        b = [
            f'in a {choice(size)}{choice(money2)}{choice(newRace)}{choice(money22)}family'
        ]

    newNPC1 = (
        f'{choice(newName)} the {choice(ability)} {choice(newRace)} {choice(occupation)}. They are always carrying their {choice(item)} wich they got from their {choice(relationship)}{choice(name)} after their home {choice(homeSize)} {choice(homeEvent)}. They {choice(alliance)} {choice(faction)}. {choice(newName)} grew up {choice(b)}. They are currently seeking {choice(goal)}. {choice(newName)} are very {personality[0]} and a bit {personality[1]}. They are {choice(age)}.'
    )
    npc = newNPC1
    return npc


def newName2():
    global name
    surNameGenerator = randint(1, 5)
    if surNameGenerator == 1:
        surName7 = (f' {choice(surName)}')
        surName6 = [surName7]
    else:
        surName4 = [choice(surName1)]
        surName5 = [choice(surName2)]
        surName6 = [f' {choice(surName4)}{choice(surName5)}']

    titleName3 = [choice(titleName2)]
    titleName4 = [choice(titleName21)]
    titleName5 = [f'{choice(titleName3)}{choice(titleName4)}']

    titleName6 = (f' {choice(titleName1)}')
    titleName7 = [titleName6]

    titleName = randint(1, 100)
    if titleName == 1:
        titles2 = [choice(position)]
    elif titleName == 2:
        titles2 = [choice(numberName)]
    elif titleName == 3:
        titles2 = (f'{choice(position)} of the {choice(raceP)}')
    else:
        titles2 = [choice(titleName7), choice(titleName5)]

    prefix = randint(1, 100)
    if prefix == 1:
        preName = [choice(preName1)]
    else:
        preName = ['']

    preName = randint(1, 100)
    if preName == 1:
        preName = [choice(preName1)]
    else:
        preName = ['']

    sufix = randint(1, 100)
    if sufix == 1:
        endName = [choice(titles2)]
    else:
        endName = [choice(surName6)]

    newName = randint(1, 100)
    if newName == 1:
        newName = [f'{choice(longName)}{choice(longName2)}{choice(longName3)}']
    elif newName == 2:
        newName = [f'{choice(Wname2)}-{choice(Wname2)}']
    elif newName == 3:
        newName = [f'{choice(l)}´{choice(Wname23)}']
    else:
        newName = [choice(firstName)]

    name = [f'{choice(preName)} {choice(newName)}{choice(endName)}']
    return choice(name)


def newClothing():
    global clothing
    clothing = [
        f'{choice(clothingType)} {choice(clothingPiece)}',
        f'{choice(weight)} {choice(armourType)} {choice(armourPiece)}',
        f'{choice(jewelryType)} {choice(jewelryPiece)}'
    ]
    clothingItem = choice(clothing)
    return clothingItem
    


def newCharacterTraits1():
    global characterTraits
    characterTraits = [
        f'having {choice(length)} {choice(texture)} {choice(colours)} hair',
        f'allways wearing their signature {choice(texture)} {choice(clothing)}',
        f'being the {choice(relationship)} of {choice(name)}'
    ]
    characterTrait = choice(characterTraits)
    return characterTrait


def newCharacterTraits():
    global characterTraits
    characterTraits = [
        f' they are known for {choice(characterTraits)}',
        f'they have a secret {choice(feeling)} {choice(name)}',
        f'they never leave behind their {choice(item)}'
    ]
    characterTrait = choice(characterTraits)
    return characterTrait

def randomNames():
    for i in range(1):

        surNameGenerator = randint(1, 5)
        if surNameGenerator == 1:
            surName7 = (f' {choice(surName)}')
            surName6 = [surName7]
        else:
            surName4 = [choice(surName1)]
            surName5 = [choice(surName2)]
            surName6 = [f' {choice(surName4)}{choice(surName5)}']

        titleName3 = [choice(titleName2)]
        titleName4 = [choice(titleName21)]
        titleName5 = [f'{choice(titleName3)}{choice(titleName4)}']

        titleName6 = (f' {choice(titleName1)}')
        titleName7 = [titleName6]

        titleName = randint(1, 100)
        if titleName == 1:
            titles2 = [choice(position)]
        elif titleName == 2:
            titles2 = [choice(numberName)]
        elif titleName == 3:
            titles2 = (f'{choice(position)} of the {choice(raceP)}')
        else:
            titles2 = [choice(titleName7), choice(titleName5)]

        prefix = randint(1, 100)
        if prefix == 1:
            preName = [choice(preName1)]
        else:
            preName = ['']

        preName = randint(1, 100)
        if preName == 1:
            preName = [choice(preName1)]
        else:
            preName = ['']

        sufix = randint(1, 100)
        if sufix == 1:
            endName = [choice(titles2)]
        else:
            endName = [choice(surName6)]

        name = randint(1, 50)
        if name == 1:
            name = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif name == 2:
            name = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif name == 3:
            name = [f'{choice(l)}´{choice(Wname23)}']
        elif name == 4:
            name = [f'{choice(longName)}{choice(longName2)}']
        else:
            name = [choice(firstName)]

        newName = (f'{choice(preName)} {choice(name)}{choice(endName)}')

        name = newName
        return name


'''
def randomDesription():
    global item
    global name
    print(
        'What do you want to know about them? 1- their favourite item, 2- one of their relationships, 3- their favourite piece of clothing'
    )
    rDanswer = input('')
    print('')
    if rDanswer.isnumeric() != True:
        rDanswer = 0
        randomDesription()

    rDanswer = int(rDanswer)
    if rDanswer == 1:
        newItem()
        print(f'They love their {choice(item)}')
    elif rDanswer == 2:
        newName2()
        print(f'They are the {choice(relationship)} of {choice(name)}')
    elif rDanswer == 3:
        rDclothing = randint(1, 5)

        if rDclothing == 1:
            print(
                f'They like wearing their {choice(armourType)} {choice(armourPiece)}'
            )
        elif rDclothing == 2:
            print(
                f'They like wearing their {choice(jewelryType)} {choice(jewelryPiece)}'
            )
        else:
            print(
                f'They like wearing their {choice(clothingType)} {choice(clothingPiece)}'
            )

'''
    


def randomNameAndDescription():
    global name
    global item
    surNameGenerator = randint(1, 5)
    if surNameGenerator == 1:
        surName7 = (f' {choice(surName)}')
        surName6 = [surName7]
    else:
        surName4 = [choice(surName1)]
        surName5 = [choice(surName2)]
        surName6 = [f' {choice(surName4)}{choice(surName5)}']

    titleName3 = [choice(titleName2)]
    titleName4 = [choice(titleName21)]
    titleName5 = [f'{choice(titleName3)}{choice(titleName4)}']

    titleName6 = (f' {choice(titleName1)}')
    titleName7 = [titleName6]

    titleName = randint(1, 100)
    if titleName == 1:
        titles2 = [choice(position)]
    elif titleName == 2:
        titles2 = [choice(numberName)]
    else:
        titles2 = [choice(titleName7), choice(titleName5)]

    prefix = randint(1, 100)
    if prefix == 1:
        preName = [choice(preName1)]
    else:
        preName = ['']

    sufix = randint(1, 5)
    if sufix == 1:
        endName = [choice(titles2)]
    else:
        endName = [choice(surName6)]

    newName1 = (f'{choice(preName)} {choice(firstName)}{choice(endName)}')

    rDaNclothing = randint(1, 5)

    if rDaNclothing == 1:
        rDaNclothing2 = (
            f'it seems like they are always wearing their {choice(armourType)} {choice(armourPiece)}'
        )
    elif rDaNclothing == 2:
        rDaNclothing2 = (
            f'it seems like they are always wearing their {choice(jewelryType)} {choice(jewelryPiece)}'
        )
    else:
        rDaNclothing2 = (
            f'it seems like they are alwayse wearing their {choice(clothingType)} {choice(clothingPiece)}'
        )

    newName2()
    newItem()
    nameAndDescription=f'Have you heard about {newName1}? They are the {choice(relationship)} of {choice(name)}, {rDaNclothing2} and they love their {choice(item)}'
    return nameAndDescription


def randomCharacter():
    global item
    newName = [0]

    newRace = randint(1, 10)
    if newRace == 1:
        newRace = [f'{choice(race2)}']
    elif newRace == 2:
        newRace = [f'{choice(race2)}']
    elif newRace == 3:
        newRace = [f'{choice(race3)}']
    else:
        newRace = [choice(race)]

    if choice(newRace) == 'human':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'wood elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'high elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'dark elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'mountain dwarf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'hill dwarf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'lightfoot halfling':
        newName = [choice(firstName)]

    elif choice(newRace) == 'stout halfling':
        newName = [choice(firstName)]

    elif choice(newRace) == 'tiefling':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'half orc':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'forest gnome':
        newName = [choice(firstName)]

    elif choice(newRace) == 'rock gnome':
        newName = [choice(firstName)]

    elif choice(newRace) == 'half elf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'aasimar':
        newName = randint(1, 3)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    if choice(newRace) == 'firbolg':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'triton':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'tabaxi':
        newName = [
            choice(firstName),
            choice(Wgem),
            choice(Welement),
            choice(Welement2),
            choice(Wtype),
            choice(Wgem)
        ]

    elif choice(newRace) == 'lizardfolk':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'kenku':
        newName = [choice(firstName)]

    elif choice(newRace) == 'goblin':
        newName = randint(1, 5)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'hobgoblin':
        newName = randint(1, 4)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'bugbear':
        newName = randint(1, 5)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'orc':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'kobold':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'yuan-ti':
        newName = randint(1, 4)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    ability = [choice(descriptor)]
    classN = randint(1, 10)
    if classN == 1:
        classN = choice(classS)
    elif classN == 2:
        classN = choice(classD)
    elif classN == 3:
        classN = choice(classI)
    elif classN == 4:
        classN = choice(classW)
    elif classN == 5:
        classN = choice(classC)
    else:
        if choice(ability) == 'strong':
            classN = choice(classS)
        elif choice(ability) == 'dextorous':
            classN = choice(classD)
        elif choice(ability) == 'intelligent':
            classN = choice(classI)
        elif choice(ability) == 'wise':
            classN = choice(classW)
        elif choice(ability) == 'charismatic':
            classN = choice(classC)
        else:
            classN = randint(1, 5)
            if classN == 1:
                classN = choice(classS)
            elif classN == 2:
                classN = choice(classD)
            elif classN == 3:
                classN = choice(classI)
            elif classN == 4:
                classN = choice(classW)
            elif classN == 5:
                classN = choice(classC)

    if choice(ability) == 'strong':
        weapon2 = choice(weaponS)
    elif choice(ability) == 'dextorous':
        weapon2 = choice(weaponD)
    else:
        weapon2 = choice(weapon)

    classN = [classN]
    weapon2 = [weapon2]
    newItem2()
    newName2()

    a = randint(1, 3)
    if a == 1:
        money22 = [f' {choice(money1)} ']
        money2 = [' ']
    else:
        money2 = [f' {choice(money)} ']
        money22 = [' ']


    character = f'{choice(newName)} the {choice(ability)} {choice(newRace)} {choice(classN)}. They are always carrying their {choice(item)} wich they got from their {choice(relationship)}{choice(name)} after their home {choice(homeSize)} {choice(homeEvent)}. They wield their {choice(weapon2)}. {choice(newName)} originate from a {choice(size)}{choice(money2)}{choice(newRace)}{choice(money22)}family. They are currently seeking {choice(goal)}'
    return character


def randomArtifact():
    global Wname

    Wname = [
        f'{choice(longName)}{choice(longName2)}{choice(longName3)}',
        f'{choice(firstName)}', f'{choice(Wname2)}-{choice(Wname2)}',
        f'{choice(l)}´{choice(Wname23)}'
    ]

    a = randint(1, 19)

    if a == 1:
        artifact = f'{choice(Wname)}, {choice(Wtitle)} of {choice(Wtitle1)}'
    elif a == 2:
        artifact = f'{choice(Wname)}, {choice(Wtitle)} of the {choice(Wtitle11)}'
    elif a == 3:
        artifact = f'{choice(Wname)}, {choice(Wtitle)} of the {choice(Welement)}'
    elif a == 4:
        artifact = f'{choice(Wname)} the {choice(Welement)}{choice(Wtype)}'
    elif a == 5:
        artifact = f'{choice(Welement)}{choice(Wtype)}'
    elif a == 6:
        a = randint(1, 3)
        if a == 1:
            artifact = f'{choice(Wname)}´s {choice(Wtype22)}'
        else:
            artifact = f'{choice(Wname)}´s {choice(Wtype2)}'
        a = 0
    elif a == 7:
        artifact = f'{choice(Wname)}´s {choice(Wtitle1)}'
    elif a == 8:
        a = randint(1, 3)
        if a == 1:
            artifact = f'{choice(Wname)}, the {choice(Wtype22)} of {choice(firstName)}'
        else:
            artifact = f'{choice(Wname)}, the {choice(Wtype2)} of {choice(firstName)}'
    elif a == 9:
        a = randint(1, 3)
        if a == 1:
            artifact = f'{choice(Wtype2)} of the {choice(Wname3)}'
        else:
            artifact = f'{choice(Wtype22)} of the {choice(Wname3)}'
    elif a == 10:
        artifact = f'the {choice(Welement)}{choice(Wtype)}'
    elif a == 11:
        artifact = f'the {choice(Wgem)}{choice(Wtype)}'
    elif a == 12:
        artifact = f'the {choice(Wgem)}{choice(Wtype22)}'
    elif a == 13:
        a = randint(1, 2)
        if a == 1:
            artifact = f'the {choice(Wtype22)} of {choice(Wname)}'
        elif a == 2:
            artifact = f'the {choice(Wtype)} of {choice(Wname)}'
    elif a == 14:
        a = randint(1, 3)
        if a == 1:
            artifact = f'{choice(Wcolour)}{choice(Wtype)}'
        elif a == 2:
            artifact = f'{choice(Wcolour)}{choice(Wtype2)}'
        elif a == 3:
            artifact = f'{choice(Wcolour)}{choice(Wtype22)}'
    elif a == 15:
        a = randint(1, 2)
        if a == 1:
            artifact = f'the {choice(Wtype22)} of {choice(Welement2)}'
        elif a == 2:
            artifact = f'the {choice(Wtype22)} of {choice(Welement)}'
    elif a == 16:
        a = randint(1, 4)
        if a == 1:
            artifact = f'{choice(Wcolour)}{choice(Wtype23)}'
        elif a == 2:
            artifact = f'the {choice(Wtype23)} of the {choice(Welement)}'
        elif a == 3:
            artifact = f'{choice(Wname)}´s {choice(Wtype23)}'
        elif a == 4:
            artifact = f'{choice(Wname)}´s {choice(Wtype23)} of {choice(Wtitle1)}'
    elif a == 17:
        a = randint(1, 2)
        if a == 1:
            artifact = f'the {choice(Wname3)}{choice(Wtype)}'
        else:
            artifact = f'{choice(Wname3)}{choice(Wtype)}'
    elif a == 18:
        a = randint(1, 2)
        if a == 1:
            artifact = f'the {choice(Wtype2)} of the {choice(Wname3)}kin'
        else:
            artifact = f'{choice(Wtype2)} of the {choice(Wname3)}kin'

    elif a == 19:
        artifact = f'the {choice(Wname3)}{choice(Wtype22)}'

    return artifact


def randomHeroOfOld():
    global Wname
    global name
    newName2()

    Wname = [
        f'{choice(longName)}{choice(longName2)}{choice(longName3)}',
        f'{choice(firstName)}', f'{choice(Wname2)}-{choice(Wname2)}',
        f'{choice(l)}´{choice(Wname23)}'
    ]

    person = [
        f'{choice(Wname)} {choice(titleName1)}',
        f'{choice(Wname)} the {choice(Wname3)}',
        f'{choice(Wname)} the {choice(position)} of the {choice(raceP)}'
    ]

    a = randint(1, 9)

    if a == 1:
        weapon = (f'{choice(firstName)}´s {choice(Wtitle1)}')

    elif a == 2:
        a = randint(1, 3)
        if a == 1:
            weapon = (f'{choice(Wtype2)} of the {choice(Wname3)}')
        else:
            weapon = (f'{choice(Wtype22)} of the {choice(Wname3)}')

    elif a == 3:
        weapon = (f'{choice(Welement)}{choice(Wtype)}')

    elif a == 4:
        weapon = (f'{choice(Wgem)}{choice(Wtype)}')

    elif a == 5:
        weapon = (f'{choice(Wgem)}{choice(Wtype22)}')

    elif a == 6:
        a = randint(1, 3)
        if a == 1:
            weapon = (f'{choice(Wcolour)}{choice(Wtype)}')
        elif a == 2:
            weapon = (f'{choice(Wcolour)}{choice(Wtype2)}')
        elif a == 3:
            weapon = (f'{choice(Wcolour)}{choice(Wtype22)}')

    elif a == 7:
        a = randint(1, 2)
        if a == 1:
            weapon = (f'{choice(Wtype22)} of {choice(Welement2)}')
        elif a == 2:
            weapon = (f'{choice(Wtype22)} of {choice(Welement)}')

    elif a == 8:
        weapon = (f'{choice(Wtype2)} of the {choice(Wname3)}kin')

    elif a == 9:
        weapon = (f'{choice(Wname3)}{choice(Wtype)}')

    legend=f'{choice(name)} carried the {weapon} on their journey to {choice(event)} {choice(person)}'
    return legend


def randomNPC():
    global item

    newName = [0]

    newRace = randint(1, 30)
    if newRace == 1:
        newRace = [f'{choice(race2)}']
    elif newRace == 2:
        newRace = [f'{choice(race2)}']
    elif newRace == 3:
        newRace = [f'{choice(race2)}']
    elif newRace == 4:
        newRace = [f'{choice(race2)}']
    elif newRace == 5:
        newRace = [f'{choice(race2)}']
    elif newRace == 6:
        newRace = [f'{choice(race3)}']
    elif newRace == 7:
        newRace = [f'{choice(race3)}']
    else:
        newRace = [choice(race)]

    if choice(newRace) == 'human':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'wood elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'high elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'dark elf':
        newName = randint(1, 10)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'mountain dwarf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'hill dwarf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'lightfoot halfling':
        newName = [choice(firstName)]

    elif choice(newRace) == 'stout halfling':
        newName = [choice(firstName)]

    elif choice(newRace) == 'tiefling':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'half orc':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'forest gnome':
        newName = [choice(firstName)]

    elif choice(newRace) == 'rock gnome':
        newName = [choice(firstName)]

    elif choice(newRace) == 'half elf':
        newName = [choice(firstName)]

    elif choice(newRace) == 'aasimar':
        newName = randint(1, 3)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        else:
            newName = [choice(firstName)]

    if choice(newRace) == 'firbolg':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'triton':
        newName = randint(1, 5)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'tabaxi':
        newName = [
            choice(firstName),
            choice(Wgem),
            choice(Welement),
            choice(Welement2),
            choice(Wtype),
            choice(Wgem)
        ]

    elif choice(newRace) == 'lizardfolk':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'kenku':
        newName = [choice(firstName)]

    elif choice(newRace) == 'goblin':
        newName = randint(1, 5)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'hobgoblin':
        newName = randint(1, 4)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'bugbear':
        newName = randint(1, 5)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'orc':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'kobold':
        newName = randint(1, 3)
        if newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    elif choice(newRace) == 'yuan-ti':
        newName = randint(1, 4)
        if newName == 1:
            newName = [
                f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
            ]
        elif newName == 2:
            newName = [f'{choice(Wname2)}-{choice(Wname2)}']
        elif newName == 3:
            newName = [f'{choice(l)}´{choice(Wname23)}']
        else:
            newName = [choice(firstName)]

    ability = [choice(descriptor)]
    occupation = randint(1, 10)
    if occupation == 1:
        occupation = choice(occupationS)
    elif occupation == 2:
        occupation = choice(occupationD)
    elif occupation == 3:
        occupation = choice(occupationI)
    elif occupation == 4:
        occupation = choice(occupationW)
    elif occupation == 5:
        occupation = choice(occupationC)
    else:
        if choice(ability) == 'strong':
            occupation = choice(occupationS)
        elif choice(ability) == 'dextorous':
            occupation = choice(occupationD)
        elif choice(ability) == 'intelligent':
            occupation = choice(occupationI)
        elif choice(ability) == 'wise':
            occupation = choice(occupationW)
        elif choice(ability) == 'charismatic':
            occupation = choice(occupationC)
        else:
            occupation = randint(1, 5)
            if occupation == 1:
                occupation = choice(occupationS)
            elif occupation == 2:
                occupation = choice(occupationD)
            elif occupation == 3:
                occupation = choice(occupationI)
            elif occupation == 4:
                occupation = choice(occupationW)
            elif occupation == 5:
                occupation = choice(occupationC)

    occupation = [occupation]
    newItem2()
    newName2()

    a = randint(1, 3)
    if a == 1:
        money22 = [f' {choice(money1)} ']
        money2 = [' ']
    else:
        money2 = [f' {choice(money)} ']
        money22 = [' ']

    shuffle(personality)

    a = randint(1, 10)
    if a == 1:
        if randint(1, 3) == 1:
            b = [f'{choice(family1)}, the other parent {choice(lost)}']
        else:
            if randint(1, 3) == 1:
                c = f'one of their parents {choice(lost)}, and the other one {choice(lost)}'
            else:
                c = f'their parents {choice(lost)}'

            b = [f'{choice(family)}, {c}']
    else:
        b = [
            f'in a {choice(size)}{choice(money2)}{choice(newRace)}{choice(money22)}family'
        ]

    b5=randint(1,3)
    if b5 == 1:
      pointOfInterest1=choice(talent)
      pointOfInterest2=choice(appearance)
    elif b5 == 2:
      pointOfInterest1=choice(mannerism)
      pointOfInterest2=choice(talent)
    elif b5 == 3:
      pointOfInterest1=choice(appearance)
      pointOfInterest2=choice(mannerism)

    npc=f'{choice(newName)} the {choice(ability)} {choice(newRace)} {choice(occupation)}. They are always carrying their {choice(item)} wich they got from their {choice(relationship)}{choice(name)} after their home {choice(homeSize)} {choice(homeEvent)}. They {choice(alliance)} {choice(faction)}. {choice(newName)} grew up {choice(b)}. They are currently seeking {choice(goal)}. {choice(newName)} are very {personality[0]} and a bit {personality[1]}. They are {choice(age)}. Some other notable things about them are: {pointOfInterest1} and {pointOfInterest2}, they have a tendesy to be a bit {choice(interaction)}. Their greatest Ideal is: {choice(ideal)}. They {choice(bond)}, and {choice(flaw)}.'
    return npc


'''
def randomEncounter():
    global newNPC1
    f = 1

    a = randint(1, 9)

    if a == 1:
        weapon = (f'{choice(firstName)}´s {choice(Wtitle1)}')

    elif a == 2:
        a = randint(1, 3)
        if a == 1:
            weapon = (f'{choice(Wtype2)} of the {choice(Wname3)}')
        else:
            weapon = (f'{choice(Wtype22)} of the {choice(Wname3)}')

    elif a == 3:
        weapon = (f'{choice(Welement)}{choice(Wtype)}')

    elif a == 4:
        weapon = (f'{choice(Wgem)}{choice(Wtype)}')

    elif a == 5:
        weapon = (f'{choice(Wgem)}{choice(Wtype22)}')

    elif a == 6:
        a = randint(1, 3)
        if a == 1:
            weapon = (f'{choice(Wcolour)}{choice(Wtype)}')
        elif a == 2:
            weapon = (f'{choice(Wcolour)}{choice(Wtype2)}')
        elif a == 3:
            weapon = (f'{choice(Wcolour)}{choice(Wtype22)}')

    elif a == 7:
        a = randint(1, 2)
        if a == 1:
            weapon = (f'{choice(Wtype22)} of {choice(Welement2)}')
        elif a == 2:
            weapon = (f'{choice(Wtype22)} of {choice(Welement)}')

    elif a == 8:
        weapon = (f'{choice(Wtype2)} of the {choice(Wname3)}kin')

    elif a == 9:
        weapon = (f'{choice(Wname3)}{choice(Wtype)}')

    print(
        'Where are you? 1-Grassland, 2-Forest, 3-Desert, 4-Mountain, 5-Arctic, 6-Joungle, 8-Costal, 9-Sea, 10-Underdark, 11-Hell, 12-Abyss'
    )
    a = input('')

    print('What level are you? 1-20?')
    b = input('')
    if b.isnumeric() == True:
        b = int(b)
    else:
        print('page 302')
        print('page 82')
        randomEncounter()

    print('How many are you?')
    c = input('')
    if c.isnumeric() == True:
        c = int(c)
    else:
        randomEncounter()

    if b <= 4:
        if a == '1':
            d = randint(1, 8)
            if d == 1:
                g = randint(1, 4)
                print(
                    f'1 Hobgoblin(page. 186 MM), and {b*c+g} goblins(page. 166 MM)'
                )
                print(
                    f'They are {choice(tribeAlliance)} from the nearby goblin tribe'
                )
                if b * c > 1:
                    if b * c == 2:
                        f = 1.5
                    elif b * c <= 6:
                        f = 2
                    elif b * c <= 10:
                        f = 2.5
                    elif b * c <= 14:
                        f = 3
                    else:
                        f = 4
                e = 100 + (50 * (b * c + g) * f)
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 2:
                print(f'1 Griffon(page. 174 MM)')
                print('It is out hunting')
                print(f'It is {450} xp')

            elif d == 3:
                print(f'{b+c} Bandits ambush them(page. 343 MM)')
                if b + c > 1:
                    if b + c == 2:
                        f = 1.5
                    elif b + c <= 6:
                        f = 2
                    elif b + c <= 10:
                        f = 2.5
                    elif b + c <= 14:
                        f = 3
                    else:
                        f = 4
                e = (50 * (b + c)) * f
                e = int(e)
                print(f'They are {e} xp')

            elif d == 4:
                newName2()
                g = randint(1, 4)
                print(f'{b+c+g} Guards walk past(page. 347 MM)')
                print(f'They are searching for the criminal{choice(name)}.')
                if b + c + g > 1:
                    if b + c + g == 2:
                        f = 1.5
                    elif b + c + g <= 6:
                        f = 2
                    elif b + c + g <= 10:
                        f = 2.5
                    elif b + c + g <= 14:
                        f = 3
                    else:
                        f = 4
                e = (25 * (b + c + g)) * f
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 5:
                newName2()
                print(
                    f'the criminal{choice(name)} runs past(Spy, page. 349 MM)')
                print(f'Wich is worth {200}')

            elif d == 6:
                print('two people on horseback run past, they are:')
                newNPC()
                print(newNPC1)
                print('and')
                newNPC()
                print(newNPC1)

            elif d == 7:
                g = randint(1, 6)
                print(
                    f'they stumble onto {b+c+g} tribal warriors(page. 350 MM)')
                print(
                    f'They are {choice(tribeAlliance)} from the nearby tribe')
                if b + c + g > 1:
                    if b + c + g == 2:
                        f = 1.5
                    elif b + c + g <= 6:
                        f = 2
                    elif b + c + g <= 10:
                        f = 2.5
                    elif b + c + g <= 14:
                        f = 3
                    else:
                        f = 4
                e = (25 * (b + c + g)) * f
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 8:
                newName2()
                shuffle(magicItemA)
                print(
                    f'the wandering merchant{choice(name)}(Illusionist. page. 214 VGtM) riding on it´s donkey {choice(Wgem)}{choice(clothingPiece)} rides past'
                )
                print(
                    f'{choice(name)} sells a {magicItemA[0]} and a {magicItemA[1]} for double their normal prize({(randint(1,6)+1)*10}gp for consumables and {((randint(1,6)+1)*10)*2}gp for normal items)'
                )


#------------------------------------------
        if a == '8':
            d = randint(1, 8)
            if d == 1:
                g = randint(1, 4)
                print(
                    f'1 Cult Fanatic(page. 345 MM), and {b*c+g} Cultists(page. 345 MM)'
                )
                print(f'They are from the cult of the Kraken')
                if b * c + g > 1:
                    if b * c + g == 2:
                        f = 1.5
                    elif b * c + g <= 6:
                        f = 2
                    elif b * c + g <= 10:
                        f = 2.5
                    elif b * c + g <= 14:
                        f = 3
                    else:
                        f = 4
                e = 450 + (25 * (b * c + g) * f)
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 2:
                g = randint(1, 3)
                print(f'{g} Sea Hags(page. 179 MM)')
                print('Their coven is nearby')

                if g > 1:
                    if g == 2:
                        f = 1.5
                    elif g <= 6:
                        f = 2

                print(f' They are {(g*450)*f} xp')

            elif d == 3:
                print(f'{b} Ochre Jelly (page. 243 MM)')

                if b > 1:
                    if b == 2:
                        f = 1.5
                    elif b <= 6:
                        f = 2

                e = (450 * (b)) * f
                e = int(e)
                print(f'They are {e} xp')

            elif d == 4:
                newName2()
                g = randint(1, 6)
                print(f'{g+c} Acolytes walk past(page. 342 MM)')
                print(f'They are searching for the {weapon}.')
                if c + g > 1:
                    if c + g == 2:
                        f = 1.5
                    elif c + g <= 6:
                        f = 2
                    elif c + g <= 10:
                        f = 2.5
                    elif c + g <= 14:
                        f = 3
                    else:
                        f = 4
                e = (50 * (c + g)) * f
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 5:
                newName2()
                print(
                    f'the pirate{choice(name)} runs past(Swashbuckler, page. 217 VGtM)'
                )
                print(f'Wich is worth {700}')

            elif d == 6:
                print(
                    f'a boat on the horizon coming closer from the {choice(faction)}.'
                )
                print('the two most interesting people on the boat is:')
                newNPC()
                print(newNPC1)
                print('and')
                newNPC()
                print(newNPC1)

            elif d == 7:
                g = randint(1, 6)
                print(
                    f'they stumble onto {b+c+g} tribal warriors(page. 350 MM)')
                print(
                    f'They are {choice(tribeAlliance)} from the nearby  tribe')
                if b + c + g > 1:
                    if b + c + g == 2:
                        f = 1.5
                    elif b + c + g <= 6:
                        f = 2
                    elif b + c + g <= 10:
                        f = 2.5
                    elif b + c + g <= 14:
                        f = 3
                    else:
                        f = 4
                e = (25 * (b + c + g)) * f
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 8:
                newName2()
                shuffle(magicItemA)
                print(
                    f'the wandering merchant{choice(name)}(Illusionist. page. 214 VGtM) riding on it´s donkey {choice(texture)}{choice(clothingPiece)} rides past'
                )
                print(
                    f'{choice(name)} sells a {magicItemA[0]} and a {magicItemA[1]} for double their normal prize({(randint(1,8)+1)*9}gp for consumables and {((randint(1,6)+1)*11)*2}gp for normal items)'
                )

        if a == '9':
            d = randint(1, 8)
            if d == 1:
                g = randint(1, 4)
                print(
                    f'a ship carrying 1 Cult Fanatic(page. 345 MM), and {b*c+g} Cultists(page. 345 MM)'
                )
                print(f'They are from the cult of the Kraken')
                if b * c + g > 1:
                    if b * c + g == 2:
                        f = 1.5
                    elif b * c + g <= 6:
                        f = 2
                    elif b * c + g <= 10:
                        f = 2.5
                    elif b * c + g <= 14:
                        f = 3
                    else:
                        f = 4
                e = 450 + (25 * (b * c + g) * f)
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 2:
                g = randint(1, 3)
                print(f'{g} Sea Hags(page. 179 MM)')
                print('Their coven is nearby')

                if g > 1:
                    if g == 2:
                        f = 1.5
                    elif g <= 6:
                        f = 2

                print(f' They are {(g*450)*f} xp')

            elif d == 3:
                g = randint(1, 6)
                print(
                    f'a Sahuagin Priestess and {b+g} Sahuagins (page. 263 and 264 MM)'
                )
                print(
                    f'they are {choice(tribeAlliance)} from their local tribe')

                if b + g > 1:
                    if b + g == 2:
                        f = 1.5
                    elif b + g <= 6:
                        f = 2
                    elif b + g <= 10:
                        f = 2.5
                    elif b + g <= 14:
                        f = 3
                    else:
                        f = 4

                e = (450 + (b * 100) * f)
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 4:
                newNPC()
                g = randint(1, 6)
                print(
                    f'{g+c} Bandits on a pirateship approches (page. 343 MM)')
                print(f'They are {alliance} {faction}.')
                print(f'their captain is:')
                print(newNPC1)
                if c + g > 1:
                    if c + g == 2:
                        f = 1.5
                    elif c + g <= 6:
                        f = 2
                    elif c + g <= 10:
                        f = 2.5
                    elif c + g <= 14:
                        f = 3
                    else:
                        f = 4
                e = (25 * (c + g)) * f
                e = int(e)
                print(f'They are worth {e} xp')

            elif d == 5:
                print(f'an island is on the horizon')
                randomIsland()

            elif d == 6:
                print(
                    f'a boat on the horizon coming closer from the {choice(faction)}.'
                )
                print('the two most interesting people on the boat is:')
                newNPC()
                print(newNPC1)
                print('and')
                newNPC()
                print(newNPC1)

            elif d == 7:
                newNPC()
                h = [weapon, newNPC1]
                print(f'a ship searching for {choice(h)} sailes past')

            elif d == 8:
                newName2()
                shuffle(magicItemA)
                print(
                    f'a tradeship with the merchant{choice(name)}(Illusionist. page. 214 VGtM) riding on it´s donkey {choice(texture)}{choice(clothingPiece)} rides past'
                )
                print(
                    f'{choice(name)} sells a {magicItemA[0]} and a {magicItemA[1]} for double their normal prize({(randint(1,6)+1)*9}gp for consumables and {((randint(1,10)+1)*8)*2}gp for normal items)'
                )


def randomIsland():
    global artifact

    a = choice(terrain)
    if a == 'desert':
        shuffle(desert)
        b = desert[0]
        c = desert[1]
    elif a == 'joungle':
        shuffle(joungle)
        b = joungle[0]
        c = joungle[1]
    elif a == 'grassland':
        shuffle(grassland)
        b = grassland[0]
        c = grassland[1]
    elif a == 'mountain':
        shuffle(mountain)
        b = mountain[0]
        c = mountain[1]
    elif a == 'forest':
        shuffle(forest)
        b = forest[0]
        c = forest[1]

    newNPC()
    newArtifact()

    print(
        f'the {a} island has a {b} and a {c}. {newNPC1} is also on this island, {choice(searching)} the {artifact}.'
    )



def randomDungeon():
    global door

    print(
        'What do you want? 1-Starting area, 2-Passage, 3-Chamber, 4-Chamber type, 5-Door, 6-Exit, 7-Stairs'
    )
    a = input('')

    if a == '1':
        print(choice(dungeonStartingArea))

    elif a == '2':
        if randint(1, 10) == 10:
            door = "secret door"
        else:
            door = ""
        print(choice(dungeonPassage))
        if randint(1, 10) == 10:
            print(f'Passage is: {choice(dungeonPassageWith)} wide')
        else:
            print('Passage is: 10ft. wide')

    elif a == '3':
        if randint(1, 5) == 5:
            print(choice(dungeonChamber1))
            print(f'Number of exists: {choice(dungeonChamberExits1)}')
        else:
            print(choice(dungeonChamber))
            print(f'Number of exists: {choice(dungeonChamberExits)}')

    elif a == '4':
        print(
            'What sort of dungeon is it?, 1-Lair, 2-Mine, 3-Planar gate, 4-Death trap'
        )
        b = input('')
        if b == '1':
            print(choice(dungeonLair))
        elif b == '2':
            print(choice(dungeonMine))
        elif b == '3':
            print(choice(dungeonPlanarGate))
        elif b == '4':
            print(choice(dungeonPlanarGate))

    elif a == '5':
        print(choice(dungeonDoor))

    elif a == '6':
        print(choice(dungeonExitLocation))
        print(choice(dungeonExitType))
        print(f'Behind the exit: {choice(dungeonBeyondDoor)}')

    elif a == '7':
        print(choice(dungeonStairs))
'''

def randomEstablishment():
  global adjective
  global item
  newItem3()
  newAdjective()
  race4=[choice(race3),choice(race2),choice(race)]
  item.append(choice(Wname3))
  item.append(choice(race4))
  establishment=f'the {choice(adjective)} {choice(item)}'
  return establishment

def randomFirstName():
    a=randint(1,30)
    if a == 1:
        name=f'{choice(Wname2)} {choice(Wname2)}'
    elif a == 2:
        name=f"{choice(l)}'{choice(Wname23)}"
    elif a == 3:
        name=f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
    else:
        name=choice(firstName)
    return name

def randomMagicItem():
    a = randint(1, 4)
    if a == 1:
        w=(f'{choice(Wtype2)} of {choice(Welement2)}')
    elif a == 2:
        w=(
            f'{choice([choice(armourPiece),choice(Wtype22)])} of {choice(Welement2)}'
        )
    else:
      w=(f'{choice(element)} {choice(Wtype2)}')
    return w
