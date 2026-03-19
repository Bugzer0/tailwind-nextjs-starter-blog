interface Project {
  title: string
  description: string
  href?: string
  imgSrc?: string
}

const projectsData: Project[] = [
  {
    title: 'GlucoAI App',
    description: `Smart blood glucose management app powered by AI, helping diabetics track glucose, A1C, insulin, and nutrition. Integrates with popular CGM devices like Dexcom and FreeStyle Libre. Analyzes trends and provides personalized suggestions for better blood glucose control.`,
    imgSrc: '/static/images/glucoai-app-logo.png',
    href: 'https://apps.apple.com/app/glucoai',
  },
  {
    title: 'Metabolic Health Blog',
    description: `Blog sharing in-depth knowledge about diabetes management, nutrition, CGM technology, and healthy living. Updated daily with expert articles, app reviews, practical guides, and success stories from the community.`,
    imgSrc: '/static/images/blog-logo.png',
    href: 'https://glucoai.app/blog',
  },
]

export default projectsData
