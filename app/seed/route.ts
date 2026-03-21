import postgres from 'postgres';
import { clubs, alt_names, stadiums, competitions, players, goals, matches } from '../../python_shit/data';

const sql = postgres(process.env.POSTGRES_URL!, { ssl: 'require' });

async function seedClubs() {
  await sql`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`;
  await sql`
    CREATE TABLE IF NOT EXISTS clubs (
      id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      country VARCHAR(255),
      city VARCHAR(255)
    );
  `;
  const insertedClubs = await Promise.all(
    clubs.map((club) => sql`
      INSERT INTO clubs (id, name, country, city)
      VALUES (${club.id}, ${club.name}, ${club.country}, ${club.city})
      ON CONFLICT (id) DO NOTHING;
    `)
  );
  return insertedClubs;
}

async function seedStadiums() {
  await sql`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`;
  await sql`
    CREATE TABLE IF NOT EXISTS stadiums (
      id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      country VARCHAR(255),
      city VARCHAR(255),
      capacity INT
    );
  `;
  const insertedStadiums = await Promise.all(
    stadiums.map((s) => sql`
      INSERT INTO stadiums (id, name, country, city, capacity)
      VALUES (${s.id}, ${s.name}, ${s.country}, ${s.city}, ${s.capacity})
      ON CONFLICT (id) DO NOTHING;
    `)
  );
  return insertedStadiums;
}

async function seedCompetitions() {
  await sql`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`;
  await sql`
    CREATE TABLE IF NOT EXISTS competitions (
      id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      type INT NOT NULL
    );
  `;
  const insertedCompetitions = await Promise.all(
    competitions.map((c) => sql`
      INSERT INTO competitions (id, name, type)
      VALUES (${c.id}, ${c.name}, ${c.type})
      ON CONFLICT (id) DO NOTHING;
    `)
  );
  return insertedCompetitions;
}

async function seedPlayers() {
  await sql`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`;
  await sql`
    CREATE TABLE IF NOT EXISTS player (
      id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
      name VARCHAR(255) NOT NULL,
      last_name VARCHAR(255) NOT NULL,
      nationality VARCHAR(255),
      position VARCHAR(255)
    );
  `;
  const insertedPlayers = await Promise.all(
    players.map((p) => sql`
      INSERT INTO player (id, name, last_name, nationality, position)
      VALUES (${p.id}, ${p.name}, ${p.last_name}, ${p.nationality}, ${p.position})
      ON CONFLICT (id) DO NOTHING;
    `)
  );
  return insertedPlayers;
}

async function seedMatches() {
  await sql`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`;
  await sql`
    CREATE TABLE IF NOT EXISTS matches (
      id VARCHAR(255) PRIMARY KEY,
      date VARCHAR(255) NOT NULL,
      home_club_id UUID REFERENCES clubs(id),
      away_club_id UUID REFERENCES clubs(id),
      home_goals INT,
      away_goals INT,
      score_add_info VARCHAR(255),
      winner_club_id VARCHAR(255),
      competition_id UUID REFERENCES competitions(id),
      stadium_id UUID REFERENCES stadiums(id),
      round VARCHAR(255),
      comp_add_info VARCHAR(255)
    );
  `;
  const insertedMatches = await Promise.all(
    matches.map((m) => sql`
      INSERT INTO matches (id, date, home_club_id, away_club_id, home_goals, away_goals, score_add_info, winner_club_id, competition_id, stadium_id, round, comp_add_info)
      VALUES (${m.id}, ${m.date}, ${m.home_club_id || null}, ${m.away_club_id || null}, ${m.home_goals}, ${m.away_goals}, ${m.score_add_info}, ${m.winner_club_id}, ${m.competition_id}, ${m.stadium_id}, ${m.round}, ${m.comp_add_info})
      ON CONFLICT (id) DO NOTHING;
    `)
  );
  return insertedMatches;
}

async function seedGoals() {
  await sql`CREATE EXTENSION IF NOT EXISTS "uuid-ossp"`;
  await sql`
    CREATE TABLE IF NOT EXISTS goals (
      id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
      match_id VARCHAR(255) REFERENCES matches(id),
      club_id UUID REFERENCES clubs(id),
      player_id UUID REFERENCES player(id),
      minute INT NOT NULL,
      penalty BOOLEAN DEFAULT FALSE,
      own_goal BOOLEAN DEFAULT FALSE
    );
  `;
  const insertedGoals = await Promise.all(
    goals.map((g) => sql`
      INSERT INTO goals (id, match_id, club_id, player_id, minute, penalty, own_goal)
      VALUES (${g.id}, ${g.match_id}, ${g.club_id}, ${g.player_id}, ${g.minute}, ${g.penalty}, ${g.own_goal})
      ON CONFLICT (id) DO NOTHING;
    `)
  );
  return insertedGoals;
}

export async function GET() {
  try {
    const result = await sql.begin(async (sql) => {
      // Create tables and seed them in order to respect foreign key constraints
      await seedClubs();
      await seedStadiums();
      await seedCompetitions();
      await seedPlayers();
      await seedMatches();
      await seedGoals();
    });

    return Response.json({ message: 'Database seeded successfully with all tables' });
  } catch (error) {
    console.error('Error seeding database:', error);
    return Response.json({ error: String(error) }, { status: 500 });
  }
}
