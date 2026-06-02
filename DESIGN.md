# 🎬 Movixra API Documentation

## Base URL

```bash
/api/v1/
```

---

# 1. Get All Movies With Available Shows

Returns all movies that currently have active shows.

## Endpoint

```http
GET /api/v1/movies/
```

## Response

```json
{
  "success": true,
  "data": [
    {
      "movie_title": "Lets Start",
      "movie_poster": "img.webp",
      "movie_slug": "lets-start",
      "movie_format": "IMAX",
      "movie_language": "English"
    },
    {
      "movie_title": "Lets Start 1",
      "movie_poster": "img.webp",
      "movie_slug": "lets-start1",
      "movie_format": "IMAX",
      "movie_language": "English"
    }
  ]
}
```

---

# 2. Get Available Shows of a Movie

Returns all available shows for a specific movie.

## Endpoint

```http
GET /api/v1/cinema/movies/<movie-slug>/available-shows/
```

## Response

```json
{
  "success": true,
  "message": "Available shows fetched successfully.",
  "errors": null,
  "data": [
    {
      "movie": "Lets Start",
      "screen": "Hall 1",
      "slug": "lets-start-hall-1-120000",
      "format_type": "IMAX",
      "show_date": "2026-07-01",
      "start_time": "12:00:00",
      "end_time": "14:00:00",
      "is_active": true
    },
    {
      "movie": "Lets Start",
      "screen": "Hall 1",
      "slug": "lets-start-hall-1-150000",
      "format_type": "IMAX",
      "show_date": "2026-07-01",
      "start_time": "15:00:00",
      "end_time": "17:00:00",
      "is_active": true
    }
  ]
}
```

---

# 3. Get Movie Details

Returns detailed information about a specific movie.

## Endpoint

```http
GET /api/v1/movies/<movie-slug>/
```

## Example

```http
GET /api/v1/movies/lets-start-2023/
```

## Response

```json
{
  "id": 1,
  "title": "Lets Start",
  "slug": "lets-start-2023",
  "description": "This is the movie named Lets Start.",
  "poster": "http://res.cloudinary.com/dtxh9hjpd/image/upload/v1780310067/oojawjl4lgclxd0wiq75.png",
  "trailer_url": "https://www.outfsf.com",
  "rating": 3.4,
  "release_date": "2023-12-12",
  "duration_minutes": 120,
  "genres": [
    {
      "id": 1,
      "name": "Action",
      "slug": "action"
    }
  ],
  "language": "Urdu"
}
```

---

# 4. Get Movie Cast

Returns the cast members of a specific movie.

## Endpoint

```http
GET /api/v1/movies/<movie-slug>/cast/
```

## Example

```http
GET /api/v1/movies/lets-start-2023/cast/
```

## Response

```json
[
  {
    "id": 1,
    "actor": {
      "id": 1,
      "name": "Husnain",
      "slug": "husnain",
      "bio": "hero",
      "birth_date": "2026-06-01",
      "photo": "http://res.cloudinary.com/dtxh9hjpd/image/upload/v1780311865/gyu2d8al3j0r1pvrilkt.png"
    },
    "role_name": "Developer"
  }
]
```

---

# 5. Get Show Seats & Booking Status

Returns all seats of a specific show along with their booking status.

## Endpoint

```http
GET /api/v1/booking/shows/<show-slug>/seats/
```

## Response

```json
{
  "success": true,
  "message": "Seats fetched successfully.",
  "errors": null,
  "data": {
    "show": "lets-begin-hall-1-120000",
    "hall": "Hall 1",
    "seats": [
      {
        "id": 1,
        "seat_number": "A1",
        "seat_type": "Regular",
        "price": "500.00",
        "is_booked": true
      },
      {
        "id": 2,
        "seat_number": "A2",
        "seat_type": "Regular",
        "price": "500.00",
        "is_booked": false
      }
    ]
  }
}
```

---

# 6. Book Movie Tickets

Creates a booking for selected seats of a show.

## Endpoint

```http
POST /api/v1/booking/shows/<show-slug>/book/
```

## Example Request

```json
{
  "customer_email": "demo@gmail.com",
  "seat_ids": [1, 2]
}
```

## Response

```json
{
  "success": true,
  "message": "Booking created successfully. Please complete payment within 5 minutes.",
  "errors": null,
  "data": {
    "booking_id": "a3b32753-ca31-4f2f-a56e-af1c789f8423",
    "customer_email": "demo@gmail.com",
    "total_amount": "1000.00",
    "status": "pending",
    "show_slug": "lets-begin-hall-1-120000",
    "created_at": "2026-06-02T04:32:55.658332Z",
    "booked_seats": [
      {
        "id": 5,
        "seat": 1,
        "seat_number": "A1",
        "price": "500.00"
      },
      {
        "id": 6,
        "seat": 2,
        "seat_number": "A2",
        "price": "500.00"
      }
    ]
  }
}
```

---

# 7. Payment of Booking
## Endpoint
```
POST api/v1/payments/create/<uuid:booking_id>/
```
## Response

```
{
    "success": true,
    "approval_url": "https://www.sandbox.paypal.com/checkoutnow?token=XXXX",
    "paypal_order_id": "XXXX"
}
```

# 📌 Notes

* All responses are returned in JSON format.
* Seat booking is temporary until payment is completed.
* Booking status is initially marked as `pending`.
* Seat availability updates dynamically based on bookings.
* Authentication is currently not required.
* Payment integration will be added later.

---

