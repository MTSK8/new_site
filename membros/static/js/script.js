document.addEventListener("DOMContentLoaded", function() {
    let currentPage = 1;
    let hasNextPage = true; 
    let isFetching = false;
    let lastRequestedPage = 1;
    const container = document.querySelector('.infinite-container');

    window.addEventListener('scroll', () => {
        if (!hasNextPage || isFetching) return;

        const scrollPosition = window.innerHeight + window.scrollY;
        const pageBottom = document.documentElement.offsetHeight - 200;

        if (scrollPosition >= pageBottom) {
            carregarMaisHistorias();
        }
    });

    async function carregarMaisHistorias() {
        if (isFetching || !hasNextPage) return;
        
        isFetching = true;
        let nextPageToRequest = currentPage + 1;

        if (nextPageToRequest === lastRequestedPage) {
            isFetching = false;
            return;
        }

        lastRequestedPage = nextPageToRequest;

        try {
            const response = await fetch(`?page=${nextPageToRequest}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (response.ok) {
                const data = await response.json();
                
                if (container && data.html) {
                    container.insertAdjacentHTML('beforeend', data.html);
                    currentPage = nextPageToRequest;
                }

                hasNextPage = data.has_next;
            } else {
                console.error("Erro ao buscar mais histórias.");
            }
        } catch (error) {
            console.error("Erro de conexão:", error);
        } finally {
            isFetching = false;
        }
    }
});