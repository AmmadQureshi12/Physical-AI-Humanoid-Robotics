Branch: 001-ai-embodied-intelligence | Date: 2025-12-07 | Plan: [link to plan.md]
Input: Feature specification from /specs/001-ai-embodied-intelligence/spec.md

Feature Name: AI Systems in the Physical World - Embodied Intelligence

Dependencies

User Stories Dependencies:

US1 must be completed before US2 and US3 (foundational ROS 2 knowledge).

US2 must be completed before US3 (simulation and AI integration).

US3 is required before US4 (capstone integration).

US4 is the capstone and can be developed in parallel with final polish tasks.

Parallel Execution Examples:

US2 & US3 can run in parallel after US1 completion.

Diagram creation, lab exercise development, and testing can run in parallel with content development.

Implementation Strategy

MVP Scope: Complete Chapter 1: ROS 2 Fundamentals module with basic simulation environment and humanoid control capabilities.

Incremental Delivery:

Phase 1: Project setup and foundational ROS 2 curriculum

Phase 2: Simulation environment (Gazebo & Unity)

Phase 3: AI perception & VLA (Vision-Language-Action) integration

Phase 4: Capstone humanoid project

Phase 5: Polish, appendices, and cross-cutting concerns

Phase 1: Setup Tasks
Goal

Initialize project structure, install required dependencies, and set up development environment for the 5-chapter curriculum.

Independent Test Criteria

All team members can build and run the Docusaurus-based curriculum website with dependencies installed.

Tasks

 [X] T001 Set up project directory structure in book/ according to new research.md

 [X] T002 Install and configure ROS 2 Humble Hawksbill on Ubuntu 22.04

 [X] T003 Install and configure Gazebo 11+ for simulation

 [X] T004 Install Unity 2022.3 LTS for digital twin visualization

 [X] T005 Install NVIDIA Isaac ROS tools

 [X] T006 Install OpenAI Whisper for voice processing

 [X] T007 Install Nav2 for humanoid navigation

 [X] T008 Set up Docusaurus documentation framework

 [X] T009 Create project configuration files (package.json, docusaurus.config.js, sidebars.js)

 [X] T010 Configure testing framework (pytest)

Phase 2: Foundational Tasks
Goal

Establish basic curriculum structure, common tools, and preparatory content for all chapters.

Independent Test Criteria

All foundational components are working and accessible to students.

Tasks

 [X] T011 Create book/ folder structure for 5 chapters

 [X] T012 Set up Docusaurus config for 5 chapters with navigation

 [X] T013 Create index.md files for all chapters with placeholder content

 [X] T014 Create diagrams/ folders for each chapter

 [X] T015 Create code-samples/ folders for each chapter

 [X] T016 Create spec.md template files for each chapter

 [X] T017 Develop setup guides for ROS 2, Gazebo, Unity, and Isaac

 [X] T018 Create troubleshooting guide for environment setup issues

 [X] T019 Establish testing protocol for curriculum validation

Phase 3: [US1] Chapter 1 - ROS 2 Fundamentals
Goal

Students can complete Module 1 demonstrating ROS 2 basic functionality and simulated robot control.

Independent Test Criteria

Students can create a ROS 2 Python package to control a simulated joint.

Tasks

 [X] T020 Create chapter-01-ros2-fundamentals/index.md

 [X] T021 Create chapter-01-ros2-fundamentals/spec.md

 [X] T022 Add ROS 2 architecture diagram (diagrams/ros2-architecture.svg)

 [X] T023 Add node communication diagram (diagrams/node-communication.svg)

 [X] T024 Add service call diagram (diagrams/service-calls.svg)

 [X] T025 Add code-samples: ros2-package-template.py, joint-control-node.py

 [X] T026 Add exercises: basic ROS 2 package, topic subscription, service implementation

 [X] T027 Test ROS 2 joint control simulation

 [X] T028 Document troubleshooting for ROS 2

Phase 4: [US2] Chapter 2 - Simulation Skills (Gazebo & Unity)
Goal

Students create humanoid URDFs and simulate physics interactions with sensor integration.

Independent Test Criteria

Students can simulate humanoid robots in Gazebo and visualize sensors in Unity.

Tasks

 [X] T029 Create chapter-02-digital-twin/index.md

 [X] T030 Create chapter-02-digital-twin/spec.md

 [X] T031 Create diagrams: gazebo-physics-pipeline, unity-rendering-pipeline, sensor-integration

 [X] T032 Code samples: humanoid-urdf-model.urdf, simulation-environment.world, unity-scene-description.txt

 [X] T033 Exercises: URDF creation, physics simulation, sensor integration

 [X] T034 Implement and test simulation environment

 [X] T035 Document troubleshooting for simulation issues

Phase 5: [US3] Chapter 3 - AI Perception & VLA Integration
Goal

Students implement a humanoid robot VLA pipeline: voice command → planning → action execution.

Independent Test Criteria

Students can demonstrate multi-step tasks with ROS 2 integration.

Tasks

 [X] T036 Create chapter-03-vla-integration/index.md

 [X] T037 Create chapter-03-vla-integration/spec.md

 [X] T038 Create diagrams: vla-pipeline, cognitive-planning, ros2-integration

 [X] T039 Code samples: voice-processing-pipeline.py, cognitive-planner.py, ros2-action-server.py

 [X] T040 Exercises: voice command system, cognitive planning, VLA integration

 [X] T041 Implement VLA pipeline with OpenAI Whisper

 [X] T042 Test multi-step command execution

 [X] T043 Document troubleshooting for VLA issues

Phase 6: [US4] Chapter 4 - Capstone Humanoid Project
Goal

Students integrate all components into an autonomous humanoid capable of perception, navigation, and manipulation.

Independent Test Criteria

Complete autonomous humanoid demonstration with ROS 2, AI, and simulation integration.

Tasks

 [X] T044 Create chapter-04-capstone-project/index.md

 [X] T045 Create chapter-04-capstone-project/spec.md

 [X] T046 Diagrams: end-to-end-system.svg, component-integration.svg

 [X] T047 Code samples: main-capstone-implementation.py, voice-command-demo.launch, multi-step-task-execution.py

 [X] T048 Exercises: planning, system integration, validation testing

 [X] T049 Implement full capstone system

 [X] T050 Test sim-to-real transfer and multi-step scenarios

 [X] T051 Document troubleshooting for capstone project

Phase 7: [US5] Chapter 5 - Polish & Appendices
Goal

Finalize curriculum, add cross-cutting content, appendices, references, and final polish.

Independent Test Criteria

Curriculum meets all specifications with full documentation, 5 chapters, 10+ diagrams, and 10k-15k words.

Tasks

 [X] T052 Create chapter-05-appendices/setup-guide.md

 [X] T053 Create chapter-05-appendices/troubleshooting.md

 [X] T054 Create chapter-05-appendices/references.md (minimum 20 APA sources)

 [X] T055 Verify all code examples work on hardware (RTX 4070 Ti, Jetson Orin Nano)

 [X] T056 Validate real-time performance (<100ms sensor, <500ms action planning)

 [X] T057 Ensure curriculum meets 10k-15k words requirement

 [X] T058 Final review and deploy to Docusaurus