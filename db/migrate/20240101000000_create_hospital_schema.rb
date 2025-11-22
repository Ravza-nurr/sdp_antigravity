class CreateHospitalSchema < ActiveRecord::Migration[8.0]
  def change
    create_table :branches do |t|
      t.string :name, null: false
      t.timestamps
    end

    create_table :patients do |t|
      t.string :name, null: false
      t.string :surname, null: false
      t.string :tc_no, null: false, index: { unique: true }
      t.string :phone
      t.string :email
      t.timestamps
    end

    create_table :doctors do |t|
      t.string :name, null: false
      t.string :room_no
      t.references :branch, foreign_key: true
      t.timestamps
    end

    create_table :appointments do |t|
      t.references :patient, null: false, foreign_key: true
      t.references :doctor, null: false, foreign_key: true
      t.date :date, null: false
      t.string :time, null: false
      t.string :status, default: 'pending'
      t.timestamps
    end
  end
end
