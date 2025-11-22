module Api
  module V1
    class AppointmentsController < ApplicationController
      # GET /api/v1/appointments
      def index
        appointments = Appointment.includes(:patient, :doctor).all
        render json: appointments.as_json(include: [:patient, :doctor])
      end

      # POST /api/v1/appointments
      def create
        appointment = Appointment.new(appointment_params)
        if appointment.save
          render json: appointment, status: :created
        else
          render json: { errors: appointment.errors.full_messages }, status: :unprocessable_entity
        end
      end

      private

      def appointment_params
        params.require(:appointment).permit(:patient_id, :doctor_id, :date, :time, :status)
      end
    end
  end
end
