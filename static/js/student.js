const token = localStorage.getItem('accessToken');
if (!token) {
    classMessage.textContent = 'No estás autenticado. Redirigiendo al login...';
    classMessage.className = 'text-danger';
    setTimeout(() => window.location.href = '/static/index.html', 2000);
}


const authHeader = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
};

document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    const createClassForm = document.getElementById('create-class-form');
    const classMessage = document.getElementById('class-message');

    loadTeachers();
    loadClasses();
    const kind = localStorage.getItem('kind');
    if(kind !== 'student') {
        window.location.href = '/static/index.html'; // Redirect to login
        return; // Stop script execution if not authenticated
    }


    // --- Logout Logic ---
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('accessToken');
            localStorage.removeItem('kind');
            window.location.href = '/static/index.html'; // Redirect to login
        });
    }

    // --- Create Class Logic ---
    if (createClassForm) {
        createClassForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            classMessage.textContent = ''; // Clear previous messages

            

            const start_datetime = document.getElementById('start_datetime').value;
            const end_datetime = document.getElementById('end_datetime').value;
            const teacher_id = document.getElementById('teacher_id').value;
            const student_id = document.getElementById('student_id').value;

            const classData = {
                start_datetime: start_datetime,
                end_datetime: end_datetime,
                teacher_id: parseInt(teacher_id),
                student_id: parseInt(student_id)
            };
            const startDate = new Date(classData.start_datetime);
            const endDate = new Date(classData.end_datetime);
            const now = new Date();
            console.log('Start Date:', startDate);
            console.log('End Date:', endDate);
            console.log('Current Date:', now);
            if (startDate <= now) {
                classMessage.textContent = 'La fecha de inicio debe ser mayor a la fecha actual.';
                classMessage.className = 'text-danger';
                return;
            }

            if (endDate <= startDate) {
                classMessage.textContent = 'La fecha de fin debe ser mayor a la fecha de inicio.';
                classMessage.className = 'text-danger';
                return;
            }

            const diffInMilliseconds = endDate - startDate;
            const twoHoursInMilliseconds = 2 * 60 * 60 * 1000;

            if (diffInMilliseconds > twoHoursInMilliseconds) {
                classMessage.textContent = 'La duración de la clase no puede ser mayor a 2 horas.';
                classMessage.className = 'text-danger';
                return;
            }
            
            try {
                const response = await fetch('/class-schedules/', {
                    method: 'POST',
                    headers: authHeader,
                    body: JSON.stringify(classData)
                });

                if (response.ok) {
                    classMessage.textContent = '¡Clase creada exitosamente!';
                    classMessage.className = 'text-success';
                    createClassForm.reset(); // Clear the form
                } else {
                    const errorData = await response.json();
                    classMessage.textContent = `Error: ${errorData.detail || 'No se pudo crear la clase.'}`;
                    classMessage.className = 'text-danger';
                }
            } catch (error) {
                console.error('Error al crear la clase:', error);
                classMessage.textContent = 'Ocurrió un error de red al intentar crear la clase.';
                classMessage.className = 'text-danger';
            }
        });
    }
});



const loadTeachers = async () => {
    const teacherSelect = document.getElementById('teacher_id');
    if (!teacherSelect) {
        return;
    }

    const token = localStorage.getItem('accessToken');
    if (!token) {
        console.error('No estás autenticado. No se pueden cargar los profesores.');
        return;
    }

    try {
        const response = await fetch('/teachers/', {
            method: 'GET',
            headers: authHeader
        });

        if (response.ok) {
            const teachers = await response.json();
            teacherSelect.innerHTML = '<option hidden>Seleccione un profesor</option>';
            teachers.forEach(teacher => {
                const option = document.createElement('option');
                option.value = teacher.id;
                option.textContent = `${teacher.first_name} ${teacher.last_name}`;
                teacherSelect.appendChild(option);
            });
        } else {
            const errorData = await response.json();
            console.error('Error al cargar los profesores:', errorData.detail || response.statusText);
        }
    } catch (error) {
        console.error('Error de red al cargar los profesores:', error);
    }
};



const loadClasses = async () => {
    const classTableBody = document.getElementById('classes-table-body');
    if (!classTableBody) return;

    try {
        const response = await fetch('/class-schedules/', {
            method: 'GET',
            headers: authHeader
        });
        console.log('response', response);
        if (!response.ok) {
            throw new Error('No se pudieron cargar las clases.');
        }

        const classes = await response.json();
        classTableBody.innerHTML = ''; // Limpiar filas existentes

        if (classes.length === 0) {
            const row = document.createElement('tr');
            const cell = document.createElement('td');
            cell.colSpan = 3; // Asumiendo 3 columnas
            cell.textContent = 'No hay clases programadas.';
            cell.className = 'text-center';
            row.appendChild(cell);
            classTableBody.appendChild(row);
            return;
        }

        classes.forEach(cls => {
            const row = document.createElement('tr');

            const studentCell = document.createElement('td');
            studentCell.textContent = `${cls.student.first_name} ${cls.student.last_name}`;
            row.appendChild(studentCell);

            const teacherCell = document.createElement('td');
            teacherCell.textContent = `${cls.teacher.first_name} ${cls.teacher.last_name}`;
            row.appendChild(teacherCell);

            const startCell = document.createElement('td');
            startCell.textContent = new Date(cls.start_datetime).toLocaleString();
            row.appendChild(startCell);

            const endCell = document.createElement('td');
            endCell.textContent = new Date(cls.end_datetime).toLocaleString();
            row.appendChild(endCell);

            classTableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error al cargar las clases:', error);
        classTableBody.innerHTML = '';
        const row = document.createElement('tr');
        const cell = document.createElement('td');
        cell.colSpan = 3;
        cell.textContent = 'Error al cargar las clases.';
        cell.className = 'text-danger text-center';
        row.appendChild(cell);
        classTableBody.appendChild(row);
    }
};
    
