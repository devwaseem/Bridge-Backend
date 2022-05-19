/*
|-------------------------------------------------------------------------------
| Development config               https://maizzle.com/docs/environments/#local
|-------------------------------------------------------------------------------
|
| The exported object contains the default Maizzle settings for development.
| This is used when you run `maizzle build` or `maizzle serve` and it has
| the fastest build time, since most transformations are disabled.
|
*/

module.exports = {
  inlineCSS: true,
  website_url: "https://webridge.app",
  support_email: "support@webridge.app",
  build: {
    templates: {
      source: 'src/templates',
      destination: {
        path: 'build_local',
      },
    },
  },
}
