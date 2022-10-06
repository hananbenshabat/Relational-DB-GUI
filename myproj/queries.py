# Queries Array
# Contains the queries
# noinspection SqlResolve
QUERIES = [
    # Query 0:
    """
        SELECT *
        FROM employees
    """,
    # Query 1:
    """
        SELECT *
        FROM invoices
    """,
    # Query 2:
    """
        SELECT *
        FROM tracks
    """,
    # Query 3:
    """
        SELECT invoice_."BillingCountry" AS "Country"
        FROM invoices AS invoice_
        WHERE invoice_."BillingCountry" IN ('USA', 'United Kingdom', 'Canada')
        GROUP BY 1 ORDER BY 1 DESC
    """,
    # Query 4:
    """
        SELECT CAST(strftime('%Y', invoice_."InvoiceDate") AS BIGINT) AS "Year",
            ROUND(SUM(CASE WHEN invoice_."BillingCountry" = 'USA' 
                THEN invoice_."Total" END), 2) AS "USA",
            ROUND(SUM(CASE WHEN invoice_."BillingCountry" = 'United Kingdom' 
                THEN invoice_."Total" END), 2) AS "United Kingdom",
            ROUND(SUM(CASE WHEN invoice_."BillingCountry" = 'Canada'
                THEN invoice_."Total" END), 2) AS "Canada"
        FROM invoices AS invoice_
        WHERE invoice_."BillingCountry" IN ('USA', 'United Kingdom', 'Canada')
        GROUP BY 1 ORDER BY 1 DESC
    """,
    # Query 5:
    """
          SELECT FirstName||" "||LastName as "Customers From Brazil"
          FROM Customers
          WHERE Country = "Brazil";
    """,
    # Query 6:
    """
        SELECT c.FirstName||" "||c.LastName as "Customers", 
               i.InvoiceId,i.InvoiceDate,i.BillingCountry
        FROM Customers c
        LEFT JOIN Invoices i ON i.CustomerId = c.CustomerId
        WHERE c.Country = "Brazil";
    """,
    # Query 7:
    """
        SELECT BillingCountry, COUNT(InvoiceId)
        FROM Invoices
        GROUP BY BillingCountry;
    """,
    # Query 8:
    """
        SELECT COUNT(InvoiceLineId) as "Number Of Line Items"
        FROM Invoice_items 
        WHERE InvoiceId = 37;
    """,
    # Query 9:
    """
        SELECT  c.FirstName||" "||c.LastName as "Customer", 
                i.BillingCountry, e.FirstName||" "||e.LastName as "Sale Agent", i.Total
        FROM Invoices i
        JOIN Customers c ON c.CustomerId = i.CustomerId
        JOIN Employees e ON e.EmployeeId = c.SupportRepId;
    """,
    # Query 10:
    """
        SELECT i.InvoiceId, COUNT(il.InvoiceLineId) as "Number of invoice lines "
        FROM Invoices i
        JOIN Invoice_items il ON i.InvoiceId = il.InvoiceId
        GROUP BY i.InvoiceId;
    """,
    # Query 11:
    """
        SELECT a.Title as "Album", mt.Name as "Media type", g.Name as "Genre"
        FROM Tracks t
        JOIN Albums a ON a.AlbumId = t.AlbumId
        JOIN Media_types mt ON mt.MediaTypeId = t.MediaTypeId
        JOIN Genres g ON t.GenreId = g.GenreId
        GROUP BY a.Title;
    """,
    # Query 12:
    """
        SELECT COUNT(InvoiceId) as "Total Invoices"
        FROM Invoices
        WHERE InvoiceDate between "2009-01-01" AND "2011-01-01";
    """,
    # Query 13:
    """
        SELECT "Media Type" as "Top Media Type", 
            MAX("Times Purchased") as "Times Purchased"
        FROM (SELECT m.Name as "Media type", 
            COUNT (il.Quantity) as "Times Purchased" FROM Invoice_items il
        JOIN Tracks t ON il.TrackId = t.Trackid
        JOIN media_types m ON m.MediaTypeId = t.MediaTypeId
        GROUP BY m.Name);
    """,
    # Query 14:
    """
        SELECT p.Name, COUNT(pt.TrackId) as "Number Of Tracks"
        FROM Playlists p
        JOIN Playlist_track pt ON p.PlaylistId = pt.PlaylistId
        GROUP BY p.name;
    """,
    # Query 15:
    """
        SELECT e.FirstName||" "||e.LastName as "Sales Agent", 
            COUNT(c.SupportRepId) as "Customer Count"
        FROM Employees e
        JOIN Customers c ON c.SupportRepId = e.EmployeeId
        GROUP BY e.EmployeeId;
    """,
    # Query 16:
    """
        SELECT InvoiceLineId, t.Name as "Song", ar.Name as "Artist"
        FROM Invoice_items i 
        JOIN Tracks t ON t.TrackId = i.TrackId
        JOIN Albums a ON a.AlbumId = t.AlbumId
        JOIN Artists ar ON ar.ArtistId = a.ArtistId
        WHERE i.TrackId < 10
        ORDER BY t.TrackId;
    """,
    # Query 17:
    """
        SELECT SUM(Total) as "Total Sales"
        FROM invoices
        WHERE InvoiceDate between "2009-01-01" AND "2010-01-01";
    """,
    # Query 18:
    """
        SELECT SUM(Total) as "Total Sales"
        FROM invoices
        WHERE InvoiceDate between "2010-01-01" AND "2011-01-01";
    """,
    # Query 19:
    """
        SELECT SUM(Total) as "Total Sales"
        FROM invoices
        WHERE InvoiceDate between "2011-01-01" AND "2012-01-01";
    """
]

# Notes array
# Contains the notes of the queries
NOTES = [
    # Note 0 - for query 0:
    "All of the data, unfiltered from the Employees table",
    # Note 1 - for query 1:
    "All of the data, unfiltered from the Invoices table",
    # Note 2 - for query 2:
    "All of the data, unfiltered from the Tracks table",
    # Note 3 - for query 3:
    "Billing countries: USA, United Kingdom, Canada",
    # Note 4 - for query 4:
    "Billing sum per year of USA, United Kingdom, Canada",
    # Note 5 - for query 5:
    "Customers from Brazil",
    # Note 6 - for query 6:
    "Invoices of customers who are from Brazil",
    # Note 7 - for query 7:
    "Number of invoices per country, using: GROUP BY",
    # Note 8 - for query 8:
    "Number of line items of Invoice ID 37",
    # Note 9 - for query 9:
    "Customer, Country, Agent, Total of invoices and customers",
    # Note 10 - for query 10:
    "Invoices, includes the number of invoice line items",
    # Note 11 - for query 11:
    "Tracks, displays no IDs",
    # Note 12 - for query 12:
    "Amount of Invoices in 2009 and 2011",
    # Note 13 - for query 13:
    "Most purchased Media Type",
    # Note 14 - for query 14:
    "Total number of tracks in each playlist",
    # Note 15 - for query 15:
    "Count of customers assigned to each sales agent",
    # Note 16 - for query 16:
    "Purchased track name AND artist name with each invoice",
    # Note 17 - for query 17:
    "Respective total sales of the year 2009",
    # Note 18 - for query 18:
    "Respective total sales of the year 2010",
    # Note 19 - for query 19:
    "Respective total sales of the year 2011"
]

# Queries Example Array
# Contains the valid example queries
QUERIES_VALID_EXAMPLE = [
    # Query Valid Example 0:
    """
        SELECT *
        FROM playlists
    """,
    # Query Valid Example 1:
    """
        SELECT *
        FROM genres
    """,
    # Query Valid Example 2:
    """
        SELECT *
        FROM artists
    """,
    # Query Valid Example 3:
    """
        SELECT *
        FROM albums
    """
]

# Notes Example array
# Contains the notes of the valid example queries
NOTES_VALID_EXAMPLE = [
    # Note valid example 0 - for query valid example 0:
    "All of the data, unfiltered from the playlists table",
    # Note valid example 1 - for query valid example 1:
    "All of the data, unfiltered from the genres table",
    # Note valid example 2 - for query valid example 2:
    "All of the data, unfiltered from the artists table",
    # Note valid example 3 - for query valid example 3:
    "All of the data, unfiltered from the albums table"
]

# Queries Example Array
# Contains the invalid example queries
# noinspection SqlResolve
QUERIES_INVALID_EXAMPLE = [
    # Query Invalid Example 0:
    """
     
    """,
    # Query Invalid Example 1:
    """
        Random Words
                                Spaces
        More Random Words
    """,
    # Query Invalid Example 2:
    """
        SELECT NotExistingColumn
        FROM playlists
    """,
    # Query Invalid Example 3:
    """
        FROM albums
    """
]

# Notes Example array
# Contains the notes of the invalid example queries
NOTES_INVALID_EXAMPLE = [
    # Note invalid example 0 - for query invalid example 0:
    "Empty query, nothing is written",
    # Note invalid example 1 - for query invalid example 1:
    "Random words, not an sql query",
    # Note invalid example 2 - for query invalid example 2:
    "Selects a column that doesnt exists from an existing table",
    # Note invalid example 3 - for query invalid example 3:
    "Half of a query"
]
