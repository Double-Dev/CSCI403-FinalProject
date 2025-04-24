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


SELECT occurance_date.OCC_MONTH, 
    CASE 
        WHEN EXTRACT(MONTH FROM occurance_date.OCCURANCE_FULL_DATE) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM occurance_date.OCCURANCE_FULL_DATE) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM occurance_date.OCCURANCE_FULL_DATE) IN (6, 7, 8) THEN 'Summer'
        WHEN EXTRACT(MONTH FROM occurance_date.OCCURANCE_FULL_DATE) IN (9, 10, 11) THEN 'Fall'
    END AS season,
    COUNT(*) AS count
FROM toronto_crimes
JOIN occurance_date ON toronto_crimes.OCC_DATE = occurance_date.OCCURANCE_FULL_DATE
GROUP BY occurance_date.OCC_MONTH, season
ORDER BY 
  CASE occurance_date.OCC_MONTH
    WHEN 'January' THEN 1
    WHEN 'February' THEN 2
    WHEN 'March' THEN 3
    WHEN 'April' THEN 4
    WHEN 'May' THEN 5
    WHEN 'June' THEN 6
    WHEN 'July' THEN 7
    WHEN 'August' THEN 8
    WHEN 'September' THEN 9
    WHEN 'October' THEN 10
    WHEN 'November' THEN 11
    WHEN 'December' THEN 12
  END, count DESC;
