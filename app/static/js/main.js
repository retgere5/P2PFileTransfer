/**
 * P2P Dosya Transferi - Ana JavaScript Dosyası
 * Bu dosya, tüm sayfalarda kullanılan ortak JavaScript işlevlerini içerir.
 */

// Sayfa yüklendiğinde çalışacak kodlar
document.addEventListener('DOMContentLoaded', function() {
    // Navbar aktif bağlantı vurgulama
    highlightActiveNavLink();
    
    // Tooltips'leri etkinleştir
    enableTooltips();
    
    // Footer yılını güncelle
    updateFooterYear();
    
    // Mobil menü davranışı
    setupMobileMenu();
});

/**
 * Navbar'daki aktif bağlantıyı vurgular
 */
function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (currentPath.includes(href) && href !== '/')) {
            link.classList.add('active');
        }
    });
}

/**
 * Bootstrap tooltips'leri etkinleştirir
 */
function enableTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Footer'daki yıl bilgisini günceller
 */
function updateFooterYear() {
    const yearElement = document.querySelector('.footer-year');
    if (yearElement) {
        yearElement.textContent = new Date().getFullYear();
    }
}

/**
 * Mobil menü davranışını ayarlar
 */
function setupMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Menü dışına tıklandığında menüyü kapat
        document.addEventListener('click', function(event) {
            const isClickInside = navbarToggler.contains(event.target) || navbarCollapse.contains(event.target);
            
            if (!isClickInside && navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        });
        
        // Menü öğesine tıklandığında menüyü kapat
        const navLinks = navbarCollapse.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }
}

/**
 * Kopyalama işlevi
 * @param {string} text - Kopyalanacak metin
 * @param {HTMLElement} button - Kopyalama butonu (opsiyonel)
 * @returns {Promise<boolean>} - Kopyalama başarılı ise true, değilse false
 */
function copyToClipboard(text, button = null) {
    return navigator.clipboard.writeText(text)
        .then(() => {
            if (button) {
                const originalHTML = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i>';
                
                setTimeout(() => {
                    button.innerHTML = originalHTML;
                }, 1500);
            }
            return true;
        })
        .catch(err => {
            console.error('Kopyalama hatası:', err);
            return false;
        });
}

/**
 * Dosya boyutunu formatlar
 * @param {number} bytes - Bayt cinsinden dosya boyutu
 * @param {number} decimals - Ondalık basamak sayısı
 * @returns {string} - Formatlanmış dosya boyutu
 */
function formatFileSize(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

/**
 * Tarih ve saati formatlar
 * @param {Date|number|string} date - Tarih nesnesi, timestamp veya tarih dizesi
 * @returns {string} - Formatlanmış tarih ve saat
 */
function formatDateTime(date) {
    const dateObj = new Date(date);
    return dateObj.toLocaleString('tr-TR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * HTML karakterlerini escape eder
 * @param {string} text - Escape edilecek metin
 * @returns {string} - Escape edilmiş metin
 */
function escapeHTML(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Rastgele bir ID oluşturur
 * @param {number} length - ID uzunluğu
 * @returns {string} - Rastgele ID
 */
function generateRandomId(length = 8) {
    return Math.random().toString(36).substring(2, 2 + length);
}

/**
 * Hata mesajı gösterir
 * @param {string} message - Hata mesajı
 * @param {HTMLElement} container - Mesajın ekleneceği konteyner
 * @param {number} timeout - Mesajın görüntülenme süresi (ms)
 */
function showError(message, container, timeout = 5000) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-danger alert-dismissible fade show';
    alert.innerHTML = `
        <i class="fas fa-exclamation-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.insertBefore(alert, container.firstChild);
    
    if (timeout > 0) {
        setTimeout(() => {
            alert.remove();
        }, timeout);
    }
}

/**
 * Başarı mesajı gösterir
 * @param {string} message - Başarı mesajı
 * @param {HTMLElement} container - Mesajın ekleneceği konteyner
 * @param {number} timeout - Mesajın görüntülenme süresi (ms)
 */
function showSuccess(message, container, timeout = 5000) {
    const alert = document.createElement('div');
    alert.className = 'alert alert-success alert-dismissible fade show';
    alert.innerHTML = `
        <i class="fas fa-check-circle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    container.insertBefore(alert, container.firstChild);
    
    if (timeout > 0) {
        setTimeout(() => {
            alert.remove();
        }, timeout);
    }
} 