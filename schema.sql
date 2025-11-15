CREATE DATABASE IF NOT EXISTS ticketing;
USE ticketing;

CREATE TABLE IF NOT EXISTS events(
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    total_tickets INT NOT NULL,
    total_tickets_sold INT DEFAULT 0,
    total_tickets_exchange INT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tickets(
    id VARCHAR(255) PRIMARY KEY,
    code VARCHAR(255) NOT NULL UNIQUE,
    sale_date DATETIME NOT NULL,
    exchange BOOLEAN DEFAULT false,
    exchange_date DATETIME NULL,
    event_id VARCHAR(255) NOT NULL,
    CONSTRAINT fk_ticket_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS events_historic (
    id VARCHAR(255) NULL,
    name VARCHAR(50) NULL,
    start_date DATETIME NULL,
    end_date DATETIME NULL,
    total_tickets INT NULL,
    total_tickets_sold INT NULL,
    total_tickets_exchange INT NULL,
    update_date DATETIME NULL
);
