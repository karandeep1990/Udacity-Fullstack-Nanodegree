#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def simpleSqlExecution(sql, params):
    conn = connect()
    c = conn.cursor()
    c.execute(sql, params)
    my_list = c.fetchall()
    conn.commit()
    conn.close()
    return my_list

def sqlNoReturn(sql, params):
    conn = connect()
    c = conn.cursor()
    c.execute(sql, params)
    conn.commit()
    conn.close()

def deleteMatches():
    """ Delete all rows from matches table, clears table """
    sql = "DELETE FROM matches"
    sqlNoReturn(sql, ())

def deletePlayers():
    """ Delete all rows from players table, clears table """
    sql = "DELETE FROM players"
    sqlNoReturn(sql, ())


def countPlayers():
    """ Count total players registered """
    sql = "SELECT COUNT(*) FROM players"
    count = simpleSqlExecution(sql, ())[0][0]
    return count


def registerPlayer(name):
    """Adds a player to the tournament database. Name doesnt have to be unique"""

    sql = "INSERT INTO players (name) VALUES (%s)"
    sqlParams = (name, ) # requires comma for one value inside tuple
    sqlNoReturn(sql, sqlParams)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    """
     1) Combine players and matches table (keep players table columns)
     2) Show player id
        show player name
        Count a win for player Id if in winner (grouped by player Id and name)
        Count all matches (grouped by player Id and name)
     4) Sort descending by wins
    """

    sql = ("SELECT players.id as id, name, "
        "COUNT(CASE players.id WHEN winner THEN 1 ELSE NULL END) AS wins, "
        "COUNT(matches.id) as matches "
        "FROM players "
        "LEFT JOIN matches ON players.id IN (winner, loser) "
        "GROUP BY players.id, name "
        "ORDER BY wins DESC")

    conn = connect()
    c = conn.cursor()
    c.execute(sql)
    myPlayers = c.fetchall()
    conn.commit()
    conn.close()
    return myPlayers

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players into the matches table.
    
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    sql = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    sqlNoReturn(sql, (winner, loser))
 
 
def swissPairings():
    """Returns a list of pairs of players (in adjanecet standing) for the next round of a match.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    pairings = []

    standings = playerStandings()
    standingId = 0
    while standingId < len(standings):
        standing1 = standings[standingId]
        standing2 = standings[standingId+1]
        pairings.append((standing1[0], standing1[1], standing2[0], standing2[1]))
        standingId += 2

    return pairings
