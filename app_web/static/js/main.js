// Initialize Select2 for all select elements with class 'select2'
$(document).ready(function() {
    $('.select2').select2({
        theme: 'bootstrap-5',
        width: '100%'
    });
});

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize popovers
var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
});

// Show loading spinner
function showLoading() {
    const spinner = `
        <div class="spinner-overlay">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
        </div>
    `;
    $('body').append(spinner);
}

// Hide loading spinner
function hideLoading() {
    $('.spinner-overlay').remove();
}

// AJAX setup
$.ajaxSetup({
    beforeSend: function() {
        showLoading();
    },
    complete: function() {
        hideLoading();
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
        showAlert('error', 'Ha ocurrido un error. Por favor, intente nuevamente.');
    }
});

// Show alert message
function showAlert(type, message) {
    const alertClass = type === 'error' ? 'danger' : type;
    const alert = `
        <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    $('.container').prepend(alert);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        $('.alert').alert('close');
    }, 5000);
}

// Format date
function formatDate(date) {
    return new Date(date).toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

// Handle form submissions
$('form').on('submit', function(e) {
    const form = $(this);
    const submitButton = form.find('button[type="submit"]');
    
    // Disable submit button
    submitButton.prop('disabled', true);
    
    // Re-enable after 5 seconds (prevent double submission)
    setTimeout(() => {
        submitButton.prop('disabled', false);
    }, 5000);
});

// Handle task status changes
$('.task-status-select').on('change', function() {
    const taskId = $(this).data('task-id');
    const newStatus = $(this).val();
    
    $.ajax({
        url: `/proyectos/tareas/${taskId}/cambiar-estado/`,
        method: 'POST',
        data: {
            estado: newStatus,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            showAlert('success', 'Estado de la tarea actualizado correctamente');
            // Update UI if needed
            updateTaskUI(taskId, newStatus);
        }
    });
});

// Update task UI based on status
function updateTaskUI(taskId, status) {
    const taskElement = $(`#task-${taskId}`);
    taskElement.removeClass('completed in-progress pending');
    taskElement.addClass(status.toLowerCase());
    
    // Update status badge
    const statusBadge = taskElement.find('.status-badge');
    statusBadge.text(status);
}

// Handle skill selection
$('.skill-select').on('change', function() {
    const selectedSkills = $(this).val();
    updateSkillBadges(selectedSkills);
});

// Update skill badges
function updateSkillBadges(skills) {
    const container = $('.skill-badges');
    container.empty();
    
    skills.forEach(skill => {
        const badge = `
            <span class="skill-badge">
                ${skill}
                <button type="button" class="btn-close btn-close-white ms-2" aria-label="Remove"></button>
            </span>
        `;
        container.append(badge);
    });
}

// Handle market analysis chart updates
function updateMarketChart(chartId, data) {
    const ctx = document.getElementById(chartId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Tendencias del Mercado Laboral'
                }
            }
        }
    });
}

// Handle infinite scroll for task list
let page = 1;
let loading = false;

$(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
        if(!loading) {
            loading = true;
            loadMoreTasks();
        }
    }
});

function loadMoreTasks() {
    $.ajax({
        url: `/proyectos/tareas/?page=${page + 1}`,
        method: 'GET',
        success: function(response) {
            if(response.tasks.length > 0) {
                response.tasks.forEach(task => {
                    appendTask(task);
                });
                page++;
                loading = false;
            }
        }
    });
}

function appendTask(task) {
    const taskHtml = `
        <div class="task-item ${task.estado.toLowerCase()}" id="task-${task.id}">
            <h5>${task.titulo}</h5>
            <p>${task.descripcion}</p>
            <div class="task-meta">
                <span class="badge bg-${getStatusColor(task.estado)}">${task.estado}</span>
                <span class="due-date">Fecha límite: ${formatDate(task.fecha_fin_estimada)}</span>
            </div>
        </div>
    `;
    $('.task-list').append(taskHtml);
}

function getStatusColor(status) {
    const colors = {
        'PENDIENTE': 'warning',
        'EN_PROGRESO': 'info',
        'COMPLETADA': 'success',
        'CANCELADA': 'danger'
    };
    return colors[status] || 'secondary';
}

// Export functions for use in other scripts
window.appHelpers = {
    showLoading,
    hideLoading,
    showAlert,
    formatDate,
    formatCurrency,
    updateTaskUI,
    updateSkillBadges,
    updateMarketChart
}; 