from random import randint, choice, shuffle

townName1=['Dark','Coom','Wings','Trout','Larc','Hogs','Wells','Conr','Ash','Apple','Dun','Butter','Orin','Cras','Times','Mill','Eld','Lante','Froste', 'Flames', 'Thunders', 'Minde', 'Nighte', 'Withers', 'Stare', 'Dawne',
    'Shadows', 'Moone','Steep','Dead','Sleet','Summers','Gray','Stone','Pine','Rust','Amber','Shroud','Gold','Bleak','Steel','Laste','Old','Cave','Smooth','River','Gray']
townName2=[
  'ton','bury','wich','fall','iston','side','pond','shire','bourne','by','caster','dale','mere','stone','ham','glos','burgh','wind','storm','mire','light','more','point','strand','fort','minster','ville','break','point','pond','mire','call']

Welement = [
    'Frost', 'Flame', 'Thunder', 'Mind', 'Night', 'Wither', 'Star', 'Dawn',
    'Shadow', 'Moon', 'Light'
]
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
    'Andriet', 'Bernard', 'Charles', 'Charlot', 'Colin', 'Denis', 'Durant','Ernault', 'Ethor', 'Felix', 'Gilles', 'Henry', 'Hugo', 'Imbert', 'Jean','Louis', 'Louys', 'Loys', 'Martin', 'Michel', 'Mille', 'Nicolas', 'Oudart','Perrin', 'Pierre', 'Richart', 'Robert', 'Simon', 'Vincent', 'Affra','Allet', 'Anna', 'Apell', 'Brida', 'Cecilia', 'Clara', 'Ella', 'Els','Elsbeth', 'Engel', 'Eva', 'Fela', 'Geras', 'Guttel', 'Irmel', 'Kuan','Lucia', 'Margret', 'Marlein', 'Martha', 'Reusin', 'Ursel', 'Vrsula','Berthard', 'Allexander', 'Casper', 'Clas', 'Cristin', 'Cristoff', 'Felix','Frantz', 'Fritz', 'Gerhart', 'Hans', 'Hartmann', 'Heintz', 'Herman','Jacob', 'Jorg', 'Karll', 'Kilian', 'Linhart', 'Lorentz', 'Ludwig', 'Marx','Melchor', 'Mertin', 'Michel', 'Moritz', 'Osswald', 'Ott', 'Peter','Rudolff', 'Sigmund', 'Steffan', 'Symon', 'Thoman', 'Ulrich', 'Wendel','Wilhelm', 'Wolff', 'Wolfgang', 'Aella', 'Chloros', 'Daphne', 'Dione','Elektra', 'Euadne', 'Eudora', 'Helene', 'Ianthe', 'Kallisto', 'Karme','Kirke', 'Kleio', 'Klotho', 'Kynthia', 'Leto', 'Niobe', 'Ourania','Phaenna', 'Theia', 'Adonis', 'Aeson', 'Aias', 'Argos', 'Brontes','Deimos', 'Erbos', 'Hektor', 'Heros', 'Iason', 'Kadmos', 'Kastor', 'Koios','Kreios', 'Laios', 'Linos', 'Lykos', 'Mentor', 'Pallas', 'Phricxus','Xantos', 'Alfhild', 'Arnbjorg', 'Ase', 'Alog', 'Astrid', 'Auda', 'Audhid','Bodil', 'Brenna', 'Brynhild', 'Dagmar', 'Erika', 'Eira', 'Gudrun','Helga', 'Hertha', 'Hilde', 'Ingrid', 'Iona', 'Jorunn', 'Kari', 'Kenna','Magnhild', 'Nanna', 'Olga', 'Ragna', 'Ragnhild', 'Runa', 'Saga','Sigfrid', 'Signe', 'Sigrid', 'Sigrunn', 'Solveg', 'Svanhild', 'Thora','Torborg', 'Torunn', 'Tove', 'Unn', 'Vigdis', 'Ylva', 'Yngvild', 'Agni','Asger', 'Asmund', 'Bjarte', 'Bjorg', 'Brandr', 'Brandt', 'Brynjar','Clader', 'Colborn', 'Cuyler', 'Egil', 'Einar', 'Eric', 'Erlnad', 'Fiske','Fritjof', 'Frode', 'Geir', 'Halvar', 'Hemming', 'Hjalmar', 'Hjotr','Ivar', 'Knud', 'Leif', 'Liufr', 'Oddr', 'Olin', 'Ormr', 'Ove', 'Sigurd','Skari', 'Snorri', 'Sten', 'Sigandr', 'Stigr', 'Sven', 'Trygve', 'Ulf','Vali', 'Vidar', 'Aelia', 'Alba', 'Aquila', 'Calia', 'Camilla', 'Casia','Claudia', 'Cloe', 'Drusa', 'Fabia', 'Fausta', 'Fulvia', 'Glaucia','Iovita', 'Iulia', 'Laelia', 'Livia', 'Lucilla', 'Marcia', 'Nona','Octania', 'Paulina', 'Petronia', 'Porcia', 'Tacita', 'Tullia', 'Vita','Aelia', 'Aetius', 'Atilus', 'Avitus', 'Balbus', 'Brutus', 'Caius','Casian', 'Cato', 'Celsus', 'Ennius', 'Gaius'
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
  'they have Distinctive Jewelry','they have Piercings','they have Flamboyant Clothes','they have Formal Clothes','they have Ragged Clothes','they have Pronounced Scar','they have Missing Teeth','they have Missing Fingers','they have an Unusual Eye Colour','they have Tattoos','they have a Birthmark','they have an Unusual Skin Colour','they are Bald',f'they have Braided {choice(beardHair)}','they have an Unusual Hair Colour','they have a Nerveous Eye Twitch','they have a Distinctice Nose','Distinctive Posture','Exceptionally Beautiful','Exceptionally Ugly']
talent=[
  'they Play Musical Instrument','they Speak Several Languages','they are Unbelivably Lucky','they have Perfect Memory','they are Great With Animals','they are Great With Children','they are Great at Solving Puzzles','they are Great at a Game','they are Great at Impersonations','they Draw Beautifully','they Paint Beautifully','they Sing Beautifully','they can Drink Everyone under the Table','they are an Expert Carpenter','they are an Expert Cook','they are an Expert Dart Thrower','they are an Expert Juggler','they are a Skilled Actor','they are a Master of Disguise','they are a Skilled Dancer',"they Know Thieves' Cant"]
mannerism=[
  f'they are Prone to {choice(singWhistle)} quietly','they Speak in Rhyme or Another Peculiar Way',f'they have a Particularly {choice(lowHigh)} Voice','they are a Lisp or Stutter','they Enunciates Overly Clearly','they Whisper','they Use Flowery Speech and Long Words','they Frequently Use the Wrong Word','they Use Colourful Oaths and Exclamations','they Make Constant Jokes and Puns','they are Prone to Predictions of Doom','they Fidget','they Squint a lot','they Stare into the Distance','they are always Chewing Something','they Pace around','they Tap their Fingers','they Bite their Fingernails','they Twirl their hair','they Tug their Beard']
interaction=[
'Argumentative','Arrogant','Blustering','Rude','Curious','Friendly','Honest','Hot Tempered','Irritable','Ponderous','Quiet','Suspicious']
ideal=[
  'Beauty','Charity','Greater Good','Life','Respect','Self-Sacrifice','Community','Fairness','Honor','Logic','Responsibility','Tradition','Balance','Knowledge','Live and let Live','Moderation','Neutrality','People','Domination','Greed','Might','Pain','Retribution','Slaughter','Change','Creativity','Freedom','Independence','No Limits','Whimsy','Aspiration','Discovery','Glory','Nation','Redemption','Power','Faith','Fairness','Friendship','Honesty','Might','Sincerity','Destiny','Generosity','Free Thinking','Family','Obligation','Nature','Self-Improvement','Mastery']
bond=[
  'are Dedicated to Fulfilling a Personal Life Goal','are Protective of a Close Family Member','are Protective of their Colleagues','are Loyal to their Benefactor','are Captivated by a Romantic Interest','are Drawn to a Special Place','are Protective of a Sentimental Keepsake','are Protective of a Valuable Possession','are Out For Revenge','Owe their Life to Someone','do Everything for the Common People','are Being Hunted','are Seeking Atonement for their Missdoings','are Protective of the Land']
flaw=[
  'posses Forbidden Love','Enjoys Decadent Pleasures','are Arrogant',"Envies Someone's Possesions",'are Greedy','are Prone to Rage','have a Powerful Enemy','have Specific Phobia','have a Shameful History','did a Secret Crime','are Foolhardy Bravery','Judge Others Harshly and Themself Even More Severly','Put to Much Trust into Authority','are Inflexible in Their Thinking','are Suspicious of others','are Obsessive','are Always in Debt','are Cowardly','are a Kleptomaniac','are Forgetfull','have a "Tell" that Shows When They are Lying','would do Anything for Fame','are quite Direct','Love to get Drunk','have Trust Issues','are Jealous','are Bloodthirsty','are Dogmatic','have a Need to Win Arguments','Like Keeping Secrets','Belive They are Better than Everyone','are Bitter','are Violent','belive in the Reign of the Strong','Natuarly Lie a Lot','are Seeking Knowledge','Follow Orders, even to the detriment of themself and others','are Pridefull']
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
Wname3 = [
    'Crab', 'Lion', 'Tiger', 'Wolf', 'Angel', 'Devil', 'Daemon', 'Demon',
    'Fiend', 'Hawk', 'Eagle', 'Elephant', 'Dragon', 'Ant', 'Spider','Eel','Pegasus','Pony','Stag','Lamb','Goat','Spirit','Undead','Eagle','Dog','Satyr'
]
factionName1=['School','Univeristy','Guild','Alliance','Church','Library','Inquisition','Kingdom','Order','Cult','Enclave','Society','Knights','Dicipline','Cabal']
shuffle(factionName1)
factionName21=[f'{choice(longName)}{choice(longName2)}{choice(longName3)}',f'{choice(Welement)}',f'the {choice(Wgem)}',f'the {choice(Wname3)}']
factionName22=[f'{choice(longName)}{choice(longName2)}{choice(longName3)}',f'{choice(Welement)}',f'the {choice(Wgem)}',f'the {choice(Wname3)}']
factionName23=[f'{choice(longName)}{choice(longName2)}{choice(longName3)}',f'{choice(Welement)}',f'the {choice(Wgem)}',f'the {choice(Wname3)}']
faction1=f'the {factionName1[0]} of {choice(factionName21)}'
faction2=f'the {factionName1[1]} of {choice(factionName22)}'
faction3=f'the {factionName1[2]} of {choice(factionName23)}'
factions=[faction1,faction2,faction3]

stats = [
    'Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom',
    'Charisma'
]
descriptor = [
    'strong', 'dextorous', 'tough', 'intelligent', 'wise', 'charismatic'
]
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
l = ['B', 'D', 'G', 'K', 'L', 'M', 'N', 'Q', 'R', 'T', 'H', 'X']
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
    'have a weak connection with', 'have a rivalry with', 'are persecuted by', 'are exiled from'
]
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
governorName=[
  'King/Queen','Prince/Princess','Emperor','Pharaoh','Chief','Elector','High Priest','Governor','Elderman','Duke','Baron','Arch Magus','President','Emperor','Chancellor','Count','Mayor','Lord/Lady','Consul','Magister','Warlord']
knownFor=[
  "delicious cuisine",'rude people','greedy merchants','artists and writers',f'great hero: {choice(firstName)}','flowers','hordes of beggars','tough warriors','dark magic','recent decadence','powerful piety',"people's gambling addiction",'lack of piety',"people's high level of education",'well known wines','well known fashion symbols','political intrigue','powerful guilds','strong drinks','extreme patriotism']
rulerStatus=[
  'Respected for their fairness','Respected for their justness','Feared as a horrible tyrant','Known as a easily manipulated weakling','Looked down upon as an illegitimate ruler','Controlled by a powerful monster','Unkown, but the rumours refer to a cabal of some sort','the one in power, but the throne has been contested for a long while, so they might not stay as that for much longer','the one in power as they resently seized the throne','known for being an aggressive idiot','on their deathbed, as many compete for the throne','known for being iron-willed']
calamity=[
  'suspected for a vampire infestation','the ground of a new cult who seeks converts',f'the area for the suspected murder of {choice(firstName)}',"the ground of a war between rivalling thieves' guilds",'the ground of a deadly plague','inhabited by {choice(firstName)} the powerful wizard','under the threat of corrupt officials','under the threat of marauding monsters','under an economic drought due to trade disruption','flooded multiple times over','under the threat of undead','prophecized to be inevitably doomed','on the brink of war','on the brink of complete anarchy due to internal strife','besiged by enemies','investigating a scandal that threatens powerful families','covered in adventures because of a recently discovered dungeon','under a struggle for power from religious sects']
a=randint(1,3)
if a != 1:
    racialRelation=['']
else:
    racialRelation=['and there are tension between the different cultures/races','and the cultural/racial majority rules the city','and the cultural/racial minority rare the rulers of the place','and the cultural/racial minority are refugees','and the cultural/racial majority oppresses the minority','and the cultural/racial minority oppresses the majority']    
residenceType=[
  'abandoned squat','middle-class home','upper-class home','crowded tenement','orphanage',"hidden slaver's den",'front for a secret cult','lavish guarded mansion']
religiousType=[
  'temple to a good diety','temple to a neutral diety','home of ascetics','abondoned shrine','library dedicated to religious study','hidden shrine to a fiend','hidden temple of a evil god',f'temple of a false diety led by the charlatan {choice(firstName)}']
tavernType=[
  'quiet, low-key bar','dirt-cheap hole',"thieves' guild hangout",'gathering place to the secret society','upper-class dining den',"specific guild's catery",'members-only club','brothel']
warehouseType=[
  'empty','heavily guarded','cheap','bulk','live animal','weapons','goods from a distant land','secret smugglers']
shopType=[
  'pawnshop','herbs store','fruits and vegetable shop','dried meat store','mortician store','bookstore','moneylender','weapons and armour store','candle shop','smithy',"carpenter's store","weaver's store",'jewelery store','bakery',"mapmaker's shop","tailor's shop","ropemaker's shop","mason's store",'scribe store','bucket shop']
element = [
  'fire', 'thunder', 'ice', 'lightning', 'psycic', 'radiant']
jewelryType=Wgem
adjectiveOther = [
  'silver','golden','staggering','laughing','prancing','gilded','running','howling','slaughtered','leering','drunken','leaping','roaring','frowning','lonely','wandering','mysterious','barking','black','gleaming'
]
relationship = [
    'friend', 'enemy', 'nemesis', 'lover', 'frenemy', 'firstborn child',
    'rival', 'companion', 'partner', 'distant cousin', 'apprentice'
]
feeling = [
    'love for', 'hate for', 'friendship with', 'rivalry with', 'pact with'
]
Welement2 = [
    'Invulerability', 'Invisibility', 'Blinking', 'Shielding', 'Fury',
    'Telepathy', 'Trueseeing', 'Resurrection', 'Might', 'Magi', 'Pure Good',
    'Pure Evil', 'Fear', 'Binding', 'Paralysis', 'Polymorph', 'Secrets',
    'Tentacles'
]
def newItem2():
    global item
    item = [
        f'{choice(texture)} {choice(clothingType)} {choice(clothingPiece)}',
        f'{choice(Wgem)} {choice(jewelryPiece)}',
        f'{choice(clothingType)} {choice(clothingPiece)}', f'{choice(trinket)}'
    ]


def randomNPC():
    #----------------------randomNPC--------
    global item
    global newName
    global ability
    global newRace
    global pointOfInterest
    global pointOfInterest1
    global pointOfInterest2
    global NPC

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

    NPC=f'{choice(newName)} the {choice(ability)} {choice(newRace)} {choice(occupation)}. They are always carrying their {choice(item)} wich they got from their {choice(relationship)}{choice(name)}. They {choice(alliance)} {choice(factions)}. {choice(newName)} grew up {choice(b)}. They are currently seeking {choice(goal)}. {choice(newName)} are very {personality[0]} and a bit {personality[1]}. They are {choice(age)}. Some other notable things about them are: {pointOfInterest1} and {pointOfInterest2}, they have a tendesy to be a bit {choice(interaction)}. Their greatest Ideal is: {choice(ideal)}. They {choice(bond)}, and {choice(flaw)}.'    

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
def newItem3():
  global item
  item = [
        f'{choice(clothingPiece)}',
        f'{choice(jewelryPiece)}',
        f'{choice(clothingPiece)}',
    ]

b=0
def randomBuilding():
    global building
    global adjective
    global item
    global b
    a=randint(1,20)

    if a == 1:
        shuffle(residenceType)
        building=(f'the {residenceType[b]} of {choice(firstName)}')
    elif a < 4:
        shuffle(religiousType)
        building=(f'the {religiousType[b]}')
    elif a < 6:
        shuffle(warehouseType)
        building=(f'the {warehouseType[b]} warehouse')
    elif a < 13:
        shuffle(shopType)
        building=(f'the {shopType[b]} of {choice(firstName)}')
    elif a < 20:
        shuffle(tavernType)
        newItem3()
        newAdjective()
        race4=[choice(race3),choice(race2),choice(race)]
        item.append(choice(Wname3))
        item.append(choice(race4))
        building=(f'{choice(adjective)} {choice(item)}, the {tavernType[b]} of {choice(firstName)}')
    b+=1

monster=[]
traits=[]
def monsterType():
  global monsterType1
  b=randint(1,100)
  if b < 30:
    monsterType1 = 'Humanoid'
  elif b < 40:
    monsterType1 = 'Beast'
  elif b < 50:
    monsterType1 = 'Monstrosity'
  elif b < 60:
    monsterType1 = 'Fiend'
  elif b < 70:
    monsterType1 = 'Undead'
  elif b < 80:
    monsterType1 = 'Fey'
  elif b < 81:
    monsterType1 = 'Celestial'
  elif b < 85:
    monsterType1 = 'Elemental'
  elif b < 88:
    monsterType1 = 'Construct'
  elif b < 90:
    monsterType1 = 'Dragon'
  elif b < 95:
    monsterType1 = 'Beast'
  elif b < 97:
    monsterType1 = 'Plant'
  elif b < 98:
    monsterType1 = 'Monstrosity'
  elif b <= 100:
    monsterType1 = 'Aberration'


def statsGenerator():
  global str
  global dex
  global con
  global int2
  global wis
  global cha
  global pb
  global ac
  global atk
  global dmg
  global save
  global hp
  global stats
  global stats2
  global monsterType1
  global primaryStat
  global primaryStat1
  global size
  global hp2
  
  if monsterType1 == 'Aberration':
      str = randint(6,14)
      dex = randint(6,15)
      con = randint(8,14)
      int2 = randint(9,16)
      wis = randint(2,14)
      cha = randint(2,14)
  elif monsterType1 == 'Beast':
      str = randint(4,19)
      dex = randint(4,19)
      con = randint(8,16)
      int2 = randint(1,12)
      wis = randint(2,16)
      cha = randint(4,14)
  elif monsterType1 == 'Celestial':
      str = randint(7,16)
      dex = randint(7,17)
      con = randint(9,14)
      int2 = randint(7,18)
      wis = randint(7,17)
      cha = randint(7,19)
  elif monsterType1 == 'Construct':
      str = randint(7,16)
      dex = randint(7,17)
      con = randint(9,14)
      int2 = randint(7,18)
      wis = randint(7,17)
      cha = randint(7,19)
  elif monsterType1 == 'Dragon':
      str = randint(4,19)
      dex = randint(4,19)
      con = randint(9,16)
      int2 = randint(1,12)
      wis = randint(2,16)
      cha = randint(4,14)
  elif monsterType1 == 'Elemental':
      str = randint(4,19)
      dex = randint(4,19)
      con = randint(8,16)
      int2 = randint(1,12)
      wis = randint(2,16)
      cha = randint(4,14)
  elif monsterType1 == 'Fey':
      traits.append('Fey Ancestory')
      str = randint(4,16)
      dex = randint(8,19)
      con = randint(8,14)
      int2 = randint(7,16)
      wis = randint(8,17)
      cha = randint(9,19)
  elif monsterType1 == 'Fiend':
      str = randint(6,17)
      dex = randint(6,17)
      con = randint(8,17)
      int2 = randint(6,17)
      wis = randint(6,17)
      cha = randint(6,17)
  elif monsterType1 == 'Giant':
      str = randint(12,19)
      dex = randint(4,15)
      con = randint(14,19)
      int2 = randint(5,13)
      wis = randint(5,13)
      cha = randint(5,13)
  elif monsterType1 == 'Humanoid':
      str = randint(6,17)
      dex = randint(6,17)
      con = randint(8,17)
      int2 = randint(6,17)
      wis = randint(6,17)
      cha = randint(6,17)
  elif monsterType1 == 'Monstrosity':
      str = randint(4,19)
      dex = randint(4,19)
      con = randint(8,16)
      int2 = randint(1,12)
      wis = randint(2,16)
      cha = randint(4,14)
  elif monsterType1 == 'Ooze':
      str = randint(4,19)
      dex = randint(4,19)
      con = randint(8,16)
      int2 = randint(1,12)
      wis = randint(2,16)
      cha = randint(4,14)
  elif monsterType1 == 'Plant':
      str = randint(4,17)
      dex = randint(4,17)
      con = randint(8,17)
      int2 = randint(1,15)
      wis = randint(2,16)
      cha = randint(4,14)
  elif monsterType1 == 'Undead':
      str = randint(6,17)
      dex = randint(6,17)
      con = randint(8,17)
      int2 = randint(3,13)
      wis = randint(3,13)
      cha = randint(3,13)

  str += cr/2
  if str.is_integer() == False:
    str-=0.5
  dex += cr/2
  if dex.is_integer() == False:
    dex-=0.5
  con += cr/2
  if con.is_integer() == False:
    con-=0.5
  int2 += cr/2
  if int2.is_integer() == False:
    int2-=0.5
  wis += cr/2
  if wis.is_integer() == False:
    wis-=0.5
  cha += cr/2
  if cha.is_integer() == False:
    cha-=0.5
  
  stats=[str,dex,con,int2,wis,cha]
  stats2=[str,dex,con,int2,wis,cha]

  for i in range(len(stats)):
      if stats[i]>11:
        stats[i]=(stats[i]-10)/2
        stats[i]+=0.0
        if stats[i].is_integer() == False:
          stats[i]-=0.5
      elif stats[i]==10:
        stats[i]=0
      elif stats[i]==11:
        stats[i]=0
      elif stats[i]<10:
        stats[i]=(stats[i]-10)/2
        if stats[i].is_integer() == False:
          stats[i]-=0.5

  monster.append(monsterType1)
  monster.append(stats2)

  size3=randint(0,2)
  size1=['small','medium','large']
  size2=[6,8,10]
  size=size1[size3]
  
  if cr < 5:
    pb=2
  elif cr < 9:
    pb=3
  elif cr < 13:
    pb=4
  elif cr < 17:
    pb=5
  elif cr < 21:
    pb=6
  elif cr < 25:
    pb=7
  elif cr < 29:
    pb=8
  else:
    pb=9
    
  ac = 10+stats[1]
  hp = randint(size2[size3],size2[size3]*(cr*3))+stats[2]*(cr*5)
  hp2 = (f'{cr*5}d{size2[size3]}+{stats[2]*(cr*5)}')
  if hp < 100:
    hp+=50
    hp2=(f'{hp2}+50')
  save = 13
  if str<dex:
      primaryStat=stats[1]
      primaryStat1='dex'
  else:
      primaryStat=stats[0]
      primaryStat1='str'
    


def giveTraits():
  global monsterName
  if monsterType1 == 'Humanoid':
    monsterName=choice(firstName)
    giveTraits1()
  elif monsterType1 == 'Fiend':
    monsterName=f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
    giveTraits1()
  elif monsterType1 == 'Undead':
    monsterName=f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
    giveTraits1()
  elif monsterType1 == 'Fey':
    monsterName=choice(firstName)
    giveTraits1()
  elif monsterType1 == 'Giant':
    monsterName=choice(Wname2)
    giveTraits1()
  else:
    o=randint(1,3)
    if o==1:
       monsterName=f'{choice(longName)}'
    elif o==2:
       monsterName=f'{choice(longName)}{choice(longName2)}'
    elif o==3:
       monsterName=f'{choice(longName)}{choice(longName2)}{choice(longName3)}'
    giveTraits2()

def giveTraits1():
  global traitFlying
  global traitWater
  global traitMonsterous
  global traitOther
  global traitInt
  global traitWis
  global traitCha
  global traitStr
  global traitDex
  global traitCon
  global str
  global dex
  global con
  global int2
  global wis
  global cha
  global primaryStat
  global primaryStat1
  global weapon
  global weaponDex
  global weaponStr
  global weaponNatural
  global weaponRanged
  b=randint(1,100)
  if b == 1:
    traits.append(choice(traitFlying))
    monster.append(f'Flyspeed {choice(speed)}ft')
  elif b == 2:
    traits.append(choice(traitWater))
  elif b < 20:
    traits.append(choice(traitMonsterous))
  elif b == 21:
    if wis >= 12:
      traits.append(choice(traitWis))
  elif b == 20:
    if int2 >= 12:
      traits.append(choice(traitInt))
  elif b == 22:
    if cha >= 12:
      traits.append(choice(traitCha))
  elif b == 23:
    if str >= 12:
      traits.append(choice(traitStr))
  elif b == 24:
    if dex >= 12:
      traits.append(choice(traitDex))
  elif b == 25:
    if con >= 12:
      traits.append(choice(traitCon))
  elif b < 70:
    traits.append(choice(traitOther))
  elif b < 90:
    traits.append('Multiattack')
  elif b == 100:
    for i in range(randint(2,5)):
      giveTraits1()

  b=randint(1,20)
  if b == 1:
    weapon=[choice(weaponNatural)]
  elif b < 6:
    weapon=[choice(weaponRanged)]
  elif b == 20:
    b=randint(1,20)
    if b == 1:
      weapon=[choice(weaponNatural)]
    elif b < 6:
        if primaryStat1 == 'str':
          weapon=[choice(weaponStr)]
        elif primaryStat1 == 'dex':
          weapon=[choice(weaponDex)]
        weapon=(f'{weapon} and {choice(weaponRanged)}')
    b=randint(1,20)
    if b == 1:
      weapon=[choice(weaponNatural)]
    elif b < 6:
      weapon=[choice(weaponRanged)]
  else:
    if primaryStat1 == 'str':
      weapon=[choice(weaponStr)]
    elif primaryStat1 == 'dex':
      weapon=[choice(weaponDex)]


  if primaryStat1 == 'str':
    weapon=[choice(weaponStr)]
  elif primaryStat1 == 'dex':
    weapon=[choice(weaponDex)]
  weapon=(f'{choice(weapon)} and {choice(weaponRanged)}')

def giveTraits2():
  global traitFlying
  global traitWater
  global traitMonsterous
  global traitOther
  global primaryStat
  global primaryStat1
  global weapon
  global weaponDex
  global weaponStr
  global weaponNatural
  global weaponRanged
  b=randint(1,20)
  if b == 1:
    traits.append(choice(traitFlying))
    monster.append(f'Flyspeed {choice(speed)}ft')
  elif b == 2:
    traits.append(choice(traitWater))
  elif b < 7:
    traits.append(choice(traitOther))
  elif b < 15:
    traits.append(choice(traitMonsterous))
  elif b < 17:
    traits.append('Multiattack')
  elif b == 20:
    for i in range(randint(2,5)):
      giveTraits2()

  b=randint(1,50)
  if b < 30:
    weapon=[choice(weaponNatural)]
  elif b < 49:
    weapon=[choice(weaponNatural1)]
  else:
    if int2 > 6:
      if primaryStat1 == 'str':
        weapon=[choice(weaponStr)]
      elif primaryStat1 == 'dex':
        weapon=[choice(weaponDex)]
    else:
      weapon=[choice(weaponNatural)]

def givePersonality():
  b=randint(1,3)
  if b == 1:
    monster.append(choice(appearance))
    monster.append(choice(talent))
  elif b == 2:
    monster.append(choice(mannerism))
    monster.append(choice(talent))
  elif b == 1:
    monster.append(choice(appearance))
    monster.append(choice(mannerism))

  monster.append(choice(interaction))
  monster.append(choice(ideal))
  monster.append(choice(bond))
  monster.append(choice(flaw))
  
cr=5

monsterType()
statsGenerator()
  
ranger = cr/2
if ranger.is_integer() == False:
    ranger+=0.5

ranger=int(ranger)
alignment=['Lawful','Neutral','Chaotic']
alignment1=['Good','Neutral','Evil']
speed=[20,30,40,50,60]
underWater=['fin','gills']
damageType1=['Frost','Fire','Psycic','Thunder','Force','Lightning','Acid','Poison']
damageType=['Slashing','Piercing','Bludgeoning']

traitOther=[
  'Aggressive','Ambusher',f'Magic Weapon({cr}d6 {choice(damageType1)})','Avoidance','Blindsense','Blood Frenzy','Brute','Charge','Charm','Enlarge','Reduce','Grappler','Leadership','Martial Advantage','Mimicry','Nimble Escape','Pack Tactics','Parry','Pounce','Rampage','Reckless','Redirect Attack','Relentless','Siege Monster','Arcane Spellcasting','Standing Leap','Steadfast','Sure-footed','Surprise Attack','Wounded Fury','Relentless Endurance','Deflect Missile','Uncanny Dodge','Sneak Attack',f'Second Wind (1d10+{cr})','Luck','Taunt','Mental Resistance','Telepathic','Psionic Spellcasting','Sorcery','Divine Spellcasting',f'Armour (Leather, ac={11+stats[1]})',f'Armour (Chain Shirt, ac={13+stats[1]})',f'Armour (Breastplate, ac={14+stats[1]})',f'Armour (Chainmail, ac={16})',f'Armour (Plate, ac={18})',f'Shield (ac={ac+2})']
traitMonsterous=[
  f'Breath Weapon({cr}d6 {choice(damageType1)})','Chameleon Skin','Change Shape','Constrict','Damage Absorption','Damage Transfer','Death Burst','Enhanced Sight (See through magical darkness)','Echolocation',f'Elemtental Body ({cr}d8 {choice(damageType1)})','False Appearance','Etherealness','Frightful Presence','Illumination','Illusory Appearance','Immutable Form','Incorporeal Movement','Innate Spellcasting','Inscrutable','Invisibility','Keen Senses','Labyrinthine Recall','Life Drain','Light Sensitivity','Magic Resistance','Otherworldy Perception','Possesion','Reactive','Read Thoughts','Regeneration','Rejuvination','Shadow Stealth','Shapechanger','Slippery','Spiderclimb','Stench','Sunlight Sensitivity','Superior Invisibility','Swallow','Teleport','Terrain Camouflage','Tunneler','Two Heads','Overwelming Fortitude','Web','Tree Stride','Spiky','Stunning Shriek','Shadowblend','Hypnosis','Antimagic Ward',f'{choice(damageType1)} Absorption','Antimagic Susceptibility','Crushing Hug','Adhesive','Swallow',f'Natural Armour (hide, ac={ac+1})',f'Natural Armour (fur, ac={ac+2})',f'Natural Armour (scales, ac={ac+3})',f'Natural Armour (ac={ac+ranger})']
traitWater=['Amphibious','Hold Breath']
traitFlying=['Dive Attack','Flyby']
traitLegendary=['Legendary Resistance','Legendary Actions','Lair']
traitStr=['Crushing']
traitDex=['Blurred Movement', 'Evasion']
traitCon=[f'Tough Defence (ac={ac+stats[2]})']
traitInt=[f'Knowing Defence (ac={ac+stats[3]})',f'Arcane Ward ({cr*stats[3]} temp hp)']
traitWis=[f'Wise Defence (ac={ac+stats[4]})',f'Psychic Ward ({cr*stats[4]} temp hp)']
traitCha=[f'Suave Defence (ac={ac+stats[5]})']

weaponStr=[
  'Unarmed Strike','Club','Greatclub','Handaxe','Javelin','Lighthammer','Mace','Quarterstaff','Sickle','Spear','Battleaxe','Glaive','Greataxe','Greatsword','Halberd','Lance','Longsword','Maul','Morningstar','Pike','Trident','War pick','Warhammer']
weaponDex=['Unarmed Strike','Dagger','Rapier','Scimitar','Shortsword','Whip']
weaponRanged=['Light Crossbow','Dart','Shortsword','Sling','Blowgun','Hand Crossbow','Heavy Crossbow','Longbow','Net']
weaponNatural=['Tentacles','Bite','Claws','Hooves','Horn','Tail','Sting']
weaponNatural1=['Slam','Fist','Tusk','Beak','Hook','Spike','Pseudopod','Ram','Mandibles']

phobia=['darkness','heights','flying','pain','open spaces or crowds','needles or pointed objects','riding on a horse','choking','flowers','being touched','spiders','numbers','thunder and lightning',
        'disorder or untidiness','imperfection','failure','human-like figures','being alone','sickness','stairs or steep slopes','amphibians','books','plants','ugliness','being ridiculed','mirrors','snow',
        'clocks','time','confined spaces','dogs','trees','accidents','cats','insects','teenagers','horses','speaking in public','blood','reptiles','water','insects','large things','small things','death or dead things',
        'the night','the dark','rain','birds','snakes','paper','love','flying','fire','being stared at','the full moon','speed','magic','witches and witchcraft','animals']

beardHair=['Beard','Hair']
singWhistle=['Singing','Whisteling','Humming']
lowHigh=['Low','High']
appearance=['they have Distinctive Jewelry','they have Piercings','they have Flamboyant Clothes','they have Formal Clothes','they have Ragged Clothes','they have a Pronounced Scar','they have Missing Teeth','they have Missing Fingers','they have an Unusual Eye Colour','they have Tattoos','they have a Birthmark','they have an Unusual Skin Colour','they are Bald',f'they have Braided {choice(beardHair)}','they have an Unusual Hair Colour','they have a Nerveous Eye Twitch','Dthey have a Distinctice Nose','they have a Distinctive Posture','they are Exceptionally Beautiful','they are Exceptionally Ugly']
talent=['they Play a Musical Instrument','they Speak Several Languages','they are Unbelivably Lucky','they have a Perfect Memory','they are Great With Animals','they are Great With Children','they are Great at Solving Puzzles','they are Great at a Game','they are Great at Impersonations','they Draw Beautifully','they Paint Beautifully','they Sing Beautifully','they can Drink Everyone under the Table','they are an Expert Carpenter','they are an Expert Cook','they are an Expert Dart Thrower','they are an Expert Juggler','they are a Skilled Actor','they are a Master of Disguise','they are a Skilled Dancer',"they Know Thieves' Cant"]
mannerism=[f'they are Prone to {choice(singWhistle)} quietly','they Speak in Rhyme or Another Peculiar Way',f'they have a Particularly {choice(lowHigh)} Voice','they have a Lisp or Stutter','they Enunciate Overly Clearly','they Whisper','they Use Flowery Speech and Long Words','they Frequently Use the Wrong Word','they Use Colourful Oaths and Exclamations','they Make Constant Jokes and Puns','they are Prone to Predictions of Doom','they are always Fidgeting on something','they Squint their eyes','they always Stare into the Distance','they are always Chewing on Something','they Pace around','they Tap their Fingers','they Bite their Fingernails','they Twirl their hair','they Tug their Beard']
interaction=['Argumentative','Arrogant','Blustering','Rude','Curious','Friendly','Honest','Hot Tempered','Irritable','Ponderous','Quiet','Suspicious']
ideal=['Beauty','Charity','Greater Good','Life','Respect','Self-Sacrifice','Community','Fairness','Honor','Logic','Responsibility','Tradition','Balance','Knowledge','Live and let Live','Moderation','Neutrality','People','Domination','Greed','Might','Pain','Retribution','Slaughter','Change','Creativity','Freedom','Independence','No Limits','Whimsy','Aspiration','Discovery','Glory','Nation','Redemption','Power','Faith','Fairness','Friendship','Honesty','Might','Sincerity','Destiny','Generosity','Free Thinking','Family','Obligation','Nature','Self-Improvement','Mastery']
bond=['are Dedicated to Fulfilling a Personal Life Goal','are Protective of a Close Family Member','are Protective of Colleagues','are Loyal to their Benefactor','are Captivated by a Romantic Interest','are Drawn to a Special Place','are Protective of a Sentimental Keepsake','are Protective of a Valuable Possession','are Out For Revenge','Owe their Life to Someone','do Everything for the Common People','are Being Hunted','are Seeking Atonement for their Missdoings','are Protective of the Land']
flaw=['they partake in Forbidden Love','they Enjoy Decadent Pleasures','they are Arrogant',"they Envy Someone's Possesion",'they are Greedy','they are Prone to Rage','they have a Powerful Enemy',f'they have a Phobia for {choice(phobia)}','they have a Shameful History','they commited a Secret Crime','they are in the Possesion of Forbidden Lore','they are Foolhardedly Brave','they Judge Others Harshly and Themself Even More Severly','they Put to Much Trust into Authority','they are Inflexible in Their Thinking','they are Suspicious of everyone','they are Obsessive','they are Always in Debt','they are Cowardly','they are a Kleptomaniac','they are Forgetfull','they have a "Tell" that Shows When They are Lying','they would do Anything for Fame','they are Direct','they Love to get Drunk','they have Trust Issues','they are Jealous','they have a Bloodthirst','they are Dogmatic','they have a Need to Win Arguments','they Like Keeping Secrets','they Belive They are Better than Everyone','they are quite Bitter','they are Violent','they belive in the Reign of the Strong','they Natuarly Lies a Lot','they are Seeking Knowledge','they Follow Orders','they are Pridefull']

def run():
    for i in range(ranger):
        giveTraits()
    monster.append(f'{hp}hp ({hp2})')
    monster.append(size)
    if traits==[]:
        print()
    else:
        for i in range(len(traits)):
            monster.append(traits[i])
    monster.append(choice(weapon))
    monster.append(f'+{primaryStat+pb} to hit')

    if monsterType1 == 'Humanoid':
        givePersonality()
    elif monsterType1 == 'Fiend':
        givePersonality()
    elif monsterType1 == 'Undead':
        givePersonality()
    elif monsterType1 == 'Fey':
        givePersonality()
    elif monsterType1 == 'Humanoid':
        givePersonality()
    elif monsterType1 == 'Giant':
        givePersonality()


    townName=f'{choice(townName1)}{choice(townName2)}'

    print(f'Welcome to {townName}. A city filled with wonder.')
    randomNPC()
    print(f'Their leader is {choice(governorName)} {choice(newName)} the {choice(ability)} {choice(newRace)}. They have recently been making dealings with {choice(factions)}. Some other notable things about them are: {pointOfInterest1} and {pointOfInterest2}, they have a tendesy to be a bit {choice(interaction)}. Their greatest Ideal is: {choice(ideal)}. They {choice(bond)}, and they {choice(flaw)}.')
    print(f'{choice(newName)} is currently {choice(rulerStatus)}.')
    print(f'The City has resently been {choice(calamity)}, {choice(racialRelation)}')
    randomBuilding()
    print(f'Some interesting buildings in this city are:')
    for i in range(randint(2,5)):
        randomBuilding()
        print(building)
    print(f'The city is known for their {choice(knownFor)}.')
    print(f'Some notable people within {townName} is:')
    for i in range(randint(2,5)):
        randomNPC()
        print(NPC)

    print(f'{monsterName} is also around {townName}')
    print(*monster, sep=', ')

