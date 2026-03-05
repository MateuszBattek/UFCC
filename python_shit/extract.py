from bs4 import BeautifulSoup
import re
import json

def getWinner(score):
    goalsList = score.split('-')
    goalsHome = int(goalsList[0])
    goalsAway = int(goalsList[1])
    if goalsHome > goalsAway:
        winner = 1
    elif goalsHome < goalsAway:
        winner = 2
    else:
        winner = 0

    return winner

def parse_fa_cup_table(html_content):
    """
    Parsuje tabelę FA Cup i zwraca listę słowników z danymi meczów.

    Args:
        html_content (str): Treść HTML zawierająca tabelę.

    Returns:
        list: Lista słowników, gdzie każdy słownik reprezentuje mecz.
    """
    # Używamy BeautifulSoup do parsowania HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Lokalizujemy główną tabelę
    table = soup.find('table')

    if not table:
        return []

    # Definiujemy pozycje (indeksy) dla interesujących nas kolumn,
    # bazując na strukturze komórek <td> w wierszach <tr>.
    # W oryginalnym nagłówku: Match no., Date of match, Home, Score, Away, Competition, Venue
    # Wiersze danych wyglądają tak:
    # [Match no., Date, (img), Home, Score, Away, (img), Competition, Venue]
    # Indeksy <td>: 0, 1, 2, 3, 4, 5, 6, 7, 8

    # Nagłówki, które chcemy zachować
    headers = [
        "Match no.",
        "Date of match",
        "Home",
        "Score",
        "Away",
        "Competition",
        "Venue"
    ]

    # Indeksy kolumn <td> odpowiadające nagłówkom w wierszach z danymi
    column_indices = [0, 1, 3, 4, 5, 7, 8]

    match_data = []

    # Iterujemy przez wiersze tabeli, pomijając pierwszy wiersz (nagłówki)
    rows = table.find_all('tr')

    prev_winner = None
    # Zaczynamy od drugiego wiersza (indeks 1), bo pierwszy to nagłówki
    for row in rows[1:]:
        cells = row.find_all('td')

        if len(cells) < 9:  # Oczekujemy co najmniej 9 komórek w wierszu danych
            continue

        match_entry = {}

        for i, header in enumerate(headers):
            cell_index = column_indices[i]
            cell = cells[cell_index]


            # Ekstrakcja tekstu z komórki i czyszczenie białych znaków oraz zbędnego HTML
            text = cell.get_text(strip=True)

            # Wyczyść ewentualne podziały linii i nadmiarowe spacje wewnątrz komórki
            text = re.sub(r'\s+', ' ', text).strip()

            match_entry[header] = text



        # Add winner column
        pattern = re.compile("^[0-9]+-[0-9]+$")
        pattern2 = re.compile("[0-9]+-[0-9]+")

        if pattern.match(match_entry['Score']):
            winner = getWinner(match_entry['Score'])
            if winner == 1:
                match_entry['Winner'] = match_entry['Home']
            elif winner == 2:
                match_entry['Winner'] = match_entry['Away']
            elif winner == 0:
                match_entry['Winner'] = 'Tie'
        elif match_entry['Score'] == "w/o":
            match_entry['Winner'] = prev_winner
        elif 'aet' in match_entry['Score'] and not 'pens' in match_entry['Score']:
            winner = getWinner(re.search(pattern2, match_entry['Score']).group(0))
            if winner == 1:
                match_entry['Winner'] = match_entry['Home']
            elif winner == 2:
                match_entry['Winner'] = match_entry['Away']
            elif winner == 0:
                match_entry['Winner'] = 'Tie'
        elif 'pens' in match_entry['Score']:
            winner = getWinner(re.findall(pattern2, match_entry['Score'])[1])
            if winner == 1:
                match_entry['Winner'] = match_entry['Home']
            elif winner == 2:
                match_entry['Winner'] = match_entry['Away']
            elif winner == 0:
                match_entry['Winner'] = 'Tie'
        # elif match_entry['Score'] == 'tbc':
        #     match_entry['Winner'] = prev_winner

        # Special cases
        if match_entry['Home'] == "Jura Sud Foot(Jura won the tie as they appeared in the 6eme tour)":
            match_entry['Home'] = 'Jura Sud Foot'
            match_entry['Winner'] = match_entry['Home']
            match_entry['Extra_info'] = "(Jura won the tie as they appeared in the 6eme tour)"
        elif match_entry['Match no.'] == '4671':
            match_entry['Winner'] = 'US Sarre-Union'
        elif match_entry['Match no.'] == '4683':
            match_entry['Winner'] = 'US Turcs Bischwiller'
        elif match_entry['Match no.'] == '3053':
            match_entry['Winner'] = 'Tie'
        elif match_entry['Match no.'] == '3864':
            match_entry['Score'] = '2-3'
            match_entry['Winner'] = match_entry['Away']



        if 'Winner' in match_entry and match_entry['Winner'] != 'Tie':
            prev_winner = match_entry['Winner']
        # Dodajemy wiersz do listy
        match_data.append(match_entry)

    return match_data


# --- Część wykonawcza ---

match_list = list()

for i in range(15):
    f = open(f"list{i+1}.txt")
    html_input = f.read()
    match_list += parse_fa_cup_table(html_input)

print(len(match_list))

with open('match_list.json', 'w', encoding='utf-8') as f:
    json.dump(match_list, f, ensure_ascii=False, indent=4)