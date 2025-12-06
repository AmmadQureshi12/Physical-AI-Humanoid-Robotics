Physical AI & Humanoid Robotics - Capstone Book
Welcome to the repository for the Physical AI & Humanoid Robotics technical book and capstone module specification. This project is built with Docusaurus and serves as a comprehensive guide for engineering students and professionals venturing into the world of humanoid robotics, physical AI, and robot learning.

📚 Project Overview
This repository contains the source code and content for a technical book designed to be a "Capstone Module" for advanced robotics curriculum. It bridges the gap between simulation and reality, covering the entire stack from ROS 2 fundamentals to Vision-Language-Action (VLA) models.

Key Objectives
Curriculum Design: Provide a rigorous, university-standard module specification.
Technical Guide: Offer step-by-step tutorials on building a digital twin and "brain" for a humanoid robot.
Sim-to-Real: Demonstrate the architecture for deploying trained policies from NVIDIA Isaac Lab to physical hardware.
🚀 Features & Modules
The book is structured into four core modules culminating in a final capstone project:

Module 1: The Robotic Nervous System - Mastery of ROS 2, nodes, topics, and real-time communication.
Module 2: The Digital Twin - High-fidelity simulation using Gazebo, Unity, and URDF modeling.
Module 3: The AI-Robot Brain - Perception pipelines and reinforcement learning with NVIDIA Isaac.
Module 4: Vision-Language-Action (VLA) - Integrating LLMs for cognitive planning and natural language instruction.
Capstone Project: Students build a fully simulated humanoid robot capable of:

Receiving spoken instructions.
Generating action plans via LLMs.
Navigating complex environments (Nav2).
Manipulating objects.
🛠 Tech Stack
Framework: Docusaurus v3
Languages: TypeScript, MDX, React
Diagrams: Mermaid.js
Math: KaTeX
Search: Local Search Plugin
Development Methodology: Spec-Driven Development (SDD) with Gemini Agent
🏁 Getting Started
To run the documentation site locally, follow these steps:

Prerequisites
Node.js (version 20.0 or above)
npm
Installation
Clone the repository:

git clone https://github.com/harisawan27/q4-book-hackathon.git
cd q4-book-hackathon
Navigate to the website directory:

cd website
Install dependencies:

npm install
Running Locally
Start the development server:

npm start
The site will open automatically at http://localhost:3000.

Building for Production
Generate static files for deployment:

npm run build
Serve the built version locally to test:

npm run serve
🤝 Contributing
This project uses a Spec-Driven Development workflow.

Specs First: All major changes start with a specification in the specs/ directory.
AI-Assisted: We use an AI agent to generate content and code based on these specs.
Manual Review: All AI-generated content is reviewed for academic rigor and technical accuracy.
📄 License
This project is open-source. Copyright © 2025 Physical AI & Humanoid Robotics.
