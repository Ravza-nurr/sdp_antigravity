Rails.application.routes.draw do
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  # API Version 1
  namespace :api do
    namespace :v1 do
      resources :patients, only: [:index, :create]
      resources :doctors, only: [:index, :create] do
        collection do
          get 'available' # GET /api/v1/doctors/available
        end
      end
      resources :appointments, only: [:index, :create]
    end
  end

  # Health check
  get "up" => "rails/health#show", as: :rails_health_check
end
