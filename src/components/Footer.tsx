const links = [
  { label: 'GitHub', href: 'https://github.com/shahleon' },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/shahnewaz-leon/' },
  {
    label: 'Google Scholar',
    href: 'https://scholar.google.com/citations?user=42p6FYoAAAAJ&hl=en&oi=ao',
  },
]

export default function Footer() {
  return (
    <footer className="border-t border-line py-8">
      <div className="max-w-content mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-muted">
        <span>Shahnewaz Leon</span>
        <div className="flex gap-5">
          {links.map((l) => (
            <a
              key={l.label}
              href={l.href}
              target="_blank"
              rel="noopener noreferrer"
              className="hover:text-ink transition-colors"
            >
              {l.label}
            </a>
          ))}
        </div>
      </div>
    </footer>
  )
}
