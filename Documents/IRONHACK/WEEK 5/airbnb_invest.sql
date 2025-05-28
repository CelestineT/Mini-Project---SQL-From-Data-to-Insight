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
