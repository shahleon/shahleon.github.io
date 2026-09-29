import Image from 'next/image'

const links = [
  { label: 'sleon3@ncsu.edu', href: 'mailto:sleon3@ncsu.edu' },
  { label: 'GitHub', href: 'https://github.com/shahleon' },
  { label: 'LinkedIn', href: 'https://www.linkedin.com/in/shahnewaz-leon/' },
  {
    label: 'Google Scholar',
    href: 'https://scholar.google.com/citations?user=42p6FYoAAAAJ&hl=en&oi=ao',
  },
]

export default function Hero() {
  return (
    <section id="about" className="max-w-content mx-auto px-6 py-16">
      <div className="flex flex-col sm:flex-row gap-10 items-start">
        <div className="shrink-0">
          <Image
            src="/headshot-leon.jpg"
            alt="Shahnewaz Leon"
            width={144}
            height={144}
            className="rounded-full object-cover"
            priority
          />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-ink mb-1">Shahnewaz Leon</h1>
          <p className="text-muted text-sm mb-5">
            PhD in Computer Science · NC State University · 2026
          </p>
          <p className="text-ink leading-relaxed mb-3">
            I study how programmers navigate code, and how that navigation can
            be predicted from the behavior of the people around them.
          </p>
          <p className="text-muted leading-relaxed mb-7">
            Before the PhD, I spent eight years as a software engineer in
            Dhaka, building backend systems, distributed services, and search
            infrastructure.
          </p>
          <div className="flex flex-wrap gap-x-5 gap-y-2 text-sm">
            {links.map((l) => (
              <a
                key={l.label}
                href={l.href}
                target={l.href.startsWith('mailto') ? undefined : '_blank'}
                rel={l.href.startsWith('mailto') ? undefined : 'noopener noreferrer'}
                className="text-individual hover:underline"
              >
                {l.label}
              </a>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
