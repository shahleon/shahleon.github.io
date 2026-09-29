type Publication = {
  authors: string
  leonName: string
  title: string
  venue: string
  doi: string | null
  scholarHref: string | null
  replication: string | null
  badge: string | null
}

// Ordered reverse-chronologically. The four dissertation papers have exact
// venue strings from the authorship statement; the others are from Scholar.
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
    scholarHref: null,
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
    scholarHref: null,
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
    scholarHref: null,
    replication: 'https://doi.org/10.5281/zenodo.18459372',
    badge: 'Best Paper Honorable Mention',
  },
  {
    authors:
      'Sandeep Kaur Kuttal, Sandeep Sthapit, Shahnewaz Leon, Ronnie Phillips, and Philip Rahal.',
    leonName: 'Shahnewaz Leon',
    title:
      'From Artifacts to Strategies: A Gendered Lens on Web Information Foraging.',
    venue:
      'International Conference on Human-Computer Interaction (HCII), pp. 52–67. Springer Nature, 2026.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:W7OEmFMy1HYC',
    replication: null,
    badge: null,
  },
  {
    authors:
      'Shandler A. Mason, Natalie Meuser, Audrey Si, Sandeep Sthapit, Shahnewaz Leon, Manali Teke, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      "Who's Left Out? A Case Study on Promoting Equitable Participation in Remote Collaboration Software.",
    venue:
      'International Conference on Human-Computer Interaction (HCII), pp. 502–521. Springer Nature, 2026.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:Y0pCki6q_DkC',
    replication: null,
    badge: null,
  },
  {
    authors: 'Shahnewaz Leon and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'The Power of the Collective: Cross-Session Behavioral Priors for Developer Navigation Prediction.',
    venue: 'Proceedings of IEEE VL/HCC 2026. Accepted, to appear.',
    doi: null,
    scholarHref: null,
    replication: 'http://bit.ly/4eMlb5T',
    badge: null,
  },
  {
    authors: 'Shahnewaz Leon.',
    leonName: 'Shahnewaz Leon',
    title: 'Modeling Code Navigation in Collaborative Software Engineering Tasks.',
    venue:
      'IEEE Symposium on Visual Languages and Human-Centric Computing (VL/HCC), pp. 423–424. IEEE, 2025.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:qjMakFHDy7sC',
    replication: null,
    badge: null,
  },
  {
    authors:
      'Abim Sedhain, Sruti Srinivasa Ragavan, Brett McKinney, Shahnewaz Leon, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'Unveiling Value-Cost Dynamics in StackOverflow with IFT-Enhanced Clustering.',
    venue:
      'International Conference on Human-Computer Interaction (HCII), pp. 355–364. Springer Nature, 2025.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:2osOgNQ5qMEC',
    replication: null,
    badge: null,
  },
  {
    authors:
      'Abim Sedhain, Sruti Srinivasa Ragavan, Brett McKinney, Shahnewaz Leon, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title: 'Predicting information foraging on Q&A websites.',
    venue:
      'International Conference on Human-Computer Interaction (HCII), pp. 322–342. Springer Nature, 2025.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:9yKSN-GCB0IC',
    replication: null,
    badge: null,
  },
  {
    authors:
      'Abim Sedhain, Vaishvi Diwanji, Helen Solomon, Shahnewaz Leon, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      "Developers' information seeking in Question & Answer websites through a gender lens.",
    venue: 'Journal of Computer Languages, 79, 101267. Elsevier, 2024.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:d1gkVwhDpl0C',
    replication: null,
    badge: null,
  },
  {
    authors:
      'Shahnewaz Leon, Mahzabin Tamanna, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'Comparing foraging behavior across code hosting and Q&A platforms through a gender lens.',
    venue:
      'IEEE Symposium on Visual Languages and Human-Centric Computing (VL/HCC), pp. 235–238. IEEE, 2023.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:u5HHmVD_uO8C',
    replication: null,
    badge: null,
  },
  {
    authors:
      'Abim Sedhain, Shahnewaz Leon, Riley Raasch, and Sandeep Kaur Kuttal.',
    leonName: 'Shahnewaz Leon',
    title:
      'Developers foraging behavior in code hosting sites: a gender perspective.',
    venue:
      'International Conference on Human-Computer Interaction (HCII), pp. 575–593. Springer Nature, 2023.',
    doi: null,
    scholarHref:
      'https://scholar.google.com/citations?view_op=view_citation&hl=en&user=42p6FYoAAAAJ&citation_for_view=42p6FYoAAAAJ:u-x6o8ySG0sC',
    replication: null,
    badge: null,
  },
]

function AuthorLine({
  authors,
  leonName,
}: {
  authors: string
  leonName: string
}) {
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
                  {pub.scholarHref && (
                    <a
                      href={pub.scholarHref}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-individual hover:underline"
                    >
                      Google Scholar
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
