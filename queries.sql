SELECT 
location.NEIGHBORHOOD_158, crime_info.OFFENSE, COUNT(*) as count, 
RANK() OVER (PARTITION BY location.NEIGHBORHOOD_158 ORDER BY COUNT(*) DESC) as ranking
FROM toronto_crimes
JOIN crime_info ON toronto_crimes.UCR = crime_info.UCR
JOIN location ON toronto_crimes.LONG_WGS84 = location.LONG_WGS84 
    AND toronto_crimes.LAT_WGS84 = location.LAT_WGS84
GROUP BY location.NEIGHBORHOOD_158, crime_info.OFFENSE;


WITH crime_location AS (
    SELECT location_type.LOCATION_TYPE, crime_info.MCI_CATEGORY, COUNT(*) AS count
    FROM toronto_crimes
    JOIN crime_info ON toronto_crimes.UCR = crime_info.UCR
    JOIN location ON toronto_crimes.LONG_WGS84 = location.LONG_WGS84 
        AND toronto_crimes.LAT_WGS84 = location.LAT_WGS84
    JOIN location_type ON location.PREMIS_TYPE = location_type.PREMIS_TYPE
    GROUP BY location_type.LOCATION_TYPE, crime_info.MCI_CATEGORY
), rankings AS (
    SELECT *, RANK() OVER (PARTITION BY LOCATION_TYPE ORDER BY count DESC) AS rank
    FROM crime_location
) SELECT LOCATION_TYPE, MCI_CATEGORY, count, rank
FROM rankings;


