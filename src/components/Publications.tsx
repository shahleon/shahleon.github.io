type Publication = {
  authors: string
  leonName: string
  title: string
  venue: string
  doi: string | null
  replication: string | null
  badge: string | null
}

const publications: Publication[] = [
  {
    authors:
      'Shahnewaz Leon, Zhengdong Zhang, Prasad Tadepalli, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'Learning to Navigate (L2N): A Human-Centered Framework for Local Code Search.',
    venue:
      'Artificial Intelligence in HCI, HCII 2026, Part IV, LNAI 16746, pp. 338–358. Springer Nature, 2026.',
    doi: '10.1007/978-3-032-31048-4_21',
    replication: 'https://doi.org/10.5281/zenodo.13755783',
    badge: null,
  },
  {
    authors:
      'Shahnewaz Leon, Abhishek Ravindra Desai, Sachin Kanth, Nour Mahmoud, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'What Teams Seek and How They Seek It: Understanding Foraging Diets in Collaborative Software Debugging.',
    venue:
      'Learning and Collaboration Technologies, HCII 2026, Part II, LNCS 16732, pp. 258–276. Springer Nature, 2026.',
    doi: '10.1007/978-3-032-30781-1_17',
    replication: null,
    badge: null,
  },
  {
    authors: 'Shahnewaz Leon and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'Where Will They Click Next? A Social Foraging Model for Collaborating Teams.',
    venue: 'Proceedings of CHI 2026, ACM, 2026.',
    doi: '10.1145/3772318.3791506',
    replication: 'https://doi.org/10.5281/zenodo.18459372',
    badge: 'Best Paper Honorable Mention',
  },
  {
    authors: 'Shahnewaz Leon and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'The Power of the Collective: Cross-Session Behavioral Priors for Developer Navigation Prediction.',
    venue: 'Proceedings of IEEE VL/HCC 2026. Accepted, to appear.',
    doi: null,
    replication: 'http://bit.ly/4eMlb5T',
    badge: null,
  },
]

function AuthorLine({ authors, leonName }: { authors: string; leonName: string }) {
  const parts = authors.split(leonName)
  return (
    <span className="text-sm text-muted">
      {parts[0]}
      <strong className="text-ink">{leonName}</strong>
      {parts[1]}
    </span>
  )
}

export default function Publications() {
  return (
    <section id="publications" className="py-16">
      <div className="max-w-content mx-auto px-6">
        <h2 className="text-2xl font-bold text-ink mb-10">Publications</h2>
        <ol className="space-y-8">
          {publications.map((pub, i) => (
            <li key={i} className="flex gap-5">
              <span className="text-muted text-sm font-medium tabular-nums shrink-0 pt-0.5">
                {i + 1}.
              </span>
              <div>
                <AuthorLine authors={pub.authors} leonName={pub.leonName} />
                {pub.badge && (
                  <span className="ml-2 inline-block text-xs font-medium px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200 align-middle">
                    {pub.badge}
                  </span>
                )}
                <p className="text-sm text-ink font-medium mt-0.5 mb-0.5">
                  &ldquo;{pub.title}&rdquo;
                </p>
                <p className="text-sm text-muted mb-1.5">{pub.venue}</p>
                <div className="flex flex-wrap gap-4 text-xs">
                  {pub.doi && (
                    <a
                      href={`https://doi.org/${pub.doi}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-individual hover:underline"
                    >
                      DOI
                    </a>
                  )}
                  {pub.replication && (
                    <a
                      href={pub.replication}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-individual hover:underline"
                    >
                      Replication package
                    </a>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  )
}
