document.addEventListener('DOMContentLoaded', () => {
    console.log('MAIN JS LOADED');
    // Mega Menu Toggle (for accessibility or tap on mobile)
    const shopTrigger = document.getElementById('shop-trigger');
    const megaMenu = document.getElementById('mega-menu');

    if (shopTrigger) {
        shopTrigger.parentElement.addEventListener('mouseenter', () => console.log('MEGA MENU HOVER ENTER'));
        shopTrigger.parentElement.addEventListener('mouseleave', () => console.log('MEGA MENU HOVER LEAVE'));
        
        shopTrigger.addEventListener('click', (e) => {
            if (window.innerWidth < 1024) {
                e.preventDefault();
                megaMenu.style.display = megaMenu.style.display === 'block' ? 'none' : 'block';
                megaMenu.style.opacity = megaMenu.style.opacity === '1' ? '0' : '1';
                megaMenu.style.transform = megaMenu.style.transform === 'translateY(0)' ? 'translateY(10px)' : 'translateY(0)';
            }
        });
    }

    // Header Scroll Effect
    const header = document.querySelector('.main-header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.padding = '10px 0';
            header.style.backgroundColor = 'rgba(0, 0, 0, 0.95)';
        } else {
            header.style.padding = '15px 0';
            header.style.backgroundColor = 'var(--black)';
        }
    });

    // Mobile Menu
    const menuToggle = document.getElementById('menu-toggle');
    const mobileNav = document.getElementById('mobile-nav');
    const closeMenu = document.getElementById('close-menu');

    if (menuToggle) {
        menuToggle.addEventListener('click', () => {
            mobileNav.classList.add('active');
        });
    }

    if (closeMenu) {
        closeMenu.addEventListener('click', () => {
            mobileNav.classList.remove('active');
        });
    }

    // Filter Logic
    const filterBtns = document.querySelectorAll('.filter-btn');
    const productCards = document.querySelectorAll('.car-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            const filter = btn.textContent;
            productCards.forEach(card => {
                const cardScale = card.dataset.scale;
                if (filter === 'ALL' || (cardScale && cardScale.includes(filter))) {
                    card.style.display = 'block';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0) scale(1)';
                    }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px) scale(0.95)';
                    setTimeout(() => card.style.display = 'none', 400);
                }
            });
        });
    });

    // Search Overlay Logic
    const searchOpen = document.getElementById('search-open');
    const searchClose = document.getElementById('search-close');
    const searchOverlay = document.getElementById('search-overlay');
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    // Fetch products for search (from a hidden data element or global variable)
    // For now, we simulate fetching from the DOM cards
    const getProductData = () => {
        const cards = document.querySelectorAll('.car-card');
        return Array.from(cards).map(card => {
            // Get ID from various possible locations (data-product-id, or the onclick URL)
            const id = card.dataset.productId || card.getAttribute('onclick')?.match(/\/product\/(\d+)/)?.[1];
            return {
                id: id,
                name: card.querySelector('h3')?.textContent || 'Car Model',
                scale: card.querySelector('.scale-tag')?.textContent || '1:18',
                image: card.querySelector('img')?.src || '',
                price: card.querySelector('.price')?.textContent || '₹0'
            };
        });
    };

    if (searchOpen) {
        searchOpen.addEventListener('click', () => {
            searchOverlay.classList.add('active');
            setTimeout(() => searchInput.focus(), 500);
        });
    }

    if (searchClose) {
        searchClose.addEventListener('click', () => {
            searchOverlay.classList.remove('active');
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const products = getProductData();
            
            if (query.length < 1) {
                searchResults.innerHTML = '';
                return;
            }

            const filtered = products.filter(p => p.name.toLowerCase().includes(query));
            
            searchResults.innerHTML = filtered.map(p => `
                <div class="search-item" onclick="window.location.href='/product/${p.id}'">
                    <h4>${p.name}</h4>
                    <p>${p.scale} | ${p.price}</p>
                </div>
            `).join('');
        });
    }

    // Keyboard ESC to close overlays
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            searchOverlay.classList.remove('active');
            mobileNav.classList.remove('active');
            document.getElementById('edit-profile-modal')?.classList.remove('active');
            document.getElementById('cart-drawer')?.classList.remove('active');
        }
    });

    // Profile Tab Switching
    const tabs = document.querySelectorAll('.profile-tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const target = tab.dataset.tab;
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('active');
            });
            document.getElementById(`${target}-tab`).classList.add('active');
            
            if (target === 'collection') loadCollection();
        });
    });

    // Edit Profile Modal
    const editTrigger = document.querySelector('.edit-trigger');
    const modal = document.getElementById('edit-profile-modal');
    const closeModal = document.querySelector('.close-modal');
    
    if (editTrigger) {
        editTrigger.addEventListener('click', () => modal.classList.add('active'));
    }
    
    if (closeModal) {
        closeModal.addEventListener('click', () => modal.classList.remove('active'));
    }

    const editForm = document.getElementById('edit-profile-form');
    if (editForm) {
        editForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(editForm);
            const res = await fetch('/update_profile', {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.success) {
                location.reload();
            } else {
                alert(data.message);
            }
        });
    }

    // Cart Drawer Logic
    const cartDrawer = document.getElementById('cart-drawer');
    const cartBtn = document.querySelector('.cart-btn');
    const closeDrawer = document.querySelector('.close-drawer');
    
    if (cartBtn && cartDrawer) {
        cartBtn.addEventListener('click', (e) => {
            e.preventDefault();
            cartDrawer.classList.toggle('active');
            loadCart();
        });
    }

    if (closeDrawer && cartDrawer) {
        closeDrawer.addEventListener('click', () => {
            cartDrawer.classList.remove('active');
        });
    }

    // Add to Cart Logic
    document.addEventListener('click', async (e) => {
        const btn = e.target.closest('.add-to-cart, .add-to-cart-btn, .add-btn');
        if (!btn) return;

        e.preventDefault();
        e.stopPropagation();
        
        let productId = btn.dataset.productId;
        if (!productId) {
            const card = btn.closest('.car-card');
            if (card) {
                const clickAttr = card.getAttribute('onclick');
                productId = clickAttr?.match(/\/product\/(\d+)/)?.[1];
            }
        }
        if (!productId && window.location.pathname.includes('/product/')) {
            productId = window.location.pathname.split('/').pop();
        }

        if (!productId) return;

        try {
            const res = await fetch('/add_to_cart', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({product_id: productId})
            });
            const data = await res.json();
            if (data.success) {
                loadCart();
                cartDrawer?.classList.add('active');
            } else {
                if (res.status === 401) window.location.href = '/login';
                else alert(data.message);
            }
        } catch (err) {
            console.error("Cart error:", err);
        }
    });

    // Add to Collection
    document.addEventListener('click', async (e) => {
        const btn = e.target.closest('.collect-btn, .add-to-collection-btn');
        if (!btn) return;

        e.preventDefault();
        e.stopPropagation();

        let productId = btn.dataset.productId;
        if (!productId && window.location.pathname.includes('/product/')) {
            productId = window.location.pathname.split('/').pop();
        }

        if (!productId) return;

        try {
            const res = await fetch('/add_to_collection', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({product_id: productId})
            });
            const data = await res.json();
            alert(data.message);
            if (data.success) {
                // Refresh owned count if on profile page
                if (window.location.pathname === '/profile') loadCollection();
            }
        } catch (err) {
            console.error("Collection error:", err);
        }
    });

    async function loadCart() {
        try {
            const res = await fetch('/get_cart');
            const data = await res.json();
            const container = document.getElementById('cart-items');
            const totalEl = document.getElementById('cart-total-amount');
            const countBadge = document.querySelector('.cart-count');
            
            // Sync header badge immediately
            if (countBadge) countBadge.textContent = data.items ? data.items.length : 0;
            
            // If drawer elements are missing (e.g. before drawer is added to all pages), exit gracefully
            if (!container || !totalEl) return;

            if (!data.items || data.items.length === 0) {
                container.innerHTML = '<div class="empty-cart"><p>Your cart is empty</p></div>';
                totalEl.textContent = '₹0';
                return;
            }
            
            container.innerHTML = data.items.map(item => `
                <div class="cart-item">
                    <div class="cart-item-img"><img src="/static/assets/${item.image}"></div>
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <p>₹${item.price.toLocaleString('en-IN')}</p>
                    </div>
                </div>
            `).join('');
            totalEl.textContent = `₹${data.total.toLocaleString('en-IN')}`;
        } catch (err) {
            console.error("loadCart error:", err);
        }
    }

    async function loadCollection() {
        try {
            const res = await fetch('/get_collection');
            const data = await res.json();
            const grid = document.getElementById('user-collection-grid');
            
            console.log('COLLECTION DATA:', data);

            if (!grid) return;

            if (data.items.length === 0) {
                grid.innerHTML = '<div class="empty-state"><p>Your garage is empty.</p><a href="/shop" class="btn btn-primary">EXPLORE MODELS</a></div>';
                return;
            }
            
            grid.innerHTML = data.items.map(item => `
                <div class="car-card" onclick="window.location.href='/product/${item.id}'">
                    <div class="car-image">
                        <img src="/static/assets/${item.image}" alt="${item.name}">
                        <span class="scale-tag">${item.scale}</span>
                    </div>
                    <div class="car-info">
                        <h3>${item.name}</h3>
                        <p class="price">₹${item.price.toLocaleString('en-IN')}</p>
                    </div>
                </div>
            `).join('');
            
            // Update stats
            const ownedCount = document.querySelector('.stat-value');
            if (ownedCount) ownedCount.textContent = data.items.length;
        } catch (err) {
            console.error("loadCollection error:", err);
        }
    }

    // Initialize Cart and Collection on load
    loadCart();
    if (window.location.pathname === '/profile') loadCollection();
});
