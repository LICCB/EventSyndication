--
-- File generated with SQLiteStudio v3.1.1 on Thu Dec 1 15:26:14 2016
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: EventInfo
CREATE TABLE EventInfo (
    EventID          INTEGER	   PRIMARY KEY
                                   UNIQUE
                                   NOT NULL,
    EventName        VARCHAR       NOT NULL,
    EventDescription VARCHAR,
    EventLocation    VARCHAR
);


-- Table: EventLog
CREATE TABLE EventLog (
    TripID     INTEGER  PRIMARY KEY
                        UNIQUE
                        NOT NULL,
    EventID    INTEGER  REFERENCES EventInfo (EventID),
    EventStart DATETIME NOT NULL,
    EventEnd   DATETIME,
    PostingID  INTEGER  REFERENCES Postings (PostingID) 
);


-- Table: Postings
CREATE TABLE Postings (
    PostingID  INTEGER NOT NULL
                       PRIMARY KEY
                       UNIQUE,
    TripID     INTEGER REFERENCES EventLog (TripID) 
                       NOT NULL,
    Facebook   BIT     DEFAULT (0) 
                       NOT NULL,
    MeetUp     BIT     NOT NULL
                       DEFAULT (0),
    EventBrite BIT     NOT NULL
                       DEFAULT (0) 
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
