-- Show warnings;
warnings;

drop table if exists FullPitches;
drop table if exists PartialPitches;
drop table if exists tempPitches;
drop table if exists NonPlayerBallOrStrikeEjections;
drop table if exists PlayerBallOrStrikeEjections;
drop table if exists NonPlayerEjections;
drop table if exists PlayerEjections;
drop table if exists tempEjections;
drop table if exists AtBats;
drop table if exists GameOfficials;
drop table if exists Games;
drop table if exists tempGames;
drop table if exists PlayerNames;
drop table if exists Teams;

-- Creating Teams

create table Teams (
    teamID decimal(2),
    abbreviation char(3),
    place char(15),
    name char(15),

    primary key(teamID)
);

INSERT INTO Teams
VALUES 
(01,'ANA', 'Los Angeles', 'Angels'),
(02,'ARI','Arizona', 'Diamondbacks'),
(03,'ATL','Atlanta', 'Braves'),
(04,'BAL','Baltimore', 'Orioles'),
(05,'BOS','Boston', 'Red Sox'),
(06,'CHA','Chicago', 'White Sox'),
(07,'CHN','Chicago', 'Cubs'),
(08,'CIN','Cincinnati','Reds'),
(09,'CLE','Cleveland','Indians'),
(10,'COL','Colorado','Rockies'),
(11,'DET','Detroit','Tigers'),
(12,'HOU','Houston','Astros'),
(13,'KCA','Kansas City','Royals'),
(14,'LAN','Los Angeles','Dodgers'),
(15,'MIA','Miami','Marlins'),
(16,'MIL','Milwaukee','Brewers'),
(17,'MIN','Cincinnati','Reds'),
(18,'NYA','New York','Yankees'),
(19,'NYN','New York','Mets'),
(20,'OAK','Oakland','Athletics'),
(21,'PHI','Philadelphia','Phillies'),
(22,'PIT','Pittsburg','Pirates'),
(23,'SDN','San Diego','Padres'),
(24,'SEA','Seattle','Mariners'),
(25,'SFN','San Francisco','Giants'),
(26,'SLN','St. Louis','Cardinals'),
(27,'TBA','Tampa Bay','Rays'),
(28,'TEX','Texas','Rangers'),
(29,'TOR','Toronto','Blue Jays'),
(30,'WAS','Washington','Nationals');

-- Creating PlayerNames

create table PlayerNames (
            playerID decimal(6),
            firstName char(20),
            lastName char(20),
-- Key Constraints
            primary key (playerID)
-- Integrity Constraints
);

load data LOCAL infile '~/Documents/ece356/DockerForA2/ece356_project/MLB/player_names.csv' ignore into table PlayerNames
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines;

-- Creating Games

create table TempGames (
            attendance int,
            awayScore int,
            awayTeamName char(3),
            date datetime,
            elapsed_time int,
            gameID decimal(9),
            homeScore decimal(2),
            homeTeamName char(3),
            startTime varchar(8),
            umpire1B char(20),
            umpire2B char(20),
            umpire3B char(20),
            umpireHP char(20),
            venueName text,
            weather text,
            wind text,
            delay int
);

load data LOCAL infile '~/Documents/ece356/DockerForA2/ece356_project/MLB/games.csv' ignore into table TempGames
     fields terminated by ','
     enclosed by '"'
     lines terminated by '\n'
     ignore 1 lines
     (attendance,
     awayScore,
     awayTeamName, -- awayTeamID
     date,
     elapsed_time,
     gameID,
     homeScore,
     homeTeamName, -- homeTeamID
     startTime,
     umpire1B,
     umpire2B,
     umpire3B,
     umpireHP,
     venueName,
     weather,
     wind,
     delay
     );

create table Games (
            attendance int,
            awayScore int,
            awayTeamID decimal(2),
            dateTime datetime,
            elapsed_time int,
            gameID decimal(9),
            homeScore decimal(2),
            homeTeamID decimal(2),
            venueName text,
            weather text,
            wind text,
            delay int,

            primary key (gameID),
            foreign key (homeTeamID) references Teams(teamID),
            foreign key (awayTeamID) references Teams(teamID)
            
);

-- insert into Games
--     SELECT attendance, awayScore, Teams.teamID, date +  STR_TO_DATE(startTime, '%h:%i %p'), elapsed_time, gameID, homeScore, B.teamID, venueName, weather, wind, delay
--     FROM (
--         TempGames INNER JOIN Teams ON TempGames.awayTeamName = Teams.abbreviation

--         INNER JOIN 

--         (SELECT * FROM Teams) AS B ON TempGames.homeTeamName = B.abbreviation
--     ) 
--     WHERE gameID is not NULL;

insert into Games
    SELECT attendance, awayScore, Teams.teamID, date, elapsed_time, gameID, homeScore, B.teamID, venueName, weather, wind, delay
    FROM (
        TempGames INNER JOIN Teams ON TempGames.awayTeamName = Teams.abbreviation

        INNER JOIN 

        (SELECT * FROM Teams) AS B ON TempGames.homeTeamName = B.abbreviation
    ) 
    WHERE gameID is not NULL;

-- Creating GameOfficials

create table GameOfficials(
    gameID decimal(9),
    umpire1B char(20),
    umpire2B char(20),
    umpire3B char(20),
    umpireHP char(20),

    primary key(gameID),
    foreign key (gameID) references Games(gameID)
);

insert into GameOfficials select gameID,  umpire1B,  umpire2B,  umpire3B,  umpireHP from TempGames;

-- Creatings AtBats

create table AtBats (
            abID decimal(10),
            batterID decimal(6),
            event text,
            gameID decimal(9),
            inning int,
            outs decimal(1),
            pScore int,
            pThrows char(1),
            pitcherID decimal(6),
            stand char(1),
            isTop BOOL,

		    primary key (abID),
            foreign key (gameID) references Games(gameID),
		    foreign key (batterID) references PlayerNames(playerID),
		    foreign key (pitcherID) references PlayerNames(playerID),

       	    check (outs <= 3 AND outs >= 0),
            check (pThrows = 'L' OR pThrows = 'R'),
            check (stand = 'L' OR stand = 'R'),
            check (isTop = 1 OR isTop = 0)
);

load data LOCAL infile '~/Documents/ece356/DockerForA2/ece356_project/MLB/atbats.csv' ignore into table AtBats
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (abID,batterID,event,gameID,inning,outs,pScore,pThrows,pitcherID,stand,@isTop)
    set isTop = if (@isTop like 'TRUE', 1, 0);

-- Creatings Ejections

create table tempEjections (
            abID decimal(10),
            des text,
            gameID decimal(9),
            playerID decimal(6),
            bs char(1),
            correct varchar(2),
            abbreviation char(3)
);

load data LOCAL infile '~/Documents/ece356/DockerForA2/ece356_project/MLB/ejections.csv' ignore into table tempEjections
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (abID,des,@throwAway,gameID,playerID,@throwAway,bs,correct,abbreviation,@throwAway);

create table PlayerEjections (
            abID decimal(10),
            des text,
            gameID decimal(9),
            playerID decimal(6),
            teamID decimal(2),
-- Key Constraints
            primary key (gameID, playerID),
		    foreign key (playerID) references PlayerNames(playerID),
            foreign key (abID) references AtBats(abID),
            foreign key (gameID) references Games(gameID),
		    foreign key (teamID) references Teams(teamID)
-- Integrity Constraints
       	    -- None
);

insert into PlayerEjections select DISTINCT A.abID, des, gameID, playerID, Teams.teamID from (
    (select MIN(abID) as abID from tempEjections group by gameID, playerID) as A
    INNER JOIN
    tempEjections ON A.abID = tempEjections.abid
    INNER JOIN Teams ON tempEjections.abbreviation = Teams.abbreviation)
    WHERE playerID in (select PlayerID from PlayerNames);

create table NonPlayerEjections (
            abID decimal(10),
            des text,
            gameID decimal(9),
            playerID decimal(6),
            teamID decimal(2),
-- Key Constraints
            primary key (gameID, playerID),
            foreign key (abID) references AtBats(abID),
            foreign key (gameID) references Games(gameID),
		    foreign key (teamID) references Teams(teamID)
-- Integrity Constraints
       	    -- None
);

insert into NonPlayerEjections select DISTINCT A.abID, des, gameID, playerID, Teams.teamID from (
    (select MIN(abID) as abID from tempEjections group by gameID, playerID) as A
    INNER JOIN
    tempEjections ON A.abID = tempEjections.abid
    INNER JOIN Teams ON tempEjections.abbreviation = Teams.abbreviation)
    WHERE playerID not in (select PlayerID from PlayerNames);

create table PlayerBallOrStrikeEjections (
            gameID decimal(10),
            playerID decimal(6),
		    correct varchar(2),
-- Key Constraints
		    primary key (gameID, playerID)
            -- foreign key (playerID) references PlayerEjections(playerID),
            -- foreign key (gameID) references PlayerEjections(gameID)
-- Integrity Constraints
       	    -- None
);

insert into PlayerBallOrStrikeEjections select DISTINCT gameID, playerID, correct from (
    (select MIN(abID) as abID from tempEjections group by gameID, playerID) as A
    INNER JOIN
    tempEjections ON A.abID = tempEjections.abid
    INNER JOIN Teams ON tempEjections.abbreviation = Teams.abbreviation)
    WHERE playerID in (select PlayerID from PlayerNames) and tempEjections.bs = 'Y';

create table NonPlayerBallOrStrikeEjections (
            gameID decimal(10),
            playerID decimal(6),
		    correct varchar(2),
-- Key Constraints
		    primary key (gameID, playerID)
            -- foreign key (playerID) references PlayerEjections(playerID),
            -- foreign key (gameID) references PlayerEjections(gameID)
-- Integrity Constraints
       	    -- None
);

insert into NonPlayerBallOrStrikeEjections select DISTINCT gameID, playerID, correct from (
    (select MIN(abID) as abID from tempEjections group by gameID, playerID) as A
    INNER JOIN
    tempEjections ON A.abID = tempEjections.abid
    INNER JOIN Teams ON tempEjections.abbreviation = Teams.abbreviation)
    WHERE playerID not in (select PlayerID from PlayerNames) and tempEjections.bs = 'Y';

drop table temporaryEjections;

-- Creating Pitches

create table tempPitches (
    px decimal(6,3),
    pz decimal(6,3),
    startSpeed decimal(4,1),
    endSpeed decimal(3,1),
    spinRate decimal(7,3),
    spinDir decimal(6,3),
    breakAngle decimal(4,1),
    breakLength decimal(3,1),
    breakY decimal(3,1),
    aX decimal(6,3),
    aY decimal(6,3),
    aZ decimal(6,3),
    szBot decimal(5,3),
    szTop decimal(5,3),
    typeConfidence decimal(6,3),
    vX0 decimal(6,3),
    vY0 decimal(6,3),
    vZ0 decimal(6,3),
    x0 decimal(6,3),
    z0 decimal(6,3),
    pfxX decimal(5,3),
    pfxZ decimal(5,3),
    nasty decimal(3),
    zone decimal(2),
    code char(2),
    type char(1),
    pitchType char(2),
    batterScore int,
    abID decimal(10),
    bCount int, 
    sCount int, 
    outs int, 
    pitchNum int,
    on1b int,
    on2b int,
    on3b int,
-- Key Constraints
		   primary key (abID, pitchNum),
		   foreign key (abID) references AtBats(abID)
-- Integrity Constraints
        --    check (outs >= 0 AND outs <= 2),
        --    check (sCount >= 0 AND sCount <= 2),
        --    check (bCount >= 0 AND bCount <= 3)
);




load data LOCAL infile '~/Documents/ece356/DockerForA2/ece356_project/MLB/pitches.csv' ignore into table tempPitches
    fields terminated by ','
    enclosed by '"'
    lines terminated by '\n'
    ignore 1 lines
    (@px,
    @pz,
    @startSpeed,
    @endSpeed,
    @spinRate,
    @spinDir,
    @breakAngle,
    @breakLength,
    @breakY,
    @aX,
    @aY,
    @aZ,
    @szBot,
    @szTop,
    @typeConfidence,
    @vX0,
    @vY0,
    @vZ0,
    @throwAway,
    @x0,
    @throwAway,
    @throwAway,
    @z0,
    @pfxX,
    @pfxZ,
    @nasty,
    @zone,
    code,
    type,
    @pitchType,
    @throwAway,
    batterScore,
    abID,
    bCount,
    sCount,
    outs,
    pitchNum,
    on1b,
    on2b,
    on3b)
    set px = if (@px like '', NULL, @px),
    pz = if (@pz like '', NULL, @pz),
    startSpeed = if (@startSpeed like '', NULL, @startSpeed),
    endSpeed = if (@endSpeed like '', NULL, @endSpeed),
    spinRate = if (@spinRate like '', NULL, @spinRate),
    spinDir = if (@spinDir like '', NULL, @spinDir),
    breakAngle = if (@breakAngle like '', NULL, @breakAngle),
    breakLength = if (@breakLength like '', NULL, @breakLength),
    breakY = if (@breakY like '', NULL, @breakY),
    aX = if (@aX like '', NULL, @aX),
    aY = if (@aY like '', NULL, @aY),
    aZ = if (@aZ like '', NULL, @aZ),
    szBot = if (@szBot like '', NULL, @szBot),
    szTop = if (@szTop like '', NULL, @szTop),
    typeConfidence = if (@typeConfidence like '', NULL, @typeConfidence),
    vX0 = if (@vX0 like '', NULL, @vX0),
    vY0 = if (@vY0 like '', NULL, @vY0),
    vZ0 = if (@vZ0 like '', NULL, @vZ0),
    x0 = if (@x0 like '', NULL, @x0),
    z0 = if (@z0 like '', NULL, @z0),
    pfxX = if (@pfxX like '', NULL, @pfxX),
    pfxZ = if (@pfxZ like '', NULL, @pfxZ),
    nasty = if (@nasty like '', NULL, @nasty),
    zone = if (@zone like '', NULL, @zone),
    pitchType = if (@pitchType like '', NULL, @pitchType);




    create table FullPitches (
    code char(2),
    type char(1),
    batterScore int,
    abID decimal(10),
    bCount int, 
    sCount int, 
    outs int, 
    pitchNum int,
    on1b int,
    on2b int,
    on3b int,
-- Key Constraints
		   primary key (abID, pitchNum),
		   foreign key (abID) references AtBats(abID)
-- Integrity Constraints
        --    check (outs >= 0 AND outs <= 2),
        --    check (sCount >= 0 AND sCount <= 2),
        --    check (bCount >= 0 AND bCount <= 3)
);

create table PartialPitches (
    px decimal(6,3),
    pz decimal(6,3),
    startSpeed decimal(4,1),
    endSpeed decimal(3,1),
    spinRate decimal(7,3),
    spinDir decimal(6,3),
    breakAngle decimal(4,1),
    breakLength decimal(3,1),
    breakY decimal(3,1),
    aX decimal(6,3),
    aY decimal(6,3),
    aZ decimal(6,3),
    szBot decimal(5,3),
    szTop decimal(5,3),
    typeConfidence decimal(6,3),
    vX0 decimal(6,3),
    vY0 decimal(6,3),
    vZ0 decimal(6,3),
    x0 decimal(6,3),
    z0 decimal(6,3),
    pfxX decimal(5,3),
    pfxZ decimal(5,3),
    nasty decimal(3),
    zone decimal(2),
    code char(2),
    type char(1),
    pitchType char(2),
    abID decimal(10),
    pitchNum int,

-- Key Constraints
		   primary key (abID, pitchNum),
		   foreign key (abID) references AtBats(abID)
-- Integrity Constraints
        --    check (outs >= 0 AND outs <= 2),
        --    check (sCount >= 0 AND sCount <= 2),
        --    check (bCount >= 0 AND bCount <= 3)
);

INSERT into PartialPitches
    SELECT 
    px,
    pz,
    startSpeed,
    endSpeed,
    spinRate,
    spinDir,
    breakAngle,
    breakLength,
    breakY,
    aX,
    aY,
    aZ,
    szBot,
    szTop,
    typeConfidence,
    vX0,
    vY0,
    vZ0,
    x0,
    z0,
    pfxX,
    pfxZ,
    nasty,
    zone,
    code,
    type,
    pitchType,
    abID,
    pitchNum
  
    FROM tempPitches
    WHERE px is not NULL
    AND pz is not NULL
    AND startSpeed is not NULL
    AND endSpeed is not NULL
    AND spinRate is not NULL
    AND spinDir is not NULL
    AND breakAngle is not NULL
    AND breakLength is not NULL
    AND breakY is not NULL
    AND aX is not NULL
    AND aY is not NULL
    AND aZ is not NULL
    AND szBot is not NULL
    AND szTop is not NULL
    AND typeConfidence is not NULL
    AND vX0 is not NULL
    AND vY0 is not NULL
    AND vZ0 is not NULL
    AND pfxX is not NULL
    AND pfxZ is not NULL
    AND nasty is not NULL
    AND zone is not NULL
    AND code is not NULL
    AND type is not NULL
    AND pitchType is not NULL
    AND pitchNum is not NULL;

insert into FullPitches
    SELECT   
    code,
    type,
    batterScore,
    abID,
    bCount, 
    sCount, 
    outs, 
    pitchNum,
    on1b,
    on2b,
    on3b
    FROM tempPitches;

