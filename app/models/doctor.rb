# app/models/doctor.rb
class Doctor < ApplicationRecord
  # Domain: Represents medical staff.
  # Relationships: Belongs to a Branch (Poliklinik).

  belongs_to :branch, optional: true # Optional for now to simplify seed data
  has_many :appointments
  has_many :patients, through: :appointments

  validates :name, presence: true
  validates :room_no, presence: true

  # Scope for "Available Doctors" logic (Simplified)
  # In a real app, this would check against existing appointments.
  scope :available_on, ->(date) {
    # Mock logic: All doctors are available unless fully booked (not implemented here)
    all
  }
end
