import MatchCard from "../components/MatchCard";

const matches = [
  {
    matchId: 5426,
    date: "March 7th, 2026",
    homeTeam: "Newcastle United F.C.",
    awayTeam: "Manchester City F.C.",
    homeLogo:
      "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    awayLogo:
      "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    homeScore: 2,
    awayScore: 1,
    competition: "England - FA Cup",
    stadium: "St James' Park",
    isFeatured: true,
  },
  {
    matchId: 5427,
    date: "March 10th, 2026",
    homeTeam: "Newcastle United F.C.",
    awayTeam: "FC Barcelona",
    homeLogo:
      "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    awayLogo:
      "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
    homeScore: 0,
    awayScore: 3,
    competition: "Europe - UCL",
    stadium: "St James' Park",
    isFeatured: false,
  },
  {
    matchId: 5428,
    date: "March 11th, 2026",
    homeTeam: "Real Madrid C. F.",
    awayTeam: "Manchester City F.C.",
    homeLogo:
      "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
    awayLogo:
      "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    homeScore: 3,
    awayScore: 2,
    competition: "Europe - UCL",
    stadium: "Santiago Bernabéu",
    isFeatured: false,
  },
  {
    matchId: 5429,
    date: "March 14th, 2026",
    homeTeam: "West Ham United",
    awayTeam: "Manchester City F.C.",
    homeLogo:
      "https://upload.wikimedia.org/wikipedia/en/c/c2/West_Ham_United_FC_logo.svg",
    awayLogo:
      "https://upload.wikimedia.org/wikipedia/en/e/eb/Manchester_City_FC_badge.svg",
    homeScore: 1,
    awayScore: 4,
    competition: "England - Premier League",
    stadium: "London Stadium",
    isFeatured: false,
  },
  {
    matchId: 5430,
    date: "March 14th, 2026",
    homeTeam: "Chelsea F.C.",
    awayTeam: "Newcastle United",
    homeLogo: "https://upload.wikimedia.org/wikipedia/en/c/cc/Chelsea_FC.svg",
    awayLogo:
      "https://upload.wikimedia.org/wikipedia/en/5/56/Newcastle_United_Logo.svg",
    homeScore: 2,
    awayScore: 2,
    competition: "England - Premier League",
    stadium: "Stamford Bridge",
    isFeatured: false,
  },
  {
    matchId: 5431,
    date: "March 14th, 2026",
    homeTeam: "Real Madrid C. F.",
    awayTeam: "Elche C. F.",
    homeLogo:
      "https://upload.wikimedia.org/wikipedia/en/5/56/Real_Madrid_CF.svg",
    awayLogo:
      "https://upload.wikimedia.org/wikipedia/commons/e/e0/Elche_CF_logo.svg",
    homeScore: 5,
    awayScore: 0,
    competition: "Spain - La Liga",
    stadium: "Santiago Bernabéu",
    isFeatured: false,
  },
  {
    matchId: 5432,
    date: "March 15th, 2026",
    homeTeam: "FC Barcelona",
    awayTeam: "FC Sevilla",
    homeLogo:
      "https://upload.wikimedia.org/wikipedia/en/4/47/FC_Barcelona_%28crest%29.svg",
    awayLogo:
      "https://upload.wikimedia.org/wikipedia/en/3/3b/Sevilla_FC_logo.svg",
    homeScore: 3,
    awayScore: 1,
    competition: "Spain - La Liga",
    stadium: "Camp Nou",
    isFeatured: false,
  },
];

export default function MatchList() {
  return (
    <div>
      {/* Page Header */}
      <div className="mb-6">
        <h1
          className="text-3xl font-bold tracking-tight"
          style={{ color: "#2C3E6B" }}
        >
          Match List
        </h1>
        <p className="mt-2" style={{ color: "#4A6FA5" }}>
          Recent and upcoming UFCC-relevant fixtures
        </p>
        <div
          className="mt-3 h-1 w-16 rounded-full"
          style={{ backgroundColor: "#F0C34E" }}
        />
      </div>

      {/* Scrollable Table */}
      <div
        className="overflow-x-auto rounded-lg"
        style={{ border: "1px solid rgba(74,111,165,0.2)" }}
      >
        {/* Column Headers */}
        <div
          className="flex items-center px-3 py-2 text-xs font-bold uppercase tracking-wider"
          style={{
            backgroundColor: "#2C3E6B",
            color: "rgba(255,255,255,0.8)",
            minWidth: "900px",
          }}
        >
          <span style={{ width: "42px" }} className="text-center shrink-0">
            #
          </span>
          <span style={{ width: "110px" }} className="shrink-0 text-center">
            Date
          </span>
          <span style={{ width: "200px" }} className="shrink-0 text-center">
            Home
          </span>
          <span style={{ width: "50px" }} className="text-center shrink-0">
            Score
          </span>
          <span style={{ width: "200px" }} className="shrink-0 text-center">
            Away
          </span>
          <span
            style={{ width: "180px", paddingLeft: "8px" }}
            className="shrink-0"
          >
            Competition
          </span>
          <span className="flex-1 text-right" style={{ minWidth: "100px" }}>
            Stadium
          </span>
        </div>

        {/* Match Rows */}
        {matches.map((match, index) => (
          <MatchCard key={index} {...match} />
        ))}
      </div>
    </div>
  );
}
