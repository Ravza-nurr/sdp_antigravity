module Api
  module V1
    class DoctorsController < ApplicationController
      # GET /api/v1/doctors
      def index
        doctors = Doctor.includes(:branch).all
        render json: doctors.as_json(include: :branch)
      end

      # POST /api/v1/doctors
      def create
        doctor = Doctor.new(doctor_params)
        if doctor.save
          render json: doctor, status: :created
        else
          render json: { errors: doctor.errors.full_messages }, status: :unprocessable_entity
        end
      end

      # GET /api/v1/doctors/available?date=YYYY-MM-DD
      def available
        date = params[:date]
        # Vibe Coding: Simple, readable logic for the exam context
        available_doctors = Doctor.available_on(date)
        render json: available_doctors
      end

      private

      def doctor_params
        params.require(:doctor).permit(:name, :branch_id, :room_no)
      end
    end
  end
end
