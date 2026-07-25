// Expense Tracker Application Frontend Controller

// Default Initial Mock Expenses (if server is empty)
const initialMockExpenses = [
    { id: 101, title: "Supermarket Groceries", amount: 145.50, category: "Groceries", date: "2026-07-24", payment_method: "Credit Card", notes: "Weekly household food & items" },
    { id: 102, title: "Electric Utility Bill", amount: 92.00, category: "Utilities & Bills", date: "2026-07-20", payment_method: "UPI / Online Transfer", notes: "Monthly electricity payment" },
    { id: 103, title: "Restaurant Dinner", amount: 64.80, category: "Food & Dining", date: "2026-07-18", payment_method: "Credit Card", notes: "Team dinner outing" },
    { id: 104, title: "Fuel Refill", amount: 45.00, category: "Transportation", date: "2026-07-15", payment_method: "Debit Card", notes: "Gasoline for car" },
    { id: 105, title: "Online Shopping", amount: 120.00, category: "Shopping", date: "2026-07-10", payment_method: "Credit Card", notes: "New headphones" },
    { id: 106, title: "Doctor Checkup", amount: 80.00, category: "Health & Medical", date: "2026-07-05", payment_method: "Cash", notes: "Routine health consultation" }
];

let state = {
    user: null,
    expenses: [],
    activeTab: 'tab-total',
    charts: {}
};

// Initialize Application on Page Load
document.addEventListener('DOMContentLoaded', async () => {
    // Set default date picker to today
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.getElementById('exp-date');
    if (dateInput) dateInput.value = today;

    // Check stored user session from LocalStorage / Server
    const storedUser = localStorage.getItem('expense_user');
    if (storedUser) {
        state.user = JSON.parse(storedUser);
    }

    // Fetch Expenses from Server API
    await fetchExpensesFromServer();

    // Render screen based on auth state
    updateAuthScreenState();

    // Attach Sidebar Navigation Event Listeners
    setupNavigationListeners();
});

// ==================== AUTHENTICATION & LOGIN FLOW ==================== //

function updateAuthScreenState() {
    const loginScreen = document.getElementById('login-screen');
    const dashboardScreen = document.getElementById('dashboard-screen');

    if (state.user && state.user.logged_in) {
        loginScreen.classList.remove('active');
        dashboardScreen.classList.add('active');

        // Update User Name Badge
        document.getElementById('user-display-name').textContent = state.user.identity;
        document.getElementById('report-user-str').textContent = state.user.identity;

        // Render Dashboard Data
        renderDashboardData();
    } else {
        dashboardScreen.classList.remove('active');
        loginScreen.classList.add('active');
    }
}

// Handle Mobile / Email Sign In
async function handleAuthLogin(e) {
    e.preventDefault();
    const identityInput = document.getElementById('identity-input').value.trim();

    if (!identityInput) return;

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identity: identityInput, type: 'email_phone' })
        });
        const data = await res.json();
        
        state.user = data.user;
        localStorage.setItem('expense_user', JSON.stringify(state.user));
        updateAuthScreenState();
    } catch (err) {
        // Fallback offline login
        state.user = { identity: identityInput, type: 'email_phone', logged_in: true };
        localStorage.setItem('expense_user', JSON.stringify(state.user));
        updateAuthScreenState();
    }
}

// Handle Google Email ID Sign In Option
async function handleGoogleLogin() {
    const googleEmail = "google.user@gmail.com";
    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identity: googleEmail, type: 'google' })
        });
        const data = await res.json();
        
        state.user = data.user;
        localStorage.setItem('expense_user', JSON.stringify(state.user));
        updateAuthScreenState();
    } catch (err) {
        state.user = { identity: googleEmail, type: 'google', logged_in: true };
        localStorage.setItem('expense_user', JSON.stringify(state.user));
        updateAuthScreenState();
    }
}

// Quick Demo Guest Access
function quickGuestAccess() {
    state.user = { identity: "guest_demo@example.com", type: "guest", logged_in: true };
    localStorage.setItem('expense_user', JSON.stringify(state.user));
    updateAuthScreenState();
}

// Handle Sign Out / Logout
async function handleLogout() {
    try {
        await fetch('/api/auth/logout', { method: 'POST' });
    } catch (e) {}
    state.user = null;
    localStorage.removeItem('expense_user');
    updateAuthScreenState();
}

// ==================== EXPENSE DATA API OPERATIONS ==================== //

async function fetchExpensesFromServer() {
    try {
        const res = await fetch('/api/expenses');
        const data = await res.json();
        if (data.expenses && data.expenses.length > 0) {
            state.expenses = data.expenses;
        } else {
            // Load mock initial expenses if server has none
            state.expenses = [...initialMockExpenses];
        }
    } catch (err) {
        state.expenses = [...initialMockExpenses];
    }
}

// KEY POINT 1: ADD EXPENSES
async function submitAddExpense(e) {
    e.preventDefault();

    const title = document.getElementById('exp-title').value.trim();
    const amount = parseFloat(document.getElementById('exp-amount').value);
    const category = document.getElementById('exp-category').value;
    const date = document.getElementById('exp-date').value;
    const payment_method = document.getElementById('exp-payment').value;
    const notes = document.getElementById('exp-notes').value.trim();

    const newExpense = {
        id: Date.now(),
        title,
        amount,
        category,
        date,
        payment_method,
        notes
    };

    try {
        await fetch('/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newExpense)
        });
    } catch (err) {}

    state.expenses.unshift(newExpense);
    document.getElementById('add-expense-form').reset();
    
    // Reset date to today
    document.getElementById('exp-date').value = new Date().toISOString().split('T')[0];

    // Re-render views
    renderDashboardData();
    switchTab('tab-view');
    alert('Expense added successfully!');
}

// KEY POINT 6: EDIT EXPENSE
function openEditModal(expenseId) {
    const expense = state.expenses.find(exp => exp.id == expenseId);
    if (!expense) return;

    document.getElementById('edit-exp-id').value = expense.id;
    document.getElementById('edit-exp-title').value = expense.title;
    document.getElementById('edit-exp-amount').value = expense.amount;
    document.getElementById('edit-exp-category').value = expense.category;
    document.getElementById('edit-exp-date').value = expense.date;
    document.getElementById('edit-exp-payment').value = expense.payment_method;
    document.getElementById('edit-exp-notes').value = expense.notes || '';

    document.getElementById('edit-modal').classList.add('active');
}

function closeEditModal() {
    document.getElementById('edit-modal').classList.remove('active');
}

async function submitEditExpense(e) {
    e.preventDefault();
    const id = document.getElementById('edit-exp-id').value;
    const title = document.getElementById('edit-exp-title').value.trim();
    const amount = parseFloat(document.getElementById('edit-exp-amount').value);
    const category = document.getElementById('edit-exp-category').value;
    const date = document.getElementById('edit-exp-date').value;
    const payment_method = document.getElementById('edit-exp-payment').value;
    const notes = document.getElementById('edit-exp-notes').value.trim();

    const updatedData = { title, amount, category, date, payment_method, notes };

    try {
        await fetch(`/api/expenses/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        });
    } catch (err) {}

    const index = state.expenses.findIndex(exp => exp.id == id);
    if (index !== -1) {
        state.expenses[index] = { ...state.expenses[index], ...updatedData };
    }

    closeEditModal();
    renderDashboardData();
    alert('Expense updated successfully!');
}

// KEY POINT 7: DELETE EXPENSE
async function deleteExpenseItem(expenseId) {
    if (!confirm('Are you sure you want to delete this expense record?')) return;

    try {
        await fetch(`/api/expenses/${expenseId}`, { method: 'DELETE' });
    } catch (err) {}

    state.expenses = state.expenses.filter(exp => exp.id != expenseId);
    renderDashboardData();
}

// ==================== RENDERING DASHBOARD VIEWS ==================== //

function renderDashboardData() {
    renderTotalExpensesMetrics();  // Key Point 4
    renderRecentExpensesTable();  // Key Point 3
    renderViewExpensesTable();    // Key Point 3
    renderSearchResults();        // Key Point 2
    renderCategoryReport();       // Key Point 5
    renderChartAnalytics();       // Key Point 8
    renderFinancialReport();      // Key Point 9
    renderMonthlyExpenses();      // Key Point 11
}

// KEY POINT 4: TOTAL EXPENSES METRICS
function renderTotalExpensesMetrics() {
    const totalAmount = state.expenses.reduce((sum, exp) => sum + Number(exp.amount), 0);
    const totalCount = state.expenses.length;

    // Current Month total calculation
    const currentMonthStr = new Date().toISOString().slice(0, 7); // "YYYY-MM"
    const thisMonthAmount = state.expenses
        .filter(exp => exp.date && exp.date.startsWith(currentMonthStr))
        .reduce((sum, exp) => sum + Number(exp.amount), 0);

    // Top spending category
    const catMap = {};
    state.expenses.forEach(exp => {
        catMap[exp.category] = (catMap[exp.category] || 0) + Number(exp.amount);
    });
    let topCat = 'N/A';
    let maxSpend = 0;
    for (const [cat, amt] of Object.entries(catMap)) {
        if (amt > maxSpend) {
            maxSpend = amt;
            topCat = cat;
        }
    }

    document.getElementById('stat-total-amount').textContent = `$${totalAmount.toFixed(2)}`;
    document.getElementById('stat-total-count').textContent = totalCount;
    document.getElementById('stat-this-month').textContent = `$${thisMonthAmount.toFixed(2)}`;
    document.getElementById('stat-top-category').textContent = topCat;
}

// KEY POINT 3: VIEW EXPENSES & RECENT TABLE
function renderRecentExpensesTable() {
    const tbody = document.getElementById('recent-expenses-rows');
    if (!tbody) return;

    const recentList = state.expenses.slice(0, 5);
    if (recentList.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" class="text-muted text-center">No expense entries found.</td></tr>`;
        return;
    }

    tbody.innerHTML = recentList.map(exp => `
        <tr>
            <td>${exp.date}</td>
            <td><strong>${escapeHtml(exp.title)}</strong></td>
            <td><span class="category-tag">${exp.category}</span></td>
            <td>${exp.payment_method}</td>
            <td><strong>$${Number(exp.amount).toFixed(2)}</strong></td>
        </tr>
    `).join('');
}

function renderViewExpensesTable() {
    const tbody = document.getElementById('view-expenses-rows');
    if (!tbody) return;

    if (state.expenses.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-muted text-center">No expenses available. Click "Add Expenses" to start.</td></tr>`;
        return;
    }

    tbody.innerHTML = state.expenses.map(exp => `
        <tr>
            <td>#${exp.id}</td>
            <td>${exp.date}</td>
            <td>
                <strong>${escapeHtml(exp.title)}</strong>
                ${exp.notes ? `<br><small class="text-muted">${escapeHtml(exp.notes)}</small>` : ''}
            </td>
            <td><span class="category-tag">${exp.category}</span></td>
            <td>${exp.payment_method}</td>
            <td><strong>$${Number(exp.amount).toFixed(2)}</strong></td>
            <td>
                <div class="action-btns">
                    <button class="btn-icon btn-edit" title="Edit Expense" onclick="openEditModal(${exp.id})">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                    <button class="btn-icon btn-delete" title="Delete Expense" onclick="deleteExpenseItem(${exp.id})">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// KEY POINT 2: SEARCH EXPENSES
function renderSearchResults() {
    const tbody = document.getElementById('search-expenses-rows');
    if (!tbody) return;

    const keyword = (document.getElementById('search-keyword')?.value || '').toLowerCase();
    const selectedCategory = document.getElementById('search-category')?.value || 'ALL';
    const selectedPayment = document.getElementById('search-payment')?.value || 'ALL';

    const filtered = state.expenses.filter(exp => {
        const matchesKeyword = exp.title.toLowerCase().includes(keyword) || (exp.notes && exp.notes.toLowerCase().includes(keyword));
        const matchesCategory = selectedCategory === 'ALL' || exp.category === selectedCategory;
        const matchesPayment = selectedPayment === 'ALL' || exp.payment_method === selectedPayment;
        return matchesKeyword && matchesCategory && matchesPayment;
    });

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="6" class="text-muted text-center">No matching expenses found for the current search filter.</td></tr>`;
        return;
    }

    tbody.innerHTML = filtered.map(exp => `
        <tr>
            <td>${exp.date}</td>
            <td><strong>${escapeHtml(exp.title)}</strong></td>
            <td><span class="category-tag">${exp.category}</span></td>
            <td>${exp.payment_method}</td>
            <td><strong>$${Number(exp.amount).toFixed(2)}</strong></td>
            <td>
                <div class="action-btns">
                    <button class="btn-icon btn-edit" onclick="openEditModal(${exp.id})"><i class="fa-solid fa-pen"></i></button>
                    <button class="btn-icon btn-delete" onclick="deleteExpenseItem(${exp.id})"><i class="fa-solid fa-trash"></i></button>
                </div>
            </td>
        </tr>
    `).join('');
}

// KEY POINT 5: CATEGORY REPORT
function renderCategoryReport() {
    const container = document.getElementById('category-report-bars');
    if (!container) return;

    const totalSpend = state.expenses.reduce((sum, exp) => sum + Number(exp.amount), 0);
    const catMap = {};

    state.expenses.forEach(exp => {
        catMap[exp.category] = (catMap[exp.category] || 0) + Number(exp.amount);
    });

    if (totalSpend === 0) {
        container.innerHTML = `<p class="text-muted">No expense data available for report.</p>`;
        return;
    }

    const sortedCats = Object.entries(catMap).sort((a, b) => b[1] - a[1]);

    container.innerHTML = sortedCats.map(([cat, amt]) => {
        const percent = Math.round((amt / totalSpend) * 100);
        return `
            <div class="cat-progress-item">
                <div class="cat-progress-meta">
                    <span>${cat}</span>
                    <span>$${amt.toFixed(2)} (${percent}%)</span>
                </div>
                <div class="progress-track">
                    <div class="progress-fill" style="width: ${percent}%;"></div>
                </div>
            </div>
        `;
    }).join('');
}

// KEY POINT 8: CHART ANALYTICS
function renderChartAnalytics() {
    const catCanvas = document.getElementById('categoryDonutChart');
    const monthlyCanvas = document.getElementById('monthlyBarChart');
    const pieCanvas = document.getElementById('categoryPieChart');

    if (!catCanvas || !monthlyCanvas) return;

    // Aggregate category totals
    const catMap = {};
    state.expenses.forEach(exp => {
        catMap[exp.category] = (catMap[exp.category] || 0) + Number(exp.amount);
    });

    const catLabels = Object.keys(catMap);
    const catData = Object.values(catMap);

    const chartColors = ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#f43f5e', '#6366f1', '#06b6d4', '#ec4899'];

    // Donut Chart
    if (state.charts.donut) state.charts.donut.destroy();
    state.charts.donut = new Chart(catCanvas, {
        type: 'doughnut',
        data: {
            labels: catLabels,
            datasets: [{
                data: catData,
                backgroundColor: chartColors
            }]
        },
        options: { responsive: true, maintainAspectRatio: false }
    });

    // Small Pie Chart in Category Report tab
    if (pieCanvas) {
        if (state.charts.pie) state.charts.pie.destroy();
        state.charts.pie = new Chart(pieCanvas, {
            type: 'pie',
            data: {
                labels: catLabels,
                datasets: [{
                    data: catData,
                    backgroundColor: chartColors
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }

    // Monthly Bar Chart aggregation
    const monthMap = {};
    state.expenses.forEach(exp => {
        const monthKey = exp.date ? exp.date.slice(0, 7) : 'Other';
        monthMap[monthKey] = (monthMap[monthKey] || 0) + Number(exp.amount);
    });

    const monthLabels = Object.keys(monthMap).sort();
    const monthData = monthLabels.map(m => monthMap[m]);

    if (state.charts.bar) state.charts.bar.destroy();
    state.charts.bar = new Chart(monthlyCanvas, {
        type: 'bar',
        data: {
            labels: monthLabels,
            datasets: [{
                label: 'Monthly Spend ($)',
                data: monthData,
                backgroundColor: '#3b82f6',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: { y: { beginAtZero: true } }
        }
    });
}

// KEY POINT 9: FINANCIAL REPORT
function renderFinancialReport() {
    const totalAmount = state.expenses.reduce((sum, exp) => sum + Number(exp.amount), 0);
    const count = state.expenses.length;
    const avg = count > 0 ? (totalAmount / count) : 0;

    document.getElementById('report-date-str').textContent = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById('report-stat-total').textContent = `$${totalAmount.toFixed(2)}`;
    document.getElementById('report-stat-count').textContent = count;
    document.getElementById('report-stat-avg').textContent = `$${avg.toFixed(2)}`;

    const tbody = document.getElementById('report-category-rows');
    if (!tbody) return;

    const catMap = {};
    state.expenses.forEach(exp => {
        if (!catMap[exp.category]) {
            catMap[exp.category] = { count: 0, sum: 0 };
        }
        catMap[exp.category].count += 1;
        catMap[exp.category].sum += Number(exp.amount);
    });

    tbody.innerHTML = Object.entries(catMap).map(([cat, obj]) => {
        const pct = totalAmount > 0 ? ((obj.sum / totalAmount) * 100).toFixed(1) : 0;
        return `
            <tr>
                <td><strong>${cat}</strong></td>
                <td>${obj.count}</td>
                <td>$${obj.sum.toFixed(2)}</td>
                <td>${pct}%</td>
            </tr>
        `;
    }).join('');
}

// KEY POINT 11: MONTHLY EXPENSES
function renderMonthlyExpenses() {
    const tbody = document.getElementById('monthly-expenses-rows');
    if (!tbody) return;

    const monthMap = {};
    state.expenses.forEach(exp => {
        const monthKey = exp.date ? exp.date.slice(0, 7) : 'Unknown';
        if (!monthMap[monthKey]) {
            monthMap[monthKey] = { count: 0, total: 0 };
        }
        monthMap[monthKey].count += 1;
        monthMap[monthKey].total += Number(exp.amount);
    });

    const sortedMonths = Object.keys(monthMap).sort().reverse();

    if (sortedMonths.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="text-muted text-center">No monthly records available.</td></tr>`;
        return;
    }

    tbody.innerHTML = sortedMonths.map(m => {
        const item = monthMap[m];
        const avg = item.count > 0 ? (item.total / item.count) : 0;
        return `
            <tr>
                <td><strong>${m}</strong></td>
                <td>${item.count} items</td>
                <td><strong>$${item.total.toFixed(2)}</strong></td>
                <td>$${avg.toFixed(2)}</td>
            </tr>
        `;
    }).join('');
}

// KEY POINT 10: EXPORT SUMMARY (CSV & JSON)
function exportToCSV() {
    if (state.expenses.length === 0) {
        alert('No expenses available to export.');
        return;
    }

    const headers = ["ID", "Date", "Title", "Category", "Payment Method", "Amount", "Notes"];
    const rows = state.expenses.map(exp => [
        exp.id,
        exp.date,
        `"${(exp.title || '').replace(/"/g, '""')}"`,
        `"${exp.category}"`,
        `"${exp.payment_method}"`,
        exp.amount,
        `"${(exp.notes || '').replace(/"/g, '""')}"`
    ]);

    const csvContent = "data:text/csv;charset=utf-8," 
        + [headers.join(","), ...rows.map(r => r.join(","))].join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `expense_summary_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function exportToJSON() {
    if (state.expenses.length === 0) {
        alert('No expenses available to export.');
        return;
    }

    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(state.expenses, null, 2));
    const link = document.createElement("a");
    link.setAttribute("href", dataStr);
    link.setAttribute("download", `expense_summary_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// NAVIGATION & THEME HELPERS
function setupNavigationListeners() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabId = item.getAttribute('data-tab');
            switchTab(tabId);
        });
    });
}

function switchTab(tabId) {
    state.activeTab = tabId;

    // Update active nav button
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-tab') === tabId);
    });

    // Update tab visibility
    document.querySelectorAll('.tab-pane').forEach(pane => {
        pane.classList.toggle('active', pane.id === tabId);
    });

    // Update Top Header Title
    const titleMap = {
        'tab-total': 'Total Expenses',
        'tab-add': 'Add Expenses',
        'tab-view': 'View Expenses',
        'tab-search': 'Search Expenses',
        'tab-category': 'Category Report',
        'tab-chart': 'Chart Analytics',
        'tab-report': 'Financial Report',
        'tab-monthly': 'Monthly Expenses',
        'tab-export': 'Export Summary'
    };
    if (titleMap[tabId]) {
        document.getElementById('page-title').textContent = titleMap[tabId];
    }

    // Refresh charts if chart tab clicked
    if (tabId === 'tab-chart' || tabId === 'tab-category') {
        setTimeout(renderChartAnalytics, 100);
    }
}

function toggleTheme() {
    document.body.classList.toggle('light-theme');
    const icon = document.querySelector('.theme-toggle i');
    if (document.body.classList.contains('light-theme')) {
        icon.className = 'fa-solid fa-sun';
    } else {
        icon.className = 'fa-solid fa-moon';
    }
}

function escapeHtml(str) {
    return String(str || '').replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
