<template>
    <footer class="footer">
        <div class="footer-container">
            <p>&copy; {{ currentYear }} Система бронирования аудиторий и оборудования</p>
            <p class="footer-links">
                <a href="mailto:support@example.com">Поддержка</a>
                <span class="divider">|</span>
                <a href="#">Документация</a>
                <span class="divider">|</span>
                <a href="https://github.com" target="_blank">GitHub</a>
            </p>
        </div>
    </footer>
</template>

<script setup lang="ts">
const currentYear = new Date().getFullYear();
</script>

<style scoped>
.footer {
    background: #2c3e50;
    color: rgba(255,255,255,0.7);
    padding: 24px 20px;
    margin-top: auto;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.footer-container {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.footer p {
    margin: 0;
    font-size: 0.9rem;
}

.footer-links {
    display: flex;
    align-items: center;
    gap: 10px;
}

.footer-links a {
    color: rgba(255,255,255,0.6);
    text-decoration: none;
    transition: color 0.2s;
}

.footer-links a:hover {
    color: white;
}

.divider {
    color: rgba(255,255,255,0.3);
}

@media (max-width: 600px) {
    .footer-container {
        flex-direction: column;
        text-align: center;
    }
}
</style>