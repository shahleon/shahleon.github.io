export default function Nav() {
  return (
    <nav className="sticky top-0 z-50 bg-white border-b border-line">
      <div className="max-w-content mx-auto px-6 h-14 flex items-center justify-between">
        <a
          href="#about"
          className="font-semibold text-ink hover:text-individual transition-colors text-sm"
        >
          Shahnewaz Leon
        </a>
        <div className="flex items-center gap-6 text-sm">
          <a href="#research" className="text-muted hover:text-ink transition-colors">
            Research
          </a>
          <a href="#publications" className="text-muted hover:text-ink transition-colors">
            Publications
          </a>
          <a href="#experience" className="text-muted hover:text-ink transition-colors">
            Experience
          </a>
          <a href="#cv" className="text-muted hover:text-ink transition-colors">
            CV
          </a>
        </div>
      </div>
    </nav>
  )
}
