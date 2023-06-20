-- Generated by Oracle SQL Developer Data Modeler 23.1.0.087.0806
--   at:        2023-06-17 19:25:45 CEST
--   site:      Oracle Database 11g
--   type:      Oracle Database 11g



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE affiliation (
    user_user_id  INTEGER NOT NULL,
    team_team_id  INTEGER NOT NULL,
    team_event_id INTEGER NOT NULL
);

ALTER TABLE affiliation
    ADD CONSTRAINT affiliation_pk PRIMARY KEY ( user_user_id,
                                                team_team_id,
                                                team_event_id );

CREATE TABLE amenity_category (
    amenity_cat_id       SERIAL NOT NULL,
    name                 VARCHAR(20) NOT NULL,
    facility_facility_id INTEGER
);

ALTER TABLE amenity_category ADD CONSTRAINT amenity_category_pk PRIMARY KEY ( amenity_cat_id );

CREATE TABLE casual (
    event_id         INTEGER NOT NULL,
    num_users        INTEGER NOT NULL,
    pitch_capacity   INTEGER NOT NULL,
    places_available INTEGER
);

ALTER TABLE casual ADD CONSTRAINT casual_pk PRIMARY KEY ( event_id );

CREATE TABLE city (
    city_id  SERIAL NOT NULL,
    name     VARCHAR(20) NOT NULL,
    province VARCHAR(20) NOT NULL
);

ALTER TABLE city ADD CONSTRAINT city_pk PRIMARY KEY ( city_id );

CREATE TABLE competitive (
    event_id        INTEGER NOT NULL,
    num_teams       INTEGER NOT NULL,
    max_num_teams   INTEGER NOT NULL,
    teams_available INTEGER
);

ALTER TABLE competitive ADD CONSTRAINT competitive_pk PRIMARY KEY ( event_id );

CREATE TABLE event (
    event_id                           SERIAL NOT NULL,
    name                               VARCHAR(30) NOT NULL,
    sport_type                         VARCHAR(30) NOT NULL,
    status                             VARCHAR(30) NOT NULL,
    pitch_pitch_id                     INTEGER NOT NULL, 
--  ERROR: Column name length exceeds maximum allowed length(30) 
    calendar_entry_calendar_entry_id   INTEGER NOT NULL,
    pitch_capacity                     INTEGER NOT NULL,
    city_name                          VARCHAR(30) NOT NULL,
    city_province                      VARCHAR 
--  ERROR: VARCHAR size not specified 
     NOT NULL, 
--  ERROR: Column name length exceeds maximum allowed length(30) 
    periodic_event_periodic_event_id   INTEGER, 
--  ERROR: Column name length exceeds maximum allowed length(30) 
    periodic_eventv1_periodic_event_id INTEGER
);

CREATE UNIQUE INDEX event__idx ON
    event (
        calendar_entry_calendar_entry_id
    ASC );

ALTER TABLE event ADD CONSTRAINT event_pk PRIMARY KEY ( event_id );

CREATE TABLE facility (
    facility_id  SERIAL NOT NULL,
    address      VARCHAR(20) NOT NULL,
    city_city_id INTEGER NOT NULL
);

CREATE UNIQUE INDEX facility__idx ON
    facility (
        city_city_id
    ASC );

ALTER TABLE facility ADD CONSTRAINT facility_pk PRIMARY KEY ( facility_id );

CREATE TABLE frequency (
    frequency_id SERIAL NOT NULL,
    name         VARCHAR(20) NOT NULL
);

ALTER TABLE frequency ADD CONSTRAINT frequency_pk PRIMARY KEY ( frequency_id );

CREATE TABLE gear_type (
    gear_type_id SERIAL NOT NULL,
    name         VARCHAR(20) NOT NULL
);

ALTER TABLE gear_type ADD CONSTRAINT gear_type_pk PRIMARY KEY ( gear_type_id );

CREATE TABLE "group" (
    user_id              INTEGER NOT NULL,
    event_id             INTEGER NOT NULL,
    competitive_event_id INTEGER NOT NULL,
    team_team_id         INTEGER NOT NULL,
    team_event_id        INTEGER NOT NULL
);

ALTER TABLE "group" ADD CONSTRAINT group_pk PRIMARY KEY ( user_id,
                                                          event_id );

ALTER TABLE "group"
    ADD CONSTRAINT group_pkv1 UNIQUE ( competitive_event_id,
                                       team_team_id,
                                       team_event_id );

CREATE TABLE periodic_event (
    periodic_event_id      SERIAL NOT NULL,
    frequency_frequency_id INTEGER NOT NULL,
    start_date             DATE NOT NULL,
    end_date               DATE NOT NULL
);

CREATE UNIQUE INDEX periodic_event__idx ON
    periodic_event (
        frequency_frequency_id
    ASC );

ALTER TABLE periodic_event ADD CONSTRAINT periodic_event_pk PRIMARY KEY ( periodic_event_id );

-- CREATE TABLE permission (
--     permission_id SERIAL NOT NULL
-- );

-- ALTER TABLE permission ADD CONSTRAINT permission_pk PRIMARY KEY ( permission_id );

CREATE TABLE pitch (
    pitch_id                 SERIAL NOT NULL,
    capacity                 INTEGER NOT NULL,
    pitch_type_pitch_type_id INTEGER NOT NULL,
    facility_facility_id     INTEGER NOT NULL
);

ALTER TABLE pitch ADD CONSTRAINT pitch_pk PRIMARY KEY ( pitch_id );

CREATE TABLE pitch_type (
    pitch_type_id SERIAL NOT NULL,
    name          VARCHAR(20) NOT NULL
);

ALTER TABLE pitch_type ADD CONSTRAINT pitch_type_pk PRIMARY KEY ( pitch_type_id );

CREATE TABLE reservation (
    event_id   INTEGER NOT NULL,
    pay_status CHAR(1) NOT NULL
);

ALTER TABLE reservation ADD CONSTRAINT reservation_pk PRIMARY KEY ( event_id );

CREATE TABLE single (
    event_id        INTEGER NOT NULL,
    casual_event_id INTEGER NOT NULL,
    user_user_id    INTEGER NOT NULL
);

ALTER TABLE single ADD CONSTRAINT single_pk PRIMARY KEY ( event_id );

ALTER TABLE single ADD CONSTRAINT single_pkv1 UNIQUE ( casual_event_id,
                                                       user_user_id );

CREATE TABLE sport_gear (
    sport_gear_id          SERIAL NOT NULL,
    name                   VARCHAR(20) NOT NULL,
    facility_facility_id   INTEGER NOT NULL,
    gear_type_gear_type_id INTEGER NOT NULL
);

ALTER TABLE sport_gear ADD CONSTRAINT sport_gear_pk PRIMARY KEY ( sport_gear_id );

CREATE TABLE sport_type (
    sport_type_id   INTEGER NOT NULL,
    sport_type_name CHAR 
--  WARNING: CHAR size not specified 
     NOT NULL,
    event_event_id  INTEGER
);

ALTER TABLE sport_type ADD CONSTRAINT pitch_typev1_pk PRIMARY KEY ( sport_type_id );

CREATE TABLE stat_city (
    year         INTEGER NOT NULL,
    month        INTEGER NOT NULL,
    quantity     INTEGER NOT NULL,
    city_city_id INTEGER NOT NULL
);

CREATE TABLE stat_sport_type (
    year                     INTEGER NOT NULL,
    month                    INTEGER NOT NULL,
    quantity                 INTEGER,
    sport_type_sport_type_id INTEGER NOT NULL
);

CREATE TABLE team (
    team_id  SERIAL NOT NULL,
    name     VARCHAR(20) NOT NULL,
    event_id INTEGER NOT NULL
);

ALTER TABLE team ADD CONSTRAINT team_pk PRIMARY KEY ( team_id,
                                                      event_id );

CREATE TABLE "user" (
    user_id                  SERIAL NOT NULL,
    password                 VARCHAR(30) NOT NULL,
    first_name                     VARCHAR(30),
    last_name                  VARCHAR(30),
    date_of_birth            DATE,
    email                    VARCHAR(30) NOT NULL
    -- permission_permission_id INTEGER NOT NULL
);

ALTER TABLE "user" ADD CONSTRAINT user_pk PRIMARY KEY ( user_id );

CREATE TABLE week_day (
    week_day_id                      SERIAL NOT NULL,
    name                             VARCHAR(30) NOT NULL, 
--  ERROR: Column name length exceeds maximum allowed length(30) 
    periodic_event_periodic_event_id INTEGER
);

ALTER TABLE week_day ADD CONSTRAINT week_day_pk PRIMARY KEY ( week_day_id );

ALTER TABLE affiliation
    ADD CONSTRAINT affiliation_team_fk FOREIGN KEY ( team_team_id,
                                                     team_event_id )
        REFERENCES team ( team_id,
                          event_id );

ALTER TABLE affiliation
    ADD CONSTRAINT affiliation_user_fk FOREIGN KEY ( user_user_id )
        REFERENCES "user" ( user_id );

ALTER TABLE amenity_category
    ADD CONSTRAINT amenity_category_facility_fk FOREIGN KEY ( facility_facility_id )
        REFERENCES facility ( facility_id );

ALTER TABLE casual
    ADD CONSTRAINT casual_event_fk FOREIGN KEY ( event_id )
        REFERENCES event ( event_id );

ALTER TABLE competitive
    ADD CONSTRAINT competitive_event_fk FOREIGN KEY ( event_id )
        REFERENCES event ( event_id );

ALTER TABLE event
    ADD CONSTRAINT event_periodic_eventv1_fk FOREIGN KEY ( periodic_eventv1_periodic_event_id )
        REFERENCES periodic_event ( periodic_event_id );

ALTER TABLE event
    ADD CONSTRAINT event_pitch_fk FOREIGN KEY ( pitch_pitch_id )
        REFERENCES pitch ( pitch_id );

ALTER TABLE facility
    ADD CONSTRAINT facility_city_fk FOREIGN KEY ( city_city_id )
        REFERENCES city ( city_id );

ALTER TABLE "group"
    ADD CONSTRAINT group_competitive_fk FOREIGN KEY ( competitive_event_id )
        REFERENCES competitive ( event_id );

ALTER TABLE "group"
    ADD CONSTRAINT group_reservation_fk FOREIGN KEY ( event_id )
        REFERENCES reservation ( event_id );

ALTER TABLE "group"
    ADD CONSTRAINT group_team_fk FOREIGN KEY ( team_team_id,
                                               team_event_id )
        REFERENCES team ( team_id,
                          event_id );

ALTER TABLE periodic_event
    ADD CONSTRAINT periodic_event_frequency_fk FOREIGN KEY ( frequency_frequency_id )
        REFERENCES frequency ( frequency_id );

ALTER TABLE pitch
    ADD CONSTRAINT pitch_facility_fk FOREIGN KEY ( facility_facility_id )
        REFERENCES facility ( facility_id );

ALTER TABLE pitch
    ADD CONSTRAINT pitch_pitch_type_fk FOREIGN KEY ( pitch_type_pitch_type_id )
        REFERENCES pitch_type ( pitch_type_id );

ALTER TABLE single
    ADD CONSTRAINT single_casual_fk FOREIGN KEY ( casual_event_id )
        REFERENCES casual ( event_id );

ALTER TABLE single
    ADD CONSTRAINT single_reservation_fk FOREIGN KEY ( event_id )
        REFERENCES reservation ( event_id );

ALTER TABLE single
    ADD CONSTRAINT single_user_fk FOREIGN KEY ( user_user_id )
        REFERENCES "user" ( user_id );

ALTER TABLE sport_gear
    ADD CONSTRAINT sport_gear_facility_fk FOREIGN KEY ( facility_facility_id )
        REFERENCES facility ( facility_id );

ALTER TABLE sport_gear
    ADD CONSTRAINT sport_gear_gear_type_fk FOREIGN KEY ( gear_type_gear_type_id )
        REFERENCES gear_type ( gear_type_id );

ALTER TABLE sport_type
    ADD CONSTRAINT sport_type_event_fk FOREIGN KEY ( event_event_id )
        REFERENCES event ( event_id );

ALTER TABLE stat_city
    ADD CONSTRAINT stat_city_city_fk FOREIGN KEY ( city_city_id )
        REFERENCES city ( city_id );

ALTER TABLE stat_sport_type
    ADD CONSTRAINT stat_sport_type_sport_type_fk FOREIGN KEY ( sport_type_sport_type_id )
        REFERENCES sport_type ( sport_type_id );

-- ALTER TABLE "user"
--     ADD CONSTRAINT user_permission_fk FOREIGN KEY ( permission_permission_id )
--         REFERENCES permission ( permission_id );

ALTER TABLE week_day
    ADD CONSTRAINT week_day_periodic_event_fkv1 FOREIGN KEY ( periodic_event_periodic_event_id )
        REFERENCES periodic_event ( periodic_event_id );

CREATE OR REPLACE VIEW V_Event ( event_id
   , name
   , sport_type
   , status
   , Pitch_pitch_id
   , Calendar_Entry_calendar_entry_id
   , Pitch_capacity
   , City_name
   , City_province
   , Periodic_Event_periodic_event_id
   , Periodic_Eventv1_periodic_event_id )
 AS SELECT
    event_id
   , name
   , sport_type
   , status
   , Pitch_pitch_id
   , Calendar_Entry_calendar_entry_id
   , Pitch_capacity
   , City_name
   , City_province
   , Periodic_Event_periodic_event_id
   , Periodic_Eventv1_periodic_event_id
 FROM 
    Event 
;

-- --  ERROR: Invalid View V_Stat_User 

-- CREATE OR REPLACE VIEW V_Stat_User ( Year
--    , Month
--    , new_users )
--  AS SELECT
--     Year
--    , Month
--    , new_users
--  FROM 
--     Stat_User 
-- ;

-- CREATE OR REPLACE VIEW V_User ( user_id
--    , password
--    , name
--    , surname
--    , date_of_birth
--    , email
--    , Permission_permission_id )
--  AS SELECT
--     user_id
--    , password
--    , name
--    , surname
--    , date_of_birth
--    , email
--    , Permission_permission_id
--  FROM 
--     "user" 
-- ;


CREATE OR REPLACE FUNCTION arc_fkarc_2_competitive()
    RETURNS TRIGGER AS $$
DECLARE
    d INTEGER;
BEGIN
    SELECT
        a.event_id
    INTO d
    FROM
        event a
    WHERE
        a.event_id = NEW.event_id;

    IF (d IS NULL OR d <> 'competitive') THEN
        RAISE EXCEPTION 'FK competitive_Event_FK in Table competitive violates Arc constraint on Table Event - discriminator column event_id doesn''t have value Competitive';
    END IF;

    RETURN NEW;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RAISE;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER arc_fkarc_2_competitive
    BEFORE INSERT OR UPDATE OF event_id ON competitive
    FOR EACH ROW
    EXECUTE FUNCTION arc_fkarc_2_competitive();

CREATE OR REPLACE FUNCTION arc_fkarc_2_casual()
    RETURNS TRIGGER AS $$
DECLARE
    d INTEGER;
BEGIN
    SELECT
        a.event_id
    INTO d
    FROM
        event a
    WHERE
        a.event_id = NEW.event_id;

    IF (d IS NULL OR d <> 'casual') THEN
        RAISE EXCEPTION 'FK casual_Event_FK in Table casual violates Arc constraint on Table Event - discriminator column event_id doesn''t have value casual';
    END IF;

    RETURN NEW;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RAISE;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER arc_fkarc_2_casual
    BEFORE INSERT OR UPDATE OF event_id ON casual
    FOR EACH ROW
    EXECUTE FUNCTION arc_fkarc_2_casual();

CREATE OR REPLACE FUNCTION arc_fkarc_3_single()
    RETURNS TRIGGER AS $$
DECLARE
    d INTEGER;
BEGIN
    SELECT
        a.event_id
    INTO d
    FROM
        reservation a
    WHERE
        a.event_id = NEW.event_id;

    IF (d IS NULL OR d <> 'single') THEN
        RAISE EXCEPTION 'FK single_Reservation_FK in Table single violates Arc constraint on Table Reservation - discriminator column event_id doesn''t have value single';
    END IF;

    RETURN NEW;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RAISE;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER arc_fkarc_3_single
    BEFORE INSERT OR UPDATE OF event_id ON single
    FOR EACH ROW
    EXECUTE FUNCTION arc_fkarc_3_single();

CREATE OR REPLACE FUNCTION arc_fkarc_3_group()
    RETURNS TRIGGER AS $$
DECLARE
    d INTEGER;
BEGIN
    SELECT
        a.event_id
    INTO d
    FROM
        reservation a
    WHERE
        a.event_id = NEW.event_id;

    IF (d IS NULL OR d <> 'group') THEN
        RAISE EXCEPTION 'FK group_Reservation_FK in Table "group" violates Arc constraint on Table Reservation - discriminator column event_id doesn''t have value group';
    END IF;

    RETURN NEW;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
    WHEN OTHERS THEN
        RAISE;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER arc_fkarc_3_group
    BEFORE INSERT OR UPDATE OF event_id ON "group"
    FOR EACH ROW
    EXECUTE FUNCTION arc_fkarc_3_group();



-- Oracle SQL Developer Data Modeler Summary Report: 
-- 
-- CREATE TABLE                            23
-- CREATE INDEX                             3
-- ALTER TABLE                             47
-- CREATE VIEW                              3
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                  10
-- WARNINGS                                 1
