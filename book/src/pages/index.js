import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/">
            Read Book →
          </Link>
          <Link
            className="button button--outline button--lg"
            to="https://github.com/AmmadQureshi12/Physical-AI-Humanoid-Robotics">
            View on GitHub →
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="A comprehensive guide to humanoid robotics, ROS 2, and AI integration">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--12">
                <p>
                  This comprehensive curriculum guides you through the essential concepts of humanoid robotics, embodied AI, and the integration of large language models with physical systems. From foundational ROS 2 concepts to advanced Vision-Language-Action (VLA) models, you'll learn to build AI-driven humanoid robots capable of perception, reasoning, and action in real-world environments.
                </p>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.modules}>
          <div className="container">
            <div className="row">
              <div className="col col--12">
                <h2>Curriculum</h2>
              </div>
            </div>

            <div className="row">
              <div className="col col--12">
                <h3>Module 1: ROS 2 Fundamentals</h3>
                <p>
                  Lay the foundation for humanoid robotics with the Robot Operating System 2. This module covers the essential concepts of distributed robotics software, including nodes, topics, services, and actions. You'll learn to build robust communication architectures for complex robotic systems.
                </p>
                <h4>What you'll learn:</h4>
                <ul>
                  <li>ROS 2 architecture and distributed computing principles</li>
                  <li>Node design patterns and message passing</li>
                  <li>Services and actions for synchronous and asynchronous communication</li>
                  <li>Launch files and system configuration</li>
                  <li>Debugging and introspection tools for complex systems</li>
                </ul>
                <Link to="/docs/chapter-01-ros2-fundamentals/">
                  Start Module 1
                </Link>
              </div>
            </div>

            <div className="row" style={{marginTop: '2rem'}}>
              <div className="col col--12">
                <h3>Module 2: Simulation Skills (Gazebo & Unity)</h3>
                <p>
                  Before breaking hardware, test and validate robotic systems in high-fidelity simulation environments. This module covers physics-based simulation in Gazebo and Unity, digital twin creation, and the transfer of learned behaviors from simulation to real hardware.
                </p>
                <h4>What you'll learn:</h4>
                <ul>
                  <li>Physics simulation principles and URDF modeling</li>
                  <li>Gazebo environment setup and robot simulation</li>
                  <li>Unity integration for visual feedback and teleoperation</li>
                  <li>Digital twin creation for sensor simulation</li>
                  <li>Sim-to-real transfer techniques for locomotion and manipulation</li>
                </ul>
                <Link to="/docs/chapter-02-digital-twin/">
                  Start Module 2
                </Link>
              </div>
            </div>

            <div className="row" style={{marginTop: '2rem'}}>
              <div className="col col--12">
                <h3>Module 3: AI Perception & VLA Integration</h3>
                <p>
                  Integrate artificial intelligence into your robotic platform with Vision-Language-Action models. This module focuses on connecting large language models and computer vision systems with real robotic hardware to create intelligent, responsive systems.
                </p>
                <h4>What you'll learn:</h4>
                <ul>
                  <li>Computer vision integration with ROS 2</li>
                  <li>Vision-Language-Action pipeline architecture</li>
                  <li>Speech-to-text and natural language processing with Whisper</li>
                  <li>AI agent integration for cognitive planning</li>
                  <li>Real-time perception-action loops</li>
                </ul>
                <Link to="/docs/chapter-03-vla-integration/">
                  Start Module 3
                </Link>
              </div>
            </div>

            <div className="row" style={{marginTop: '2rem'}}>
              <div className="col col--12">
                <h3>Module 4: Capstone Humanoid Project</h3>
                <p>
                  Synthesize your learning in a comprehensive project building an AI-driven humanoid robot. This module integrates all previous concepts into a single, functioning system capable of receiving natural language commands and executing complex tasks.
                </p>
                <h4>What you'll learn:</h4>
                <ul>
                  <li>System integration across all layers of the humanoid stack</li>
                  <li>Real-time control and balance for bipedal locomotion</li>
                  <li>AI agent coordination for task planning and execution</li>
                  <li>Hardware integration and safety considerations</li>
                  <li>Validation and testing of integrated systems</li>
                </ul>
                <Link to="/docs/chapter-04-capstone-project/">
                  Start Module 4
                </Link>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.capstone} style={{marginTop: '2rem', paddingTop: '2rem', borderTop: '1px solid #ccc'}}>
          <div className="container">
            <div className="row">
              <div className="col col--12">
                <h2>Capstone Project: AI-Driven Humanoid Robot</h2>
                <p>
                  The culmination of this curriculum is the development of a complete AI-driven humanoid robot. Students will integrate:
                </p>
                <ul>
                  <li><strong>Robust Locomotion</strong>: Stable bipedal walking based on perception and planning</li>
                  <li><strong>Interactive AI</strong>: Natural language command interpretation and execution</li>
                  <li><strong>Perception Systems</strong>: Computer vision for navigation and manipulation</li>
                  <li><strong>Safety & Control</strong>: Real-time control systems with fail-safes</li>
                </ul>
                <p>
                  By the end of the curriculum, students will have built and validated an AI-driven humanoid system that demonstrates the full integration of perception, reasoning, and action in a physical platform.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}