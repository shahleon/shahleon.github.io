import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Shahnewaz Leon',
  description:
    'PhD in Computer Science, NC State University. Research on code navigation in individual, social, and collective context.',
  openGraph: {
    title: 'Shahnewaz Leon',
    description:
      'PhD in Computer Science, NC State University. Research on code navigation.',
    url: 'https://shahleon.github.io',
    siteName: 'Shahnewaz Leon',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-white text-ink antialiased">{children}</body>
    </html>
  )
}
