type Detail = {
  label: string
  text: string
}

type Role = {
  title: string
  org: string
  period: string
  description: string
  details?: Detail[]
}

const roles: Role[] = [
  {
    title: 'Instructor of Record',
    org: 'CSC 216: Software Development Fundamentals · NC State University',
    period: 'May 2026 – Aug 2026',
    description:
      'Sole instructor for an undergraduate Java course at NC State. Delivered all in-class lectures for the full summer session, designed and graded projects and exams, managed a team of teaching assistants, and mentored student groups through multi-week software projects with code review and design feedback.',
  },
  {
    title: 'Senior Software Engineer',
    org: 'Monstarlab · Bangladesh',
    period: 'Aug 2017 – Jul 2022',
    description:
      'Led backend engineering across five concurrent client products in fintech, health-tech, and construction management. Owned end-to-end API architecture from high-level design through CI/CD and production support. Led cross-functional backend teams of three to five engineers, conducted technical interviews, and mentored junior engineers.',
    details: [
      {
        label: 'Recruitment Platform',
        text: 'Built a fully serverless hiring pipeline on AWS Lambda and EventBridge. Automated job posting ingestion using Puppeteer and CasperJS, application processing via a Spring Boot data service, and candidate outreach via Twilio and SendGrid. Each component was a discrete, independently deployable service.',
      },
      {
        label: 'Genetic Health Platform',
        text: 'Built backend services for a consumer genetic testing product. Implemented an audit trail pattern for sensitive health and disease-risk data, integrated Stripe payment processing and OAuth2 authentication via Spring Security, and designed to meet compliance requirements for regulated health data.',
      },
      {
        label: 'Construction Management',
        text: 'Built a new Spring Boot REST API service to power a new frontend without touching legacy source systems. Federated data from heterogeneous sources including SOAP services, REST APIs, and direct database reads. Implemented background jobs to keep master data in sync across the boundary.',
      },
      {
        label: 'APIs and Infrastructure',
        text: 'Designed and delivered REST APIs in Java Spring Boot and PHP across all client products. Configured CI/CD pipelines with GitHub Actions and AWS CodePipeline. Optimized MySQL and PostgreSQL query performance. Implemented distributed caching with Redis.',
      },
    ],
  },
  {
    title: 'Backend Developer',
    org: 'Ekhanei.com · Bangladesh',
    period: 'Apr 2016 – Jul 2017',
    description:
      'Developed REST API microservices in PHP (Slim, Silex, Lumen) for one of Bangladesh\'s largest online classifieds platforms, serving 1M+ daily active users. Scaled distributed backend infrastructure and real-time search indexing with Elasticsearch and MySQL. Built a content moderation microservice that automatically flagged abusive posts for human review, reducing manual triage load.',
  },
  {
    title: 'Software Developer',
    org: 'SekaiLab Bangladesh',
    period: 'Jul 2015 – Mar 2016',
    description:
      'Built a dynamic influence-mapping and graph analytics engine inside an HR platform. The system modeled relationships and information flow between employees, surfacing influence networks not visible in org-chart hierarchies.',
  },
  {
    title: 'Software Engineer',
    org: 'Fronture Technologies · Bangladesh',
    period: 'Feb 2014 – Nov 2014',
    description:
      'Developed REST services for enterprise time-tracking applications. Automated CI build workflows in Team Foundation Server, reducing manual build and integration steps for the engineering team.',
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
                {role.details && role.details.length > 0 && (
                  <div className="mt-3 space-y-2">
                    {role.details.map((d, j) => (
                      <p key={j} className="text-sm text-ink leading-relaxed">
                        <span className="font-medium">{d.label}.</span>{' '}{d.text}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
