import sqlite3
from sqlite3 import Error
import sys

def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        conn.row_factory = sqlite3.Row
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeApp(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def createTables(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        cur = _conn.cursor()
        print("Create table country")
        cur.execute("""CREATE TABLE IF NOT EXISTS country(
                    c_countrykey decimal(2,0) not null primary key,
                    c_name char(25) not null
                    )""")
        
        print("Create table label")
        cur.execute("""CREATE TABLE IF NOT EXISTS label(
                    l_labelkey decimal(3,0) not null primary key,
                    l_name char(25) not null,
                    l_countrykey decimal(2,0) references country(c_countrykey)
                    )""")

        print("Create table users")
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
                    u_userkey decimal(3,0) not null primary key,
                    u_displayname char(30) not null,
                    u_countrykey decimal(2,0) references country (c_countrykey),
                    u_email char(100) not null
                    )""")
        
        print("Create table artist")
        cur.execute("""CREATE TABLE IF NOT EXISTS artists(
                    a_artistkey decimal(3,0) not null primary key,
                    a_name char(30) not null,
                    a_countrykey decimal(2,0) references country (c_countrykey),
                    a_labelkey decimal(2,0) references label (l_labelkey)
                    )""")

        print("Create table tracks")
        cur.execute("""CREATE TABLE IF NOT EXISTS tracks(
                    t_trackkey decimal(3,0) not null primary key,
                    t_name char(50) not null,
                    t_artistkey decimal(3,0) references artist (a_artistkey)
                    )""")

        print("Create table playlists")
        cur.execute("""CREATE TABLE IF NOT EXISTS playlists(
                    p_playlistkey decimal(3,0) not null primary key,
                    p_name char(50) not null
                    )""")

        print("Creating relationship between users and playlists")
        cur.execute("""CREATE TABLE IF NOT EXISTS userplay(
                    up_userkey decimal(3,0) references user (u_userkey),
                    up_playlistkey decimal(3,0) references playlist (p_playlistkey)
                    )""")
        
        print("Creatin relationship between playlists and tracks")
        cur.execute("""CREATE TABLE IF NOT EXISTS playtrack(
                    pt_playlistkey decimal(3,0) references playlists (p_playlistkey),
                    pt_trackkey decimal(3,0) references tracks (t_trackkey)
                    )""")
        
        _conn.commit()
    except Error as e:
        print(e)

#Sql queries
#User queries
def getAllUsers(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT u_displayname as name FROM users""")
        users = response.fetchall()
        num = 1
        for user in users:
            print(str(num) + ". " + user["name"])
            num += 1
        
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def getUserByName(_conn):
    print("++++++++++++++++++++++++++++++++++")
    userName = input("Name of User: ")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT u_displayname as name, c_name, u_email as email
                                FROM users
                                JOIN country ON c_countrykey = u_countrykey
                                WHERE u_displayname = :uName """, {'uName': userName})
        user = response.fetchone()
        print("--------------------------")
        print(user['name'], user['c_name'], user['email'])
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def getUserPlaylists(_conn):
    print("++++++++++++++++++++++++++++++++++")
    nameUser = input("Name of User to Fetch: ")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT p_name as name
                                FROM playlists
                                JOIN userplay on up_playlistkey = p_playlistkey
                                JOIN users on u_userkey = up_userkey
                                WHERE u_displayname = :name""", {'name': nameUser})
        playlists = response.fetchall()
        num = 1
        print("\nPlaylists " + nameUser + " is following:")
        for playlist in playlists:
            print(str(num) + ". " + playlist['name'])
            num += 1
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def updateUser(_conn):
    option = input("""
---------------------------
Update Options:
1 - User's Name
2 - User's Country
3 - User's Email
--------------------------
>>> """)
    chosenUser = input("Name of User to Update: ")
    try:
        if option == '1':
            updatedName = input("New User name: ")
            cur = _conn.cursor()
            cur.execute("""UPDATE users 
                                    SET u_displayname = :newName 
                                    WHERE u_displayname = :oldName""", {'newName': updatedName, 'oldName': chosenUser})
        if option == '2':
            updatedCountry = input("New User country: ")
            cur = _conn.cursor()
            response = cur.execute("SELECT c_countrykey as ckey FROM country WHERE c_name = :name", {'name': updatedCountry})
            newCountry = response.fetchone()
            cur.execute("""UPDATE users 
                        SET u_countrykey = :newCountry 
                        WHERE u_displayname = :Name""", {'newCountry': newCountry['ckey'], 'Name': chosenUser})
        if option == '3':
            updatedEmail = input("New User email: ")
            cur = _conn.cursor()
            cur.execute("""UPDATE users 
                        SET u_email = :newEmail 
                        WHERE u_displayname = :Name""", {'newEmail': updatedEmail, 'Name': chosenUser})
        
        _conn.commit()
        print("Success!")
    except Error as e:
        print(e)
    
def deleteUser(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        chosenUser = input("Name of User to Delete: ")
        cur = _conn.cursor()
        response = cur.execute("SELECT u_userkey as key FROM users WHERE u_displayname = :name", {'name': chosenUser})
        user = response.fetchone()

        cur.execute("""DELETE FROM users
                    WHERE u_userkey = :id""", {'id': user['key']})
        cur.execute("""DELETE FROM userplay
                    WHERE up_userkey = :id""", {'id': user['key']})
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def createUser(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        newName = input("Name: ")
        newCountry = input("Country: ")
        newEmail = input("Email: ")

        cur = _conn.cursor()
        response = cur.execute("SELECT c_countrykey as key FROM country WHERE c_name = :name", {'name': newCountry})
        countryKey = response.fetchone()
        response = cur.execute("SELECT max(u_userkey) as key from users")
        maxId = response.fetchone()
        newId = maxId['key'] + 1
        cur.execute("""INSERT INTO users (u_userkey, u_displayname, u_countrykey, u_email)
                    VALUES (?,?,?,?)""", (newId, newName, countryKey['key'], newEmail))
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

#Playlist queries
def getAllPlaylists(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT p_name as name FROM playlists""")
        playlists = response.fetchall()
        num = 1
        for playlist in playlists:
            print(str(num) + ". " + playlist["name"])
            num += 1
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def getPlaylistFollowers(_conn):
    print("++++++++++++++++++++++++++++++++++")
    namePlaylist = input("Name of Playlist to Fetch: ")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT u_displayname as name
                                FROM users
                                JOIN userplay on up_userkey = u_userkey
                                JOIN playlists on p_playlistkey = up_playlistkey
                                WHERE p_name = :name""", {'name': namePlaylist})
        users = response.fetchall()
        num = 1
        print("Followers of " + namePlaylist + ":")
        for user in users:
            print(str(num) + ". " + user['name'])
            num += 1
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def getPlaylistTracks(_conn):
    print("++++++++++++++++++++++++++++++++++")
    namePlaylist = input("Name of Playlist to Fetch: ")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT t_name, a_name, l_name
                                FROM tracks
                                JOIN artists on a_artistkey = t_artistkey
                                JOIN label on l_labelkey = a_labelkey
                                JOIN playtrack on pt_trackkey = t_trackkey
                                JOIN playlists on p_playlistkey = pt_playlistkey
                                WHERE p_name = :name""", {'name': namePlaylist})
        tracks = response.fetchall()
        num = 1
        print("Tracks of " + namePlaylist + ":")
        for track in tracks:
            print(str(num) + ". " + track['t_name'] + " by " + track['a_name'] + " in " + track['l_name'])
            num += 1
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def updatePlaylist(_conn):
    print("++++++++++++++++++++++++++++++++++")
    chosenPlaylist = input("Name of Playlist to Update: ")
    updatedPlaylist = input("New Playlist Name: ")
    try:
        cur = _conn.cursor()
        cur.execute("""UPDATE playlists 
                    SET p_name = :newName 
                    WHERE p_name = :oldName""", {'newName': updatedPlaylist, 'oldName': chosenPlaylist})
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def addFollowerPlaylist(_conn):
    print("++++++++++++++++++++++++++++++++++")
    namePlaylist = input("Name of Playlist to follow: ")
    nameUser = input("Name of User to Follow Playlist: ")

    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT p_playlistkey as key FROM playlists WHERE p_name = :name""", {'name': namePlaylist})
        pId = response.fetchone()
        response = cur.execute("""SELECT u_userkey as key FROM users WHERE u_displayname = :name""", {'name': nameUser})
        uId = response.fetchone()

        response = cur.execute("""INSERT INTO userplay (up_userkey, up_playlistkey) 
                                VALUES (:ukey, :pkey)""", {'ukey': uId['key'], 'pkey': pId['key']})
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def removeFollowerPlaylist(_conn):
    print("++++++++++++++++++++++++++++++++++")
    namePlaylist = input("Name of Playlist to unfollow: ")
    nameUser = input("Name of User to Unfollow from Playlist: ")

    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT p_playlistkey as key FROM playlists WHERE p_name = :name""", {'name': namePlaylist})
        pId = response.fetchone()
        response = cur.execute("""SELECT u_userkey as key FROM users WHERE u_displayname = :name""", {'name': nameUser})
        uId = response.fetchone()

        response = cur.execute("""DELETE FROM userplay  
                                WHERE up_userkey = :ukey
                                    AND up_playlistkey = :pkey""", {'ukey': uId['key'], 'pkey': pId['key']})
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def addTrackPlaylist(_conn):
    print("++++++++++++++++++++++++++++++++++")
    namePlaylist = input("Name of Playlist: ")
    nameTrack = input("Name of Track to Add: ")

    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT p_playlistkey as key FROM playlists WHERE p_name = :name""", {'name': namePlaylist})
        pId = response.fetchone()
        response = cur.execute("""SELECT t_trackkey as key FROM tracks WHERE t_name = :name""", {'name': nameTrack})
        tId = response.fetchone()

        response = cur.execute("""INSERT INTO playtrack (pt_playlistkey, pt_trackkey) 
                                VALUES (:pkey, :tkey)""", {'tkey': tId['key'], 'pkey': pId['key']})
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def removeTrackPlaylist(_conn):
    print("++++++++++++++++++++++++++++++++++")
    namePlaylist = input("Name of Playlist: ")
    nameTrack = input("Name of Track to Remove: ")

    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT p_playlistkey as key FROM playlists WHERE p_name = :name""", {'name': namePlaylist})
        pId = response.fetchone()
        response = cur.execute("""SELECT t_trackkey as key FROM tracks WHERE t_name = :name""", {'name': nameTrack})
        tId = response.fetchone()

        response = cur.execute("""DELETE FROM playtrack  
                                WHERE pt_playlistkey = :pkey
                                    AND pt_trackkey = :tkey""", {'tey': tId['key'], 'pkey': pId['key']})
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def deletePlaylist(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        chosenPlaylist = input("Name of Playlist to Delete: ")
        cur = _conn.cursor()
        response = cur.execute("SELECT p_playlistkey as key FROM playlists WHERE p_name = :name", {'name': chosenPlaylist})
        playlist = response.fetchone()

        cur.execute("""DELETE FROM playlists
                    WHERE p_playlistkey = :id""", {'id': playlist['key']})
        cur.execute("""DELETE FROM userplay
                    WHERE up_playlistkey = :id""", {'id': playlist['key']})
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def createPlaylist(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        newName = input("Playlist Name: ")

        cur = _conn.cursor()
        response = cur.execute("SELECT max(p_playlistkey) as key from playlists")
        maxId = response.fetchone()
        newId = maxId['key'] + 1
        cur.execute("""INSERT INTO playlists (p_playlistkey, p_name)
                    VALUES (?,?)""", (newId, newName))
        _conn.commit()
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

#Artist options
def getAllArtists(_conn):
    print("++++++++++++++++++++++++++++++++++")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT a_name as name FROM artists""")
        artists = response.fetchall()
        num = 1
        for artist in artists:
            print(str(num) + ". " + artist["name"])
            num += 1
        
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def getArtistByName(_conn):
    print("++++++++++++++++++++++++++++++++++")
    artistName = input("Name of Artist: ")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT a_name as name, c_name, l_name as label
                                FROM artists
                                JOIN country ON c_countrykey = a_countrykey
                                JOIN label ON l_labelkey = a_labelkey
                                WHERE a_name = :uName """, {'uName': artistName})
        artist = response.fetchone()
        print("--------------------------")
        print(artist['name'], artist['c_name'], artist['label'])
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def getArtistTracks(_conn):
    print("++++++++++++++++++++++++++++++++++")
    nameArtist = input("Name of Artist to Fetch: ")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT t_name
                                FROM tracks
                                JOIN artists on a_artistkey = t_artistkey
                                WHERE a_name = :name""", {'name': nameArtist})
        tracks = response.fetchall()
        num = 1
        print("Tracks of " + nameArtist + ":")
        for track in tracks:
            print(str(num) + ". " + track['t_name'])
            num += 1
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

def getArtistPlaylists(_conn):
    print("++++++++++++++++++++++++++++++++++")
    nameArtist = input("Name of Artist to Fetch: ")
    try:
        cur = _conn.cursor()
        response = cur.execute("""SELECT p_name as name
                                FROM playlists
                                JOIN playtrack on pt_playlistkey = p_playlistkey
                                JOIN tracks on t_trackkey = pt_trackkey
                                JOIN artists on a_artistkey = t_artistkey
                                WHERE a_name = :name""", {'name': nameArtist})
        playlists = response.fetchall()
        num = 1
        print("\nPlaylists " + nameArtist + " is following:")
        for playlist in playlists:
            print(str(num) + ". " + playlist['name'])
            num += 1
    except Error as e:
        print(e)
    print("++++++++++++++++++++++++++++++++++")

#Table options
def userOptions(conn):
    option = input("""
---------------------------
1 - Get All Users
2 - Get User Info By Name
3 - Get Playlist User Follows
4 - Update User Info 
5 - Delete User
6 - Create User
--------------------------
>>> """)
    if option == '1':
        getAllUsers(conn)
    elif option == '2':
        getUserByName(conn)
    elif option == '3':
        getUserPlaylists(conn)
    elif option == '4':
        updateUser(conn)
    elif option == '5':
        deleteUser(conn)
    elif option == '6':
        createUser(conn)
    else:
        print("Unknown option. Taking you back to main menu!")

def playlistOptions(conn):
    option = input("""
---------------------------
1 - Get All Playlists
2 - Get Users Following Playlist
3 - Get Playlist's Tracks
4 - Update Playlist Name
5 - Add Follower to Playlist
6 - Remove Follower from Playlist
7 - Add Track to Playlist
8 - Remove Track from Playlist
9 - Delete Playlist
10 - Create Playlist
--------------------------
>>> """)
    if option == '1':
        getAllPlaylists(conn)
    elif option == '2':
        getPlaylistFollowers(conn)
    elif option == '3':
        getPlaylistTracks(conn)
    elif option == '4':
        updatePlaylist(conn)
    elif option == '5':
        addFollowerPlaylist(conn)
    elif option == '6':
        removeFollowerPlaylist(conn)
    elif option == '7':
        addTrackPlaylist(conn)
    elif option == '8':
        removeTrackPlaylist(conn)
    elif option == '9':
        deletePlaylist(conn)
    elif option == '10':
        createPlaylist(conn)
    else:
        print("Unknown option. Taking you back to main menu!")

def artistOptions(conn):
    option = input("""
---------------------------
1 - Get All Artists
2 - Get Artist Info By Name
3 - Get Artist Tracks
4 - Get Playlists with Artist
--------------------------
>>> """)
    if option == '1':
        getAllArtists(conn)
    elif option == '2':
        getArtistByName(conn)
    elif option == '3':
        getArtistTracks(conn)
    elif option =='4':
        getArtistPlaylists(conn)
    else:
        print("Unknown option. Taking you back to main menu!")

def options(conn, database):
    option = input("""
---------------------------
Options:
1 - Users
2 - Playlists
3 - Artists
0 - Exit
--------------------------
>>> """)
    if option == '0':
        closeApp(conn, database)
        sys.exit()
    elif option == '1':
        userOptions(conn)
    elif option == '2':
        playlistOptions(conn)
    elif option == '3':
        artistOptions(conn)
    else:
        print("Incorrect option. Try Again!")


def main():
    database = r"music.sqlite"
    
    conn = openConnection(database)
    print("Welcome to the music project!")
    while True :
        options(conn, database)

if __name__ == '__main__':
    main()