-- ============================================
-- Seed Data for Portfolio Projects Table
-- This file inserts sample data into the table
-- Use this after running schema.sql
-- ============================================

-- Insert a sample project: Task Tracker App
INSERT INTO projects (
    title,              -- Title of the project
    description,        -- Brief description of what the project does
    image_url,          -- URL or local path to the project image
    github_url,         -- Link to the GitHub repository
    live_url            -- Link to the live hosted version (if available)
)
VALUES (
    'Task Tracker App',  -- Project title
    'A full-stack task and productivity tracker with CRUD features.',  -- Project description
    'static/images/task-tracker.png',  -- Image used in the frontend
    'https://github.com/Yanis101k/task-tracker',  -- GitHub source code
    'http://localhost:5000/projects/1'  -- Preview or hosted version
);

-- Insert another project: Library Management System
INSERT INTO projects (
    title,
    description,
    image_url,
    github_url,
    live_url
)
VALUES (
    'Library Management System',
    'A Python & SQLite-based app to manage books, members, and loans.',
    'static/images/library-system.png',
    'https://github.com/Yanis101k/library-system',
    'http://localhost:5000/projects/2'
);

-- Add more projects below using the same structure if needed
