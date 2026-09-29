type Role = {
  title: string
  org: string
  period: string
  description: string
}

const roles: Role[] = [
  {
    title: 'Instructor of Record',
    org: 'CSC 216: Software Development Fundamentals · NC State University',
    period: 'May 2026 – Aug 2026',
    description:
      'Sole instructor of record for an undergraduate course. Managed teaching assistants and student code evaluation.',
  },
  {
    title: 'Senior Software Engineer',
    org: 'Monstarlab · Bangladesh',
    period: 'Aug 2017 – Jul 2022',
    description:
      'Architected event-driven distributed microservices and automated CI/CD with Terraform, GitHub Actions, and AWS. Owned data aggregation pipelines for large-scale enterprise services in Spring Boot. Engineered serverless recruitment pipelines on AWS Lambda and EventBridge. Built the GeneLife genetic testing application with an audit trail pattern for customer DNA and health data and Stripe payment integration. Defined HLD and LLD, led technical specification reviews, and mentored junior engineers.',
  },
  {
    title: 'Backend Developer',
    org: 'Ekhanei.com · Bangladesh',
    period: 'Apr 2016 – Jul 2017',
    description:
      'Scaled distributed backend infrastructure and real-time search indexing for an e-commerce platform serving over 1 million daily active users, using Elasticsearch and MySQL.',
  },
  {
    title: 'Software Developer',
    org: 'SekaiLab Bangladesh',
    period: 'Jul 2015 – Mar 2016',
    description:
      'Built a dynamic influence-mapping and graph analytics engine inside an HR platform.',
  },
  {
    title: 'Software Engineer',
    org: 'Fronture Technologies · Bangladesh',
    period: 'Feb 2014 – Nov 2014',
    description:
      'Automated CI build workflows in Team Foundation Server and developed backend REST services for enterprise time-tracking applications.',
  },
]

export default function Experience() {
  return (
    <section id="experience" className="bg-panel py-16">
      <div className="max-w-content mx-auto px-6">
        <h2 className="text-2xl font-bold text-ink mb-10">Professional Experience</h2>
        <div className="space-y-8">
          {roles.map((role, i) => (
            <div key={i} className="flex gap-6">
              <div className="flex flex-col items-center shrink-0 pt-1.5">
                <div className="w-2.5 h-2.5 rounded-full bg-line border-2 border-muted" />
                {i < roles.length - 1 && (
                  <div className="w-px flex-1 bg-line mt-2" />
                )}
              </div>
              <div className="pb-2">
                <div className="flex flex-col sm:flex-row sm:items-baseline sm:gap-3 mb-0.5">
                  <h3 className="font-semibold text-ink">{role.title}</h3>
                  <span className="text-xs text-muted tabular-nums">{role.period}</span>
                </div>
                <p className="text-sm text-muted mb-2">{role.org}</p>
                <p className="text-sm text-ink leading-relaxed">{role.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
