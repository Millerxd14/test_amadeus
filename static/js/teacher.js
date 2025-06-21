// --- Token Check and Auth Header ---
const token = localStorage.getItem('accessToken');
if (!token) {
    alert('No estás autenticado. Redirigiendo al login...');
    window.location.href = '/static/index.html';
}


const authHeader = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
};

document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.getElementById('logout-btn');
    const createClassForm = document.getElementById('create-class-form');
    const createStudentForm = document.getElementById('create-student-form');
    const classMessage = document.getElementById('class-message');
    const studentMessage = document.getElementById('student-message');


    

    // Load students once the page is ready and authHeader is available.
    loadStudents();
    console.log('Loading students...');
    loadClasses();
    console.log('Loading classes...');

    const kind = localStorage.getItem('kind');
    if(kind !== 'teacher') {
        window.location.href = '/static/index.html'; // Redirect to login
        return; // Stop script execution if not authenticated
    }   


    // --- Logout Logic ---
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            localStorage.removeItem('accessToken');
            window.location.href = '/static/index.html';
        });
    }

    // --- Create Class Logic ---
    if (createClassForm) {
        createClassForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            classMessage.textContent = '';

            const classData = {
                start_datetime: document.getElementById('start_datetime').value,
                end_datetime: document.getElementById('end_datetime').value,
                teacher_id: parseInt(document.getElementById('teacher_id').value),
                student_id: parseInt(document.getElementById('student_id').value)
            };
            const startDate = new Date(classData.start_datetime);
            const endDate = new Date(classData.end_datetime);
            const now = new Date();

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
                    createClassForm.reset();
                    loadClasses(); // Reload classes after successful creation
                } else {
                    const errorData = await response.json();
                    classMessage.textContent = `Error: ${errorData.detail || 'No se pudo crear la clase.'}`;
                    classMessage.className = 'text-danger';
                }
            } catch (error) {
                classMessage.textContent = 'Ocurrió un error de red.';
                classMessage.className = 'text-danger';
            }
        });
    }

    // --- Create Student Logic ---
    if (createStudentForm) {
        createStudentForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            studentMessage.textContent = '';

            const studentData = {
                first_name: document.getElementById('first_name').value,
                last_name: document.getElementById('last_name').value,
                age: parseInt(document.getElementById('age').value),
                document_number: document.getElementById('document_number').value,
                password: document.getElementById('password').value
            };

            try {
                // NOTE: You need to create this endpoint in your FastAPI backend
                const response = await fetch('/students/', { 
                    method: 'POST',
                    headers: authHeader,
                    body: JSON.stringify(studentData)
                });

                if (response.ok) {
                    studentMessage.textContent = '¡Estudiante creado exitosamente!';
                    studentMessage.className = 'text-success';
                    createStudentForm.reset();
                    loadStudents(); // Reload students after successful creation
                } else {
                    const errorData = await response.json();
                    studentMessage.textContent = `Error: ${errorData.detail || 'No se pudo crear el estudiante.'}`;
                    studentMessage.className = 'text-danger';
                }
            } catch (error) {
                studentMessage.textContent = 'Ocurrió un error de red.';
                studentMessage.className = 'text-danger';
            }
        });
    }
});


const loadStudents = async () => {
    const studentSelect = document.getElementById('student_id');
    if (!studentSelect) return;

    try {
        // This function is called after the main script execution,
        // so authHeader will be defined.
        const response = await fetch('/students/', {
            method: 'GET',
            headers: authHeader
        });

        if (!response.ok) {
            throw new Error('No se pudieron cargar los estudiantes.');
        }

        const students = await response.json();

        students.forEach(student => {
            const option = document.createElement('option');
            option.value = student.id;
            option.textContent = `${student.first_name} ${student.last_name}`;
            studentSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error al cargar estudiantes:', error);
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