from datetime import datetime
import json

with open("match_list.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)


with open("alt_names.json", mode="r", encoding="utf-8") as read_file:
    alt_names = json.load(read_file)

winners_count = {}
leaders_count = {}
most_wins = 0
currentLeader = ""

for match in data:
    if 'Winner' in match and match['Winner'] != 'Tie':
        if match['Winner'] in alt_names:
            name = alt_names[match['Winner']]
        else:
            name = match['Winner']


        if name not in winners_count:
            winners_count[name] = 1
        else:
            winners_count[name] += 1

        # if winners_count[match['Winner']] > most_wins and currentLeader != match['Winner']:
        #     most_wins = winners_count[match['Winner']]
        #     currentLeader = match['Winner']
            # print(str(most_wins) + ' ' + match['Winner'] + ' ' + match['Date of match'])


def winners_sorted(winners_count):
    sorted_list_of_tuples = sorted(
        winners_count.items(),
        key=lambda item: item[1],
        reverse=True
    )

    sorted_winners_count = dict(sorted_list_of_tuples)

    return sorted_winners_count

winners_count = winners_sorted(winners_count)
#
# for winner, count in winners_count.items():
#     print(winner + ": " + str(count))
#
# print(len(winners_count))

# for match in data:
#     if match['Winner'] == 'Aston Villa' or match['Winner'] == 'Blackburn Rovers':
#         print(match['Match no.'] + ' ' + match['Winner'] + ' ' + match['Date of match'])

# prev_winner = None
# for match in data:
#     if match['Winner'] == 'FC Barcelona' and prev_winner != 'FC Barcelona':
#         print(match['Date of match'])
#     if match['Winner'] != 'Tie':
#         prev_winner = match['Winner']

# print(list(winners_count.keys()))

winners_from_website_list = ["Aston Villa", "Ipswich Town", "Blackburn Rovers", "Sevilla Atletico", "Everton",	"RC Lens B",
                             "Arsenal", "CD Castellon", "Burnley", "FK Spartak Subotica", "Preston North End", "NK Osijek",
                             "Sunderland", "TuRa Ludwigshafen", "Sheffield United", "FC St Pauli", "Bolton Wanderers",
                             "FC Girondins de Bordeaux", "West Bromwich Albion", "Besancon Football", "Liverpool",
                             "Jugovinil Kastel Gomilica", "Manchester United", "UD Las Palmas", "Wolverhampton Wanderers",
                             "Granada CF", "Bayer 04 Leverkusen", "FC Villefranche", "FC Bayern Munich", "US Sarre-Union",
                             "Newcastle United", "FSV Schifferstadt", "Real Madrid CF", "Alemannia Aachen", "Huddersfield Town",
                             "FK Novi Sad", "FC Barcelona", "Elche CF", "Middlesbrough", "FVgg Mombach", "Chelsea",
                             "Besiktas JK", "Birmingham City", "Unio Esportiva Lleida", "Derby County", "JSCBA Nimes",
                             "Sheffield Wednesday", "NK Varteks Varazdin", "West Ham United", "CD Badajoz", "Manchester City",
                             "Kisvarda FC", "Tottenham Hotspur", "Tennis Borussia Berlin", "Bury", "Real Sporting de Gijon",
                             "Notts County", "FK Proleter Zrenjanin", "Stoke City", "Exeter City", "FC Basel", "Etoile Carouge FC",
                             "Nottingham Forest", "AS Cannes", "Portsmouth", "FC Briolet", "Leicester City", "AC Ajaccio",
                             "CE Palavas", "ES Paulhan Pezenas", "Grasshoppers", "Szeged-Csanád Grosics Akadémia", "Millwall",
                             "US Turcs Bischwiller", "Borussia Dortmund", "Union Sportive de Valenciennes Anzin", "Valencia CF",
                             "AJ Auxerre B", "Galatasaray SK", "RC Strasbourg Alsace", "Bristol City", "AS Lyon Duchere",
                             "FC Zurich", "Tours FC", "Blackpool", "SM Caen", "Cardiff City", "US Reipertswiller",
                             "Hamburger SV", "VfR Frankenthal", "Paris Saint-Germain FC", "NK Omis", "Queen's Park Rangers",
                             "FK Velez Mostar", "Nimes Olympique", "Brighton & Hove Albion", "FK Vojvodina", "AS Beauvais Oise",
                             "Wanderers", "FC Rouen 1899", "Servette Geneve", "Stade Rennais FC", "FC Kaiserslautern",
                             "SV St. Ingbert", "RC Deportivo de la Coruna", "CA Osasuna", "Eintracht Frankfurt", "OGC Nice",
                             "Leeds United", "FC Sochaux B", "Old Etonians", "NK Dinara Knin", "Palamos CF", "FCO Dijon",
                             "Atletico Madrid", "Aldershot", "Bradford City", "SC Bastia", "FK Pirmasens", "Chesterfield",
                             "AF Lozere", "FK Sloboda Tuzla", "Trabzonspor", "Doncaster Rovers", "Real Betis Balompie",
                             "HNK Jadran Kaštel Sućurac", "Charlton Athletic", "NK Omladinac Vranjic", "Real Zaragoza",
                             "Rot Weiss Ludenscheid", "BSC Young Boys", "Gillingham", "FC Saarbrucken", "FC Schalke 04",
                             "HNK Rijeka", "Canet Roussillon B", "Sevilla FC", "Berliner FC Dynamo", "Plymouth Argyle",
                             "Olympique Lyonnais B", "NK Junak Sinj", "ES Uzes", "FC Barcelona B", "Rot Weiss Oberhausen",
                             "NK Neretva", "NK Olimpija Ljubljana", "FK Sarajevo", "Rot Weiss Essen", "Pau FC",
                             "Monts d'Or Azergues Chasselay", "SR Colmar", "Club Gimnastic de Tarragona", "Real Sociedad",
                             "SC Selongey", "SAS Epinal", "CD San Fernando", "ASM Belfort", "NK Radnik Velika Gorica",
                             "AC Milan", "Wimbledon", "Red Star Belgrade", "Como 1907", "Reading", "Paksi FC", "FC Martigues",
                             "Evian Thonon Gaillard FC", "RCD Espanyol", "Boluspor", "Luton Town", "Deportivo Alaves",
                             "Grimsby Town", "AC Sparta Prague", "Southampton", "FC Dinamo Bucharest", "Port Vale",
                             "OFK Kikinda", "DSC Arminia Bielefeld", "NK Dinamo Vinkovci", "OC Perpignan", "Motril CF",
                             "AS Perpignan Mediterranee", "TSG 1899 Hoffenheim", "Borussia Neunkirchen", "Queen's Park, Glasgow",
                             "1. FC Koln", "FC Limonest Saint-Didier", "Oldham Athletic", "AEC St-Gilles", "RCD Mallorca",
                             "VfL Osnabruck", "FC St Gallen", "Aydinspor", "Jerez CF", "AS Beziers B", "Atalanta BC",
                             "CE L'Hospitalet", "Dinamo Zagreb", "Alicante CF", "Westfalia Herne", "FC Kaiserslautern Amateure",
                             "UD Melilla", "AD Ceuta FC", "Hull City", "NK Merkator Ljubljana", "ASV Landau 1946", "Holstein Kiel",
                             "VfB Stuttgart", "CF Ciudad de Murcia", "SV Werder Bremen", "Berliner SV 92", "Real Oviedo",
                             "SD Eibar", "Fulham", "FC Lugano", "Bradford (Park Avenue)", "Terrassa FC", "Real Valladolid",
                             "Talavera CF", "Eintracht Trier", "Viktoria 89 Berlin", "Cordoba CF", "Torquay United",
                             "Toulouse FC", "VfR Baumholder", "FK Vardar", "NK Orkan Dugi Rat", "Radnicki Nis", "Croydon Common",
                             "FC Nantes", "Spartak Moscow", "Crystal Palace", "Trebes FC", "Hajduk Split", "Altay SK",
                             "Northampton Town", "Zalaegerszegi TE", "Hertha BSC", "NK Jedinstvo Bihac", "Swindon Town",
                             "Tranmere Rovers", "Fortuna Dusseldorf", "Burgos CF", "MTK Budapest FC", "GOSK Jug", "AS Monaco",
                             "Entente St Clement Montferrier", "Kettering Town", "VfR Wormatia Worms", "UJA Alfortville",
                             "NK Zadar", "Stade Lavallois Mayenne FC", "SG Wattenscheid 09", "FC Sete 34", "Wuppertaler SV",
                             "AS Saint-Etienne", "Credobus Mosonmagyarovar", "HNK Val Kastel Stari", "Hercules de Alicante CF",
                             "Racing Club Strasbourg B", "US Carcassonne", "Tasmania 1900 Berlin", "NK Omladinac Zadar",
                             "Borussia Moenchengladbach", "Debreceni VSC", "Fenerbahce SK", "Bayer Uerdingen",
                             "FK Zeljeznicar Sarajevo", "FC Mulhouse", "Neuchatel Xamax", "SV Saar 05 Saarbrucken",
                             "RC Celta de Vigo", "CD Tenerife", "SC Fortuna Koln", "FC Winterthur", "NK Solin",
                             "FC La Chaux-de-Fonds", "RC Lens", "SK Sigma Olomouc", "Real Sociedad B", "IFK Norrkoping",
                             "USL Dunkerque", "FC Istres", "La Clermontaise", "Le Havre AC", "NK DOSK Drnis", "HNK Velebit Benkovac",
                             "AS Frontignan AC", "Diosgyori VTK", "Jura Sud Foot", "Poli Ejido 2012 Sociedad Deportiva",
                             "Villareal CF", "Mezokovesd Zsory SE", "Stade Brestois 29", "FC Dahn 1913", "RCD Mallorca B",
                             "CD Logrones", "Partizan Belgrade", "Le Puy Foot 43 Auvergne", "Real Murcia", "FC Metz", "AJ Auxerre",
                             "Budapest Honved", "Athletic Club de Bilbao", "Renton", "Newport County", "NK Mura Murska Sobota",
                             "Ferencvaros TC", "Endesa Andorra", "Watford", "Juventus", "Real Racing Club de Santander",
                             "Rodez AF", "Barnsley", "Slavia Prague", "Clapham Rovers", "FK Jedinstvo Brcko", "NK Zagreb",
                             "1. FC 03 Sobernheim", "Slaven Trogir", "MJC Gruissan", "Dundee United", "AS Atlas Paillade",
                             "UE Figueres", "Dynamo Dresden", "Paris FC", "Olympique de Marseilles", "Sportfreunde Saarbrucken",
                             "AS Roma", "Oxford University", "NK Istra Pula", "AS Beziers", "FK Teteks Tetovo",
                             "FC Montceau Bourgogne", "OGC Nice B", "Xerez CD", "ASC Bas-Vernet", "UD Almeria", "Stade Montois",
                             "Norwich City", "Sariyer SK", "Merida UD", "SC Toulon", "SV Niederlahnstein", "FK Galenika Zemun",
                             "UD Logrones", "VfB Theley", "Southend United", "UP Plasencia", "Cadiz CF", "Lille OSC",
                             "Eintracht Braunschweig", "US Conques", "Brentford", "FK Leotar", "Bristol Rovers", "Real Betis B",
                             "Blackburn Olympic", "FC Sochaux-Montbeliard", "AS Marck", "CF Cala Millor", "Old Carthusians",
                             "Frejus St Raphael", "Royal Engineers", "Phoenix Bellheim", "ESTAC Troyes B", "SV Sodingen",
                             "Valencia CF Mestalla", "Racing Club de France", "Gazelec FC Ajaccio", "La Grande Motte",
                             "NK Celik Zenica", "Montpellier Herault SC B", "Montpellier Herault SC", "Wellingborough Town",
                             "CD Leganes", "Moralo CP", "US Orleans", "FC Dinamo Tblisi", "HNK Sibenik", "NK Maribor",
                             "Football Bourg-en-Bresse", "Bakirkoy SK", "Ujpest FC", "FC Bagnols Pont", "Albacete Balompie",
                             "Red Star FC 93", "Rotherham United", "Swifts", "SD Compostela", "CD Lugo", "Coventry City",
                             "FC St-Louis Neuweg", "FC Lausanne Sports", "FK Borac Banja Luka", "Phonix Ludwigshafen",
                             "Karsiyaka SK", "Rayo Vallecano de Madrid", "Stade Balarucois", "AS Nancy", "Great Marlow",
                             "CSO Amneville", "Olympique Lyonnais", "Swansea City", "DSC Wanne-Eickel", "FC Sion", "Old Forresters",
                             "Accrington", "L'Entente SSG", "Leyton Orient", "FK Buducnost Podgorica", "Walsall", "Gallia C d'Uchaud",
                             "NK Bagat Zadar", "TuS Neuendorf", "Germania Metternich", "FC Grenchen", "SSC Napoli",
                             "US Creteil-Lusitanos", "FCSR Haguenau B", "Lincoln City", "SG Union Solingen",
                             "US Quevilly-Rouen Metropole", "MSV Duisburg", "SO Cassis Carnoux", "AS Canet",
                             "Eintracht Bad Kreuznach",	"Chamois Niortais FC", "RNK Zmaj Makarska", "AFC Bournemouth",
                             "Genclerbirligi SK", "Getafe CF", "SC Ludwigshafen", "Avenir Sportif Rousson", "RB Leipzig",
                             "AS Pierrots Vauban Strasbourg", "SC Preussen Munster", "AS Monaco B", "FC Biel-Bienne",
                             "Narbonne Football", "NK Metalac Sibenik", "Dos Hermanas CF", "BSC Oppau", "Wacker 04 Berlin",
                             "1. FC Nuremberg", "Spandauer SV", "SV Weisenau", "AS Nancy B", "Glossop North End", "US Raon-l'Etape",
                             "FSV Mainz 05", "Castelnau Cres FC", "VfL Bochum", "NK Troglav 1918 Livno", "CS Chenois",
                             "RNK Split", "ACF Fiorentina"]

# for team in list(winners_count.keys()):
#     if team in winners_from_website_list:
#         continue
#     print(team)
# 
# print("--------------")
# for team in winners_from_website_list:
#     if team in list(winners_count.keys()):
#         continue
#     print(team)
date_format = '%d/%m/%Y'
champion_match_count = {}
champion_time_count = {}
reign_count = {}
current_champion = None
current_starttime = None
for match in data:
    if match['Winner'] in alt_names:
        name = alt_names[match['Winner']]
    else:
        name = match['Winner']


    if current_champion is None:
        current_champion = name
        current_starttime = datetime.strptime(match['Date of match'], date_format)
        champion_match_count[name] = 0
        champion_time_count[name] = 0
        reign_count[name] = 1
        continue

    if name == 'Tie' or current_champion == name:
        champion_match_count[current_champion] += 1
        continue

    if current_champion != name:
        champion_match_count[current_champion] += 1
        endtime = datetime.strptime(match['Date of match'], date_format)
        champion_time_count[current_champion] += (endtime - current_starttime).days

        current_champion = name
        current_starttime = datetime.strptime(match['Date of match'], date_format)
        if name not in champion_match_count:
            champion_match_count[name] = 0
            champion_time_count[name] = 0
            reign_count[name] = 1
        else:
            reign_count[name] += 1


endtime = datetime.now()
champion_time_count[current_champion] += (endtime - current_starttime).days

champion_match_count = winners_sorted(champion_match_count)
champion_time_count = winners_sorted(champion_time_count)
reign_count = winners_sorted(reign_count)

# for team, count in champion_match_count.items():
#     print(team + ": " + str(count))
#
# print("----------------------------------------------")
#
# for team, count in champion_time_count.items():
#     print(team + ": " + str(count))


# for team, count in reign_count.items():
#     print(team + ": " + str(count))
