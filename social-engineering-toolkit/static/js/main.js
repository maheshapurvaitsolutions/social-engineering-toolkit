// Social Engineering Toolkit - Main JavaScript

// Global variables
let currentUser = null;
let notifications = [];

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    checkNotifications();
});

function initializeApp() {
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

function setupEventListeners() {
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Auto-hide alerts
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            if (alert.classList.contains('auto-hide')) {
                const alertInstance = new bootstrap.Alert(alert);
                alertInstance.close();
            }
        });
    }, 5000);
}

function checkNotifications() {
    // Check for security notifications
    if (typeof fetch !== 'undefined') {
        fetch('/api/notifications')
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                return { notifications: [] };
            })
            .then(data => {
                displayNotifications(data.notifications || []);
            })
            .catch(error => {
                console.log('Notifications not available:', error.message);
            });
    }
}

function displayNotifications(notifications) {
    const container = document.getElementById('notifications-container');
    if (!container || notifications.length === 0) return;
    
    notifications.forEach(notification => {
        showNotification(notification.message, notification.type || 'info');
    });
}

function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const iconClass = getIconClass(type);
    
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show auto-hide" role="alert">
            <i class="${iconClass} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('main .container, main .container-fluid');
    if (container) {
        container.insertAdjacentHTML('afterbegin', alertHtml);
    }
}

function getIconClass(type) {
    const icons = {
        'success': 'fas fa-check-circle',
        'danger': 'fas fa-exclamation-triangle',
        'warning': 'fas fa-exclamation-circle',
        'info': 'fas fa-info-circle'
    };
    return icons[type] || icons['info'];
}

// Utility functions
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

// Campaign management functions
function deleteCampaign(campaignId) {
    if (!confirm('Are you sure you want to delete this campaign?')) {
        return;
    }
    
    fetch(`/api/campaigns/${campaignId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Campaign deleted successfully', 'success');
            location.reload();
        } else {
            showNotification('Error deleting campaign: ' + data.error, 'danger');
        }
    })
    .catch(error => {
        showNotification('Network error occurred', 'danger');
        console.error('Error:', error);
    });
}

function exportCampaignResults(campaignId) {
    window.open(`/api/campaigns/${campaignId}/export`, '_blank');
}

// Training functions
function markTrainingComplete(moduleId, score = null) {
    const data = {
        module_id: moduleId,
        completed: true
    };
    
    if (score !== null) {
        data.score = score;
    }
    
    fetch('/api/training/complete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Training progress saved', 'success');
        }
    })
    .catch(error => {
        console.error('Error saving progress:', error);
    });
}

// Security simulation functions
function simulatePhishingClick(campaignId, linkId) {
    // Record that user clicked on phishing link
    fetch('/api/phishing/click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            campaign_id: campaignId,
            link_id: linkId,
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent
        })
    })
    .then(response => response.json())
    .then(data => {
        // Show educational message
        showPhishingEducation();
    })
    .catch(error => {
        console.error('Error recording click:', error);
    });
}

function showPhishingEducation() {
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header bg-warning text-white">
                    <h5 class="modal-title">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        Security Alert: Phishing Simulation
                    </h5>
                </div>
                <div class="modal-body">
                    <div class="alert alert-warning">
                        <h6>You clicked on a simulated phishing link!</h6>
                        <p>This was a training exercise. In a real attack, this could have led to:</p>
                        <ul>
                            <li>Malware installation</li>
                            <li>Credential theft</li>
                            <li>Data compromise</li>
                        </ul>
                    </div>
                    <h6>Remember:</h6>
                    <ul>
                        <li>Always verify sender authenticity</li>
                        <li>Hover over links to see real URLs</li>
                        <li>Be suspicious of urgent requests</li>
                        <li>When in doubt, verify through official channels</li>
                    </ul>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
                        I Understand
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    const modalInstance = new bootstrap.Modal(modal);
    modalInstance.show();
    
    modal.addEventListener('hidden.bs.modal', function() {
        document.body.removeChild(modal);
    });
}

// Report generation functions
function generateReport(type) {
    const button = event.target;
    const originalText = button.textContent;
    
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
    
    fetch('/api/reports/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ type: type })
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Report generation failed');
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `security-report-${type}-${new Date().toISOString().split('T')[0]}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showNotification('Report generated successfully', 'success');
    })
    .catch(error => {
        showNotification('Error generating report: ' + error.message, 'danger');
        console.error('Error:', error);
    })
    .finally(() => {
        button.disabled = false;
        button.textContent = originalText;
    });
}

// Chart functions (if Chart.js is available)
function createCampaignChart(canvasId, data) {
    if (typeof Chart === 'undefined') return;
    
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Clicked', 'Not Clicked', 'Reported'],
            datasets: [{
                data: [data.clicked, data.not_clicked, data.reported],
                backgroundColor: [
                    '#dc3545',
                    '#28a745',
                    '#17a2b8'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Export functions
window.showNotification = showNotification;
window.deleteCampaign = deleteCampaign;
window.exportCampaignResults = exportCampaignResults;
window.markTrainingComplete = markTrainingComplete;
window.simulatePhishingClick = simulatePhishingClick;
window.generateReport = generateReport;
window.createCampaignChart = createCampaignChart;

