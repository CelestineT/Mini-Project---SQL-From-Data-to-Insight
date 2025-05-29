USE airbnb_invest;
#This returns a table with the number of times a neighbourhood has a sale under average value
SELECT neighbourhood, COUNT(*) AS count
#We SELECT FROM a query that returns the information of all sales that we want to count as valid
FROM (SELECT p.city ,p.neighbourhood, h.Sale_Price AS sale_price, p.avg_sale_price
			#Filter selection to avoid house prices that do not represent a real value (such as 10.000 or 10)
	FROM (SELECT City AS city, Neighbourhood AS neighbourhood, Sale_Price AS sale_price
			FROM nyc_housing_2019
			WHERE Sale_Price > 300000) AS h
            #Filter selection to again to calculate the house average based on real values
	JOIN (SELECT h2.city ,h2.neighbourhood, ROUND(AVG(Sale_Price),2) AS avg_sale_price
			FROM (SELECT City AS city, Neighbourhood AS neighbourhood, Sale_Price AS sale_price
					FROM nyc_housing_2019
					WHERE Sale_Price > 300000) AS h2
			GROUP BY Neighbourhood, City) AS p
	ON h.Neighbourhood = p.neighbourhood
	WHERE sale_price < avg_sale_price) AS main
WHERE neighbourhood != ''
GROUP BY neighbourhood
ORDER BY count DESC;

#Market Share per neighbourhood (Housing)
SELECT n.City AS city ,n.Neighbourhood AS neighbourhood, COUNT(n.Neighbourhood) AS total_n_neighbourhood, c.total_n_city, (COUNT(n.Neighbourhood)/total_n_city)*100 AS n_market_share
FROM nyc_housing_2019 AS n
JOIN (SELECT City, COUNT(*) AS total_n_city
		FROM nyc_housing_2019
		GROUP BY City) as c
ON n.City = c.City
WHERE n.Neighbourhood != ''
GROUP BY n.City, n.Neighbourhood
ORDER BY n_market_share DESC;

#Market Share per neighbourhood (Airbnb)
SELECT 
    c.city,
    n.neighbourhood, 
    COUNT(*) AS n_neighbourhood,
    ROUND(COUNT(*) * 100.0 / c.total_n_city, 2) AS n_market_share,
    c.n_city,
    ROUND(c.n_city * 100.0 / c.total_n_city, 2) AS c_market_share,
    c.total_n_city AS total_count
FROM nyc_airbnb_2019 AS n
JOIN (#Market Share per city (Airbnb)
		SELECT neighbourhood_group AS city, 
		COUNT(*) AS n_city, 
		SUM(COUNT(*)) OVER () AS total_n_city
		FROM nyc_airbnb_2019
		GROUP BY neighbourhood_group) AS c
ON n.neighbourhood_group = c.city
GROUP BY neighbourhood, c.city
ORDER BY n_market_share DESC;