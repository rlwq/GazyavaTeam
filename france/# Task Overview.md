## 📌 Task Title

Point par point

## 🌍 Country

France — Europe (Data Science & Classic ML)

## 📖 Storyline

Paris, 1886. Two French painters, Georges Seurat and Paul Signac, stop mixing colours on the palette. They open a completely new direction instead. They paint with tiny dots of pure colour, placed side by side. Up close, the canvas is only noise. Step back, and the eye joins the dots into a Sunday afternoon by the Seine. The style gets a name: pointillism.

140 years later, a Parisian artist known only as _Le Pointilliste_ picks up the brush to create. This time the canvas is not linen. It is Paris itself, seen through the places where its visitors stay.

Every listing in the city became a dot. Then the artist slipped in some dots of their own. Their colours came from what every traveller weighs before booking a night. Together they form letters.

The artwork was unveiled as a plain spreadsheet, with a single caption: _"Grey is pretty. It holds multiple secrets."_

## 🔥 Difficulty

Easy

## 🎯 Objective

Find the word the artist hid in the accommodation data of Paris. Separate the letters from the rest of the city, look at each of them, and read the word in the artist's order.

## 🚩 FLAG

`SIGMOID_<WORD>`, where `<WORD>` is the string extracted after successfully solving the task.

## 📂 Task Input

The provided /Users/natankatsif/Projects/gazyava/france/paris_listings.csv , and 18 columns.

- `listing_id`: Listing identifier;
- `neighbourhood`: Paris arrondissement name;
- `room_type`, `property_type`: Kind of accommodation;
- `latitude`, `longitude`: Location of the listing (shifted by up to ~150 m for privacy);
- `accommodates`, `bedrooms`, `beds`: Capacity;
- `price`: Price per night, EUR;
- `minimum_nights`: Minimum stay;
- `availability_365`: Nights available for booking in the next 365 days;
- `number_of_reviews`, `number_of_reviews_ltm`: Reviews in total / in the last 12 months;
- `reviews_per_month`: Average number of reviews per month since the first review;
- `review_scores_rating`: Average guest rating, 0–5;
- `host_is_superhost`: Whether the host has Superhost status;
- `calculated_host_listings_count`: Number of listings the host has in Paris.

## ✅ Expected Output

Submit on the platform: The flag, in the format `SIGMOID_<WORD>`.

A URL with the code and results that helped to identify and extract the flag.

## 🏆 Scoring Criteria

This task uses **Flag Evaluation**, and organisers review the linked write-up manually.

- ✅ Correct flag **and** a write-up whose code, figure and `labels.csv` show the clustered word: 100 points (PASS)
- ❌ Incorrect flag, or a correct flag without code, figure and labels that support it: 0 points (FAIL)