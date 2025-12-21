// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Introduction',
      items: ['index'],
    },
    {
      type: 'category',
      label: 'Chapter 1 - ROS 2 Fundamentals',
      items: [
        'chapter-01-ros2-fundamentals/index',
        'chapter-01-ros2-fundamentals/spec',
        'chapter-01-ros2-fundamentals/exercises',
        'chapter-01-ros2-fundamentals/troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 2 - Simulation Skills',
      items: [
        'chapter-02-digital-twin/index',
        'chapter-02-digital-twin/spec',
        'chapter-02-digital-twin/exercises',
        'chapter-02-digital-twin/troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 3 - AI Perception & VLA Integration',
      items: [
        'chapter-03-vla-integration/index',
        'chapter-03-vla-integration/spec',
        'chapter-03-vla-integration/exercises',
        'chapter-03-vla-integration/troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 4 - Capstone Humanoid Project',
      items: [
        'chapter-04-capstone-project/index',
        'chapter-04-capstone-project/spec',
        'chapter-04-capstone-project/exercises',
        'chapter-04-capstone-project/troubleshooting',
      ],
    },
    {
      type: 'category',
      label: 'Chapter 5 - Appendices',
      items: [
        'chapter-05-appendices/index',
        'chapter-05-appendices/spec',
        'chapter-05-appendices/setup-guide',
        'chapter-05-appendices/troubleshooting',
        'chapter-05-appendices/references',
        'chapter-05-appendices/hardware-validation',
        'chapter-05-appendices/performance-validation',
        'chapter-05-appendices/word-count-verification',
        'chapter-05-appendices/final-review-report',
      ],
    },
  ],
};

export default sidebars;