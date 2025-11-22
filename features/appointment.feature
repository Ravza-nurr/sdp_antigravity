# features/appointment.feature
Feature: Randevu Alma İşlemi
  As a hasta
  I want to randevu alabilmek
  So that doktora muayene olabilirim

  Scenario: Başarılı Randevu Oluşturma
    Given sistemde kayıtlı bir hasta "Ahmet" ve doktor "Dr. House" var
    When "Ahmet" isimli hasta "2024-01-01" tarihine randevu talep ederse
    Then randevu başarıyla oluşturulmalı
    And randevu listesinde "Ahmet" ve "Dr. House" görünmeli
