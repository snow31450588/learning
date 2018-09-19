
SELECT postgis_full_version();


CREATE TABLE gtest (id serial primary key, name varchar(20), geom geometry(LINESTRING));


INSERT INTO gtest (ID, NAME, GEOM)
VALUES (
  1,
  'First Geometry',
  ST_GeomFromText('LINESTRING(2 3,4 5,6 5,7 8)')
);


CREATE INDEX idx_gtest_geom ON gtest USING GIST ( geom );


with t as (select ST_GeomFromText('POLYGON((0 0, 0 6, 6 6, 6 0, 0 0))') as g)
SELECT id, name, ST_AsText(geom) AS geom, ST_AsText(ST_Intersection(g, geom)) as intersection
FROM gtest, t
WHERE
  ST_Intersects(geom,g);
