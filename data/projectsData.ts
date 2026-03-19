interface Project {
  title: string
  description: string
  href?: string
  imgSrc?: string
}

const projectsData: Project[] = [
  {
    title: 'GlucoAI App',
    description: `Ứng dụng quản lý đường huyết thông minh với AI, giúp người tiểu đường theo dõi chỉ số glucose, A1C, insulin và dinh dưỡng. Tích hợp với các thiết bị CGM phổ biến như Dexcom, FreeStyle Libre. Phân tích xu hướng và đưa ra gợi ý cá nhân hóa để kiểm soát đường huyết tốt hơn.`,
    imgSrc: '/static/images/glucoai-app-logo.png',
    href: 'https://apps.apple.com/app/glucoai',
  },
  {
    title: 'Blog về Sức khỏe Chuyển hóa',
    description: `Blog chia sẻ kiến thức chuyên sâu về quản lý tiểu đường, dinh dưỡng, công nghệ CGM, và lối sống lành mạnh. Cập nhật hàng ngày với các bài viết từ chuyên gia, review ứng dụng, hướng dẫn thực hành và câu chuyện thành công từ cộng đồng.`,
    imgSrc: '/static/images/blog-logo.png',
    href: 'https://glucoai.app/blog',
  },
]

export default projectsData
