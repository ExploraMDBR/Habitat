DROP TABLE IF EXISTS objects;
CREATE TABLE objects(
    id INTEGER PRIMARY KEY,
    modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    marker INTEGER UNIQUE,
    model TEXT NOT NULL,
    -- material TEXT NOT NULL,
    info TEXT NOT NULL,
    scale NUMBER DEFAULT 1,
    pos_x NUMBER DEFAULT 0,
    pos_y NUMBER DEFAULT 0,
    pos_z NUMBER DEFAULT 0

);

INSERT INTO objects(marker, model, info, scale) VALUES (0, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (1, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (2, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (3, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (4, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (5, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (6, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (7, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (8, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);

INSERT INTO objects(marker, model, info, scale) VALUES (9, '__default__',  
                "<p><strong>Welcome to Explora's Augmented Reality tour!</strong></p><p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>",
                 0.8);



