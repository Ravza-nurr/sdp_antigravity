source "https://rubygems.org"

git_source(:github) { |repo| "https://github.com/#{repo}.git" }

ruby "3.3.0"

# Bundle edge Rails instead: gem "rails", github: "rails/rails", branch: "main"
gem "rails", "~> 8.0.0"

# Use sqlite3 as the database for Active Record
gem "sqlite3", "~> 1.4"

# Use Puma as the app server
gem "puma", "~> 6.0"

# Build JSON APIs with ease. Read more: https://github.com/rails/jbuilder
# gem "jbuilder"

# Use Redis adapter to run Action Cable in production
# gem "redis", "~> 4.0"

# Use Kredis to get higher level data types in Redis
# gem "kredis"

# Use Active Model Serializers if needed (optional)
# gem "active_model_serializers"

group :development, :test do
  # Call 'byebug' anywhere in the code to stop execution and get a debugger console
  gem "debug", platforms: %i[ mri mingw x64_mingw ]
  gem "rspec-rails"
  gem "factory_bot_rails"
  gem "faker"
end

group :development do
  # Use Console on the browser to aid debugging
  gem "web-console"
end

group :test do
  # Use system testing [RSpec replaces this usually, but keeping for reference]
  gem "capybara"
  gem "selenium-webdriver"
  gem "cucumber-rails"
  gem "database_cleaner"
end
