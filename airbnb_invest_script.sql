USE airbnb_invest;

-- STEP 1: Airbnb revenue per neighborhood
SELECT
    neighbourhood,
    borough,
    AVG(price) AS avg_daily_price,
    COUNT(*) AS total_listings
FROM airbnb_listings
WHERE price > 0
GROUP BY neighbourhood, borough
LIMIT 10;

WITH airbnb_revenue AS (
    SELECT
        neighbourhood AS neighbourhood,
        Borough AS borough,
        AVG(price) AS avg_daily_price,
        AVG(365 - availability_365) AS avg_occupied_nights,
        AVG(price * (365 - availability_365)) AS avg_annual_revenue,
        COUNT(*) AS total_listings,
        -- Calcul de part de marché par groupe de quartiers
        ROUND(
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Borough), 2
        ) AS market_share_percent
    FROM airbnb_listings al
    WHERE price > 0 AND availability_365 BETWEEN 1 AND 364
    GROUP BY neighbourhood, borough
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
    SELECT 
        neighbourhood AS neighbourhood,
        borough,
        AVG(price) AS avg_daily_price,
        AVG(365 - availability_365) AS avg_occupied_nights,
        AVG(price * (365 - availability_365)) AS avg_annual_revenue,
        COUNT(*) AS total_listings,
        COUNT(*) / (SELECT COUNT(*) FROM airbnb_listings WHERE borough = al.borough) * 100 AS market_share_pct
    FROM airbnb_listings al
    WHERE price > 0 AND availability_365 BETWEEN 1 AND 364
    GROUP BY neighbourhood, borough;

WITH airbnb_revenue AS (
    SELECT
        neighbourhood AS neighbourhood,
        Borough AS borough,
        AVG(price) AS avg_daily_price,
        AVG(365 - availability_365) AS avg_occupied_nights,
        AVG(price * (365 - availability_365)) AS avg_annual_revenue,
        COUNT(*) AS total_listings,
        -- Calcul de part de marché par groupe de quartiers
        ROUND(
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Borough), 2
        ) AS market_share_pct
    FROM airbnb_listings al
    WHERE price > 0 AND availability_365 BETWEEN 1 AND 364
    GROUP BY neighbourhood, borough
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
        ar.borough,
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
    borough,
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

-- STEP 3: ROI calculation
-- STEP 1 to 3 inclus
    SELECT 
        neighbourhood AS neighbourhood,
        borough,
        AVG(price) AS avg_daily_price,
        AVG(365 - availability_365) AS avg_occupied_nights,
        AVG(price * (365 - availability_365)) AS avg_annual_revenue,
        COUNT(*) AS total_listings,
        COUNT(*) / (SELECT COUNT(*) FROM airbnb_listings WHERE borough = al.borough) * 100 AS market_share_pct
    FROM airbnb_listings al
    WHERE price > 0 AND availability_365 BETWEEN 1 AND 364
    GROUP BY neighbourhood, borough;

WITH airbnb_revenue AS (
    SELECT
        neighbourhood AS neighbourhood,
        Borough AS borough,
        AVG(price) AS avg_daily_price,
        AVG(365 - availability_365) AS avg_occupied_nights,
        AVG(price * (365 - availability_365)) AS avg_annual_revenue,
        COUNT(*) AS total_listings,
        -- Calcul de part de marché par groupe de quartiers
        ROUND(
            COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Borough), 2
        ) AS market_share_pct
    FROM airbnb_listings al
    WHERE price > 0 AND availability_365 BETWEEN 1 AND 364
    GROUP BY neighbourhood, borough
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
        ar.borough,
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
    borough,
    ROUND(((avg_annual_revenue - total_annual_costs) / acquisition_cost) * 100, 2) AS roi_percentage,
    AVG(ROUND(((avg_annual_revenue - total_annual_costs) / acquisition_cost) * 100, 2)) OVER(PARTITION BY borough) AS avg_roi_borough
FROM roi_calculation
WHERE avg_annual_revenue > 0 AND acquisition_cost > 0
ORDER BY roi_percentage DESC;

#Market Share per neighbourhood (Housing)
WITH borough_totals AS (SELECT Borough AS borough, 
		Neighborhood AS neighborhood,
        COUNT(*) OVER(PARTITION BY Borough) AS n_borough
FROM house_listings)

SELECT borough, neighborhood, 
	COUNT(neighborhood) AS total_listings_neighborhood,
    n_borough AS total_listings_borough,
	(COUNT(neighborhood)/n_borough)*100 AS neighborhood_share
FROM borough_totals
GROUP BY neighborhood, borough
ORDER BY neighborhood_share DESC;

#Market Share per neighbourhood (Airbnb)
WITH ab_borough_totals AS (SELECT borough, 
		neighbourhood,
        COUNT(*) OVER(PARTITION BY borough) AS n_borough
FROM airbnb_listings)

SELECT borough, neighbourhood, 
	COUNT(neighbourhood) AS total_listings_neighbourhood,
    n_borough AS total_listings_borough,
	(COUNT(neighbourhood)/n_borough)*100 AS neighbourhood_share
FROM ab_borough_totals
GROUP BY neighbourhood, borough
ORDER BY neighbourhood_share DESC;