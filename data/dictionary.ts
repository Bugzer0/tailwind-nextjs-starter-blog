/**
 * Centralized dictionary for all UI strings.
 * This file serves as the single source of truth for all user-facing text.
 * When implementing full i18n, replace this with a proper translation system
 * (e.g., next-intl) and use this structure as the base for translation files.
 */

const dictionary = {
  // Navigation
  nav: {
    home: 'Home',
    blog: 'Blog',
    tags: 'Tags',
    about: 'About',
  },

  // Home page
  home: {
    latestPosts: 'Latest Posts',
    description:
      'Glucose, diabetes, CGM, and metabolic health knowledge.',
    newsletterTitle: 'Get new health articles delivered to your inbox',
    noPosts: 'No posts yet.',
    readMore: 'Read more',
    allPosts: 'All posts',
  },

  // Blog / List
  blog: {
    allPosts: 'All Posts',
    searchArticles: 'Search articles',
    noPosts: 'No posts found.',
    previous: 'Previous',
    next: 'Next',
    publishedOn: 'Published on',
    loading: 'Loading posts...',
  },

  // Comments
  comments: {
    loadComments: 'Load Comments',
  },

  // Search
  search: {
    label: 'Search',
  },

  // Accessibility / UI controls
  ui: {
    scrollToComment: 'Scroll To Comment',
    scrollToTop: 'Scroll To Top',
    toggleMenu: 'Toggle Menu',
    themeSwitcher: 'Theme switcher',
    themeLight: 'Light',
    themeDark: 'Dark',
    themeSystem: 'System',
  },

  // Post layout
  post: {
    previousArticle: 'Previous Article',
    nextArticle: 'Next Article',
    backToBlog: 'Back to the blog',
    tags: 'Tags',
    authors: 'Authors',
    name: 'Name',
    discussOnTwitter: 'Discuss on Twitter',
    viewOnGithub: 'View on GitHub',
    twitter: 'Twitter',
    newsletterCta:
      'Like this post? Subscribe to stay updated and receive the latest post straight to your mailbox!',
  },

  // Projects page
  projects: {
    title: 'Projects',
    description: "The projects I've created, contributed to, and/or maintain. Find all on the",
    aboutPageLink: 'about page',
  },

  // Tags page
  tags: {
    title: 'Tags',
    description: 'Things I blog about',
    noTags: 'No tags found.',
  },

  // About page
  about: {
    title: 'About',
  },

  // Tools page
  tools: {
    title: 'Online Tools',
    description:
      'Useful online tools that I deployed (some of them are developed by myself, not necessarily all, though) for my personal use. Feel free to bookmark them and add them to your toolkit!',
    useTool: 'Use tool',
  },

  // 404 page
  notFound: {
    title: '404',
    message: "Sorry we couldn't find this page.",
    description: 'But dont worry, you can find plenty of other things on our homepage.',
    backHome: 'Back to homepage',
  },

  // App banner
  appBanner: {
    title: 'GlucoAI — Smart Blood Sugar Monitor',
    description: 'Track, analyze, and optimize your glucose levels with AI-powered insights.',
    download: 'Download on App Store',
  },

  // Footer
  footer: {
    privacyPolicy: 'Privacy Policy',
    termsOfService: 'Terms of Service',
    allRightsReserved: 'All Rights Reserved',
  },

  // Error pages
  error: {
    somethingWentWrong: 'Something went wrong!',
    errorDescription: 'An error occurred while loading this page. Please try again.',
    errorId: 'Error ID',
    tryAgain: 'Try again',
    applicationError: 'Application Error',
    criticalError:
      'A critical error occurred. Please refresh the page or contact support if the problem persists.',
  },

  // Site metadata
  site: {
    description:
      'Blog sharing knowledge about blood glucose management, diabetes, and metabolic health',
  },
} as const

export default dictionary
