// cypress/e2e/appointment.cy.js
describe('Hastane Randevu Sistemi E2E', () => {
  beforeEach(() => {
    // Mock API responses
    cy.intercept('GET', '/api/v1/patients', { fixture: 'patients.json' }).as('getPatients');
    cy.intercept('GET', '/api/v1/doctors', { fixture: 'doctors.json' }).as('getDoctors');
    cy.intercept('GET', '/api/v1/appointments', { fixture: 'appointments.json' }).as('getAppointments');
    cy.intercept('POST', '/api/v1/patients', { statusCode: 201, body: { id: 3, name: 'Cypress', surname: 'Test' } }).as('createPatient');
    cy.intercept('POST', '/api/v1/appointments', { statusCode: 201, body: { status: 'created' } }).as('createAppointment');
  });

  it('Hasta randevu alabilir (Mocked Backend)', () => {
    // 1. Uygulamayı aç
    cy.visit('http://localhost:8080/index.html'); 
    cy.wait(2000); // İzleyici için bekleme

    // 2. Hasta Ekle
    cy.get('#p-name').type('Cypress');
    cy.get('#p-surname').type('Test');
    cy.get('#p-tc').type('99999999999');
    cy.get('#p-phone').type('5550000000');
    cy.wait(2000); // Form doldurmayı göster
    cy.get('#patient-form button').click();
    
    cy.wait('@createPatient');
    cy.on('window:alert', (str) => {
      expect(str).to.contain('Kaydedildi');
    });
    cy.wait(2000); // Alert sonrası bekleme

    // 3. Doktorları Listele
    cy.get('#load-doctors').click();
    cy.wait('@getDoctors');
    cy.wait(3000); // Doktor listesini inceleme süresi

    // 4. Randevu Formunu Doldur
    cy.get('#a-date').type('2024-12-31');
    cy.get('#a-time').type('14:00');
    cy.wait(2000);
    
    // 5. Gönder
    cy.get('#appointment-form button').click();
    cy.wait('@createAppointment');
    cy.wait(3000); // Sonucu görme süresi
  });
});
