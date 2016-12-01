

CREATE TABLE EventInfo (
    EventID          SERIAL        PRIMARY KEY
                                   UNIQUE
                                   NOT NULL,
    EventName        VARCHAR (256) NOT NULL,
    EventDescription VARCHAR,
    EventLocation    VARCHAR
);


CREATE TABLE EventLog (
    TripID     SERIAL   PRIMARY KEY
                        UNIQUE
                        NOT NULL,
    EventID    SERIAL   REFERENCES EventInfo (EventID),
    EventStart TIMESTAMP NOT NULL,
    EventEnd   TIMESTAMP,
    PostingID  SERIAL 
);


CREATE TABLE Postings (
    PostingID  SERIAL  NOT NULL
                       PRIMARY KEY
                       UNIQUE,
    TripID     SERIAL  REFERENCES EventLog (TripID) 
                       NOT NULL,
    Facebook   BIT     DEFAULT (0::bit) 
                       NOT NULL,
    MeetUp     BIT     NOT NULL
                       DEFAULT (0::bit),
    EventBrite BIT     NOT NULL
                       DEFAULT (0::bit) 
);

ALTER TABLE EventLog
ADD CONSTRAINT postingIDfk FOREIGN KEY (PostingID) REFERENCES Postings (PostingID) MATCH FULL