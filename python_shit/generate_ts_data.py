"""
Script to generate a TypeScript data file (data.ts) from match_list.json,
alt_names.json, and teams_geo_info.json.

Produces arrays:
  - clubs:        { id, name, country, city }
  - alt_names:    { id, alt_name, club_id }
  - stadiums:     { id, name, country, city, capacity }
  - competitions: { id, name, type, round, add_info }
  - matches:      { id, date, home_club_id, away_club_id, home_goals, away_goals, score_add_info, winner_club_id, competition_id, stadium_id }
  - players:      { id, name, last_name, nationality, position }
  - goals:        { id, match_id, club_id, player_id, minute, penalty, own_goal }
"""

import json
import uuid
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MATCH_LIST_PATH = SCRIPT_DIR / "match_list.json"
ALT_NAMES_PATH = SCRIPT_DIR / "alt_names.json"
GEO_INFO_PATH = SCRIPT_DIR / "teams_geo_info.json"
OUTPUT_PATH = SCRIPT_DIR / "data.ts"


def load_json(path: Path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def make_uuid() -> str:
    return str(uuid.uuid4())


def escape_ts_string(value: str) -> str:
    """Escape characters that would break a JS/TS single-quoted string."""
    return value.replace("\\", "\\\\").replace("'", "\\'")


def resolve_club_name(raw_name: str, alt_map: dict[str, str]) -> str:
    """Return the canonical club name by following alt_names once."""
    return alt_map.get(raw_name, raw_name)


def _lookup_geo(canonical_name: str, raw_names: set[str],
                geo_map: dict[str, dict]) -> tuple[str | None, str | None]:
    """
    Try to find geo info for a club.  Check canonical name first,
    then fall back to any of its raw (alternative) names.
    Returns (None, None) when no non-empty geo data is found.
    """
    if canonical_name in geo_map:
        entry = geo_map[canonical_name]
        country, city = entry.get("country") or None, entry.get("city") or None
        if country or city:
            return country, city

    for raw in raw_names:
        if raw in geo_map:
            entry = geo_map[raw]
            country, city = entry.get("country") or None, entry.get("city") or None
            if country or city:
                return country, city

    return None, None


# ── Builders ─────────────────────────────────────────────────────────

def build_clubs_and_alt_names(matches: list[dict], alt_map: dict[str, str],
                               geo_map: dict[str, dict]):
    """
    Walk every match, collect every unique *canonical* club name,
    and produce:
      clubs      – list of { id, name, country, city }
      alt_entries – list of { id, alt_name, club_id }
      name_to_id – helper lookup  canonical_name -> club_id
    """
    canonical_names: set[str] = set()
    canonical_to_raws: dict[str, set[str]] = {}

    for m in matches:
        for field in ("Home", "Away", "Winner"):
            raw = m.get(field, "").strip()
            if raw and raw != "Tie":
                canonical = resolve_club_name(raw, alt_map)
                canonical_names.add(canonical)
                canonical_to_raws.setdefault(canonical, set()).add(raw)

    sorted_names = sorted(canonical_names)

    name_to_id: dict[str, str] = {}
    clubs: list[dict] = []
    for name in sorted_names:
        cid = make_uuid()
        name_to_id[name] = cid
        country, city = _lookup_geo(name, canonical_to_raws.get(name, set()), geo_map)
        clubs.append({"id": cid, "name": name, "country": country, "city": city, "logo": None})

    alt_entries: list[dict] = []
    for alt_name, canonical in sorted(alt_map.items()):
        if canonical in name_to_id:
            alt_entries.append({
                "id": make_uuid(),
                "alt_name": alt_name,
                "club_id": name_to_id[canonical],
            })

    return clubs, alt_entries, name_to_id


def build_stadiums(matches: list[dict], geo_map: dict[str, dict], city_to_country: dict[str, str]):
    stadiums_set = set()
    for m in matches:
        v = m.get("Venue", "").strip()
        if v:
            stadiums_set.add(v)

    stadiums = []
    stadium_to_id = {}

    for raw_venue in sorted(stadiums_set):
        parts = [p.strip() for p in raw_venue.split(",")]
        
        if len(parts) > 1:
            city = parts[-1]
            name = ", ".join(parts[:-1])
        else:
            name = parts[0]
            city = None

        # Try to infer country
        country = None
        if city and city in city_to_country:
            country = city_to_country[city]
        
        # Hardcode fallback for obvious ones
        if city == "London" and not country: country = "England"
        if city == "Glasgow" and not country: country = "Scotland"

        sid = make_uuid()
        stadium_to_id[raw_venue] = sid
        stadiums.append({
            "id": sid,
            "name": name,
            "country": country,
            "city": city,
            "capacity": None # mock
        })
    
    return stadiums, stadium_to_id


def build_competitions(matches: list[dict]):
    comps_set = set()
    for m in matches:
        c = m.get("Competition", "").strip()
        if c: comps_set.add(c)

    competitions = []
    comp_to_id = {}
    canonical_comp_to_id = {}

    continental_kws = ["Champions League", "Europa", "Conference", "Cup Winners", "Super Cup", "Copa Libertadores"]
    intercontinental_kws = ["Intercontinental", "Club World Cup"]

    for raw_comp in sorted(comps_set):
        name = raw_comp
        round_str = None
        add_info = None

        # Type logic
        ctype = 0 # national
        lower_comp = raw_comp.lower()
        if any(kw.lower() in lower_comp for kw in intercontinental_kws):
            ctype = 2
        elif any(kw.lower() in lower_comp for kw in continental_kws):
            ctype = 1

        # Extract add_info like replay, aet, 1st leg
        add_info_matches = ["replay", "1st leg", "2nd leg", "aet", "penalties"]
        for ai in add_info_matches:
            if ai in lower_comp:
                add_info = ai
                # Remove from name
                insensitive_replace = re.compile(re.escape(ai), re.IGNORECASE)
                name = insensitive_replace.sub('', name).strip("() ")
        
        # Super naive split for round - e.g. "FA Cup 1st round" -> name="FA Cup", round="1st round"
        # Look for words like 'round', 'final', 'matchday'
        round_kws = [" round", "final", "matchday"]
        for rkw in round_kws:
            idx = name.lower().find(rkw)
            if idx != -1:
                # E.g. "FA Cup 1st round" -> idx of " round"
                # Let's cleanly split at the number before " round" or the word before "final"
                # For simplicity, if it contains "final", split off "semi-final", "quarter-final" etc.
                if rkw == "final":
                    # find last space before final, e.g. "FA Cup semi-final" -> "FA Cup", "semi-final"
                    parts = name.split()
                    for i, p in enumerate(parts):
                        if "final" in p.lower():
                            round_str = " ".join(parts[i:])
                            name = " ".join(parts[:i])
                            break
                elif rkw == " round":
                    parts = name.split()
                    for i, p in enumerate(parts):
                        if "round" in p.lower():
                            # include the previous word e.g. "1st"
                            start = max(0, i-1)
                            round_str = " ".join(parts[start:i+1])
                            name = " ".join(parts[:start] + parts[i+1:])
                            break
                elif rkw == "matchday":
                    parts = name.split()
                    for i, p in enumerate(parts):
                        if "matchday" in p.lower():
                            round_str = " ".join(parts[i:i+2]) # e.g. "matchday 7"
                            name = " ".join(parts[:i] + parts[i+2:])
                            break
        
        clean_name = name.strip("- ")
        
        if clean_name not in canonical_comp_to_id:
            cid = make_uuid()
            canonical_comp_to_id[clean_name] = cid
            competitions.append({
                "id": cid,
                "name": clean_name,
                "type": ctype,
            })
            
        comp_to_id[raw_comp] = canonical_comp_to_id[clean_name]

    return competitions, comp_to_id


def build_matches(raw_matches: list[dict], alt_map: dict[str, str], name_to_id: dict[str, str], stadium_to_id: dict[str, str], comp_to_id: dict[str, str]):
    result: list[dict] = []
    
    # We need to apply the same parsing logic for round and add_info from competition name
    continental_kws = ["Champions League", "Europa", "Conference", "Cup Winners", "Super Cup", "Copa Libertadores"]
    intercontinental_kws = ["Intercontinental", "Club World Cup"]
    add_info_matches = ["replay", "1st leg", "2nd leg", "aet", "penalties"]
    round_kws = [" round", "final", "matchday"]
    for m in raw_matches:
        home_raw = m.get("Home", "").strip()
        away_raw = m.get("Away", "").strip()
        winner_raw = m.get("Winner", "").strip()

        home_canonical = resolve_club_name(home_raw, alt_map)
        away_canonical = resolve_club_name(away_raw, alt_map)

        home_club_id = name_to_id.get(home_canonical, "")
        away_club_id = name_to_id.get(away_canonical, "")

        if winner_raw == "Tie":
            winner_club_id = "tie"
        elif not winner_raw:
            winner_club_id = None
        else:
            winner_canonical = resolve_club_name(winner_raw, alt_map)
            winner_club_id = name_to_id.get(winner_canonical, "")

        # Score parsing (e.g. "1-3" or "2-2(aet)" or "w/o")
        raw_score = m.get("Score", "").strip()
        home_goals = None
        away_goals = None
        score_add_info = None

        if raw_score.lower() == "w/o":
            score_add_info = "w/o"
        else:
            # Check for extra info in parens
            paren_match = re.search(r'\((.*?)\)', raw_score)
            if paren_match:
                score_add_info = paren_match.group(1)
                raw_score = re.sub(r'\s*\(.*?\)', '', raw_score).strip()

            parts = raw_score.split("-")
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                home_goals = int(parts[0])
                away_goals = int(parts[1])

        stadium_id = stadium_to_id.get(m.get("Venue", "").strip())
        
        raw_comp = m.get("Competition", "").strip()
        competition_id = comp_to_id.get(raw_comp)
        
        # Parse round and comp_add_info from raw_comp exactly as we did for competitions
        round_str = None
        comp_add_info = None
        comp_name = raw_comp
        lower_comp = raw_comp.lower()
        
        for ai in add_info_matches:
            if ai in lower_comp:
                comp_add_info = ai
                insensitive_replace = re.compile(re.escape(ai), re.IGNORECASE)
                comp_name = insensitive_replace.sub('', comp_name).strip("() ")
                
        for rkw in round_kws:
            idx = comp_name.lower().find(rkw)
            if idx != -1:
                if rkw == "final":
                    parts = comp_name.split()
                    for i, p in enumerate(parts):
                        if "final" in p.lower():
                            round_str = " ".join(parts[i:])
                            comp_name = " ".join(parts[:i])
                            break
                elif rkw == " round":
                    parts = comp_name.split()
                    for i, p in enumerate(parts):
                        if "round" in p.lower():
                            start = max(0, i-1)
                            round_str = " ".join(parts[start:i+1])
                            comp_name = " ".join(parts[:start] + parts[i+1:])
                            break
                elif rkw == "matchday":
                    parts = comp_name.split()
                    for i, p in enumerate(parts):
                        if "matchday" in p.lower():
                            round_str = " ".join(parts[i:i+2])
                            comp_name = " ".join(parts[:i] + parts[i+2:])
                            break

        result.append({
            "id": m.get("Match no.", ""),
            "date": m.get("Date of match", ""),
            "home_club_id": home_club_id,
            "away_club_id": away_club_id,
            "home_goals": home_goals,
            "away_goals": away_goals,
            "score_add_info": score_add_info,
            "winner_club_id": winner_club_id,
            "competition_id": competition_id,
            "stadium_id": stadium_id,
            "round": round_str.strip() if round_str else None,
            "comp_add_info": comp_add_info.strip() if comp_add_info else None
        })

    return result


def build_mock_players_and_goals(clubs: list[dict], matches: list[dict]):
    players = []
    goals = []

    if not clubs or not matches:
        return players, goals

    # 10 mock players
    mock_names = [
        ("Lionel", "Messi", "Argentina", "Forward"),
        ("Cristiano", "Ronaldo", "Portugal", "Forward"),
        ("Kevin", "De Bruyne", "Belgium", "Midfielder"),
        ("Virgil", "van Dijk", "Netherlands", "Defender"),
        ("Kylian", "Mbappe", "France", "Forward"),
        ("Luka", "Modric", "Croatia", "Midfielder"),
        ("Erling", "Haaland", "Norway", "Forward"),
        ("Jude", "Bellingham", "England", "Midfielder"),
        ("Alisson", "Becker", "Brazil", "Goalkeeper"),
        ("Robert", "Lewandowski", "Poland", "Forward")
    ]

    for first, last, nat, pos in mock_names:
        players.append({
            "id": make_uuid(),
            "name": first,
            "last_name": last,
            "nationality": nat,
            "position": pos
        })

    # Add ~10 mock goals for the FIRST match that has a valid home & away club id
    valid_matches = [m for m in matches if m["home_goals"] is not None and m["home_goals"] > 0]
    if valid_matches and players:
        m = valid_matches[0]
        # Just assign goals to random players for mock purposes
        for i in range(min(5, m["home_goals"])):
            goals.append({
                "id": make_uuid(),
                "match_id": m["id"],
                "club_id": m["home_club_id"],
                "player_id": players[i]["id"],
                "minute": (i+1) * 15,
                "penalty": False,
                "own_goal": False
            })

    return players, goals


# ── TypeScript emitters ──────────────────────────────────────────────

def _indent(level: int) -> str:
    return "  " * level

def _ts_nullable_string(value: str | None) -> str:
    """Render a string value or null for the TS output."""
    if not value:
        return "null"
    return f"'{escape_ts_string(str(value))}'"

def _ts_nullable_int(value: int | None) -> str:
    if value is None:
        return "null"
    return str(value)

def _ts_bool(value: bool | None) -> str:
    if value is None: return "null"
    return "true" if value else "false"


def emit_clubs(clubs: list[dict]) -> str:
    lines = ["export const clubs = ["]
    for c in clubs:
        lines.append(f"{_indent(1)}{{")
        lines.append(f"{_indent(2)}id: '{c['id']}',")
        lines.append(f"{_indent(2)}name: '{escape_ts_string(c['name'])}',")
        lines.append(f"{_indent(2)}country: {_ts_nullable_string(c['country'])},")
        lines.append(f"{_indent(2)}city: {_ts_nullable_string(c['city'])},")
        lines.append(f"{_indent(2)}logo: {_ts_nullable_string(c['logo'])},")
        lines.append(f"{_indent(1)}}},")
    lines.append("];")
    return "\n".join(lines)


def emit_alt_names(alt_entries: list[dict]) -> str:
    lines = ["export const alt_names = ["]
    for a in alt_entries:
        lines.append(f"{_indent(1)}{{")
        lines.append(f"{_indent(2)}id: '{a['id']}',")
        lines.append(f"{_indent(2)}alt_name: '{escape_ts_string(a['alt_name'])}',")
        lines.append(f"{_indent(2)}club_id: '{a['club_id']}',")
        lines.append(f"{_indent(1)}}},")
    lines.append("];")
    return "\n".join(lines)


def emit_stadiums(stadiums: list[dict]) -> str:
    lines = ["export const stadiums = ["]
    for s in stadiums:
        lines.append(f"{_indent(1)}{{")
        lines.append(f"{_indent(2)}id: '{s['id']}',")
        lines.append(f"{_indent(2)}name: '{escape_ts_string(s['name'])}',")
        lines.append(f"{_indent(2)}country: {_ts_nullable_string(s['country'])},")
        lines.append(f"{_indent(2)}city: {_ts_nullable_string(s['city'])},")
        lines.append(f"{_indent(2)}capacity: {_ts_nullable_int(s['capacity'])},")
        lines.append(f"{_indent(1)}}},")
    lines.append("];")
    return "\n".join(lines)


def emit_competitions(competitions: list[dict]) -> str:
    lines = ["export const competitions = ["]
    for c in competitions:
        lines.append(f"{_indent(1)}{{")
        lines.append(f"{_indent(2)}id: '{c['id']}',")
        lines.append(f"{_indent(2)}name: '{escape_ts_string(c['name'])}',")
        lines.append(f"{_indent(2)}type: {c['type']},")
        lines.append(f"{_indent(1)}}},")
    lines.append("];")
    return "\n".join(lines)


def emit_players(players: list[dict]) -> str:
    lines = ["export const players = ["]
    for p in players:
        lines.append(f"{_indent(1)}{{")
        lines.append(f"{_indent(2)}id: '{p['id']}',")
        lines.append(f"{_indent(2)}name: '{escape_ts_string(p['name'])}',")
        lines.append(f"{_indent(2)}last_name: '{escape_ts_string(p['last_name'])}',")
        lines.append(f"{_indent(2)}nationality: {_ts_nullable_string(p['nationality'])},")
        lines.append(f"{_indent(2)}position: {_ts_nullable_string(p['position'])},")
        lines.append(f"{_indent(1)}}},")
    lines.append("];")
    return "\n".join(lines)


def emit_goals(goals: list[dict]) -> str:
    lines = ["export const goals = ["]
    for g in goals:
        lines.append(f"{_indent(1)}{{")
        lines.append(f"{_indent(2)}id: '{g['id']}',")
        lines.append(f"{_indent(2)}match_id: '{g['match_id']}',")
        lines.append(f"{_indent(2)}club_id: '{g['club_id']}',")
        lines.append(f"{_indent(2)}player_id: '{g['player_id']}',")
        lines.append(f"{_indent(2)}minute: {g['minute']},")
        lines.append(f"{_indent(2)}penalty: {_ts_bool(g['penalty'])},")
        lines.append(f"{_indent(2)}own_goal: {_ts_bool(g['own_goal'])},")
        lines.append(f"{_indent(1)}}},")
    lines.append("];")
    return "\n".join(lines)


def emit_matches(matches: list[dict]) -> str:
    lines = ["export const matches = ["]
    for m in matches:
        w = m["winner_club_id"]
        if w is None:
            winner = "null"
        elif w == "tie":
            winner = "'tie'"
        else:
            winner = f"'{w}'"

        lines.append(f"{_indent(1)}{{")
        lines.append(f"{_indent(2)}id: '{escape_ts_string(str(m['id']))}',")
        lines.append(f"{_indent(2)}date: '{escape_ts_string(m['date'])}',")
        lines.append(f"{_indent(2)}home_club_id: '{m['home_club_id']}',")
        lines.append(f"{_indent(2)}away_club_id: '{m['away_club_id']}',")
        lines.append(f"{_indent(2)}home_goals: {_ts_nullable_int(m['home_goals'])},")
        lines.append(f"{_indent(2)}away_goals: {_ts_nullable_int(m['away_goals'])},")
        lines.append(f"{_indent(2)}score_add_info: {_ts_nullable_string(m['score_add_info'])},")
        lines.append(f"{_indent(2)}winner_club_id: {winner},")
        lines.append(f"{_indent(2)}competition_id: {_ts_nullable_string(m['competition_id'])},")
        lines.append(f"{_indent(2)}stadium_id: {_ts_nullable_string(m['stadium_id'])},")
        lines.append(f"{_indent(2)}round: {_ts_nullable_string(m['round'])},")
        lines.append(f"{_indent(2)}comp_add_info: {_ts_nullable_string(m['comp_add_info'])},")
        lines.append(f"{_indent(1)}}},")
    lines.append("];")
    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────

def main():
    raw_matches = load_json(MATCH_LIST_PATH)
    alt_map = load_json(ALT_NAMES_PATH)
    geo_map = load_json(GEO_INFO_PATH)

    # Build reverse mapping from city to country for stadium matching
    city_to_country = {}
    for entry in geo_map.values():
        c = entry.get("city")
        cnt = entry.get("country")
        if c and cnt:
            city_to_country[c] = cnt

    clubs, alt_entries, name_to_id = build_clubs_and_alt_names(raw_matches, alt_map, geo_map)
    stadiums, stadium_to_id = build_stadiums(raw_matches, geo_map, city_to_country)
    competitions, comp_to_id = build_competitions(raw_matches)

    matches = build_matches(raw_matches, alt_map, name_to_id, stadium_to_id, comp_to_id)
    players, goals = build_mock_players_and_goals(clubs, matches)

    ts_parts = [
        "// Auto-generated from match_list.json, alt_names.json, and teams_geo_info.json",
        "",
        emit_clubs(clubs),
        "",
        emit_alt_names(alt_entries),
        "",
        emit_stadiums(stadiums),
        "",
        emit_competitions(competitions),
        "",
        emit_players(players),
        "",
        emit_goals(goals),
        "",
        emit_matches(matches),
        "",
    ]

    OUTPUT_PATH.write_text("\n".join(ts_parts), encoding="utf-8")
    print(f"[OK] Written {OUTPUT_PATH}")
    print(f"   Clubs:        {len(clubs)}")
    print(f"   Alt names:    {len(alt_entries)}")
    print(f"   Stadiums:     {len(stadiums)}")
    print(f"   Competitions: {len(competitions)}")
    print(f"   Players:      {len(players)} (mock)")
    print(f"   Goals:        {len(goals)} (mock)")
    print(f"   Matches:      {len(matches)}")


if __name__ == "__main__":
    main()
