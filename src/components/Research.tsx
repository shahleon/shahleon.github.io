type Project = {
  id: string
  tag: 'Individual' | 'Social' | 'Collective'
  color: string
  tint: string
  title: string
  venue: string
  badge: string | null
  description: string
  result: string
  doi: string | null
  replication: string | null
  placeholderLabel: string
}

const projects: Project[] = [
  {
    id: 'l2n',
    tag: 'Individual',
    color: '#2E6DB4',
    tint: '#EAF1FA',
    title:
      'Learning to Navigate (L2N): A Human-Centered Framework for Local Code Search',
    venue: 'HCII 2026',
    badge: null,
    description:
      'L2N represents a codebase as a directed graph of methods and files and searches it with beam search guided by a heuristic learned for that specific repository. A structured-perceptron training procedure updates feature weights across repository-specific training pairs until the weights converge.',
    result:
      'On large repositories, mean reciprocal rank of the relevant function rose from 0.55 to 0.94, beating Lucene and both zero-shot and fine-tuned UniXcoder across six open-source Python repositories. The advantage widened as repositories grew.',
    doi: '10.1007/978-3-032-31048-4_21',
    replication: 'https://doi.org/10.5281/zenodo.13755783',
    placeholderLabel: 'Weight-learning animation',
  },
  {
    id: 'diets',
    tag: 'Social',
    color: '#7B3FB8',
    tint: '#F0E7F9',
    title:
      'What Teams Seek and How They Seek It: Understanding Foraging Diets in Collaborative Software Debugging',
    venue: 'HCII 2026',
    badge: null,
    description:
      'Ten three-person teams debugged a real defect in the open-source reference manager JabRef while we recorded their navigation and communication. The study extended information-goal and foraging-strategy taxonomies from individual to team-level goals and behaviors.',
    result:
      '36.1% of coded strategy events served team-originating goals, showing that collaboration is a persistent layer of debugging activity rather than overhead on individual work.',
    doi: '10.1007/978-3-032-30781-1_17',
    replication: null,
    placeholderLabel: 'Study figure',
  },
  {
    id: 'pfist',
    tag: 'Social',
    color: '#7B3FB8',
    tint: '#F0E7F9',
    title:
      'Where Will They Click Next? A Social Foraging Model for Collaborating Teams',
    venue: 'CHI 2026',
    badge: 'Best Paper Honorable Mention',
    description:
      'PFIS-T predicts a developer\'s next navigation from teammates\' recent navigation (implicit cues that decay over time) and from code mentioned in team conversation (explicit cues). It is the first computational model to predict social information foraging step by step during synchronous teamwork.',
    result:
      'Predicted 81.5% of navigations across ten teams, covering up to 57.1% more steps than the strongest individual baseline. The rate of steps the model could not predict at all fell from 33.63% to 21.06%, and fell for nine of ten teams.',
    doi: '10.1145/3772318.3791506',
    replication: 'https://doi.org/10.5281/zenodo.18459372',
    placeholderLabel: 'Social scent animation',
  },
  {
    id: 'collective',
    tag: 'Collective',
    color: '#0E8A6A',
    tint: '#E2F3EE',
    title:
      'The Power of the Collective: Cross-Session Behavioral Priors for Developer Navigation Prediction',
    venue: 'VL/HCC 2026 (to appear)',
    badge: null,
    description:
      'A Markov transition model built from prior teams\' traces predicts a new team\'s navigation from its very first step, before any session history accumulates. Call-graph expansion of the candidates extends reach beyond what was directly observed by prior teams.',
    result:
      'Hit@10 of 0.804, against 0.659 for PFIS-T on the same steps. Four prior teams were sufficient. The prior runs in under 10 ms, compared to a median of 153 seconds per step for the 32B local LLM.',
    doi: null,
    replication: 'http://bit.ly/4eMlb5T',
    placeholderLabel: 'Collective pipeline figure',
  },
]

function ProjectCard({ p }: { p: Project }) {
  return (
    <div className="rounded-xl border border-line overflow-hidden flex flex-col">
      <div style={{ height: 4, backgroundColor: p.color }} />
      <div className="p-6 flex flex-col flex-1">
        {/* Tag + badge */}
        <div className="flex flex-wrap items-center gap-2 mb-3">
          <span
            className="text-xs font-semibold uppercase tracking-wide px-2.5 py-0.5 rounded-full"
            style={{ color: p.color, backgroundColor: p.tint }}
          >
            {p.tag}
          </span>
          {p.badge && (
            <span className="text-xs font-medium px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
              {p.badge}
            </span>
          )}
        </div>

        {/* Title + venue */}
        <h3 className="font-semibold text-ink text-base leading-snug mb-1">
          {p.title}
        </h3>
        <p className="text-sm text-muted mb-4">{p.venue}</p>

        {/* Description */}
        <p className="text-sm text-ink leading-relaxed mb-3">{p.description}</p>

        {/* Result */}
        <p
          className="text-sm leading-relaxed mb-5 pl-3 border-l-2 text-ink"
          style={{ borderColor: p.color }}
        >
          {p.result}
        </p>

        {/* Illustration placeholder */}
        <div className="rounded-lg border-2 border-dashed border-line bg-panel aspect-video flex items-center justify-center mb-5">
          <span className="text-xs text-muted">{p.placeholderLabel}</span>
        </div>

        {/* Links */}
        {(p.doi || p.replication) && (
          <div className="flex flex-wrap gap-4 text-sm mt-auto">
            {p.doi && (
              <a
                href={`https://doi.org/${p.doi}`}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline"
                style={{ color: p.color }}
              >
                DOI
              </a>
            )}
            {p.replication && (
              <a
                href={p.replication}
                target="_blank"
                rel="noopener noreferrer"
                className="hover:underline"
                style={{ color: p.color }}
              >
                Replication package
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default function Research() {
  return (
    <section id="research" className="bg-panel py-16">
      <div className="max-w-content mx-auto px-6">
        <h2 className="text-2xl font-bold text-ink mb-10">Research</h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {projects.map((p) => (
            <ProjectCard key={p.id} p={p} />
          ))}
        </div>
      </div>
    </section>
  )
}
