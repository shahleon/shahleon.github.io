export default function CVSection() {
  return (
    <section id="cv" className="py-16">
      <div className="max-w-content mx-auto px-6">
        <h2 className="text-2xl font-bold text-ink mb-4">CV</h2>
        <p className="text-muted text-sm mb-6">
          Full curriculum vitae including education, publications, and skills.
        </p>
        <a
          href="/resume.pdf"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block px-5 py-2.5 rounded-lg border border-individual text-individual text-sm font-medium hover:bg-individual hover:text-white transition-colors"
        >
          Download CV (PDF)
        </a>
      </div>
    </section>
  )
}
