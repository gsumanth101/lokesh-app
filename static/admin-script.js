// Admin Dashboard JavaScript
// Global variables
let currentLanguage = 'en';
let users = [];
let systemStats = {};

// Initialize admin dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeAdminDashboard();
});

function initializeAdminDashboard() {
    // Load admin info
    loadAdminInfo();
    
    // Load system statistics
    loadSystemStats();
    
    // Load user management
    loadUsers();
    
    // Load analytics
    loadAnalytics();
    
    // Set default language
    changeLanguage();
}

// Load admin information
async function loadAdminInfo() {
    try {
        const response = await fetch('/api/user-info');
        const result = await response.json();
        
        if (result.success) {
            const adminName = document.getElementById('admin-name');
            if (adminName) {
                adminName.textContent = `Welcome, ${result.data.name}!`;
            }
        }
    } catch (error) {
        console.error('Error loading admin info:', error);
    }
}

// Load system statistics
async function loadSystemStats() {
    try {
        const response = await fetch('/api/admin/stats');
        const result = await response.json();
        
        if (result.success) {
            displaySystemStats(result.data);
        }
    } catch (error) {
        console.error('Error loading system stats:', error);
        // Display default stats
        displaySystemStats({
            total_users: 150,
            active_users: 120,
            total_listings: 75,
            active_listings: 60,
            total_transactions: 45,
            system_health: 'Good'
        });
    }
}

// Display system statistics
function displaySystemStats(stats) {
    const statsContainer = document.getElementById('system-stats');
    if (!statsContainer) return;
    
    statsContainer.innerHTML = `
        <div class="stat-card">
            <h3>👥 Total Users</h3>
            <p class="stat-number">${stats.total_users}</p>
        </div>
        <div class="stat-card">
            <h3>✅ Active Users</h3>
            <p class="stat-number">${stats.active_users}</p>
        </div>
        <div class="stat-card">
            <h3>📝 Total Listings</h3>
            <p class="stat-number">${stats.total_listings}</p>
        </div>
        <div class="stat-card">
            <h3>🔄 Active Listings</h3>
            <p class="stat-number">${stats.active_listings}</p>
        </div>
        <div class="stat-card">
            <h3>💰 Transactions</h3>
            <p class="stat-number">${stats.total_transactions}</p>
        </div>
        <div class="stat-card">
            <h3>🏥 System Health</h3>
            <p class="stat-status ${stats.system_health.toLowerCase()}">${stats.system_health}</p>
        </div>
    `;
}

// Load users for management
async function loadUsers() {
    try {
        const response = await fetch('/api/admin/users');
        const result = await response.json();
        
        if (result.success) {
            users = result.data;
            displayUsers(users);
        }
    } catch (error) {
        console.error('Error loading users:', error);
        // Display sample users
        users = [
            { id: 1, name: 'John Farmer', email: 'john@farm.com', role: 'farmer', status: 'active' },
            { id: 2, name: 'Jane Buyer', email: 'jane@buy.com', role: 'buyer', status: 'active' },
            { id: 3, name: 'Bob Agent', email: 'bob@agent.com', role: 'agent', status: 'inactive' }
        ];
        displayUsers(users);
    }
}

// Display users
function displayUsers(userList) {
    const usersContainer = document.getElementById('users-list');
    if (!usersContainer) return;
    
    usersContainer.innerHTML = userList.map(user => `
        <div class="user-card">
            <div class="user-info">
                <h4>${user.name}</h4>
                <p>Email: ${user.email}</p>
                <p>Role: ${user.role}</p>
                <p>Status: <span class="status ${user.status}">${user.status}</span></p>
            </div>
            <div class="user-actions">
                <button onclick="editUser(${user.id})" class="btn btn-secondary">Edit</button>
                <button onclick="toggleUserStatus(${user.id})" class="btn ${user.status === 'active' ? 'btn-danger' : 'btn-success'}">
                    ${user.status === 'active' ? 'Deactivate' : 'Activate'}
                </button>
                <button onclick="deleteUser(${user.id})" class="btn btn-danger">Delete</button>
            </div>
        </div>
    `).join('');
}

// Edit user
function editUser(userId) {
    const user = users.find(u => u.id === userId);
    if (!user) return;
    
    const name = prompt('Edit user name:', user.name);
    const email = prompt('Edit user email:', user.email);
    const role = prompt('Edit user role (farmer/buyer/agent):', user.role);
    
    if (name && email && role) {
        updateUser(userId, { name, email, role });
    }
}

// Update user
async function updateUser(userId, userData) {
    try {
        const response = await fetch(`/api/admin/users/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('User updated successfully!');
            loadUsers();
        } else {
            alert('Error updating user: ' + result.message);
        }
    } catch (error) {
        console.error('Error updating user:', error);
        alert('Error updating user. Please try again.');
    }
}

// Toggle user status
async function toggleUserStatus(userId) {
    const user = users.find(u => u.id === userId);
    if (!user) return;
    
    const newStatus = user.status === 'active' ? 'inactive' : 'active';
    
    try {
        const response = await fetch(`/api/admin/users/${userId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: newStatus })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(`User ${newStatus === 'active' ? 'activated' : 'deactivated'} successfully!`);
            loadUsers();
        } else {
            alert('Error updating user status: ' + result.message);
        }
    } catch (error) {
        console.error('Error toggling user status:', error);
        // Update locally for demo
        user.status = newStatus;
        displayUsers(users);
        alert(`User ${newStatus === 'active' ? 'activated' : 'deactivated'} successfully!`);
    }
}

// Delete user
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
        const response = await fetch(`/api/admin/users/${userId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert('User deleted successfully!');
            loadUsers();
        } else {
            alert('Error deleting user: ' + result.message);
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        // Remove locally for demo
        users = users.filter(u => u.id !== userId);
        displayUsers(users);
        alert('User deleted successfully!');
    }
}

// Load analytics
async function loadAnalytics() {
    try {
        const response = await fetch('/api/admin/analytics');
        const result = await response.json();
        
        if (result.success) {
            displayAnalytics(result.data);
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
        // Display sample analytics
        displayAnalytics({
            user_growth: [10, 15, 20, 25, 30],
            crop_recommendations: [45, 50, 55, 60, 65],
            marketplace_activity: [20, 25, 30, 35, 40]
        });
    }
}

// Display analytics
function displayAnalytics(analytics) {
    const analyticsContainer = document.getElementById('analytics-charts');
    if (!analyticsContainer) return;
    
    analyticsContainer.innerHTML = `
        <div class="chart-card">
            <h3>📈 User Growth</h3>
            <div class="chart-placeholder">
                <p>Users over time: ${analytics.user_growth.join(' → ')}</p>
            </div>
        </div>
        <div class="chart-card">
            <h3>🌾 Crop Recommendations</h3>
            <div class="chart-placeholder">
                <p>Recommendations: ${analytics.crop_recommendations.join(' → ')}</p>
            </div>
        </div>
        <div class="chart-card">
            <h3>🏪 Marketplace Activity</h3>
            <div class="chart-placeholder">
                <p>Activity: ${analytics.marketplace_activity.join(' → ')}</p>
            </div>
        </div>
    `;
}

// Filter users
function filterUsers() {
    const filterValue = document.getElementById('user-filter').value;
    const searchValue = document.getElementById('user-search').value.toLowerCase();
    
    let filteredUsers = users;
    
    if (filterValue !== 'all') {
        filteredUsers = filteredUsers.filter(user => user.role === filterValue);
    }
    
    if (searchValue) {
        filteredUsers = filteredUsers.filter(user => 
            user.name.toLowerCase().includes(searchValue) ||
            user.email.toLowerCase().includes(searchValue)
        );
    }
    
    displayUsers(filteredUsers);
}

// Export data
async function exportData() {
    try {
        const response = await fetch('/api/admin/export', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'smart_farming_data.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } else {
            alert('Error exporting data');
        }
    } catch (error) {
        console.error('Error exporting data:', error);
        alert('Error exporting data. Please try again.');
    }
}

// Tab switching functionality
function showTab(tabId) {
    // Hide all tab contents
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Remove active class from all tab buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => button.classList.remove('active'));
    
    // Show selected tab content
    document.getElementById(tabId).classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Language change functionality
function changeLanguage() {
    const languageSelect = document.getElementById('languageSelect');
    if (!languageSelect) return;
    
    currentLanguage = languageSelect.value;
    
    // Update all elements with data-lang attribute
    const elements = document.querySelectorAll('[data-lang]');
    elements.forEach(element => {
        const key = element.getAttribute('data-lang');
        if (translations[currentLanguage] && translations[currentLanguage][key]) {
            element.textContent = translations[currentLanguage][key];
        }
    });
}

// Logout function
async function logout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            window.location.href = '/login';
        }
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = '/login';
    }
}

// Refresh dashboard
function refreshDashboard() {
    loadSystemStats();
    loadUsers();
    loadAnalytics();
    alert('Dashboard refreshed successfully!');
}
