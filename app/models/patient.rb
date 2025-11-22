# app/models/patient.rb
class Patient < ApplicationRecord
  # Vibe Coding: Using clear, readable validations to ensure data integrity.
  # Context: This model represents the core user (patient) in the hospital system.

  has_many :appointments
  has_many :doctors, through: :appointments

  validates :name, presence: true
  validates :surname, presence: true
  validates :tc_no, presence: true, uniqueness: true, length: { is: 11 }
  validates :phone, presence: true
  
  # AI-Assisted Tip: Consider adding regex validation for email if needed.
  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
end
