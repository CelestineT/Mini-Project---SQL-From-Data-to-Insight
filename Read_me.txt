The repository cointains:
    (1) Airbnb_invest.py - the python file that cleans and enriches the data gathered
    (2) airbnb_invest_script.sql - the sql script that analyzes the data from the python file
    (3) airbnb_invest.sql - the sql schema
    (4) grapher.py - needs the data form Airbnb_invest.py and the tables from airbnb_invest.sql
    (5) data - contains all the raw, clean and final data for the project
    (6) requirements.txt

airbnb_invest.sql: performs a cross-analysis of Airbnb revenue and real estate costs at the neighborhood level to identify the most profitable short-term rental investment opportunities
in New York City. It is structured in three main steps:
    (1) calculation of average Airbnb revenues, including estimated occupancy, annual income, and market share by neighborhood group;
    (2) estimation of property acquisition costs based on 2019 residential sales data;
    and (3) ROI (Return on Investment) computation, factoring in maintenance costs, property taxes, and HOA fees.                                                                                                                                             The final output ranks neighborhoods by ROI percentage, investment tier, and competition level (e.g., HIGH_Competition, MODERATE_Competition, MID_TIER_OPPORTUNITY etc), providing a data-driven guide to identify the most attractive areas for short-term rental investments.

In also performs an alaysis of the market share:
    (1) per house listings: using the house_listings table and calculating:
        a. The total listings (COUNT(*))
        b. The neighborhood market share ((total listings per neighborhood/total listings per district)*100)
    (2) per Airbnb listings: using the airbnb_listings table and calculating:
        a. The total listings (COUNT(*))
        b. The neighborhood market share ((total listings per neighborhood/total listings per district)*100)