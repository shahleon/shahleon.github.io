'use client'

import { useState } from 'react'

export default function CVSection() {
  const [open, setOpen] = useState(false)

  return (
    <section id="cv" className="py-16">
      <div className="max-w-content mx-auto px-6">
        <h2 className="text-2xl font-bold text-ink mb-4">CV</h2>
        <p className="text-muted text-sm mb-6">
          Full curriculum vitae including education, publications, and skills.
        </p>

        <div className="flex flex-wrap gap-3 mb-6">
          <button
            onClick={() => setOpen((v) => !v)}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg border border-individual text-individual text-sm font-medium hover:bg-individual hover:text-white transition-colors"
          >
            <span
              className="inline-block transition-transform duration-200"
              style={{ transform: open ? 'rotate(90deg)' : 'rotate(0deg)' }}
            >
              ▶
            </span>
            {open ? 'Hide CV' : 'View CV'}
          </button>
          <a
            href="/resume.pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-block px-5 py-2.5 rounded-lg border border-line text-muted text-sm font-medium hover:border-individual hover:text-individual transition-colors"
          >
            Download PDF
          </a>
        </div>

        {/* Animated container */}
        <div
          className="overflow-hidden transition-all duration-500 ease-in-out"
          style={{ maxHeight: open ? '900px' : '0px', opacity: open ? 1 : 0 }}
        >
          <div className="rounded-xl border border-line overflow-hidden shadow-sm">
            <iframe
              src="/resume.pdf"
              title="Shahnewaz Leon — CV"
              className="w-full"
              style={{ height: '860px' }}
            />
          </div>
        </div>
      </div>
    </section>
  )
}
