# Song Recommendation System

Welcome to the Song Recommendation System! This project aims to recommend songs based on user input using data from the Spotify API. By leveraging K-means clustering and cosine similarity, users can receive personalized song recommendations either by providing individual songs or a playlist URL.


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Documentation](#documentation)
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
2. Navigate to the project directory:

   ```bash
   cd Song-Recommendation-System
    ```
3. Run Docker:

    To start the application, run the following command:

    ```bash
    docker-compose up --build
    ```


## Usage

To use the application, follow the instructions below:

1. **Recommendation by Song**:

   - Search the song

     ![Screenshot 1](https://github.com/manantakkar18/Song-Recommendation-System/blob/main/screenshots/Screenshot%20from%202024-04-16%2011-54-51.png)

   - Select the song, enter the number of recommendations(optional), then click on Get Recommendations

     ![Screenshot 2](https://github.com/manantakkar18/Song-Recommendation-System/blob/main/screenshots/Screenshot%20from%202024-04-16%2012-13-04.png)

   - Click on the recommended song to listen it on spotify

     ![Screenshot 3](https://github.com/manantakkar18/Song-Recommendation-System/blob/main/screenshots/Screenshot%20from%202024-04-16%2012-13-48.png)

2. **Recommendation by Url**:

   - Enter spotify playlist url, enter the number of recommendations(optional), then click on Get Recommendations
     
     ![Screenshot 4](https://github.com/manantakkar18/Song-Recommendation-System/blob/main/screenshots/Screenshot%20from%202024-04-16%2012-17-47.png)

   - Click on the recommended song to listen it on spotify
      
     ![Screenshot 5](https://github.com/manantakkar18/Song-Recommendation-System/blob/main/screenshots/Screenshot%20from%202024-04-16%2012-52-02.png)
   


## Technologies Used
- Django: Backend framework for handling requests and data processing.
- React: Frontend library for building user interfaces.
- Spotify API: Provides access to song data for recommendations.
- Python: Programming language used for backend development and for creating recommendation model.
- JavaScript: Programming language used for frontend development.
- Docker: Containerization platform for packaging the application and its dependencies.


## Documentation

For detailed documentation, including class descriptions and methods, please refer to [Notion Documentation](https://www.notion.so/MananTakkar_Song-Recommendation-System-dfc0b614d4554783893d28592d8c36db?pvs=4).


## License
This project is licensed under the [MIT License](LICENSE). See the [LICENSE](https://github.com/manantakkar18/Song-Recommendation-System/blob/main/LICENSE.txt) file for details.
