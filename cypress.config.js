const { defineConfig } = require("cypress");

module.exports = defineConfig({
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    },
    baseUrl: 'http://localhost:8080', // Updated to match python server port
    video: true, // Enable video recording
    videoCompression: 32, // Compress video to save space
    videosFolder: 'cypress/videos', // Output folder
    screenshotOnRunFailure: true,
    supportFile: false,
  },
});
