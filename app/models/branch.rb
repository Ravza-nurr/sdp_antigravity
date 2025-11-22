# app/models/branch.rb
class Branch < ApplicationRecord
  has_many :doctors
  validates :name, presence: true, uniqueness: true
end
