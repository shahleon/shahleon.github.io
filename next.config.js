/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  // For GitHub Pages user site, repo must be named shahleon.github.io.
  // No basePath needed for user-page deployment (shahleon.github.io).
  // If you ever deploy as a project page instead, set:
  //   basePath: '/repo-name'
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
}

module.exports = nextConfig
