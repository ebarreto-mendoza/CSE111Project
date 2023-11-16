# Spotify Music Quiz App

## Table of Contents

- [Description](#description)
- [Phase 2](#phase-2)
- [Phase 1](#phase-1)

## Description

    The goal of this project is to utilize Spotify's Web API in order to make an application that allows a user to log in and quiz themselves. The quiz will be based on the user's saved tracks in thier playlists or thier top ranked songs that Spotify calculates.

    The project group consists of:
    - Lucero Ascencio
    - Eduardo Barreto-Mendoza

## Phase 2

## UPDATED UML Case

![An Updated UML Case Diagram that represents the main use cases of the program](/project_assets/uml_user_case2.png)

The above image represents the main user case for our application:

The user will have 3 main control options:

- **Users:** Options that have to deal with the User database and its relations
  1. **Get All Users** Returns all User's display names
  2. **Get User Info By Name** Returns entire data of a single User
  3. **Get Playlist User Follows** Returns entire data of a single User
  4. **Update User Info** Provides options to update User Info
     a. User's Name
     b. User's Country
     c. User's Email
  5. **Delete User** Deletes a user provided by User's display name
  6. **Create User** Creates a user provided with the display name, country, and email of the new User
- **Playlists:** Options that have to deal with the PLaylist database and its relations
  1. **Get All Playlists** Returns all Playlist names
  2. **Get Users Following Playlist** Returns the names of Users following the playlist provided by the playlist name
  3. **Get Playlist's Tracks** Returns the tracks ins a Playlist provided by the playlist name
  4. **Update Playlist Name** Allows user to update a playlist name provided by the name of the playlist
  5. **Add Follower to Playlist** Allows a user to add a follower to a playlist provided by the user's name and playlist's name
  6. **Remove Follower from Playlist** Allows a user to remove a follower to a playlist provided by the user's name and playlist's name
  7. **Add Track to Playlist** Allows a user to add a track to a playlist provided by the track's name and playlist's name
  8. **Remove Track from Playlist** Allows a user to remove a track to a playlist provided by the track's name and playlist's name
  9. **Delete Playlist** Deletes a playlist, includeing its followers and tracks, provided by the playlists name
  10. **Create Playlist** Creates a playlist, provided by the playlists name
- **Artists:** Options that have to deal with the Artists database and its relations
  1. **Get All Artists** Returns all artist names
  2. **Get Artist Info By Name** Returns a single artist's info provided by the artist's name
  3. **Get Artist Tracks** Returns all tracks that is owned by an artist provided by the artist's name
  4. **Get Playlists with Artist** Returns all playlists that contains tracks of a single artist, provided by the artist's name

## UPDATED E/R Diagram

## Phase 1

### UML Case

![UML Case Diagram that represents the main use case of the program](/project_assets/uml_user_case.png)

The above image represents the main user case for our application:

- **User Login:** In order to do anything, the User must be logged in
  - **View Top Tracks:** list User's top tracks in ascending order
    - **User Top Track Stats:** using the User's profile information, the Spotify API will send the User's stats.
    - **Play Track:** using the Spotify API, and the User's account, User can listen to the a single Track, one at a time.
  - **Play Game:** play a quiz game based on user’s songs
    - **Set Game Rules:** must set options (i.e. number of rounds, number of questions per round, etc.) -**User Playlist Tracks:** using Spotify API, get the tracks inside the current User’s chosen playlist, then play quiz with those tracks
    - **User Top Tracks:** using Spotify API, get the current User’s top tracks, then play quiz with those tracks
    - **Play Song:** using Spotify API, and user account, enable play song feature

### E/R Diagram

![ER Diagram with relations](/project_assets/er_diagram+relation.png)

The above ER diagram contains the following entities:

- Users
  - Spotify User information
- Playlist
  - Current User owned playlists
- Track
  - Tracks inside of Playlist or top User's tracks
- Album
  - The album information that the tracks are related to
- Artists
  - The artist information that the track is owned by
- URL
  - Deeper infomation on individual users, playlists, tracks, album, and artists that is held in other areas, besides thier respective tables.
