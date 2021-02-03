CREATE TABLE route (
    id serial PRIMARY KEY,
    route_id text NOT NULL,
    agency_id text NOT NULL,
    route_short_name text NOT NULL,
    route_long_name text NOT NULL,
    route_desc text NULL,
    route_type int NOT NULL,
    route_url text NULL,
    route_color text NULL,
    route_text_color text NOT NULL,
    route geometry
);