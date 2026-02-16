# Commerce – CS50 Web Programming Project

This project is an online auction platform built with Django as part of Harvard's CS50 Web Programming course.

## 🚀 Features

- User registration and authentication
- Create new auction listings
- Place bids on active listings
- Add listings to a personal watchlist
- Comment on listings
- Close auctions
- Automatic winner detection (highest bidder)
- Display auction status (active/closed)
- Admin panel for managing listings, bids, and comments

## 🛠️ Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap

## 📂 Project Structure

- `models.py` → Database models (Listing, Bid, Comment, Watchlist)
- `views.py` → Business logic and request handling
- `urls.py` → URL routing
- `templates/` → HTML templates
- `static/` → CSS and static files

## 🧠 Auction Logic

- Users can place bids higher than the current price.
- The listing owner can close the auction.
- When closed, the highest bidder becomes the winner.
- The winner is displayed on the listing page.

## 💬 Comment System

- Authenticated users can add comments.
- Comments are linked to a specific listing.
- Comments are displayed under each listing.

## ▶️ How to Run

1. Clone the repository  
2. Navigate to the project folder  
3. Run:

```bash
python manage.py migrate
python manage.py runserver
