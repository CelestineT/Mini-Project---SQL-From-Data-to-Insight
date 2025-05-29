USE airbnb_invest;

DROP TABLE IF EXISTS airbnb_cleaned;
CREATE TABLE airbnb_listings (
    listing_id INT PRIMARY KEY,
    price DECIMAL(10,2),
    host_id INT,
    neighbourhood_group VARCHAR(255),  -- FK vers 2019_House_Listings
    neighbourhood VARCHAR(255),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    room_type VARCHAR(255),
    minimum_nights INT,
    number_of_reviews INT,
    reviews_per_month DECIMAL(5,2),
    calculated_host_listings_count INT,
    availability_365 INT
);
CREATE TABLE house_listings (
    listing_id INT PRIMARY KEY AUTO_INCREMENT,
    city VARCHAR(50),
    neighbourhood VARCHAR(255),
    sale_price DECIMAL(15,2),
    building_class_category VARCHAR(255)
);
ALTER TABLE airbnb_listings
ADD COLUMN name TEXT AFTER listing_id;
DROP TABLE IF EXISTS house_listings;

DROP TABLE IF EXISTS house_listings;

CREATE TABLE house_listings (
    listing_id INT AUTO_INCREMENT PRIMARY KEY,
    Borough VARCHAR(50),
    Neighborhood VARCHAR(255),
    `Building Class Category` VARCHAR(255),
    `Tax Class At Present` VARCHAR(50),
    Block INT,
    Lot INT,
    `Ease-Ment` VARCHAR(50),
    `Building Class At Present` VARCHAR(50),
    Address VARCHAR(255),
    `Apartment Number` VARCHAR(50),
    `Zip Code` VARCHAR(10),
    `Residential Units` INT,
    `Commercial Units` INT,
    `Total Units` INT,
    `Land Square Feet` FLOAT,
    `Gross Square Feet` FLOAT,
    `Year Built` INT,
    `Tax Class At Time Of Sale` VARCHAR(50),
    `Building Class At Time Of Sale` VARCHAR(50),
    `Sale Price` FLOAT,
    `Sale Date` DATE,
    city VARCHAR(50),
    `Tax Class As Of Final Roll 18/1` VARCHAR(50),
    `Building Class As Of Final Roll 18/1` VARCHAR(50)
);
ALTER TABLE house_listings
MODIFY COLUMN `Year Built` SMALLINT NULL;
ALTER TABLE house_listings
MODIFY COLUMN `Year Built` SMALLINT NULL,
MODIFY COLUMN `Residential Units` INT NULL,
MODIFY COLUMN `Commercial Units` INT NULL,
MODIFY COLUMN `Total Units` INT NULL,
MODIFY COLUMN `Land Square Feet` FLOAT NULL,
MODIFY COLUMN `Gross Square Feet` FLOAT NULL,
MODIFY COLUMN `Sale Price` FLOAT NULL;

-- STEP 1: Airbnb revenue per neighborhood
SELECT
    neighbourhood,
    neighbourhood_group,
    AVG(price) AS avg_daily_price,
    COUNT(*) AS total_listings
FROM airbnb_listings
WHERE price > 0
GROUP BY neighbourhood, neighbourhood_group
LIMIT 10;

WITH airbnb_revenue AS (
    SELECT
        neighbourhood AS neighbourhood,
        neighbourhood_group,
        AVG(price) AS avg_daily_price,
        AVG(365 - availability_365) AS avg_occupied_nights,
        AVG(price * (365 - availability_365)) AS avg_annual_revenue,
        COUNT(*) AS total_listings,
        -- Calcul de part de marché par groupe de quartiers
        ROUND(
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY neighbourhood_group), 2
        ) AS market_share_percent
    FROM airbnb_listings al
    WHERE price > 0 AND availability_365 BETWEEN 1 AND 364
    GROUP BY neighbourhood, neighbourhood_group
)
SELECT * FROM airbnb_revenue
ORDER BY avg_annual_revenue DESC;

-- STEP 2: Property cost per neighborhood
WITH property_costs AS (
    SELECT
        Neighborhood AS neighbourhood,
        AVG(`Sale Price`) AS avg_property_price,
        AVG(`Sale Price` / NULLIF(`Gross Square Feet`, 0)) AS price_per_sqft,
        AVG(`Sale Price` / NULLIF(`Gross Square Feet`, 0)) * 600 AS estimated_apartment_cost
    FROM house_listings
    WHERE `Residential Units` > 0 
      AND `Gross Square Feet` > 0 
      AND `Sale Date` >= '2019-01-01'
    GROUP BY Neighborhood
)

SELECT 
    neighbourhood,
    ROUND(avg_property_price, 2) AS avg_property_price,
    ROUND(price_per_sqft, 2) AS price_per_sqft,
    ROUND(estimated_apartment_cost, 2) AS estimated_apartment_cost
FROM property_costs
ORDER BY avg_property_price DESC;

-- STEP 3: ROI calculation
-- STEP 1 to 3 inclus
WITH airbnb_revenue AS (
    SELECT 
        neighbourhood AS neighbourhood,
        neighbourhood_group,
        AVG(price) AS avg_daily_price,
        AVG(365 - availability_365) AS avg_occupied_nights,
        AVG(price * (365 - availability_365)) AS avg_annual_revenue,
        COUNT(*) AS total_listings,
        COUNT(*) / (SELECT COUNT(*) FROM airbnb_listings WHERE neighbourhood_group = al.neighbourhood_group) * 100 AS market_share_pct
    FROM airbnb_listings al
    WHERE price > 0 AND availability_365 BETWEEN 1 AND 364
    GROUP BY neighbourhood, neighbourhood_group
),

property_costs AS (
    SELECT 
        Neighborhood AS neighbourhood,
        AVG(`Sale Price`) AS avg_property_price,
        AVG(`Sale Price` / NULLIF(`Gross Square Feet`, 0)) AS price_per_sqft,
        AVG(`Sale Price` / NULLIF(`Gross Square Feet`, 0)) * 600 AS estimated_apartment_cost
    FROM house_listings
    WHERE `Residential Units` > 0 AND `Gross Square Feet` > 0 AND `Sale Date` >= '2019-01-01'
    GROUP BY Neighborhood
),

roi_calculation AS (
    SELECT 
        ar.neighbourhood AS neighborhood,
        ar.neighbourhood_group,
        ar.avg_daily_price,
        ar.avg_occupied_nights,
        ar.avg_annual_revenue,
        ar.total_listings,
        ar.market_share_pct,

        pc.avg_property_price,
        pc.estimated_apartment_cost AS acquisition_cost,

        (ar.avg_annual_revenue * 0.10) AS maintenance_costs,
        (pc.estimated_apartment_cost * 0.012) AS property_taxes,
        (pc.estimated_apartment_cost * 0.15) AS hoa_fees,

        (ar.avg_annual_revenue * 0.10) + 
        (pc.estimated_apartment_cost * 0.012) + 
        (pc.estimated_apartment_cost * 0.15) AS total_annual_costs,

        ROUND(
            ((ar.avg_annual_revenue - 
              ((ar.avg_annual_revenue * 0.10) + 
               (pc.estimated_apartment_cost * 0.012) + 
               (pc.estimated_apartment_cost * 0.15))
             ) / pc.estimated_apartment_cost) * 100, 2
        ) AS roi_percentage
    FROM airbnb_revenue ar
    JOIN property_costs pc ON ar.neighbourhood = pc.neighbourhood
)

SELECT 
    neighborhood,
    neighbourhood_group,
    avg_daily_price,
    avg_occupied_nights,
    ROUND(avg_annual_revenue, 0) AS estimated_annual_revenue,
    ROUND(acquisition_cost, 0) AS property_acquisition_cost,
    ROUND(total_annual_costs, 0) AS annual_operating_costs,

    ROUND(((avg_annual_revenue - total_annual_costs) / acquisition_cost) * 100, 2) AS roi_percentage,

    CASE 
        WHEN acquisition_cost < 400000 AND ((avg_annual_revenue - total_annual_costs) / acquisition_cost) > 0.08 
        THEN 'HIGH_ROI_OPPORTUNITY'
        WHEN acquisition_cost BETWEEN 400000 AND 800000 AND ((avg_annual_revenue - total_annual_costs) / acquisition_cost) > 0.06
        THEN 'MID_TIER_OPPORTUNITY'
        WHEN acquisition_cost > 800000 AND ((avg_annual_revenue - total_annual_costs) / acquisition_cost) > 0.04
        THEN 'PREMIUM_MARKET'
        ELSE 'LOW_ROI'
    END AS investment_tier,

    total_listings AS competition_level,
    CASE 
        WHEN total_listings > 100 THEN 'HIGH_COMPETITION'
        WHEN total_listings BETWEEN 50 AND 100 THEN 'MODERATE_COMPETITION'
        ELSE 'LOW_COMPETITION'
    END AS market_saturation,

    ROUND(acquisition_cost / (avg_annual_revenue - total_annual_costs), 1) AS payback_years

FROM roi_calculation
WHERE avg_annual_revenue > 0 AND acquisition_cost > 0
ORDER BY roi_percentage DESC;