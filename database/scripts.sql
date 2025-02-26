-- ========================
-- CREACIÓN DE TABLAS
-- ========================

-- Tabla de Users
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- almacenaremos el hash de la contraseña
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Teams (con campo de imagen en base64, llamado "image")
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    image TEXT, -- Imagen en formato base64
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Players (con campo de imagen en base64, llamado "image")
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    team_id INT REFERENCES teams(id) ON DELETE CASCADE,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    image TEXT, -- Imagen en formato base64
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Matches
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    team_a_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    team_b_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    score_team_a INT DEFAULT 0,
    score_team_b INT DEFAULT 0,
    match_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT different_teams CHECK (team_a_id <> team_b_id)
);

-- Tabla de Goals (sin campo minute_scored)
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    player_id INT REFERENCES players(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Refresh Tokens (opcional)
CREATE TABLE refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

-- Tabla de Tournament Standings (opcional)
CREATE TABLE tournament_standings (
    team_id INT PRIMARY KEY REFERENCES teams(id) ON DELETE CASCADE,
    wins INT DEFAULT 0,
    draws INT DEFAULT 0,
    losses INT DEFAULT 0,
    goals_for INT DEFAULT 0,
    goals_against INT DEFAULT 0,
    points INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Tournament Bracket
CREATE TABLE tournament_bracket (
    id SERIAL PRIMARY KEY,
    phase VARCHAR(50) NOT NULL, -- Ej.: 'Octavos', 'Cuartos', 'Semifinal', 'Final'
    match_id INT REFERENCES matches(id) ON DELETE CASCADE, -- Partido correspondiente en esa fase
    team_a_id INT REFERENCES teams(id) ON DELETE CASCADE,
    team_b_id INT REFERENCES teams(id) ON DELETE CASCADE,
    winner_team_id INT REFERENCES teams(id) ON DELETE SET NULL, -- Se llena cuando se defina un ganador
    scheduled_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT different_teams_bracket CHECK (team_a_id <> team_b_id)
);

-- ========================
-- FUNCIONES Y TRIGGERS
-- ========================

-- Función para recalcular las estadísticas de un equipo basado en los partidos disputados
CREATE OR REPLACE FUNCTION recalc_standings(p_team_id INT)
RETURNS VOID AS $$
DECLARE
    wins_a INT;
    draws_a INT;
    losses_a INT;
    goals_for_a INT;
    goals_against_a INT;
    
    wins_b INT;
    draws_b INT;
    losses_b INT;
    goals_for_b INT;
    goals_against_b INT;
    
    wins_total INT;
    draws_total INT;
    losses_total INT;
    goals_for_total INT;
    goals_against_total INT;
    points_total INT;
BEGIN
    -- Estadísticas cuando el equipo juega como team_a
    SELECT 
        COALESCE(SUM(CASE WHEN score_team_a > score_team_b THEN 1 ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN score_team_a = score_team_b THEN 1 ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN score_team_a < score_team_b THEN 1 ELSE 0 END), 0),
        COALESCE(SUM(score_team_a), 0),
        COALESCE(SUM(score_team_b), 0)
    INTO wins_a, draws_a, losses_a, goals_for_a, goals_against_a
    FROM matches
    WHERE team_a_id = p_team_id;

    -- Estadísticas cuando el equipo juega como team_b
    SELECT 
        COALESCE(SUM(CASE WHEN score_team_b > score_team_a THEN 1 ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN score_team_b = score_team_a THEN 1 ELSE 0 END), 0),
        COALESCE(SUM(CASE WHEN score_team_b < score_team_a THEN 1 ELSE 0 END), 0),
        COALESCE(SUM(score_team_b), 0),
        COALESCE(SUM(score_team_a), 0)
    INTO wins_b, draws_b, losses_b, goals_for_b, goals_against_b
    FROM matches
    WHERE team_b_id = p_team_id;

    wins_total := wins_a + wins_b;
    draws_total := draws_a + draws_b;
    losses_total := losses_a + losses_b;
    goals_for_total := goals_for_a + goals_for_b;
    goals_against_total := goals_against_a + goals_against_b;
    points_total := wins_total * 3 + draws_total;

    -- Insertar o actualizar la clasificación para el equipo
    INSERT INTO tournament_standings (team_id, wins, draws, losses, goals_for, goals_against, points, updated_at)
    VALUES (p_team_id, wins_total, draws_total, losses_total, goals_for_total, goals_against_total, points_total, NOW())
    ON CONFLICT (team_id)
    DO UPDATE SET
        wins = EXCLUDED.wins,
        draws = EXCLUDED.draws,
        losses = EXCLUDED.losses,
        goals_for = EXCLUDED.goals_for,
        goals_against = EXCLUDED.goals_against,
        points = EXCLUDED.points,
        updated_at = EXCLUDED.updated_at;
END;
$$ LANGUAGE plpgsql;

-- Función trigger para actualizaciones (INSERT o UPDATE) en la tabla de matches
CREATE OR REPLACE FUNCTION update_standings_after_match()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM recalc_standings(NEW.team_a_id);
    PERFORM recalc_standings(NEW.team_b_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Función trigger para eliminaciones en la tabla de matches
CREATE OR REPLACE FUNCTION update_standings_after_match_delete()
RETURNS TRIGGER AS $$
BEGIN
    PERFORM recalc_standings(OLD.team_a_id);
    PERFORM recalc_standings(OLD.team_b_id);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Trigger que se activa tras INSERT o UPDATE en la tabla matches
CREATE TRIGGER trigger_update_standings
AFTER INSERT OR UPDATE ON matches
FOR EACH ROW
EXECUTE FUNCTION update_standings_after_match();

-- Trigger que se activa tras DELETE en la tabla matches
CREATE TRIGGER trigger_update_standings_delete
AFTER DELETE ON matches
FOR EACH ROW
EXECUTE FUNCTION update_standings_after_match_delete();

