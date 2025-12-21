// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'AI Systems in the Physical World - Embodied Intelligence',
  tagline: 'A comprehensive guide to humanoid robotics, ROS 2, and AI integration',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://AmmadQureshi12.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub Pages deployment, it is often '/<orgName>/<repoName>/'
  baseUrl: '/Physical-AI-Humanoid-Robotics/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'AmmadQureshi12', // Usually your GitHub org/user name.
  projectName: 'Physical-AI-Humanoid-Robotics', // Usually your repo name.
  trailingSlash: false,

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/AmmadQureshi12/Physical-AI-Humanoid-Robotics/tree/main/',
        },
        blog: false, // Optional: disable the blog plugin
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'AI-Humanoid Robotics',
        logo: {
          alt: 'AI-Humanoid Robotics logo',
          src: 'img/logo.jpg',
          href: '/',  // This ensures the logo links to the root of the site
        },
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Book Chapters',
          },
          {
            to: '/docs/',
            label: 'Read Book',
            position: 'left',
          },
          {
            href: 'https://github.com/AmmadQureshi12/Physical-AI-Humanoid-Robotics',
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Chapters',
            items: [
              {
                label: 'Chapter 1: ROS 2 Fundamentals',
                to: '/docs/chapter-01-ros2-fundamentals/',
              },
              {
                label: 'Chapter 2: Simulation Skills',
                to: '/docs/chapter-02-digital-twin/',
              },
              {
                label: 'Chapter 3: AI Perception & VLA Integration',
                to: '/docs/chapter-03-vla-integration/',
              },
              {
                label: 'Chapter 4: Capstone Humanoid Project',
                to: '/docs/chapter-04-capstone-project/',
              },
              {
                label: 'Chapter 5: Appendices',
                to: '/docs/chapter-05-appendices/',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/AmmadQureshi12/Physical-AI-Humanoid-Robotics',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} AI-Humanoid Robotics Book. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;
