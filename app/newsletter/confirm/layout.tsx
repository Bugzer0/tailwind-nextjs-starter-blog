import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Newsletter Subscription Confirmed | GlucoAI',
  description:
    'Thank you for subscribing to GlucoAI newsletter. Stay updated with the latest insights on blood glucose management and diabetes care.',
  robots: {
    index: false,
    follow: false,
  },
}

export default function ConfirmLayout({ children }: { children: React.ReactNode }) {
  return children
}
