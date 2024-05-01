-- SQL script that lists all bands with Glam rock as their main style, ranked by
-- their longevity
-- Requirement:
-- Import this table dump: metal_bands.sql.zip
-- Column names must be: band_name and lifespan
-- You should use attributes formed and split for computing the lifespan
SELECT band_name, (IFNULL(SPLIT, '2022') - formed) AS lifespan
    FROM metal_bands
    WHERE styel LIKE '%Glam rock%'
    ORDER BY lifespan DESC;
