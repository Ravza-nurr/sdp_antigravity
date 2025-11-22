# app/models/appointment.rb
class Appointment < ApplicationRecord
  # Core Transactional Model
  
  belongs_to :patient
  belongs_to :doctor

  validates :date, presence: true
  validates :time, presence: true
  validates :status, inclusion: { in: %w[pending confirmed cancelled completed] }

  # Simple logic to prevent double booking (Vibe Coding: Keep it clean)
  validate :doctor_availability

  private

  def doctor_availability
    if doctor && date && time
      if doctor.appointments.where(date: date, time: time, status: ['pending', 'confirmed']).exists?
        errors.add(:base, "Doctor is not available at this time")
      end
    end
  end
end
