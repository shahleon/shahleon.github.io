'use client'

import { useState, useCallback, useRef } from 'react'

type Props = {
  frames: string[]
  captions?: string[]
  illustrative?: boolean
  accentColor?: string
  label?: string
}

export default function AnimationStepper({
  frames,
  captions,
  illustrative = false,
  accentColor = '#1f6feb',
  label,
}: Props) {
  const [idx, setIdx] = useState(0)
  const containerRef = useRef<HTMLDivElement>(null)

  const go = useCallback(
    (k: number) => setIdx(Math.max(0, Math.min(frames.length - 1, k))),
    [frames.length]
  )

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(idx + 1) }
    if (e.key === 'ArrowLeft')  { e.preventDefault(); go(idx - 1) }
  }

  return (
    <div
      ref={containerRef}
      tabIndex={0}
      onKeyDown={handleKey}
      className="rounded-lg border border-line overflow-hidden bg-white outline-none focus-visible:ring-2 focus-visible:ring-offset-1"
      style={{ '--accent': accentColor } as React.CSSProperties}
    >
      {label && (
        <div className="px-4 pt-3 pb-0">
          <span
            className="text-xs font-semibold uppercase tracking-wide"
            style={{ color: accentColor }}
          >
            {label}
          </span>
        </div>
      )}

      {/* Frame */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        src={frames[idx]}
        alt={captions?.[idx] ?? `Step ${idx + 1} of ${frames.length}`}
        className="w-full h-auto block"
      />

      {/* Controls */}
      <div className="px-4 py-3 border-t border-line flex items-center gap-3 flex-wrap bg-panel">
        <button
          onClick={() => go(idx - 1)}
          disabled={idx === 0}
          className="text-sm px-3 py-1.5 rounded border border-line bg-white text-ink disabled:opacity-40 disabled:cursor-default transition-colors"
          onMouseEnter={e => { if (idx > 0) e.currentTarget.style.borderColor = accentColor }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = '' }}
        >
          ← Back
        </button>
        <button
          onClick={() => go(idx + 1)}
          disabled={idx === frames.length - 1}
          className="text-sm px-3 py-1.5 rounded border border-line bg-white text-ink disabled:opacity-40 disabled:cursor-default transition-colors"
          onMouseEnter={e => { if (idx < frames.length - 1) e.currentTarget.style.borderColor = accentColor }}
          onMouseLeave={e => { e.currentTarget.style.borderColor = '' }}
        >
          Next →
        </button>
        <span className="text-xs text-muted tabular-nums">
          {idx + 1} / {frames.length}
        </span>
        <div className="flex gap-1.5 ml-auto flex-wrap justify-end">
          {frames.map((_, k) => (
            <button
              key={k}
              onClick={() => go(k)}
              aria-label={`Step ${k + 1}`}
              className="w-2 h-2 rounded-full transition-colors shrink-0"
              style={{ backgroundColor: k === idx ? accentColor : '#D0D4D9' }}
            />
          ))}
        </div>
      </div>

      {/* Caption */}
      {captions?.[idx] && (
        <div className="px-4 py-3 border-t border-line">
          <p
            className="text-xs text-ink leading-relaxed pl-3 border-l-2"
            style={{ borderColor: accentColor }}
          >
            {captions[idx]}
          </p>
        </div>
      )}

      {/* Illustrative notice */}
      {illustrative && (
        <div className="px-4 pb-3 pt-2">
          <p className="text-xs text-muted italic">
            Illustrative — scores, weights, and node activations shown are for explanation, not from actual runs on these specific inputs.
          </p>
        </div>
      )}
    </div>
  )
}
