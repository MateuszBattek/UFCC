import MatchCard from "../components/MatchCard";
import postgres from "postgres";

const sql = postgres(process.env.POSTGRES_URL!, { ssl: "require" });

export default async function MatchList() {
  const dbMatches = await sql`
    SELECT 
      m.id as "matchId", 
      m.date, 
      hc.name as "homeTeam", 
      ac.name as "awayTeam", 
      m.home_goals as "homeScore", 
      m.away_goals as "awayScore", 
      c.name as "competition", 
      m.round,
      s.name as "stadium"
    FROM matches m
    LEFT JOIN clubs hc ON m.home_club_id = hc.id
    LEFT JOIN clubs ac ON m.away_club_id = ac.id
    LEFT JOIN competitions c ON m.competition_id = c.id
    LEFT JOIN stadiums s ON m.stadium_id = s.id
    ORDER BY CAST(m.id AS INTEGER) DESC
    LIMIT 50;
  `;

  const matches = dbMatches.map((row) => {
    // Construct competition string with round if available
    let compString = row.competition || "Unknown Competition";
    if (row.round) {
      compString += ` - ${row.round}`;
    }

    return {
      matchId: Number(row.matchId),
      date: row.date,
      homeTeam: row.homeTeam || "Unknown",
      awayTeam: row.awayTeam || "Unknown",
      // Placeholder logos since they aren't in the DB yet
      homeLogo: "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
      awayLogo: "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
      homeScore: row.homeScore ?? 0,
      awayScore: row.awayScore ?? 0,
      competition: compString,
      stadium: row.stadium || "Unknown Stadium",
      isFeatured: false,
    };
  });

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
