# spec/requests/patients_spec.rb
require 'rails_helper'

RSpec.describe "Api::V1::Patients", type: :request do
  describe "POST /api/v1/patients" do
    context "with valid parameters" do
      let(:valid_attributes) {
        { patient: { name: "Ali", surname: "Veli", tc_no: "11111111111", phone: "555", email: "ali@test.com" } }
      }

      it "creates a new Patient" do
        expect {
          post "/api/v1/patients", params: valid_attributes
        }.to change(Patient, :count).by(1)
      end

      it "returns status code 201" do
        post "/api/v1/patients", params: valid_attributes
        expect(response).to have_http_status(:created)
      end
    end

    context "with invalid parameters" do
      it "returns status code 422" do
        post "/api/v1/patients", params: { patient: { name: "" } }
        expect(response).to have_http_status(:unprocessable_entity)
      end
    end
  end
end
