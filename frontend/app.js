const API_BASE = 'http://localhost:3000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    loadPatients();
    loadDoctors(); // Auto load for dropdowns
    loadAppointments();

    // Patient Form Submit
    document.getElementById('patient-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('p-name').value,
            surname: document.getElementById('p-surname').value,
            tc_no: document.getElementById('p-tc').value,
            phone: document.getElementById('p-phone').value,
            email: document.getElementById('p-email').value
        };

        try {
            const res = await fetch(`${API_BASE}/patients`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ patient: data })
            });
            if (res.ok) {
                alert('Hasta Kaydedildi! (Vibe Coding Success)');
                loadPatients();
                e.target.reset();
            } else {
                const err = await res.json();
                alert('Hata: ' + JSON.stringify(err));
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });

    // Appointment Form Submit
    document.getElementById('appointment-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            patient_id: document.getElementById('a-patient').value,
            doctor_id: document.getElementById('a-doctor').value,
            date: document.getElementById('a-date').value,
            time: document.getElementById('a-time').value,
            status: 'pending'
        };

        try {
            const res = await fetch(`${API_BASE}/appointments`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ appointment: data })
            });
            if (res.ok) {
                alert('Randevu Oluşturuldu!');
                loadAppointments();
                e.target.reset();
            } else {
                alert('Hata oluştu.');
            }
        } catch (error) {
            console.error(error);
        }
    });
});

async function loadPatients() {
    const res = await fetch(`${API_BASE}/patients`);
    const patients = await res.json();
    const list = document.getElementById('patient-list');
    const select = document.getElementById('a-patient');
    
    list.innerHTML = '';
    select.innerHTML = '<option value="">Hasta Seçin</option>';

    patients.forEach(p => {
        // List Item
        const li = document.createElement('li');
        li.textContent = `${p.name} ${p.surname} (TC: ${p.tc_no})`;
        list.appendChild(li);

        // Dropdown Option
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = `${p.name} ${p.surname}`;
        select.appendChild(opt);
    });
}

async function loadDoctors() {
    const res = await fetch(`${API_BASE}/doctors`);
    const doctors = await res.json();
    const list = document.getElementById('doctor-list');
    const select = document.getElementById('a-doctor');

    list.innerHTML = '';
    select.innerHTML = '<option value="">Doktor Seçin</option>';

    doctors.forEach(d => {
        const li = document.createElement('li');
        li.textContent = `Dr. ${d.name} - Oda: ${d.room_no}`;
        list.appendChild(li);

        const opt = document.createElement('option');
        opt.value = d.id;
        opt.textContent = `Dr. ${d.name}`;
        select.appendChild(opt);
    });
}

async function loadAppointments() {
    const res = await fetch(`${API_BASE}/appointments`);
    const appointments = await res.json();
    const tbody = document.querySelector('#appointment-table tbody');
    tbody.innerHTML = '';

    appointments.forEach(a => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${a.date}</td>
            <td>${a.time}</td>
            <td>${a.patient ? a.patient.name : 'Silinmiş'}</td>
            <td>${a.doctor ? a.doctor.name : 'Silinmiş'}</td>
            <td>${a.status}</td>
        `;
        tbody.appendChild(tr);
    });
}
