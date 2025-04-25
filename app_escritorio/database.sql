-- Create database
CREATE DATABASE appwebmercado;

-- Connect to database
\c appwebmercado;

-- Create job_offers table
CREATE TABLE IF NOT EXISTS job_offers (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    company VARCHAR(200) NOT NULL,
    location VARCHAR(200) NOT NULL,
    min_salary INTEGER,
    max_salary INTEGER,
    job_type VARCHAR(50) NOT NULL,
    fuente VARCHAR(50) DEFAULT 'Manual',
    description TEXT,
    requirements TEXT,
    publication_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(title, company)
);

-- Create habilidades table
CREATE TABLE IF NOT EXISTS habilidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create job_offers_habilidades table
CREATE TABLE IF NOT EXISTS job_offers_habilidades (
    job_offers_id INTEGER REFERENCES job_offers(id) ON DELETE CASCADE,
    habilidades_id INTEGER REFERENCES habilidades(id) ON DELETE CASCADE,
    PRIMARY KEY (job_offers_id, habilidades_id)
);

-- Create indices for better performance
CREATE INDEX idx_job_offers_title ON job_offers(title);
CREATE INDEX idx_job_offers_company ON job_offers(company);
CREATE INDEX idx_job_offers_location ON job_offers(location);
CREATE INDEX idx_job_offers_job_type ON job_offers(job_type);
CREATE INDEX idx_job_offers_fuente ON job_offers(fuente);
CREATE INDEX idx_habilidades_nombre ON habilidades(nombre); 