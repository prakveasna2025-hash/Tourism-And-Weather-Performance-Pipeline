-- Create the Location Dimension
CREATE TABLE IF NOT EXISTS analytics.dim_location (
    location_id SERIAL PRIMARY KEY,   -- Surrogate key for fast joins
    city_name TEXT NOT NULL UNIQUE,   -- e.g., 'Phnom Penh'
    region TEXT NOT NULL,             -- e.g., 'Capital', 'North', 'Coastal'
    latitude NUMERIC(8,5) NOT NULL,   -- Kept for spatial joins/mapping
    longitude NUMERIC(8,5) NOT NULL
);

-- Insert the 3 cities from our weather/tourism sources
INSERT INTO analytics.dim_location (city_name, region, latitude, longitude)
VALUES 
    ('Phnom Penh', 'Capital', 11.55640, 104.92820),
    ('Siem Reap', 'North', 13.36710, 103.84480),
    ('Sihanoukville', 'Coastal', 10.62530, 103.52340)
ON CONFLICT (city_name) DO NOTHING;