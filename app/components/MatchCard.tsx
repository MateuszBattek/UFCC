import Image from "next/image";

interface MatchCardProps {
  matchId: number;
  date: string;
  homeTeam: string;
  awayTeam: string;
  homeLogo: string;
  awayLogo: string;
  homeScore: number;
  awayScore: number;
  competition: string;
  stadium: string;
  isFeatured?: boolean;
}

export default function MatchCard({
  matchId,
  date,
  homeTeam,
  awayTeam,
  homeLogo,
  awayLogo,
  homeScore,
  awayScore,
  competition,
  stadium,
  isFeatured = false,
}: MatchCardProps) {
  const homeWon = homeScore > awayScore;
  const awayWon = awayScore > homeScore;

  return (
    <div
      className="flex items-center px-3 py-2 transition-all duration-150 hover:brightness-95"
      style={{
        backgroundColor: isFeatured ? "rgba(240,195,78,0.15)" : "#FFFFFF",
        borderLeft: isFeatured ? "3px solid #F0C34E" : "3px solid transparent",
        borderBottom: "1px solid rgba(74,111,165,0.12)",
        minWidth: "900px",
      }}
    >
      {/* Match ID */}
      <span
        className="text-xs font-mono shrink-0 text-center"
        style={{ color: "rgba(74,111,165,0.6)", width: "42px" }}
      >
        #{matchId}
      </span>

      {/* Date */}
      <span
        className="text-xs shrink-0"
        style={{ color: "#4A6FA5", width: "110px" }}
      >
        {date}
      </span>

      {/* Home Team */}
      <div
        className="flex items-center gap-1.5 shrink-0 justify-center"
        style={{ width: "200px" }}
      >
        <span
          className="text-sm text-center"
          style={{
            color: "#2C3E6B",
            fontWeight: homeWon ? "700" : "400",
          }}
        >
          {homeTeam}
        </span>
        <Image
          src={homeLogo}
          alt=""
          width={20}
          height={20}
          className="w-5 h-5 object-contain shrink-0"
        />
      </div>

      {/* Score */}
      <div
        className="flex items-center justify-center shrink-0 gap-1"
        style={{ width: "50px" }}
      >
        <span
          className="text-sm font-bold tabular-nums"
          style={{ color: "#2C3E6B" }}
        >
          {homeScore}
        </span>
        <span className="text-xs" style={{ color: "#4A6FA5" }}>
          –
        </span>
        <span
          className="text-sm font-bold tabular-nums"
          style={{ color: "#2C3E6B" }}
        >
          {awayScore}
        </span>
      </div>

      {/* Away Team */}
      <div
        className="flex items-center gap-1.5 shrink-0 justify-center"
        style={{ width: "200px" }}
      >
        <Image
          src={awayLogo}
          alt=""
          width={20}
          height={20}
          className="w-5 h-5 object-contain shrink-0"
        />
        <span
          className="text-sm truncate"
          style={{
            color: "#2C3E6B",
            fontWeight: awayWon ? "700" : "400",
          }}
        >
          {awayTeam}
        </span>
      </div>

      {/* Competition */}
      <span
        className="text-xs truncate shrink-0"
        style={{ color: "#4A6FA5", width: "180px", paddingLeft: "8px" }}
      >
        {competition}
      </span>

      {/* Stadium */}
      <span
        className="text-xs truncate text-right flex-1"
        style={{ color: "rgba(74,111,165,0.7)", minWidth: "100px" }}
      >
        {stadium}
      </span>
    </div>
  );
}
