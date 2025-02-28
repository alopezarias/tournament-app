-- ========================
-- CREACIÓN DE TABLAS
-- ========================

-- Tabla de Users (para autenticación)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Teams
CREATE TABLE teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    image TEXT,
    is_closed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Players (con notifications_enabled; team_id inicialmente NULL)
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    team_id INT REFERENCES teams(id) ON DELETE SET NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    image TEXT,
    notifications_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Invitations
CREATE TABLE invitations (
    id SERIAL PRIMARY KEY,
    team_id INT REFERENCES teams(id) ON DELETE CASCADE,
    inviter_id INT REFERENCES players(id) ON DELETE CASCADE,
    invitee_id INT REFERENCES players(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Matches (con start_time, end_time, duration y status)
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    team_a_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    team_b_id INT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    score_team_a INT DEFAULT 0,
    score_team_b INT DEFAULT 0,
    match_date TIMESTAMP,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration INTERVAL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT different_teams CHECK (team_a_id <> team_b_id)
);

-- Tabla de Goals (con sent_at)
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    match_id INT NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    player_id INT REFERENCES players(id) ON DELETE SET NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Tournament Standings
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
    phase VARCHAR(50) NOT NULL, -- Ej.: 'Cuartos', 'Semifinal', 'Final'
    match_id INT REFERENCES matches(id) ON DELETE CASCADE,
    team_a_id INT REFERENCES teams(id) ON DELETE CASCADE,
    team_b_id INT REFERENCES teams(id) ON DELETE CASCADE,
    winner_team_id INT REFERENCES teams(id) ON DELETE SET NULL,
    scheduled_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT different_teams_bracket CHECK (team_a_id <> team_b_id)
);

-- Tabla de Notifications
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    player_id INT REFERENCES players(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ========================
-- FUNCIONES Y TRIGGERS
-- ========================

-- Trigger function para actualizar status y duración de un partido
CREATE OR REPLACE FUNCTION update_match_status_and_duration()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.start_time IS NULL AND NEW.end_time IS NULL THEN
        NEW.status := 'pending';
        NEW.duration := NULL;
    ELSIF NEW.start_time IS NOT NULL AND NEW.end_time IS NULL THEN
        NEW.status := 'in_progress';
        NEW.duration := NULL;
    ELSIF NEW.start_time IS NOT NULL AND NEW.end_time IS NOT NULL THEN
        NEW.status := 'completed';
        NEW.duration := NEW.end_time - NEW.start_time;
    ELSE
        NEW.status := 'pending';
        NEW.duration := NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger para matches (antes de INSERT o UPDATE)
CREATE TRIGGER trg_update_match_status
BEFORE INSERT OR UPDATE ON matches
FOR EACH ROW
EXECUTE FUNCTION update_match_status_and_duration();

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

