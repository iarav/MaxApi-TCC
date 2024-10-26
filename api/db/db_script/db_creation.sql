-- Creating database
-- CREATE DATABASE max_chatbot

-- Creating the Agent table
CREATE TABLE Agent (
    id SERIAL PRIMARY KEY,
    email VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);

-- Creating the Elicitation table
CREATE TABLE Elicitation (
    id SERIAL PRIMARY KEY,
    focal_question TEXT NOT NULL,
    agent VARCHAR(20),
    concept VARCHAR(20),
    domain VARCHAR(20)
);

-- Creating the MCE table
CREATE TABLE MCE (
    id SERIAL PRIMARY KEY,
    access_code VARCHAR(20) UNIQUE NOT NULL,
    creation_date TIMESTAMP NOT NULL,
    update_date TIMESTAMP,
    agent_id INT,
    elicitation_id INT,
    FOREIGN KEY (agent_id) REFERENCES Agent(id),
    FOREIGN KEY (elicitation_id) REFERENCES Elicitation(id)
);

-- Creating the Concept table
CREATE TABLE Concept (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    behavioral_belief TEXT,
    normative_belief TEXT,
    mce_id INT,
    FOREIGN KEY (mce_id) REFERENCES MCE(id)
);
-- Creating the many-to-many relationship table between Concept and Concept
CREATE TABLE Concept_Relation (
    concept1_id INT,
    concept2_id INT,
    relation_verb VARCHAR(20),
    relation_weight CHAR(1),
    creation_date TIMESTAMP NOT NULL,
    PRIMARY KEY (concept1_id, concept2_id),
    FOREIGN KEY (concept1_id) REFERENCES Concept(id),
    FOREIGN KEY (concept2_id) REFERENCES Concept(id)
);

-- Creating the Chat_History table
CREATE TABLE Chat_History (
    id SERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    sender VARCHAR(10) CHECK (sender IN ('chatbot', 'agent')) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    step VARCHAR(20) NOT NULL, 
    mce_id INT,
    FOREIGN KEY (mce_id) REFERENCES MCE(id)
);
