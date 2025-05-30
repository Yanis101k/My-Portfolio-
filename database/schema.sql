-- =======================================================
-- Reset & Create Schema for Portfolio SQLite Database
-- This will drop the table (if it exists) and recreate it
-- =======================================================

-- Delete the 'projects' table if it already exists
DROP TABLE IF EXISTS projects;

-- Create the 'projects' table from scratch
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- Unique ID for each project, auto-incremented
    title TEXT NOT NULL,                         -- Project title (required)
    description TEXT NOT NULL,                   -- Project description (required)
    image_url TEXT,                              -- Path or URL to the project image
    github_url TEXT,                             -- URL to the project's GitHub repository
    live_url TEXT,                               -- URL to live project (or demo)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Auto-generated timestamp on creation
);



