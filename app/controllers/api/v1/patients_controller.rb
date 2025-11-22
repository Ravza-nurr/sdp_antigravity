module Api
  module V1
    class PatientsController < ApplicationController
      # GET /api/v1/patients
      def index
        patients = Patient.all
        render json: patients
      end

      # POST /api/v1/patients
      def create
        patient = Patient.new(patient_params)
        if patient.save
          render json: patient, status: :created
        else
          render json: { errors: patient.errors.full_messages }, status: :unprocessable_entity
        end
      end

      private

      def patient_params
        params.require(:patient).permit(:name, :surname, :tc_no, :phone, :email)
      end
    end
  end
end
