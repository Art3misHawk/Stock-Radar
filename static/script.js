// Enhanced JavaScript for Stock Price Fetcher with Smooth UX

// Theme management
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'professional';
        this.initTheme();
        this.setupThemeToggle();
    }

    initTheme() {
        if (this.currentTheme === 'neumorphism') {
            document.body.classList.add('theme-neumorphism');
        }
        this.updateToggleButton();
    }

    setupThemeToggle() {
        const toggleButton = document.getElementById('themeToggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', () => this.toggleTheme());
        }
    }

    toggleTheme() {
        if (this.currentTheme === 'professional') {
            this.currentTheme = 'neumorphism';
            document.body.classList.add('theme-neumorphism');
        } else {
            this.currentTheme = 'professional';
            document.body.classList.remove('theme-neumorphism');
        }
        
        localStorage.setItem('theme', this.currentTheme);
        this.updateToggleButton();
        this.showToast(`Switched to ${this.currentTheme} theme`, 'info');
    }

    updateToggleButton() {
        const toggleButton = document.getElementById('themeToggle');
        const slider = toggleButton?.querySelector('.theme-toggle-slider');
        if (toggleButton && slider) {
            if (this.currentTheme === 'neumorphism') {
                toggleButton.classList.add('active');
                slider.innerHTML = '🎨';
            } else {
                toggleButton.classList.remove('active');
                slider.innerHTML = '🏢';
            }
        }
    }
}

// Autocomplete functionality
class AutoComplete {
    constructor(inputElement, apiEndpoint) {
        this.input = inputElement;
        this.apiEndpoint = apiEndpoint;
        this.dropdown = null;
        this.currentIndex = -1;
        this.cache = new Map();
        this.debounceTimer = null;
        
        this.setupEventListeners();
        this.createDropdown();
    }

    setupEventListeners() {
        this.input.addEventListener('input', (e) => this.handleInput(e));
        this.input.addEventListener('keydown', (e) => this.handleKeydown(e));
        this.input.addEventListener('blur', () => this.hideDropdown());
        this.input.addEventListener('focus', () => {
            if (this.input.value.trim().length >= 2) {
                this.showDropdown();
            }
        });
    }

    createDropdown() {
        this.dropdown = document.createElement('div');
        this.dropdown.className = 'autocomplete-dropdown';
        this.input.parentNode.style.position = 'relative';
        this.input.parentNode.appendChild(this.dropdown);
    }

    handleInput(e) {
        const query = e.target.value.trim();
        
        clearTimeout(this.debounceTimer);
        
        if (query.length < 2) {
            this.hideDropdown();
            return;
        }

        this.debounceTimer = setTimeout(() => {
            this.search(query);
        }, 300);
    }

    async search(query) {
        if (this.cache.has(query)) {
            this.displayResults(this.cache.get(query));
            return;
        }

        try {
            const response = await fetch(`${this.apiEndpoint}/${encodeURIComponent(query)}`);
            const results = await response.json();
            
            if (response.ok) {
                this.cache.set(query, results);
                this.displayResults(results);
            }
        } catch (error) {
            console.error('Autocomplete search failed:', error);
        }
    }

    displayResults(results) {
        this.dropdown.innerHTML = '';
        this.currentIndex = -1;

        if (!results || results.length === 0) {
            this.hideDropdown();
            return;
        }

        results.slice(0, 8).forEach((result, index) => {
            const item = document.createElement('div');
            item.className = 'autocomplete-item';
            item.innerHTML = `
                <div><strong>${result['1. symbol']}</strong></div>
                <div class="small text-muted">${result['2. name']}</div>
            `;
            
            item.addEventListener('mousedown', (e) => {
                e.preventDefault();
                this.selectItem(result);
            });
            
            this.dropdown.appendChild(item);
        });

        this.showDropdown();
    }

    selectItem(item) {
        this.input.value = item['1. symbol'];
        this.hideDropdown();
        
        // Trigger quote fetch
        if (window.getQuote) {
            window.getQuote(item['1. symbol']);
        }
    }

    handleKeydown(e) {
        const items = this.dropdown.querySelectorAll('.autocomplete-item');
        
        switch (e.key) {
            case 'ArrowDown':
                e.preventDefault();
                this.currentIndex = Math.min(this.currentIndex + 1, items.length - 1);
                this.updateSelection(items);
                break;
            case 'ArrowUp':
                e.preventDefault();
                this.currentIndex = Math.max(this.currentIndex - 1, -1);
                this.updateSelection(items);
                break;
            case 'Enter':
                e.preventDefault();
                if (this.currentIndex >= 0 && items[this.currentIndex]) {
                    const symbol = items[this.currentIndex].querySelector('strong').textContent;
                    this.input.value = symbol;
                    this.hideDropdown();
                    if (window.getQuote) {
                        window.getQuote(symbol);
                    }
                }
                break;
            case 'Escape':
                this.hideDropdown();
                break;
        }
    }

    updateSelection(items) {
        items.forEach((item, index) => {
            if (index === this.currentIndex) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    }

    showDropdown() {
        this.dropdown.style.display = 'block';
        this.dropdown.classList.add('fade-in');
    }

    hideDropdown() {
        setTimeout(() => {
            this.dropdown.style.display = 'none';
            this.dropdown.classList.remove('fade-in');
        }, 150);
    }
}

// Loading states manager
class LoadingManager {
    static show(element, type = 'spinner') {
        if (!element) return;
        
        element.classList.add('loading');
        
        if (type === 'skeleton') {
            element.innerHTML = this.getSkeletonHTML();
        } else {
            const originalContent = element.innerHTML;
            element.setAttribute('data-original-content', originalContent);
            element.innerHTML = `
                <div class="d-flex align-items-center justify-content-center py-4">
                    <div class="loading-spinner me-2"></div>
                    <span>Loading...</span>
                </div>
            `;
        }
    }

    static hide(element) {
        if (!element) return;
        
        element.classList.remove('loading');
        
        const originalContent = element.getAttribute('data-original-content');
        if (originalContent) {
            element.innerHTML = originalContent;
            element.removeAttribute('data-original-content');
        }
    }

    static getSkeletonHTML() {
        return `
            <div class="loading-skeleton skeleton-title"></div>
            <div class="loading-skeleton skeleton-text"></div>
            <div class="loading-skeleton skeleton-text"></div>
            <div class="loading-skeleton skeleton-number"></div>
        `;
    }
}

// Stock comparison functionality
class StockComparison {
    constructor() {
        this.stocks = new Map();
        this.maxStocks = 4;
    }

    addStock(symbol, data) {
        if (this.stocks.size >= this.maxStocks) {
            const firstKey = this.stocks.keys().next().value;
            this.stocks.delete(firstKey);
        }
        
        this.stocks.set(symbol, data);
        this.updateDisplay();
    }

    removeStock(symbol) {
        this.stocks.delete(symbol);
        this.updateDisplay();
    }

    updateDisplay() {
        const container = document.getElementById('comparisonContainer');
        if (!container) return;

        if (this.stocks.size === 0) {
            container.innerHTML = '<p class="text-muted">Add stocks to compare them here.</p>';
            return;
        }

        let html = '<div class="comparison-container">';
        
        this.stocks.forEach((data, symbol) => {
            const changeClass = data.change >= 0 ? 'price-up' : 'price-down';
            const changeSign = data.change >= 0 ? '+' : '';
            
            html += `
                <div class="stock-comparison-card">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                        <h5 class="mb-0">${symbol}</h5>
                        <button class="btn btn-sm btn-outline-danger" onclick="stockComparison.removeStock('${symbol}')">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    <div class="mb-2">
                        <h3 class="mb-1">$${data.price.toFixed(2)}</h3>
                        <span class="${changeClass}">
                            ${changeSign}${data.change.toFixed(2)} (${data.change_percent})
                        </span>
                    </div>
                    <div class="row">
                        <div class="col-6">
                            <small class="text-muted">High: $${data.high.toFixed(2)}</small>
                        </div>
                        <div class="col-6">
                            <small class="text-muted">Low: $${data.low.toFixed(2)}</small>
                        </div>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
    }

    clear() {
        this.stocks.clear();
        this.updateDisplay();
    }
}

// Global instances
let themeManager;
let stockComparison;
let searchAutocomplete;
let symbolAutocomplete;

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize theme manager
    themeManager = new ThemeManager();
    
    // Initialize stock comparison
    stockComparison = new StockComparison();
    
    // Initialize autocomplete for search inputs
    const searchInput = document.getElementById('searchInput');
    const symbolInput = document.getElementById('symbolInput');
    
    if (searchInput) {
        searchAutocomplete = new AutoComplete(searchInput, '/api/search');
    }
    
    if (symbolInput) {
        symbolAutocomplete = new AutoComplete(symbolInput, '/api/search');
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(amount);
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-US').format(num);
}

function formatPercentChange(change, percent) {
    const sign = change >= 0 ? '+' : '';
    const color = change >= 0 ? 'price-up' : 'price-down';
    return `<span class="${color}">${sign}${change.toFixed(2)} (${percent})</span>`;
}

// Toast notification system
function showToast(message, type = 'info', duration = 4000) {
    const toastContainer = document.getElementById('toast-container') || createToastContainer();
    const toastId = 'toast-' + Date.now();
    
    const toast = document.createElement('div');
    toast.id = toastId;
    toast.className = `toast align-items-center text-white bg-${type} border-0 show`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${getToastIcon(type)} me-2"></i>${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after duration
    setTimeout(() => {
        const toastElement = document.getElementById(toastId);
        if (toastElement) {
            toastElement.remove();
        }
    }, duration);
}

function getToastIcon(type) {
    const icons = {
        success: 'check-circle',
        danger: 'exclamation-triangle',
        warning: 'exclamation-circle',
        info: 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'position-fixed top-0 end-0 p-3';
    container.style.zIndex = '1060';
    document.body.appendChild(container);
    return container;
}

// Performance optimizations
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Button loading states
function setButtonLoading(button, loading = true) {
    if (!button) return;
    
    if (loading) {
        button.disabled = true;
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.classList.add('loading');
        button.innerHTML = '<span class="loading-spinner me-2"></span>Loading...';
    } else {
        button.disabled = false;
        button.classList.remove('loading');
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
            button.removeAttribute('data-original-text');
        }
    }
}

// Global error handler with user-friendly messages
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showToast('Something went wrong. Please try again.', 'danger');
});

// Network status detection
window.addEventListener('online', () => {
    showToast('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    showToast('You are offline. Some features may not work.', 'warning');
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.card, .btn').forEach(el => {
        observer.observe(el);
    });
});
