import AnimationStepper from '@/components/AnimationStepper'

type Animation = {
  frames: string[]
  captions?: string[]
  illustrative: boolean
  accentColor: string
  label?: string
}

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
  animations: Animation[]
  staticFigure?: string   // path to a static SVG/image used instead of stepper
}

// L2N captions come from the defense-deck player (animations-src/l2n/build.py).
// They were written as spoken narration — rewrite for readers before publishing.
const L2N_CAPTIONS = [
  'Update-Weights takes one training pair, a query and the path it should have followed, and walks it down the graph. The beam starts with a single node and the weights start random.',
  'Expanding gives us the candidate set C. The dashed green ring marks the node that lies on the training path. The search itself cannot see that ring, it is only there for us.',
  'Each candidate gets one dot product. Five features, five weights, one number. That number is the whole heuristic.',
  'Sorted and cut at the beam width. Here parse() survives, so the beam still contains the path and nothing is corrected. The algorithm only acts on failure.',
  'Next level down. Same procedure, and now token() is the node we need to keep.',
  'And here it fails. token() ranks fourth and falls below the cut. The beam has lost the path completely, which is the condition that triggers the update.',
  'To correct it, we compare two averages. The mean feature vector of what the beam kept, against the mean of the path nodes it dropped. They diverge almost entirely on method name.',
  'The update is a perceptron step toward that difference. Method name rises, file and path fall. The heuristic just learned that in this repository, method names carry the signal.',
  'The beam resets onto the true node so the remaining levels still train against a reachable path. Without that, everything downstream would train from a search that is already lost.',
  'Same level, same query, same graph. Only the weights changed, and now token() ranks first. Learn-Weights repeats this across every training pair until the weights stop moving.',
]

const l2nFrames = Array.from({ length: 10 }, (_, i) =>
  `/animations/l2n/frame-${String(i + 1).padStart(2, '0')}.svg`
)

const pfistAFrames = Array.from({ length: 10 }, (_, i) =>
  `/animations/pfis-t/pfist-A${String(i + 1).padStart(2, '0')}.svg`
)

const pfistBFrames = Array.from({ length: 4 }, (_, i) =>
  `/animations/pfis-t/pfist-B${String(i + 1).padStart(2, '0')}.svg`
)

const collectiveFrames = [1, 2, 3].map(
  (n) => `/animations/collective/collective-panel-${n}.svg`
)

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
      'Standard code search tools treat every repository alike. They rely on general models that ignore the structure and history specific to the codebase at hand. L2N represents a repository as a directed graph of methods and files and guides beam search with a heuristic trained on that repository\'s own navigation history. Its advantage over both keyword search and neural code models grows as repositories get larger.',
    result:
      'On large repositories, mean reciprocal rank of the relevant function rose from 0.55 to 0.94, beating Lucene and both zero-shot and fine-tuned UniXcoder across six open-source Python repositories. The advantage widened as repositories grew.',
    doi: '10.1007/978-3-032-31048-4_21',
    replication: 'https://doi.org/10.5281/zenodo.13755783',
    animations: [
      {
        frames: l2nFrames,
        captions: L2N_CAPTIONS,
        illustrative: true,
        accentColor: '#1f6feb',
        label: 'Weight learning · Update-Weights walkthrough',
      },
    ],
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
      'We understand how individual developers navigate code, but most real debugging unfolds in teams, where what a teammate says or does can redirect where you look next. Ten three-person teams debugged a real defect in JabRef while we recorded their navigation and communication. We coded 3,248 strategy events to identify which served individual goals and which were triggered by the team. More than a third were driven by the team, making team context a structural layer of debugging, not just background noise.',
    result:
      '36.1% of coded strategy events served team-originating goals, showing that collaboration is a persistent layer of debugging activity rather than overhead on individual work.',
    doi: '10.1007/978-3-032-30781-1_17',
    replication: null,
    animations: [],
    staticFigure: '/animations/diets/study-figure.svg',
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
      "Existing models predict where a developer will navigate next based on their own history. None account for what teammates are doing or saying in real time. PFIS-T combines implicit cues from teammates' recent moves and explicit cues from code entities mentioned in conversation to predict each developer's next step during synchronous teamwork. The rate of steps the model could not explain at all fell for nine of ten teams, showing that social context carries navigational signal that individual history alone cannot capture.",
    result:
      'Predicted 81.5% of navigations across ten teams, covering up to 57.1% more steps than the strongest individual baseline. The rate of steps the model could not predict at all fell from 33.63% to 21.06%, and fell for nine of ten teams.',
    doi: '10.1145/3772318.3791506',
    replication: 'https://doi.org/10.5281/zenodo.18459372',
    animations: [
      {
        frames: pfistAFrames,
        illustrative: true,
        accentColor: '#7c3aed',
        label: 'Coverage: how a missed step becomes reachable through social cues',
      },
    ],
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
      "Models that learn from a team's own session cannot make predictions at session start, when no history has accumulated. But teams working the same task often follow similar paths. We built a Markov transition model on prior teams' navigation traces and used call-graph expansion to extend its reach beyond what those teams directly visited. Only a handful of prior teams proved sufficient to make the model competitive, suggesting that what limits navigation prediction is available behavioral history, not model sophistication.",
    result:
      'Hit@10 of 0.804, against 0.659 for PFIS-T on the same steps. Four prior teams were sufficient. The prior runs in under 10 ms, compared to a median of 153 seconds per step for the 32B local LLM.',
    doi: null,
    replication: 'http://bit.ly/4eMlb5T',
    animations: [
      {
        frames: collectiveFrames,
        illustrative: true,
        accentColor: '#0E8A6A',
        label: 'Pipeline · Traces → transition counts → ranked candidates',
      },
    ],
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

        <h3 className="font-semibold text-ink text-base leading-snug mb-1">
          {p.title}
        </h3>
        <p className="text-sm text-muted mb-4">{p.venue}</p>

        <p className="text-sm text-ink leading-relaxed mb-3">{p.description}</p>

        <p
          className="text-sm leading-relaxed mb-5 pl-3 border-l-2 text-ink"
          style={{ borderColor: p.color }}
        >
          {p.result}
        </p>

        {/* Figure: static SVG, stepper, or placeholder */}
        {p.staticFigure ? (
          <div className="rounded-lg border border-line overflow-hidden mb-5">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={p.staticFigure} alt={`Figure for ${p.title}`} className="w-full h-auto block"/>
          </div>
        ) : p.animations.length > 0 ? (
          <div className="space-y-4 mb-5">
            {p.animations.map((anim, i) => (
              <AnimationStepper key={i} {...anim} />
            ))}
          </div>
        ) : (
          <div className="rounded-lg border-2 border-dashed border-line bg-panel aspect-video flex items-center justify-center mb-5">
            <span className="text-xs text-muted">Illustration placeholder</span>
          </div>
        )}

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
        <h2 className="text-2xl font-bold text-ink mb-6">Research</h2>

        <div className="mb-10 space-y-4 text-sm text-ink leading-relaxed max-w-2xl">
          <p>
            Most of the work of software development is not writing new code but making sense of code that already exists. Before changing a system, a developer has to find the relevant parts first. Existing tools treat every codebase the same, relying on generic models that ignore the structure and history of the repository at hand.
          </p>
          <p>
            My research asks what happens when we take that context seriously. I studied code navigation at three levels: how individual developers search a repository, how teams navigate together and influence each other, and how traces from past sessions can guide a new team before it has taken a single step.
          </p>
          <p>
            The findings point toward tools that learn from the people and history already embedded in a codebase. As AI-generated code makes repositories larger and less familiar, that capacity may matter more than it ever has.
          </p>
          <p className="text-muted">
            This work was conducted in the{' '}
            <a href="https://skuttal.github.io/skk/" target="_blank" rel="noopener noreferrer" className="underline hover:text-ink">
              Human Factors + Experience Engineering (HFXE) Lab
            </a>{' '}
            at NC State, under the supervision of Sandeep Kaur Kuttal.
          </p>
        </div>

        <div className="relative">
          {/* Fade hint at bottom to signal scrollability */}
          <div className="pointer-events-none absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-panel to-transparent z-10 rounded-b-xl" />
          <div
            className="overflow-y-auto pr-1"
            style={{ maxHeight: '820px' }}
          >
            <div className="flex flex-col gap-6">
            {projects.map((p) => (
              <ProjectCard key={p.id} p={p} />
            ))}
            {/* Bottom padding so last card clears the fade */}
            <div className="h-8" />
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
