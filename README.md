# Song Recommendation Project

Welcome to the Song Recommendation System! This project aims to recommend songs based on user input using data from the Spotify API. By leveraging K-means clustering and cosine similarity, users can receive personalized song recommendations either by providing individual songs or a playlist URL.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Technologies Used](#technologies-used)
- [License](#license)

## Introduction

MeloMap is a web application that recommends songs to users based on their input. It utilizes machine learning models trained on Spotify's song data to generate recommendations.

## Features

- Users can input a song name, artist and year or a playlist Url to receive song recommendations.
- Recommendations are based on the input song's features and similarities to other songs in the dataset.
- The application provides recommendations in real-time using the data from Spotify API.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/manantakkar18/Song-Recommendation-System.git
    ```
2. Run Docker:

    To start the application, run the following command in the project root directory:

    ```bash
    docker-compose up --build
    ```

## Technologies Used
- Django: Backend framework for handling requests and data processing.
- React: Frontend library for building user interfaces.
- Spotify API: Provides access to song data for recommendations.
- Python: Programming language used for backend development and for creating recommendation model.
- JavaScript: Programming language used for frontend development.
- Docker: Containerization platform for packaging the application and its dependencies.


## License
This project is licensed under the MIT License. See the LICENSE file for details.
